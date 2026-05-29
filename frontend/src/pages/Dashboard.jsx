import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { TrendingUp, Target, ArrowRight, Smile } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from 'recharts';
import Layout from '../components/Layout';
import XPBar from '../components/XPBar';
import StreakCounter from '../components/StreakCounter';
import MoodCheckIn from '../components/MoodCheckIn';
import { authAPI, questAPI, moodAPI } from '../services/api';

export default function Dashboard() {
  const [profile, setProfile] = useState(null);
  const [stats, setStats] = useState(null);
  const [moodHistory, setMoodHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadAll = async () => {
    try {
      const [p, s, m] = await Promise.all([
        authAPI.profile(),
        questAPI.todayStats(),
        moodAPI.history(),
      ]);
      setProfile(p.data);
      setStats(s.data);
      setMoodHistory([...m.data].reverse());
    } catch (e) {
      console.error('Failed to load dashboard:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadAll(); }, []);

  if (loading) {
    return <Layout><p className="text-slate-500">Memuat dashboard...</p></Layout>;
  }

  const chartData = moodHistory.map((m) => ({
    date: new Date(m.log_date).toLocaleDateString('id-ID', { day: '2-digit', month: 'short' }),
    Mood: m.mood_score,
    Energi: m.energy_score,
  }));

  const avgMood = moodHistory.length
    ? (moodHistory.reduce((sum, m) => sum + m.mood_score, 0) / moodHistory.length).toFixed(1)
    : '–';

  return (
    <Layout>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
        <p className="text-slate-500">Pantau progress kesehatanmu hari ini.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <XPBar
          level={profile.current_level}
          currentXP={profile.xp_progress.current}
          neededXP={profile.xp_progress.needed}
          percent={profile.xp_progress.percent}
        />
        <StreakCounter current={profile.current_streak} best={profile.best_streak} />
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="card">
          <div className="flex items-center gap-2 mb-2">
            <Target className="w-4 h-4 text-primary-600" />
            <p className="text-xs text-slate-500">Quest hari ini</p>
          </div>
          <p className="text-2xl font-semibold text-slate-900">
            {stats.completed_today}<span className="text-sm text-slate-400 font-normal"> / {stats.total_active_quests}</span>
          </p>
          <p className="text-xs text-slate-500 mt-1">{stats.completion_percent}% selesai</p>
        </div>

        <div className="card">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="w-4 h-4 text-accent-400" />
            <p className="text-xs text-slate-500">XP hari ini</p>
          </div>
          <p className="text-2xl font-semibold text-slate-900">+{stats.xp_earned_today}</p>
          <p className="text-xs text-slate-500 mt-1">Total: {profile.total_xp} XP</p>
        </div>

        <div className="card">
          <div className="flex items-center gap-2 mb-2">
            <Smile className="w-4 h-4 text-warm-400" />
            <p className="text-xs text-slate-500">Mood rata-rata</p>
          </div>
          <p className="text-2xl font-semibold text-slate-900">
            {avgMood}<span className="text-sm text-slate-400 font-normal"> / 5</span>
          </p>
          <p className="text-xs text-slate-500 mt-1">7 hari terakhir</p>
        </div>

        <Link to="/quests" className="card hover:border-primary-300 transition-colors flex items-center justify-between group">
          <div>
            <p className="text-xs text-slate-500">Lanjutkan</p>
            <p className="text-base font-semibold text-slate-900 mt-1">Quest →</p>
          </div>
          <ArrowRight className="w-5 h-5 text-slate-400 group-hover:text-primary-600 group-hover:translate-x-1 transition-all" />
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="md:col-span-2 card">
          <h3 className="font-semibold text-slate-900 mb-1">Tren mood & energi</h3>
          <p className="text-sm text-slate-500 mb-4">7 hari terakhir</p>
          {chartData.length === 0 ? (
            <div className="h-48 flex items-center justify-center text-slate-400 text-sm text-center px-4">
              Belum ada data mood. Lakukan check-in pertamamu di samping →
            </div>
          ) : (
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="date" tick={{ fontSize: 12, fill: '#64748b' }} />
                <YAxis domain={[0, 5]} tick={{ fontSize: 12, fill: '#64748b' }} />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="Mood" stroke="#7F77DD" strokeWidth={2} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="Energi" stroke="#1D9E75" strokeWidth={2} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>

        <MoodCheckIn onSuccess={loadAll} />
      </div>
    </Layout>
  );
}
