"""
Seed default achievement badges.
Run: python manage.py seed_badges
"""
from django.core.management.base import BaseCommand
from badges.models import Badge


DEFAULT_BADGES = [
    # (name, description, icon, color, criteria_type, threshold, order)
    ('Langkah Pertama', 'Selesaikan quest pertamamu', 'footprints', 'green', 'QUEST_COUNT', 1, 1),
    ('Pemula Sehat', 'Selesaikan 10 quest', 'sprout', 'green', 'QUEST_COUNT', 10, 2),
    ('Konsisten', 'Selesaikan 50 quest', 'target', 'blue', 'QUEST_COUNT', 50, 3),
    ('Master Quest', 'Selesaikan 100 quest', 'crown', 'purple', 'QUEST_COUNT', 100, 4),

    ('Naik Kelas', 'Capai Level 5', 'trending-up', 'blue', 'LEVEL', 5, 5),
    ('Veteran', 'Capai Level 10', 'star', 'purple', 'LEVEL', 10, 6),
    ('Legenda', 'Capai Level 20', 'sparkles', 'amber', 'LEVEL', 20, 7),

    ('Streak 3 Hari', 'Pertahankan streak 3 hari', 'flame', 'orange', 'STREAK', 3, 8),
    ('Streak Seminggu', 'Pertahankan streak 7 hari', 'flame', 'orange', 'STREAK', 7, 9),
    ('Streak Sebulan', 'Pertahankan streak 30 hari', 'flame', 'red', 'STREAK', 30, 10),

    ('Kolektor XP', 'Kumpulkan 500 XP', 'gem', 'teal', 'TOTAL_XP', 500, 11),
    ('Pemburu XP', 'Kumpulkan 2,000 XP', 'gem', 'purple', 'TOTAL_XP', 2000, 12),
    ('Sultan XP', 'Kumpulkan 5,000 XP', 'trophy', 'amber', 'TOTAL_XP', 5000, 13),
]


class Command(BaseCommand):
    help = 'Seed database with default achievement badges.'

    def handle(self, *args, **options):
        created_count = 0
        for name, desc, icon, color, criteria, threshold, order in DEFAULT_BADGES:
            obj, created = Badge.objects.get_or_create(
                name=name,
                defaults={
                    'description': desc, 'icon': icon, 'color': color,
                    'criteria_type': criteria, 'threshold': threshold, 'order': order,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  + Created: {name}'))
            else:
                self.stdout.write(f'  - Exists:  {name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nBadge seeding complete! {created_count} new badges. '
            f'Total: {Badge.objects.count()}'
        ))
