# MindQuest 

> **Gamifikasi Rutinitas Hidup Sehat Harian**
> Dicoding Bootcamp Batch 11 — Capstone Project — Tim **DB11-G006**
> Tema: Healthy Lives & Well-being

MindQuest adalah aplikasi web full-stack yang mengubah kebiasaan self-care harian menjadi misi (quests) yang menyenangkan. Pengguna mendapat XP setiap menyelesaikan quest, naik level, membangun streak, membuka badge pencapaian, dan bersaing di leaderboard.

---

## ✅ Status: 100% Complete

| Minggu | Milestone | Status |
|---|---|---|
| 1 | Riset, UI/UX, Database Schema | ✅ Selesai |
| 2 | Setup, Autentikasi, Models | ✅ Selesai |
| 3 | Daily Quest, XP/Leveling, Mood | ✅ Selesai |
| 4 | Streak, Dashboard, Integrasi | ✅ Selesai |
| 5 | Testing, Deployment, Demo | ✅ Selesai |

**Fitur opsional yang juga diimplementasikan:** Leaderboard 🏆 · Sistem Badge/Achievement 🏅

---

##  Tech Stack

**Backend:** Django 4.2 · Django REST Framework · SimpleJWT · PostgreSQL/SQLite · drf-spectacular
**Frontend:** React 18 · Vite · Tailwind CSS · Axios · React Router · Recharts
**Testing:** pytest (backend) · Vitest + Testing Library (frontend)
**Deployment:** Railway/Render (backend) · Vercel (frontend)
**CI/CD:** GitHub Actions

---

##  Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_quests       # 20 quest default
python manage.py seed_badges       # 13 badge default
python manage.py createsuperuser
python manage.py runserver
```
Backend: `http://localhost:8000` · Swagger docs: `/api/docs/`

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
Frontend: `http://localhost:5173`

---

##  Menjalankan Test

```bash
# Backend (34 tests)
cd backend && python -m pytest

# Frontend (9 tests)
cd frontend && npm run test
```

---

##  API Endpoints

### Authentication
| Method | Endpoint | Deskripsi |
|---|---|---|
| POST | `/api/auth/register/` | Daftar user baru |
| POST | `/api/auth/login/` | Login (JWT tokens) |
| POST | `/api/auth/refresh/` | Refresh access token |
| GET | `/api/auth/me/` | Info user saat ini |
| GET | `/api/auth/profile/` | Profile + stats gamifikasi |

### Quests
| Method | Endpoint | Deskripsi |
|---|---|---|
| GET | `/api/quests/today/` | List quest aktif + status |
| GET | `/api/quests/today-stats/` | Statistik hari ini |
| POST | `/api/quests/{id}/complete/` | Selesaikan quest → +XP, streak, badge |
| GET | `/api/quests/history/` | Riwayat (paginated) |

### Mood, Badges, Leaderboard
| Method | Endpoint | Deskripsi |
|---|---|---|
| POST | `/api/mood/` | Log mood + energi harian |
| GET | `/api/mood/history/` | History 7 hari |
| GET | `/api/badges/` | Semua badge + status unlock |
| GET | `/api/leaderboard/` | Top 50 + rank kamu |

---

##  Sistem Gamifikasi

### XP Formula
XP untuk mencapai level N: **`50 × N × (N-1)`**

| Level | XP Total | Level | XP Total |
|---|---|---|---|
| 1 | 0 | 6 | 1,500 |
| 2 | 100 | 7 | 2,100 |
| 3 | 300 | 8 | 2,800 |
| 4 | 600 | 9 | 3,600 |
| 5 | 1,000 | 10 | 4,500 |

### XP per Quest
Easy: 10–15 XP · Medium: 20–25 XP · Hard: 30 XP

### Streak Logic
- Selesaikan ≥1 quest hari ini → streak +1 (jika kemarin aktif)
- Skip 1 hari → reset ke 0 · Best streak disimpan permanen

### Badge (13 total)
Berdasarkan 4 kriteria: total XP, level, streak, dan jumlah quest selesai. Otomatis unlock saat threshold tercapai.

---

##  Struktur Proyek

```
mindquest/
├── backend/
│   ├── config/          # settings, urls, wsgi
│   ├── users/           # auth, profile, leaderboard, XP/streak logic
│   ├── quests/          # quest model, completion, seed command
│   ├── mood/            # mood check-in
│   ├── badges/          # achievement system + award service
│   ├── requirements.txt
│   ├── Procfile         # deployment
│   └── railway.json
├── frontend/
│   ├── src/
│   │   ├── components/  # XPBar, QuestCard, StreakCounter, MoodCheckIn, Layout
│   │   ├── pages/       # Login, Register, Dashboard, Quests, History, Leaderboard, Badges
│   │   ├── contexts/    # AuthContext
│   │   ├── services/    # api.js (axios + auto-refresh JWT)
│   │   ├── utils/       # icon helper
│   │   └── __tests__/   # Vitest tests
│   ├── package.json
│   └── vercel.json
├── .github/workflows/   # CI pipeline
├── render.yaml
└── README.md
```

---

##  Tim DB11-G006

| ID Peserta | Nama | Peran |
|---|---|---|
| B26B11F019 | Abiyyu Akmal | Frontend Developer |
| B26B11F036 | Fersdoven Josua | Frontend Developer |
| B26B11F037 | Syakha Hanan Abdillah | Backend Developer |
| B26B11F041 | Pendri Mikola | Backend Developer |

---

## 📝 License
Capstone Project — Dicoding Bootcamp Batch 11. Educational use only.
