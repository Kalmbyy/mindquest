import { useEffect, useState } from 'react';
import { Trophy, Crown, Medal } from 'lucide-react';
import Layout from '../components/Layout';
import { leaderboardAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

export default function Leaderboard() {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    leaderboardAPI.get()
      .then((res) => setData(res.data))
      .catch((e) => console.error(e))
      .finally(() => setLoading(false));
  }, []);

  const rankStyle = (rank) => {
    if (rank === 1) return { icon: Crown, color: 'text-amber-500', bg: 'bg-amber-50 border-amber-200' };
    if (rank === 2) return { icon: Medal, color: 'text-slate-400', bg: 'bg-slate-50 border-slate-200' };
    if (rank === 3) return { icon: Medal, color: 'text-orange-400', bg: 'bg-orange-50 border-orange-200' };
    return null;
  };

  return (
    <Layout>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Peringkat</h1>
        <p className="text-slate-500">
          {data ? `Bersaing dengan ${data.total_players} hero lainnya` : 'Papan peringkat berdasarkan total XP'}
        </p>
      </div>

      {loading ? (
        <p className="text-slate-500">Memuat peringkat...</p>
      ) : !data || data.leaderboard.length === 0 ? (
        <div className="card text-center py-12">
          <Trophy className="w-12 h-12 text-slate-300 mx-auto mb-3" />
          <p className="text-slate-500">Belum ada data peringkat.</p>
        </div>
      ) : (
        <>
          {data.my_rank && (
            <div className="card mb-4 bg-primary-50 border-primary-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-primary-600 text-white flex items-center justify-center font-semibold">
                    #{data.my_rank}
                  </div>
                  <div>
                    <p className="text-sm font-medium text-slate-900">Peringkat kamu</p>
                    <p className="text-xs text-slate-500">dari {data.total_players} pemain</p>
                  </div>
                </div>
                <Trophy className="w-5 h-5 text-primary-600" />
              </div>
            </div>
          )}

          <div className="card p-0 divide-y divide-slate-100 overflow-hidden">
            {data.leaderboard.map((entry) => {
              const special = rankStyle(entry.rank);
              const isMe = entry.username === user?.username;
              const RankIcon = special?.icon;
              return (
                <div key={entry.rank}
                  className={`flex items-center gap-3 p-3.5 ${isMe ? 'bg-primary-50/50' : ''}`}>
                  <div className={`w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0 font-semibold text-sm ${
                    special ? `${special.bg} border ${special.color}` : 'bg-slate-100 text-slate-500'
                  }`}>
                    {RankIcon ? <RankIcon className="w-4 h-4" /> : entry.rank}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-slate-900 truncate">
                      {entry.username} {isMe && <span className="text-xs text-primary-600">(kamu)</span>}
                    </p>
                    <p className="text-xs text-slate-500">Level {entry.current_level} · 🔥 {entry.best_streak} hari</p>
                  </div>
                  <span className="text-sm font-semibold text-primary-600 whitespace-nowrap">
                    {entry.total_xp.toLocaleString('id-ID')} XP
                  </span>
                </div>
              );
            })}
          </div>
        </>
      )}
    </Layout>
  );
}
