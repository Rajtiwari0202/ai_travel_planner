# Neon Setup

Create a free Neon PostgreSQL project for the public demo.

Use:

- pooled connection string for the application `DATABASE_URL`
- direct connection string only when a migration workflow requires it

Never commit connection strings. Redact passwords in notes and screenshots.

After setting `DATABASE_URL`, run:

```powershell
cd F:\travelAgenticAi\backend
..\venv\Scripts\python.exe scripts\migrate.py
..\venv\Scripts\python.exe scripts\check_database.py
```
