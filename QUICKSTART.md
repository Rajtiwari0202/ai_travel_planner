# Quickstart

## Windows PowerShell

```powershell
cd F:\travelAgenticAi
.\venv\Scripts\python.exe -m pip install -r backend\requirements.txt

cd backend
..\venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

In another terminal:

```powershell
cd F:\travelAgenticAi\frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Docker Compose Demo Deploy

```powershell
cd F:\travelAgenticAi
docker compose up -d --build
```

Open `http://127.0.0.1:18080`.

Stop it with:

```powershell
docker compose down
```

## Linux/macOS

```bash
cd travelAgenticAi
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

In another terminal:

```bash
cd frontend
npm install
npm run dev
```
