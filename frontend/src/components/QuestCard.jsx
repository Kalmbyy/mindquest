import { Check } from 'lucide-react';
import { getIcon } from '../utils/icons';

const DIFFICULTY_STYLES = {
  EASY: 'bg-green-50 text-green-700 border-green-200',
  MEDIUM: 'bg-amber-50 text-amber-700 border-amber-200',
  HARD: 'bg-red-50 text-red-700 border-red-200',
};

const CATEGORY_STYLES = {
  PHYSICAL: 'bg-blue-50 text-blue-700',
  MENTAL: 'bg-purple-50 text-purple-700',
  SLEEP: 'bg-indigo-50 text-indigo-700',
  NUTRITION: 'bg-orange-50 text-orange-700',
  MINDFULNESS: 'bg-teal-50 text-teal-700',
  DIGITAL: 'bg-slate-100 text-slate-700',
};

export default function QuestCard({ quest, onComplete, completing }) {
  const Icon = getIcon(quest.icon);
  const completed = quest.is_completed_today;

  return (
    <div className={`card transition-all ${
      completed ? 'opacity-60 bg-slate-50' : 'hover:shadow-md hover:border-primary-200'
    }`}>
      <div className="flex items-start gap-3">
        <div className={`w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0 ${
          CATEGORY_STYLES[quest.category] || 'bg-slate-100 text-slate-700'
        }`}>
          {completed ? <Check className="w-6 h-6" /> : <Icon className="w-6 h-6" />}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2 mb-1">
            <h3 className={`font-semibold text-slate-900 ${completed ? 'line-through' : ''}`}>
              {quest.title}
            </h3>
            <span className="text-sm font-medium text-primary-600 whitespace-nowrap">
              +{quest.xp_reward} XP
            </span>
          </div>
          <p className="text-sm text-slate-600 mb-3 leading-relaxed">{quest.description}</p>
          <div className="flex items-center gap-2 mb-3">
            <span className={`text-xs px-2 py-0.5 rounded-md border ${DIFFICULTY_STYLES[quest.difficulty]}`}>
              {quest.difficulty_display}
            </span>
            <span className={`text-xs px-2 py-0.5 rounded-md ${CATEGORY_STYLES[quest.category]}`}>
              {quest.category_display}
            </span>
          </div>
          <button
            onClick={() => onComplete(quest.id)}
            disabled={completed || completing}
            className={`w-full py-2 px-4 rounded-lg text-sm font-medium transition-colors ${
              completed
                ? 'bg-green-100 text-green-700 cursor-not-allowed'
                : 'bg-primary-600 text-white hover:bg-primary-800'
            } disabled:opacity-50`}
          >
            {completed ? '✓ Selesai hari ini' : completing ? 'Memproses...' : 'Tandai selesai'}
          </button>
        </div>
      </div>
    </div>
  );
}
