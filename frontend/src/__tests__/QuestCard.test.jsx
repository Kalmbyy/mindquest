import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import QuestCard from '../components/QuestCard';

const mockQuest = {
  id: 1, title: 'Minum 8 gelas air', description: 'Cukupi cairan harian',
  category: 'NUTRITION', category_display: 'Nutrisi',
  difficulty: 'EASY', difficulty_display: 'Mudah',
  xp_reward: 15, icon: 'glass-water', is_completed_today: false,
};

describe('QuestCard', () => {
  it('renders quest title and XP', () => {
    render(<QuestCard quest={mockQuest} onComplete={() => {}} completing={false} />);
    expect(screen.getByText('Minum 8 gelas air')).toBeInTheDocument();
    expect(screen.getByText('+15 XP')).toBeInTheDocument();
  });

  it('calls onComplete when button clicked', () => {
    const onComplete = vi.fn();
    render(<QuestCard quest={mockQuest} onComplete={onComplete} completing={false} />);
    fireEvent.click(screen.getByText('Tandai selesai'));
    expect(onComplete).toHaveBeenCalledWith(1);
  });

  it('shows completed state when done today', () => {
    render(<QuestCard quest={{ ...mockQuest, is_completed_today: true }} onComplete={() => {}} completing={false} />);
    expect(screen.getByText('✓ Selesai hari ini')).toBeInTheDocument();
  });

  it('disables button when completing', () => {
    render(<QuestCard quest={mockQuest} onComplete={() => {}} completing={true} />);
    expect(screen.getByText('Memproses...')).toBeDisabled();
  });
});
