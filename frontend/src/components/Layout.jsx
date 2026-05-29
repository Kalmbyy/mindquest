import { Link, NavLink, useNavigate } from 'react-router-dom';
import { LayoutDashboard, Target, History, Trophy, Award, LogOut, Sparkles } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const NAV_ITEMS = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/quests', label: 'Quests', icon: Target },
  { to: '/history', label: 'Riwayat', icon: History },
  { to: '/leaderboard', label: 'Peringkat', icon: Trophy },
  { to: '/badges', label: 'Badge', icon: Award },
];

export default function Layout({ children }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => { logout(); navigate('/login'); };

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link to="/dashboard" className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-primary-600 flex items-center justify-center">
              <Sparkles className="w-4 h-4 text-white" />
            </div>
            <span className="font-bold text-lg text-slate-900">MindQuest</span>
          </Link>

          <nav className="hidden md:flex items-center gap-1">
            {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
              <NavLink key={to} to={to} className={({ isActive }) =>
                `px-3 py-2 rounded-lg text-sm font-medium flex items-center gap-2 ${
                  isActive ? 'bg-primary-50 text-primary-600' : 'text-slate-600 hover:bg-slate-100'
                }`
              }>
                <Icon className="w-4 h-4" /> {label}
              </NavLink>
            ))}
          </nav>

          <div className="flex items-center gap-3">
            <span className="text-sm text-slate-600 hidden sm:inline">
              Hi, <span className="font-medium">{user?.username}</span>
            </span>
            <button onClick={handleLogout}
              className="p-2 rounded-lg text-slate-500 hover:bg-slate-100 hover:text-red-600" title="Logout">
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>

        <nav className="md:hidden border-t border-slate-100 px-2 py-2 flex gap-1 overflow-x-auto">
          {NAV_ITEMS.map(({ to, label }) => (
            <NavLink key={to} to={to} className={({ isActive }) =>
              `flex-1 text-center py-2 px-2 rounded-lg text-xs font-medium whitespace-nowrap ${
                isActive ? 'bg-primary-50 text-primary-600' : 'text-slate-600'
              }`
            }>{label}</NavLink>
          ))}
        </nav>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-6">{children}</main>
    </div>
  );
}
