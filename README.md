# MindQuest 

> Gamifikasi Rutinitas Hidup Sehat Harian
> Dicoding Bootcamp Batch 11 — Capstone Project — Tim DB11-G006

MindQuest adalah aplikasi web full-stack yang mengubah kebiasaan self-care harian menjadi misi (quests) yang menyenangkan. Pengguna mendapat XP setiap menyelesaikan quest, naik level, membangun streak, dan mencatat mood harian.

---

## 📊 Status Progress: ~42% Complete

| Minggu | Milestone | Status |
|---|---|---|
| 1 | Riset, UI/UX, Database Schema | ✅ Selesai |
| 2 | Setup, Autentikasi, Models | ✅ Selesai |
| 3 | Daily Quest, XP/Leveling, Mood | 🟡 50% |
| 4 | Streak, Dashboard, Integrasi | ⏳ Belum |
| 5 | Testing, Deployment, Demo | ⏳ Belum |

---

## 🏗️ Arsitektur

```
mindquest/
├── backend/      # Django + DRF + JWT + PostgreSQL/SQLite
├── frontend/     # React + Vite + Tailwind + Recharts
└── docs/         # Dokumentasi tambahan
```

**Tech Stack:**
- **Backend**: Django 4.2, Django REST Framework, SimpleJWT, drf-spectacular
- **Frontend**: React 18, Vite, Tailwind CSS, Axios, React Router, Recharts
- **Database**: SQLite (dev), PostgreSQL (production)
- **Deployment**: Railway/Render (backend), Vercel/Netlify (frontend)

---

## 🚀 Quick Start

### 1. Backend (Django)

```bash
cd backend

# Buat virtualenv
python -m venv venv
source venv/bin/activate          # Linux/Mac
# venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Copy env
cp .env.example .env

# Migrate database
python manage.py migrate

# Seed 20 quest default
python manage.py seed_quests

# Buat superuser (untuk admin panel)
python manage.py createsuperuser

# Jalankan server
python manage.py runserver
```

Backend akan jalan di `http://localhost:8000`. Buka:
- `/admin/` — Django admin panel
- `/api/docs/` — Swagger UI dokumentasi API
- `/api/redoc/` — Redoc UI dokumentasi API

### 2. Frontend (React)

```bash
cd frontend

# Install dependencies
npm install

# Copy env
cp .env.example .env

# Jalankan dev server
npm run dev
```

Frontend akan jalan di `http://localhost:5173`.

---

## 🎯 Fitur yang Sudah Diimplementasikan

### Backend ✅
- [x] Custom User model + UserProfile dengan auto-create signal
- [x] JWT authentication (register, login, refresh token)
- [x] Quest model dengan 6 kategori (Physical, Mental, Sleep, Nutrition, Mindfulness, Digital)
- [x] UserQuestLog dengan unique constraint per hari
- [x] MoodLog harian (1-5 scale)
- [x] **Logika XP dan leveling**: formula `50 × level × (level-1)` (Level 2: 100 XP, Level 3: 250 XP, Level 4: 450 XP, dst.)
- [x] **Streak detection algorithm**: deteksi consecutive days, reset otomatis jika skip hari
- [x] API endpoints lengkap untuk auth, quests, dan mood
- [x] Atomic transactions untuk konsistensi data
- [x] Seed command untuk 20 quest default
- [x] Django Admin teregistrasi
- [x] Swagger/OpenAPI docs auto-generated

### Frontend ✅
- [x] AuthContext + Protected routes
- [x] API service dengan auto-refresh JWT token
- [x] Halaman Login & Register
- [x] Dashboard dengan XP bar, streak counter, statistik
- [x] Halaman Daily Quests dengan filter kategori
- [x] Komponen Mood Check-in (1-5 emoji scale)
- [x] Grafik tren mood & energi mingguan (Recharts)
- [x] Toast notification untuk feedback aksi
- [x] Layout responsive (mobile + desktop)
- [x] Level-up notification

### Belum Diimplementasikan ⏳
- [ ] Unit tests komprehensif (pytest backend, Vitest frontend)
- [ ] Bug fixing dari user testing
- [ ] Production deployment (Railway/Vercel)
- [ ] Loading states & error boundaries lebih granular
- [ ] Demo video & dokumentasi presentasi

### Optional (Nice-to-have) 🎨
- [ ] Leaderboard antar user
- [ ] Push notification reminder harian
- [ ] Badge & achievement system
- [ ] Animasi level-up

---

## 📚 API Endpoints

### Authentication
| Method | Endpoint | Deskripsi |
|---|---|---|
| POST | `/api/auth/register/` | Daftar user baru |
| POST | `/api/auth/login/` | Login (return JWT tokens) |
| POST | `/api/auth/refresh/` | Refresh access token |
| GET | `/api/auth/me/` | Info user saat ini |
| GET | `/api/auth/profile/` | Profile dengan stats gamifikasi |

### Quests
| Method | Endpoint | Deskripsi |
|---|---|---|
| GET | `/api/quests/today/` | List quest aktif + status hari ini |
| GET | `/api/quests/today-stats/` | Statistik penyelesaian hari ini |
| POST | `/api/quests/{id}/complete/` | Tandai quest selesai → +XP, update streak |
| GET | `/api/quests/history/` | Riwayat quest yang sudah diselesaikan |

### Mood
| Method | Endpoint | Deskripsi |
|---|---|---|
| POST | `/api/mood/` | Log mood + energi harian |
| GET | `/api/mood/history/` | History 7 hari terakhir |

---

## 🧮 Sistem Gamifikasi

### XP Formula
XP yang dibutuhkan untuk mencapai level N: `50 × N × (N-1)`

| Level | XP Total |
|---|---|
| 1 | 0 |
| 2 | 100 |
| 3 | 250 |
| 4 | 450 |
| 5 | 750 |
| 10 | 4,500 |

### XP per Quest (berdasarkan difficulty)
- **Easy**: 10–15 XP
- **Medium**: 20–25 XP
- **Hard**: 30 XP

### Streak Logic
- Selesaikan minimal 1 quest hari ini → streak +1 (jika kemarin juga aktif)
- Skip 1 hari → streak reset ke 0
- Best streak disimpan permanen

---

## 👥 Tim DB11-G006

| ID Peserta | Nama | Peran |
|---|---|---|
| B26B11F019 | Abiyyu Akmal | Frontend Developer |
| B26B11F036 | Fersdoven Josua | Frontend Developer |
| B26B11F037 | Syakha Hanan Abdillah | Backend Developer |
| B26B11F041 | Pendri Mikola | Backend Developer |

---

## 📝 License

Capstone Project — Dicoding Bootcamp Batch 11. Educational use only.
