# Panduan Deployment MindQuest

Deploy ke production: backend ke **Railway**, frontend ke **Vercel**, database PostgreSQL gratis.

---

## Bagian 1 — Deploy Backend ke Railway

### 1. Persiapan
- Push code ke GitHub (lihat README utama)
- Daftar akun di https://railway.app (login dengan GitHub)

### 2. Buat Project
1. Klik **New Project** → **Deploy from GitHub repo**
2. Pilih repo `mindquest`
3. Railway akan mendeteksi folder. Set **Root Directory** ke `backend`

### 3. Tambahkan PostgreSQL
1. Di project, klik **New** → **Database** → **Add PostgreSQL**
2. Railway otomatis membuat variable `DATABASE_URL`

### 4. Set Environment Variables
Di service backend → tab **Variables**, tambahkan:

```
SECRET_KEY=<generate-random-string-50-karakter>
DEBUG=False
DATABASE_URL=${{Postgres.DATABASE_URL}}
CORS_ALLOWED_ORIGINS=https://nama-app-kamu.vercel.app
```

Generate SECRET_KEY dengan:
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 5. Deploy
Railway otomatis menjalankan `Procfile` (migrate + seed + gunicorn). Tunggu sampai selesai. Catat URL backend, misal `https://mindquest-production.up.railway.app`

### 6. Verifikasi
Buka `https://url-backend-kamu/api/docs/` — harus muncul Swagger UI.

---

## Bagian 2 — Deploy Frontend ke Vercel

### 1. Persiapan
Daftar akun di https://vercel.com (login dengan GitHub)

### 2. Import Project
1. Klik **Add New** → **Project**
2. Import repo `mindquest`
3. Set **Root Directory** ke `frontend`
4. Framework Preset: **Vite** (otomatis terdeteksi)

### 3. Set Environment Variable
Tambahkan:
```
VITE_API_BASE_URL=https://url-backend-railway-kamu/api
```
(Ganti dengan URL backend dari Railway, jangan lupa `/api` di akhir)

### 4. Deploy
Klik **Deploy**. Tunggu ~1-2 menit. Vercel kasih URL, misal `https://mindquest.vercel.app`

### 5. Update CORS di Railway
Kembali ke Railway → Variables → update `CORS_ALLOWED_ORIGINS` dengan URL Vercel kamu, lalu redeploy.

---

## Bagian 3 — Verifikasi Akhir

1. Buka URL Vercel di browser
2. Daftar akun baru
3. Selesaikan beberapa quest → cek XP bertambah
4. Cek dashboard, leaderboard, badges berfungsi

Kalau semua jalan, **link untuk submit Dicoding** adalah URL Vercel kamu.

---

## Alternatif: Backend ke Render

Jika lebih suka Render daripada Railway:
1. Daftar di https://render.com
2. **New** → **Blueprint** → connect repo
3. Render akan baca `render.yaml` otomatis (sudah include database + seed)
4. Set `CORS_ALLOWED_ORIGINS` dengan URL Vercel

---

## Troubleshooting

**CORS error di browser console**
→ Pastikan `CORS_ALLOWED_ORIGINS` di backend = URL Vercel persis (dengan https, tanpa trailing slash)

**500 error saat akses API**
→ Cek logs di Railway/Render. Biasanya `DATABASE_URL` belum ter-set atau migrate gagal.

**Frontend blank putih**
→ Cek `VITE_API_BASE_URL` sudah benar dan diakhiri `/api`. Rebuild di Vercel.

**Quest kosong setelah deploy**
→ Seed command belum jalan. Di Railway, cek `Procfile` ter-eksekusi, atau jalankan manual via Railway CLI: `railway run python manage.py seed_quests`

---

## Checklist Submission Dicoding

- [ ] Backend live & `/api/docs/` accessible
- [ ] Frontend live di Vercel
- [ ] Bisa register + login
- [ ] Quest, XP, streak, mood berfungsi
- [ ] Leaderboard & badges tampil
- [ ] Repository GitHub public
- [ ] README lengkap
- [ ] Link Vercel siap di-submit
