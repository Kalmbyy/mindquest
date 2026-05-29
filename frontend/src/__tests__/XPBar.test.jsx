import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import XPBar from '../components/XPBar';

describe('XPBar', () => {
  it('renders the current level', () => {
    render(<XPBar level={3} currentXP={50} neededXP={200} percent={25} />);
    expect(screen.getByText('Level 3')).toBeInTheDocument();
  });

  it('shows XP progress text', () => {
    render(<XPBar level={3} currentXP={50} neededXP={200} percent={25} />);
    expect(screen.getByText('50 / 200 XP')).toBeInTheDocument();
  });

  it('shows XP remaining to next level', () => {
    render(<XPBar level={3} currentXP={50} neededXP={200} percent={25} />);
    expect(screen.getByText(/150 XP lagi menuju Level 4/)).toBeInTheDocument();
  });
});
