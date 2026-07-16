# cvv-app — CV Builder

A small full-stack web app for building a CV: fill in a form (personal info,
work experience, education, skills) and get a clean, print-ready CV page you
can save as a PDF straight from the browser.

- **Backend:** Python, Django, Django REST Framework, SQLite
- **Frontend:** Vue 3 (Composition API), TypeScript, Vite, Pinia, HTML/CSS

---

## Table of contents

- [Project structure](#project-structure)
- [How it works](#how-it-works)
- [Requirements](#requirements)
- [Run it locally](#run-it-locally)
  - [1. Get the code](#1-get-the-code)
  - [2. Backend setup](#2-backend-django)
  - [3. Frontend setup](#3-frontend-vue--vite)
  - [4. Open the app](#4-open-the-app)
- [Everyday commands](#everyday-commands)
- [Production build](#production-build)
- [Publishing your own copy to GitHub](#publishing-your-own-copy-to-github)
- [Troubleshooting](#troubleshooting)
- [Possible improvements](#possible-improvements)

---

## Project structure

```
cvv-app/
├── backend/                     # Django project (REST API)
│   ├── manage.py
│   ├── requirements.txt
│   ├── resume_builder/          # project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── resumes/                 # "resumes" app
│       ├── models.py            # Resume, Experience, Education, Skill
│       ├── serializers.py       # DRF nested serialization
│       ├── views.py             # ResumeViewSet (CRUD)
│       ├── urls.py
│       ├── admin.py
│       └── migrations/
├── frontend/                    # Vue 3 + TypeScript (Vite)
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── src/
│       ├── main.ts
│       ├── App.vue
│       ├── router/index.ts      # routes: /, /resumes/new, /resumes/:id/edit, /resumes/:id/preview
│       ├── store/resume.ts      # Pinia store
│       ├── api/                 # axios client + API calls
│       ├── types/resume.ts      # TypeScript interfaces
│       ├── views/               # ResumeListView, ResumeEditView, ResumePreviewView
│       └── assets/main.css      # global styles / design tokens
├── .gitignore
└── README.md
```

## How it works

- Django exposes a REST API at `/api/resumes/...` for CRUD operations on CVs.
- The Vue app talks to that API, keeps the CV currently being edited in a
  Pinia store, and renders three screens: a list of your CVs, an edit form,
  and a print-ready preview page (`window.print()` → "Save as PDF").
- In development, Vite proxies `/api/...` requests to Django (see
  `frontend/vite.config.ts`), so you don't need to worry about CORS locally.
  `django-cors-headers` is still wired up for direct cross-origin requests.

---

## Requirements

- **Python** 3.10+
- **Node.js** 18+ and npm
- **Git** (to clone/publish the repo)
- Two terminal windows (one for the backend, one for the frontend)

---

## Run it locally

### 1. Get the code

If you already have the project folder, just `cd` into it. Otherwise, clone
it from GitHub:

```bash
git clone https://github.com/YOUR_USERNAME/cvv-app.git
cd cvv-app
```

### 2. Backend (Django)

```bash
cd backend

# create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# apply migrations (creates backend/db.sqlite3)
python manage.py migrate

# (optional) create an admin user for /admin/
python manage.py createsuperuser

# start the dev server
python manage.py runserver
```

The backend runs at `http://127.0.0.1:8000/`:
- API: `http://127.0.0.1:8000/api/resumes/`
- Admin panel: `http://127.0.0.1:8000/admin/`

Keep this terminal running.

### 3. Frontend (Vue + Vite)

Open a **second terminal** in the project root:

```bash
cd frontend

npm install
npm run dev
```

### 4. Open the app

Visit **http://localhost:5173/** in your browser. All `/api/...` requests
from the frontend are automatically proxied to the Django backend running
on port 8000, so both servers need to stay running at the same time.

---

## Everyday commands

| Task                          | Command (from the right folder)     |
|--------------------------------|--------------------------------------|
| Start backend                  | `backend/` → `python manage.py runserver` |
| Start frontend                 | `frontend/` → `npm run dev`          |
| Create a new migration         | `backend/` → `python manage.py makemigrations` |
| Apply migrations               | `backend/` → `python manage.py migrate` |
| Create an admin user            | `backend/` → `python manage.py createsuperuser` |
| Install new frontend package   | `frontend/` → `npm install <package>` |
| Type-check the frontend        | `frontend/` → `npm run build` (runs `vue-tsc`) |

---

## Production build

```bash
cd frontend
npm run build      # outputs static files to frontend/dist
```

Serve the `frontend/dist` folder with any static host (Nginx, Vercel,
Netlify, etc.), and point `frontend/src/api/client.ts`'s `baseURL` at your
deployed backend URL instead of the local `/api/` proxy path.

For the backend, run Django behind a real application server such as
`gunicorn` or `uwsgi`, put it behind a reverse proxy (Nginx/Caddy), and in
`backend/resume_builder/settings.py`:
- set `DEBUG = False`
- set `ALLOWED_HOSTS` to your real domain(s)
- move `SECRET_KEY` into an environment variable
- switch `CORS_ALLOWED_ORIGINS` to your production frontend URL

---

## Publishing your own copy to GitHub

These steps assume you have this `cvv-app` folder locally and want to push
it to your own GitHub account.

### 1. Create a repository on GitHub

1. Go to [github.com](https://github.com) → **New repository**.
2. Name it, e.g. `cvv-app`.
3. Leave "Add a README", ".gitignore" and "license" **unchecked** — this
   project already includes them.
4. Click **Create repository** and copy the repository URL, e.g.
   `https://github.com/YOUR_USERNAME/cvv-app.git`.

### 2. Initialize git and make your first commit

From the `cvv-app/` root folder:

```bash
git init
git add .
git commit -m "Initial commit: CV builder (Django + Vue/TypeScript)"
```

The included `.gitignore` already excludes `node_modules/`, `venv/`,
`db.sqlite3`, and other files you don't want in version control.

### 3. Connect to GitHub and push

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/cvv-app.git
git push -u origin main
```

Replace `YOUR_USERNAME` (and `cvv-app` if you named the repo differently).

If GitHub asks you to authenticate, use a **Personal Access Token** instead
of your account password (GitHub no longer accepts passwords for git over
HTTPS): **GitHub → Settings → Developer settings → Personal access tokens →
Generate new token**, then use the token as the password when prompted.

### 4. Pushing future changes

```bash
git add .
git commit -m "Describe what changed"
git push
```

### 5. Letting someone else run it

Anyone with access to the repo can now get a working copy with:

```bash
git clone https://github.com/YOUR_USERNAME/cvv-app.git
cd cvv-app
```

...and then follow the [Run it locally](#run-it-locally) steps above,
starting from step 2 (backend setup).

---

## Troubleshooting

- **`ModuleNotFoundError: No module named 'django'`** — you forgot to
  activate the virtual environment (`source venv/bin/activate`) or run
  `pip install -r requirements.txt`.
- **Frontend loads but data never appears / network errors in the console**
  — make sure the Django server is actually running on port 8000; the Vite
  proxy only forwards requests, it doesn't start the backend for you.
- **`CORS` errors in the browser console** — this normally shouldn't happen
  in dev mode because of the Vite proxy. If you changed the frontend port,
  update `frontend/vite.config.ts` and `CORS_ALLOWED_ORIGINS` in
  `backend/resume_builder/settings.py` to match.
- **Port already in use** — stop whatever else is using port 8000 or 5173,
  or run `python manage.py runserver 8001` / `npm run dev -- --port 5174`
  and update the Vite proxy target accordingly.

---

## Possible improvements

- Photo upload for the CV
- Server-side PDF export (e.g. via WeasyPrint) instead of `window.print()`
- Multiple CV templates/themes
- User accounts, so CVs are private per user instead of globally visible
