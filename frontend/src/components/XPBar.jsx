import { Sparkles } from 'lucide-react';

export default function XPBar({ level, currentXP, neededXP, percent }) {
  return (
    <div className="card">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-full bg-primary-50 flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-primary-600" />
          </div>
          <div>
            <p className="text-xs text-slate-500">Level saat ini</p>
            <p className="text-xl font-semibold text-slate-900">Level {level}</p>
          </div>
        </div>
        <div className="text-right">
          <p className="text-xs text-slate-500">Progress</p>
          <p className="text-sm font-medium text-primary-600">{currentXP} / {neededXP} XP</p>
        </div>
      </div>
      <div className="h-3 bg-slate-100 rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-primary-400 to-primary-600 rounded-full transition-all duration-500"
          style={{ width: `${Math.min(percent, 100)}%` }}
        />
      </div>
      <p className="text-xs text-slate-500 mt-2 text-center">
        {Math.max(neededXP - currentXP, 0)} XP lagi menuju Level {level + 1}
      </p>
    </div>
  );
}
