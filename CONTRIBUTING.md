# Contributing — MindQuest (DB11-G006)

## Branch Strategy
- `main` — production-ready (protected, PR only)
- `dev` — integration branch
- `feature/*` — feature branches dari dev

## Workflow
1. `git checkout dev && git pull origin dev`
2. `git checkout -b feature/nama-fitur`
3. Commit: `git commit -m "feat: deskripsi"`
4. Push & buka PR ke `dev`
5. Review minimal 1 anggota sebelum merge

## Commit Convention
`feat:` fitur baru · `fix:` bug fix · `docs:` dokumentasi · `test:` test · `refactor:` · `chore:`

## Pembagian Tim
| Anggota | Area |
|---|---|
| Abiyyu Akmal | Frontend (UI, gamification state) |
| Fersdoven Josua | Frontend (API integration, deploy) |
| Syakha Hanan Abdillah | Backend (auth, models, quest API) |
| Pendri Mikola | Backend (XP logic, streak, deploy) |
