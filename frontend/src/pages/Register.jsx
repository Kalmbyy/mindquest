import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Sparkles } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: '', email: '', password: '', password_confirm: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); setLoading(true);
    try {
      await register(form.username, form.email, form.password, form.password_confirm);
      navigate('/dashboard');
    } catch (e) {
      const errs = e.response?.data;
      if (errs && typeof errs === 'object') {
        const firstKey = Object.keys(errs)[0];
        const msg = Array.isArray(errs[firstKey]) ? errs[firstKey][0] : errs[firstKey];
        setError(`${firstKey}: ${msg}`);
      } else setError('Pendaftaran gagal. Coba lagi.');
    } finally { setLoading(false); }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 via-white to-accent-50 p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-primary-600 mb-3">
            <Sparkles className="w-7 h-7 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-slate-900">Daftar MindQuest</h1>
          <p className="text-slate-600 mt-1">Mulai petualangan hidup sehatmu hari ini</p>
        </div>
        <form onSubmit={handleSubmit} className="card space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1.5">Username</label>
            <input type="text" required className="input-field" value={form.username}
              onChange={(e) => setForm({ ...form, username: e.target.value })} />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1.5">Email</label>
            <input type="email" required className="input-field" value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })} />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1.5">Password</label>
            <input type="password" required className="input-field" value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })} placeholder="Min. 8 karakter" />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1.5">Konfirmasi password</label>
            <input type="password" required className="input-field" value={form.password_confirm}
              onChange={(e) => setForm({ ...form, password_confirm: e.target.value })} />
          </div>
          {error && <p className="text-sm text-red-600 bg-red-50 p-3 rounded-lg">{error}</p>}
          <button type="submit" disabled={loading} className="btn-primary w-full">
            {loading ? 'Mendaftarkan...' : 'Daftar gratis'}
          </button>
          <p className="text-center text-sm text-slate-600">
            Sudah punya akun? <Link to="/login" className="text-primary-600 font-medium hover:underline">Masuk</Link>
          </p>
        </form>
      </div>
    </div>
  );
}
