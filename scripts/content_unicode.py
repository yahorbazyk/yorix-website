"""Offline Unicode hygiene for the site's content sources, using watermarks-remover.

Check is the default. Clean only applies the conservative Yorix profile; it does
not rewrite prose or claim to detect or erase statistical text watermarks.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / 'tools/watermarks-remover'
CONFIG = ROOT / 'content-unicode.config.json'
MAX_FILE_BYTES = 4 * 1024 * 1024
sys.dont_write_bytecode = True


def load_engine():
    manifest = json.loads((VENDOR / 'upstream.json').read_text(encoding='utf-8'))
    for name, entry in manifest['files'].items():
        path = VENDOR / name
        if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
            raise ValueError(f'Vendored source does not match its reviewed checksum: {name}')
    name = 'yorix_watermarks_unicode'
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, VENDOR / 'text_unicode.py')
        if spec is None or spec.loader is None:
            raise ValueError('Cannot load the pinned Unicode module')
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


def is_se_asian(char: str) -> bool:
    cp = ord(char)
    return 0x0E00 <= cp <= 0x0EFF or 0x1000 <= cp <= 0x109F or 0x1780 <= cp <= 0x17FF


def analyze_text(text: str):
    report = load_engine().inspect_text(text).to_dict()
    eligible = {
        int(hit['codepoint'][2:], 16)
        for hit in report['hits']
        if hit['kind'] in ('noncharacter', 'reserved_ignorable')
        or hit['codepoint'] in ('U+200B', 'U+FEFF')
    }
    # ZWSP can be a real word boundary. Handle whole runs in linear time.
    protected = set()
    for match in re.finditer('\u200b+', text):
        if (match.start() and is_se_asian(text[match.start() - 1])) or (
            match.end() < len(text) and is_se_asian(text[match.end()])
        ):
            protected.update(range(match.start(), match.end()))
    positions = [
        index for index, char in enumerate(text)
        if ord(char) in eligible
        and index not in protected
    ]
    counts = Counter(f'U+{ord(text[index]):04X}' for index in positions)
    findings = [
        {'codepoint': cp, 'count': count,
         'sample_offsets': [i for i in positions if f'U+{ord(text[i]):04X}' == cp][:10]}
        for cp, count in sorted(counts.items())
    ]
    return positions, findings, report


def clean_text(text: str) -> str:
    positions, _, _ = analyze_text(text)
    remove = set(positions)
    return ''.join(char for index, char in enumerate(text) if index not in remove)


def content_paths(root: Path, config: dict):
    root = root.resolve()
    excluded = set(config.get('exclude', []))
    found = set()
    for pattern in config['include']:
        if Path(pattern).is_absolute() or '..' in Path(pattern).parts:
            raise ValueError('Content patterns must stay inside the repository')
        for path in root.glob(pattern):
            if path.is_symlink():
                raise ValueError(f'Symlinks are not content sources: {path.relative_to(root)}')
            if path.is_file() and path.relative_to(root).as_posix() not in excluded:
                path.resolve().relative_to(root)
                found.add(path)
    return sorted(found)


def replace_file(path: Path, before: bytes, after: bytes):
    if before == after:
        return
    if path.is_symlink() or path.read_bytes() != before:
        raise ValueError(f'Source changed during inspection: {path}')
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.unicode-', delete=False) as output:
            temporary = Path(output.name)
            os.fchmod(output.fileno(), path.stat().st_mode & 0o777)
            output.write(after)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def run(mode='check', root=ROOT, config=None, json_output=False):
    root = Path(root).resolve()
    config = config or json.loads(CONFIG.read_text(encoding='utf-8'))
    paths = content_paths(root, config)
    if not paths:
        raise ValueError('No content sources matched the configured scope')
    results = []
    for path in paths:
        if path.stat().st_size > MAX_FILE_BYTES:
            raise ValueError(f'Content source exceeds the 4 MiB limit: {path}')
        before = path.read_bytes()
        text = before.decode('utf-8')  # Preserve CRLF and any BOM for inspection.
        positions, findings, report = analyze_text(text)
        relative = path.relative_to(root.resolve()).as_posix()
        item = {'path': relative, 'removable_count': len(positions), 'findings': findings}
        if mode == 'inspect':
            item['upstream_inspection'] = report
        if mode == 'clean' and positions:
            remove = set(positions)
            cleaned = ''.join(char for index, char in enumerate(text) if index not in remove)
            replace_file(path, before, cleaned.encode('utf-8'))
        results.append(item)
    affected = [item for item in results if item['removable_count']]
    summary = {
        'mode': mode, 'files_checked': len(paths), 'files_with_findings': len(affected),
        'removable_characters': sum(item['removable_count'] for item in affected),
        'scope': 'raw UTF-8 content sources; statistical watermarks are not assessed',
        'files': results if mode == 'inspect' else affected,
    }
    if json_output or mode == 'inspect':
        print(json.dumps(summary, ensure_ascii=True, indent=2))
    else:
        for item in affected:
            detail = ', '.join(f"{hit['codepoint']} x{hit['count']}" for hit in item['findings'])
            print(f"{item['path']}: {detail}")
        action = 'cleaned' if mode == 'clean' else 'found'
        print(f"Unicode hygiene: {len(paths)} files checked, {len(affected)} affected, "
              f"{summary['removable_characters']} characters {action}.")
    return 1 if mode == 'check' and affected else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['check', 'inspect', 'clean'], nargs='?', default='check')
    parser.add_argument('--json', action='store_true', dest='json_output')
    args = parser.parse_args(argv)
    try:
        return run(args.mode, json_output=args.json_output)
    except (OSError, ValueError, UnicodeError) as error:
        print(f'Unicode hygiene error: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
