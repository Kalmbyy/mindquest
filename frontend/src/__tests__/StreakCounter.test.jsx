import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import StreakCounter from '../components/StreakCounter';

describe('StreakCounter', () => {
  it('displays current and best streak', () => {
    render(<StreakCounter current={7} best={12} />);
    expect(screen.getByText('7')).toBeInTheDocument();
    expect(screen.getByText('12')).toBeInTheDocument();
  });

  it('shows streak labels', () => {
    render(<StreakCounter current={7} best={12} />);
    expect(screen.getByText('Streak saat ini')).toBeInTheDocument();
    expect(screen.getByText('Streak terbaik')).toBeInTheDocument();
  });
});
