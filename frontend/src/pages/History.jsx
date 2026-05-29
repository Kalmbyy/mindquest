import { useEffect, useState } from 'react';
import { History as HistoryIcon, ChevronLeft, ChevronRight } from 'lucide-react';
import Layout from '../components/Layout';
import { questAPI } from '../services/api';
import { getIcon } from '../utils/icons';

export default function History() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [count, setCount] = useState(0);
  const [hasNext, setHasNext] = useState(false);
  const [hasPrev, setHasPrev] = useState(false);

  const loadHistory = async (p) => {
    setLoading(true);
    try {
      const res = await questAPI.history(p);
      setLogs(res.data.results);
      setCount(res.data.count);
      setHasNext(!!res.data.next);
      setHasPrev(!!res.data.previous);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadHistory(page); }, [page]);

  // Group logs by date
  const grouped = logs.reduce((acc, log) => {
    const date = log.completed_date;
    if (!acc[date]) acc[date] = [];
    acc[date].push(log);
    return acc;
  }, {});

  const formatDate = (dateStr) => {
    const d = new Date(dateStr);
    return d.toLocaleDateString('id-ID', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  };

  return (
    <Layout>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Riwayat Quest</h1>
        <p className="text-slate-500">
          {count > 0 ? `Total ${count} quest telah kamu selesaikan` : 'Belum ada quest yang diselesaikan'}
        </p>
      </div>

      {loading ? (
        <p className="text-slate-500">Memuat riwayat...</p>
      ) : logs.length === 0 ? (
        <div className="card text-center py-12">
          <HistoryIcon className="w-12 h-12 text-slate-300 mx-auto mb-3" />
          <p className="text-slate-500">Belum ada riwayat quest.</p>
          <p className="text-sm text-slate-400 mt-1">Selesaikan quest pertamamu untuk mulai membangun riwayat!</p>
        </div>
      ) : (
        <div className="space-y-6">
          {Object.entries(grouped).map(([date, dateLogs]) => {
            const totalXP = dateLogs.reduce((sum, l) => sum + l.xp_earned, 0);
            return (
              <div key={date}>
                <div className="flex items-center justify-between mb-2 px-1">
                  <h2 className="text-sm font-medium text-slate-700">{formatDate(date)}</h2>
                  <span className="text-xs font-medium text-primary-600">+{totalXP} XP</span>
                </div>
                <div className="card divide-y divide-slate-100 p-0 overflow-hidden">
                  {dateLogs.map((log) => {
                    const Icon = getIcon(log.quest_icon);
                    return (
                      <div key={log.id} className="flex items-center gap-3 p-3.5">
                        <div className="w-9 h-9 rounded-lg bg-primary-50 text-primary-600 flex items-center justify-center flex-shrink-0">
                          <Icon className="w-4 h-4" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-slate-900 truncate">{log.quest_title}</p>
                          <p className="text-xs text-slate-500">{log.quest_category}</p>
                        </div>
                        <span className="text-sm font-medium text-accent-600 whitespace-nowrap">+{log.xp_earned} XP</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}

          {(hasNext || hasPrev) && (
            <div className="flex items-center justify-center gap-3 pt-2">
              <button onClick={() => setPage((p) => p - 1)} disabled={!hasPrev}
                className="flex items-center gap-1 px-3 py-2 rounded-lg border border-slate-200 text-sm font-medium text-slate-600 disabled:opacity-40 hover:bg-slate-50">
                <ChevronLeft className="w-4 h-4" /> Sebelumnya
              </button>
              <span className="text-sm text-slate-500">Halaman {page}</span>
              <button onClick={() => setPage((p) => p + 1)} disabled={!hasNext}
                className="flex items-center gap-1 px-3 py-2 rounded-lg border border-slate-200 text-sm font-medium text-slate-600 disabled:opacity-40 hover:bg-slate-50">
                Berikutnya <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      )}
    </Layout>
  );
}
