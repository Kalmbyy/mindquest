"""
Seed default quests.
Run: python manage.py seed_quests
"""
from django.core.management.base import BaseCommand
from quests.models import Quest


DEFAULT_QUESTS = [
    ('Jalan kaki 5,000 langkah', 'Aktif bergerak minimal 5,000 langkah hari ini.',
     'PHYSICAL', 'EASY', 15, 'footprints'),
    ('Olahraga 30 menit', 'Lakukan olahraga ringan-sedang selama 30 menit.',
     'PHYSICAL', 'MEDIUM', 25, 'dumbbell'),
    ('Stretching pagi', 'Lakukan peregangan ringan setelah bangun tidur.',
     'PHYSICAL', 'EASY', 10, 'activity'),
    ('Tidur 7+ jam', 'Tidur minimal 7 jam tadi malam.',
     'SLEEP', 'MEDIUM', 25, 'moon'),
    ('Tidur sebelum jam 11 malam', 'Mulai tidur sebelum pukul 23:00.',
     'SLEEP', 'MEDIUM', 20, 'bed'),
    ('Minum 8 gelas air', 'Cukupi kebutuhan cairan harian (~2 liter).',
     'NUTRITION', 'EASY', 15, 'glass-water'),
    ('Sarapan sehat', 'Makan sarapan bergizi seimbang hari ini.',
     'NUTRITION', 'EASY', 10, 'utensils'),
    ('Makan sayur & buah', 'Konsumsi minimal 1 porsi sayur dan 1 porsi buah.',
     'NUTRITION', 'EASY', 15, 'apple'),
    ('Hindari junk food', 'Tidak makan makanan cepat saji/gorengan hari ini.',
     'NUTRITION', 'HARD', 30, 'ban'),
    ('Journal 5 menit', 'Tulis perasaan/pikiran kamu di jurnal selama 5 menit.',
     'MENTAL', 'EASY', 15, 'book'),
    ('Catat 3 hal yang disyukuri', 'Tulis 3 hal yang kamu syukuri hari ini.',
     'MENTAL', 'EASY', 15, 'heart'),
    ('Baca buku 15 menit', 'Luangkan waktu untuk membaca buku non-tugas.',
     'MENTAL', 'MEDIUM', 20, 'book-open'),
    ('Meditasi 10 menit', 'Lakukan meditasi atau breathing exercise 10 menit.',
     'MINDFULNESS', 'MEDIUM', 25, 'brain'),
    ('Mindful breathing 3x sehari', 'Tarik napas dalam 5 kali, ulang 3x sepanjang hari.',
     'MINDFULNESS', 'EASY', 15, 'wind'),
    ('Istirahat layar 20 menit', 'Jauhkan diri dari semua layar selama 20 menit.',
     'DIGITAL', 'EASY', 15, 'eye'),
    ('No-phone saat makan', 'Makan tanpa membuka HP/laptop hari ini.',
     'DIGITAL', 'MEDIUM', 20, 'smartphone'),
    ('Detox sosial media 1 jam', 'Tidak buka sosial media selama 1 jam berturut-turut.',
     'DIGITAL', 'HARD', 30, 'circle-x'),
    ('Telepon teman/keluarga', 'Hubungi orang yang kamu sayangi minimal 5 menit.',
     'MENTAL', 'EASY', 15, 'phone'),
    ('Belajar hal baru', 'Pelajari hal baru selama minimal 15 menit (skill, bahasa, dll).',
     'MENTAL', 'MEDIUM', 25, 'graduation-cap'),
    ('Self-reflection malam', 'Refleksikan apa yang sudah dilakukan hari ini sebelum tidur.',
     'MINDFULNESS', 'EASY', 10, 'sparkles'),
]


class Command(BaseCommand):
    help = 'Seed database with 20 default quests for MindQuest.'

    def handle(self, *args, **options):
        created_count = 0
        for title, desc, cat, diff, xp, icon in DEFAULT_QUESTS:
            obj, created = Quest.objects.get_or_create(
                title=title,
                defaults={
                    'description': desc, 'category': cat,
                    'difficulty': diff, 'xp_reward': xp, 'icon': icon,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  + Created: {title}'))
            else:
                self.stdout.write(f'  - Exists:  {title}')

        self.stdout.write(self.style.SUCCESS(
            f'\nSeeding complete! {created_count} new quests created. '
            f'Total active: {Quest.objects.filter(is_active=True).count()}'
        ))
