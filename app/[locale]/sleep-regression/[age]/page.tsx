import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import pilots from '../../../article/pilot-articles.generated.json';
import { getPilot, pilotMetadata, PilotArticlePage } from '../../../article/PilotArticlePage';

type Props = { params: { locale: string; age: string } };

export function generateStaticParams() {
  return pilots
    .filter((pilot) => pilot.slug.startsWith('sleep-regression/'))
    .map((pilot) => ({ locale: pilot.locale, age: pilot.slug.split('/')[1] }));
}

export function generateMetadata({ params }: Props): Metadata {
  const pilot = getPilot(params.locale, `sleep-regression/${params.age}`);
  return pilot ? pilotMetadata(pilot) : {};
}

export default function LocalizedSleepRegressionArticle({ params }: Props) {
  const pilot = getPilot(params.locale, `sleep-regression/${params.age}`);
  if (!pilot) notFound();
  return <PilotArticlePage article={pilot} />;
}
