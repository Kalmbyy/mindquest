/**
 * Convert a kebab-case lucide icon name to the PascalCase component.
 * Falls back to Star if not found.
 */
import * as Icons from 'lucide-react';

export function getIcon(name) {
  if (!name) return Icons.Star;
  const pascal = name
    .split('-')
    .map((s) => s.charAt(0).toUpperCase() + s.slice(1))
    .join('');
  return Icons[pascal] || Icons.Star;
}
