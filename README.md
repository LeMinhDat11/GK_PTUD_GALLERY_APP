# ✦ Lumière — Gallery App

A personal photo gallery web app built with **FastAPI** + **ReactJS** + **SQLite**.

---

## Features

- **Authentication** — Register / Login with JWT tokens
- **Upload Photos** — Drag & drop or click to upload (PNG, JPG, GIF, WEBP, max 10MB)
- **Gallery View** — Responsive grid with small/large layout toggle
- **Search** — Real-time search by photo title
- **Photo Detail** — Full-view with metadata
- **Edit** — Update photo title and description inline or in detail view
- **Delete** — Remove photos from gallery and disk

---

## Tech Stack

| Layer    | Technology        |
|----------|-------------------|
| Backend  | FastAPI + Uvicorn |
| Frontend | React 18 + Vite   |
| Database | SQLite (via SQLAlchemy) |
| Auth     | JWT + bcrypt      |
| Storage  | Local filesystem  |

---

## Project Structure

```
gallery-app/
├── backend/
│   ├── main.py          # FastAPI routes
│   ├── models.py        # SQLAlchemy models (User, Photo)
│   ├── schemas.py       # Pydantic schemas
│   ├── auth.py          # JWT + password utils
│   ├── requirements.txt
│   └── uploads/         # Stored images
├── frontend/
│   ├── src/
│   │   ├── api.js              # Axios API client
│   │   ├── App.jsx             # Router
│   │   ├── context/
│   │   │   └── AuthContext.jsx # Auth state
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── PhotoCard.jsx
│   │   │   ├── UploadModal.jsx
│   │   │   └── Toast.jsx
│   │   └── pages/
│   │       ├── LoginPage.jsx
│   │       ├── RegisterPage.jsx
│   │       ├── GalleryPage.jsx
│   │       └── PhotoDetailPage.jsx
│   └── vite.config.js
└── start.sh
```

---

## Setup & Run

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
# API: http://localhost:8000
# Swagger docs: http://localhost:8000/docs
py -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
# App: http://localhost:3000
```

### Or run both at once:

```bash
chmod +x start.sh
./start.sh
```

---

## API Endpoints

| Method | Endpoint               | Description         | Auth |
|--------|------------------------|---------------------|------|
| POST   | /api/auth/register     | Register new user   | ✗    |
| POST   | /api/auth/login        | Login               | ✗    |
| GET    | /api/auth/me           | Get current user    | ✓    |
| GET    | /api/photos            | List photos (+ ?search=) | ✓ |
| GET    | /api/photos/{id}       | Get photo detail    | ✓    |
| POST   | /api/photos            | Upload photo        | ✓    |
| PATCH  | /api/photos/{id}       | Update title/desc   | ✓    |
| DELETE | /api/photos/{id}       | Delete photo        | ✓    |
