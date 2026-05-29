import { useEffect, useState } from 'react';
import { Award, Lock } from 'lucide-react';
import Layout from '../components/Layout';
import { badgeAPI } from '../services/api';
import { getIcon } from '../utils/icons';

const COLOR_MAP = {
  green: 'bg-green-100 text-green-600',
  blue: 'bg-blue-100 text-blue-600',
  purple: 'bg-purple-100 text-purple-600',
  amber: 'bg-amber-100 text-amber-600',
  orange: 'bg-orange-100 text-orange-600',
  red: 'bg-red-100 text-red-600',
  teal: 'bg-teal-100 text-teal-600',
};

const CRITERIA_LABEL = {
  TOTAL_XP: 'Total XP', LEVEL: 'Level', STREAK: 'Streak', QUEST_COUNT: 'Quest',
};

export default function Badges() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    badgeAPI.list()
      .then((res) => setData(res.data))
      .catch((e) => console.error(e))
      .finally(() => setLoading(false));
  }, []);

  return (
    <Layout>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Badge & Pencapaian</h1>
        <p className="text-slate-500">
          {data ? `${data.unlocked_count} dari ${data.total_count} badge terbuka` : 'Kumpulkan badge dengan menyelesaikan quest'}
        </p>
      </div>

      {data && (
        <div className="card mb-5">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-slate-700">Progress koleksi</span>
            <span className="text-sm font-medium text-primary-600">
              {Math.round((data.unlocked_count / data.total_count) * 100)}%
            </span>
          </div>
          <div className="h-2.5 bg-slate-100 rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-amber-400 to-amber-500 rounded-full transition-all duration-500"
              style={{ width: `${(data.unlocked_count / data.total_count) * 100}%` }} />
          </div>
        </div>
      )}

      {loading ? (
        <p className="text-slate-500">Memuat badge...</p>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {data.badges.map((badge) => {
            const Icon = getIcon(badge.icon);
            const unlocked = badge.is_unlocked;
            return (
              <div key={badge.id}
                className={`card text-center transition-all ${unlocked ? '' : 'opacity-60'}`}>
                <div className={`w-14 h-14 rounded-2xl mx-auto mb-3 flex items-center justify-center ${
                  unlocked ? (COLOR_MAP[badge.color] || COLOR_MAP.amber) : 'bg-slate-100 text-slate-300'
                }`}>
                  {unlocked ? <Icon className="w-7 h-7" /> : <Lock className="w-6 h-6" />}
                </div>
                <h3 className={`text-sm font-semibold mb-1 ${unlocked ? 'text-slate-900' : 'text-slate-500'}`}>
                  {badge.name}
                </h3>
                <p className="text-xs text-slate-500 leading-snug mb-2">{badge.description}</p>
                {unlocked ? (
                  <span className="inline-block text-[10px] font-medium px-2 py-0.5 rounded-full bg-accent-50 text-accent-600">
                    ✓ Terbuka
                  </span>
                ) : (
                  <span className="inline-block text-[10px] font-medium px-2 py-0.5 rounded-full bg-slate-100 text-slate-400">
                    {CRITERIA_LABEL[badge.criteria_type]} ≥ {badge.threshold}
                  </span>
                )}
              </div>
            );
          })}
        </div>
      )}
    </Layout>
  );
}
