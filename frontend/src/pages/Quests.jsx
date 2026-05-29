import { useEffect, useState } from 'react';
import { Trophy } from 'lucide-react';
import Layout from '../components/Layout';
import QuestCard from '../components/QuestCard';
import { questAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

const CATEGORIES = ['SEMUA', 'PHYSICAL', 'MENTAL', 'SLEEP', 'NUTRITION', 'MINDFULNESS', 'DIGITAL'];
const CATEGORY_LABEL = {
  SEMUA: 'Semua', PHYSICAL: 'Fisik', MENTAL: 'Mental', SLEEP: 'Tidur',
  NUTRITION: 'Nutrisi', MINDFULNESS: 'Mindfulness', DIGITAL: 'Digital'
};

export default function Quests() {
  const { refreshUser } = useAuth();
  const [quests, setQuests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [completing, setCompleting] = useState(null);
  const [filter, setFilter] = useState('SEMUA');
  const [toast, setToast] = useState(null);

  const loadQuests = async () => {
    try {
      const res = await questAPI.today();
      setQuests(res.data);
    } catch (e) { console.error(e); }
    finally { setLoading(false); }
  };

  useEffect(() => { loadQuests(); }, []);

  const showToast = (toastData, duration = 4000) => {
    setToast(toastData);
    setTimeout(() => setToast(null), duration);
  };

  const handleComplete = async (id) => {
    setCompleting(id);
    try {
      const res = await questAPI.complete(id);

      // Priority: badge unlock > level up > normal
      if (res.data.new_badges && res.data.new_badges.length > 0) {
        const badge = res.data.new_badges[0];
        showToast({ type: 'badge', text: `🏅 Badge baru: ${badge.name}!` }, 5000);
      } else if (res.data.leveled_up) {
        showToast({ type: 'levelup', text: `🎉 LEVEL UP! Kamu sekarang Level ${res.data.new_level}!` });
      } else {
        showToast({ type: 'success', text: res.data.message });
      }

      await loadQuests();
      await refreshUser();
    } catch (e) {
      showToast({ type: 'error', text: e.response?.data?.detail || 'Gagal menyelesaikan quest.' }, 3000);
    } finally {
      setCompleting(null);
    }
  };

  const filtered = filter === 'SEMUA' ? quests : quests.filter((q) => q.category === filter);
  const completedCount = quests.filter((q) => q.is_completed_today).length;

  const TOAST_STYLES = {
    success: 'bg-accent-400', levelup: 'bg-primary-600',
    badge: 'bg-warm-400', error: 'bg-red-500',
  };

  return (
    <Layout>
      {toast && (
        <div className={`fixed top-20 right-4 z-50 px-4 py-3 rounded-lg shadow-lg text-white font-medium ${TOAST_STYLES[toast.type]}`}>
          {toast.text}
        </div>
      )}

      <div className="mb-6 flex items-start justify-between flex-wrap gap-3">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Daily Quests</h1>
          <p className="text-slate-500">Selesaikan misi untuk dapatkan XP dan jaga streak-mu!</p>
        </div>
        <div className="flex items-center gap-2 px-4 py-2 bg-white border border-slate-200 rounded-lg">
          <Trophy className="w-4 h-4 text-amber-500" />
          <span className="text-sm font-medium text-slate-700">{completedCount} / {quests.length} selesai</span>
        </div>
      </div>

      <div className="flex gap-2 mb-5 overflow-x-auto pb-2">
        {CATEGORIES.map((cat) => (
          <button key={cat} onClick={() => setFilter(cat)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
              filter === cat ? 'bg-primary-600 text-white' : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
            }`}>{CATEGORY_LABEL[cat]}</button>
        ))}
      </div>

      {loading ? (
        <p className="text-slate-500">Memuat quest...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filtered.map((quest) => (
            <QuestCard key={quest.id} quest={quest} onComplete={handleComplete} completing={completing === quest.id} />
          ))}
        </div>
      )}

      {filtered.length === 0 && !loading && (
        <p className="text-center text-slate-500 py-8">Tidak ada quest di kategori ini.</p>
      )}
    </Layout>
  );
}
