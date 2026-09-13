# Basgiath War College — Rider Portal API

FastAPI backend for the portal template, backed by Supabase Postgres.

## How sign-up decides student vs. faculty

`role_for_email()` in `app/auth_utils.py` checks the email domain:
- ends with `@niet.co.in` → `role = "student"`
- anything else → `role = "faculty"`

Each new user gets an auto-generated ERP ID: `CDT-2026-0001` for students,
`FAC-2026-0001` for faculty (year = signup year, number = running count for that role).

## Setup

1. **Create a Supabase project** at supabase.com (free tier is fine) and grab your
   Postgres connection string from Project Settings → Database → Connection string.

2. **Install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and fill in `DATABASE_URL` (your Supabase connection string) and a random `SECRET_KEY`:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

4. **Seed the academic calendar** (creates tables too, if they don't exist yet)
   ```bash
   python seed.py
   ```

5. **Run the API**
   ```bash
   uvicorn app.main:app --reload
   ```
   Interactive docs: http://127.0.0.1:8000/docs

## Endpoints

| Method | Path                  | Auth | Notes |
|--------|-----------------------|------|-------|
| POST   | `/api/auth/signup`    | —    | name, email, password + year/semester/branch/section |
| POST   | `/api/auth/login`     | —    | email + password |
| GET    | `/api/me`              | ✅   | current user's profile |
| GET    | `/api/attendance`      | ✅   | current student's subject attendance |
| GET    | `/api/calendar/events` | —    | optional `?year=2026&month=8` filters |

Auth routes return `{ access_token, token_type, user }`. Send the token on
protected routes as `Authorization: Bearer <access_token>`.

## Wiring up the frontend template

In `basgiath-portal-template.html`, point the login/signup form submit handlers at
`http://127.0.0.1:8000/api/auth/login` and `/api/auth/signup`, store the returned
`access_token` (e.g. in a JS variable or `sessionStorage`), and send it as a Bearer
token on `/api/me` and `/api/attendance` calls. CORS is wide open (`allow_origins=["*"]`)
for local development — tighten it to your real frontend origin before deploying.

## Notes / known simplifications

- ERP ID numbering counts existing rows per role — fine for a class project, but not
  safe against concurrent signups at scale (would need a DB sequence for that).
- Student attendance rows are seeded with random sample percentages at signup so the
  page isn't empty; swap that block in `routers/auth.py` for real data entry later.
- Faculty accounts don't get attendance rows (attendance is student-only for now).
