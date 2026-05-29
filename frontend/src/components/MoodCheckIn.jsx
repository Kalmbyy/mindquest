import { useState } from 'react';
import { moodAPI } from '../services/api';

const MOOD_EMOJI = ['😞', '😕', '😐', '🙂', '😄'];
const ENERGY_EMOJI = ['🪫', '😴', '😌', '⚡', '🔥'];

export default function MoodCheckIn({ onSuccess }) {
  const [mood, setMood] = useState(null);
  const [energy, setEnergy] = useState(null);
  const [note, setNote] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [done, setDone] = useState(false);

  const handleSubmit = async () => {
    if (!mood || !energy) return;
    setSubmitting(true);
    setError('');
    try {
      await moodAPI.create({ mood_score: mood, energy_score: energy, note });
      setDone(true);
      onSuccess?.();
    } catch (e) {
      setError(e.response?.data?.detail || 'Gagal menyimpan mood.');
    } finally {
      setSubmitting(false);
    }
  };

  if (done) {
    return (
      <div className="card flex flex-col items-center justify-center text-center py-8">
        <div className="text-4xl mb-2">✅</div>
        <p className="font-medium text-slate-900">Check-in tersimpan!</p>
        <p className="text-sm text-slate-500 mt-1">Sampai jumpa besok untuk check-in lagi.</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h3 className="font-semibold text-slate-900 mb-1">Cek mood hari ini</h3>
      <p className="text-sm text-slate-500 mb-4">Bagaimana perasaan dan energimu hari ini?</p>

      <div className="mb-4">
        <p className="text-xs font-medium text-slate-700 mb-2">Mood</p>
        <div className="flex gap-2">
          {[1, 2, 3, 4, 5].map((i) => (
            <button key={i} onClick={() => setMood(i)}
              className={`flex-1 h-12 rounded-lg text-2xl border-2 transition-all ${
                mood === i ? 'border-primary-600 bg-primary-50 scale-105' : 'border-slate-200 hover:border-slate-300'
              }`}>{MOOD_EMOJI[i - 1]}</button>
          ))}
        </div>
      </div>

      <div className="mb-4">
        <p className="text-xs font-medium text-slate-700 mb-2">Energi</p>
        <div className="flex gap-2">
          {[1, 2, 3, 4, 5].map((i) => (
            <button key={i} onClick={() => setEnergy(i)}
              className={`flex-1 h-12 rounded-lg text-2xl border-2 transition-all ${
                energy === i ? 'border-primary-600 bg-primary-50 scale-105' : 'border-slate-200 hover:border-slate-300'
              }`}>{ENERGY_EMOJI[i - 1]}</button>
          ))}
        </div>
      </div>

      <textarea value={note} onChange={(e) => setNote(e.target.value)}
        placeholder="Catatan opsional..." className="input-field text-sm resize-none mb-3" rows={2} />

      {error && <p className="text-sm text-red-600 mb-3">{error}</p>}

      <button onClick={handleSubmit} disabled={!mood || !energy || submitting} className="btn-primary w-full">
        {submitting ? 'Menyimpan...' : 'Simpan check-in'}
      </button>
    </div>
  );
}
