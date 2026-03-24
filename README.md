# 🧮  Newton Calculator  
A lightweight web app that finds roots of any equation with Newton’s method — and remembers every step for you.

🌐 **Live Demo** → [newton-calculator.onrender.com](https://newton-calculator.onrender)  
📦 **Repo** → [github.com/abdul-0-muheed/newton-calculator](https://github.com/abdu-0-muheed/newton-calculator)

---

## 📖  Overview
Solving `f(x)=0` is the bread-and-buff of physics, chemistry, engineering, and data-science homework — but spreadsheets and handheld calculators rarely show *how* the answer was found.  
Newton Calculator **visualises every iteration**, stores your work, and lets you share a short link to the full history.  
No installs, no signup, just paste your equation and see the magic.

---

## ✨  Features
- ⚡  Instant root finding via Newton–Raphson (pure-Python, no heavy deps)  
- 🧠  Symbolic derivative auto-computed with `sympy` (falls back to numeric)  
- 📚  Automatic history: every attempt is persisted in SQLite  
- 🔗  Shareable URLs (`/calc/<id>`) for teachers / TAs / peers  
- 🎨  Clean, responsive UI (mobile first)  
- 🕵️  No tracking cookies; only session cookie for CSRF protection  
- 🧪  Optional dark theme for late–night labs  
- 🌐  Works fully offline after first load (Service-Worker cached)

---

## 🏗️  Architecture
MVC pattern inside a single Docker-ready container.

Browser  ──HTTPS──▶  Nginx  ──▶  Gunicorn/Flask  ──▶  SQLite
                                                      (calc.db)
All state lives in the DB; the service layer is **stateless** → horizontal scaling = `kubectl scale`.

---

## 🧩  Key Components
| Component | Responsibility |
|---------|----------------|
| `controller.py` | HTTP routing, validation, OAuth (Google) |
| `solver.py` | SymPy AST parsing + Newton iteration |
| `models.py` | SQLAlchemy models (`Calculation`, `User`) |
| `repository.py` | DAO layer; keeps DB details out of controllers |
| `templates/*.html` | Jinja2 views with HTMX for SPA-like UX |
| `static/js/*.js` | Visualises convergence graph with Chart.js |

---

## 🔄  Data Flow
1. User enters expression `exp(x)-x-2` and initial guess `x₀=0.5`  
2. Frontend POSTs JSON to `/api/calc`  
3. Backend parses, iterates until `|f(x)|<1e-10` or max 100 iterations  
4. Result stored → returns `{id, root, iterations, trace[]}`  
5. Frontend renders table + graph  
6. Share link `/calc/<id>` works for anyone

---

## 🧪  Tech Stack
- **Runtime**: Python 3.11  
- **Web**: Flask 2.x, Jinja2, HTMX, Alpine.js  
- **Math**: SymPy, NumPy (optional speed-up)  
- **DB**: SQLite (dev) / PostgreSQL (prod)  
- **WSGI**: Gunicorn  
- **Reverse proxy**: Nginx (TLS 1.3)  
- **CI/CD**: GitHub Actions → Docker Hub → Render

---

## 📁  Project Structure
newton-calculator/
├── app/
│   ├── __init__.py
│   ├── controller.py
│   ├── solver.py
│   ├── models.py
│   └── repository.py
├── migrations/
├── templates/
│   ├── base.html
│   ├── index.html
│   └── calc.html
├── static/
│   ├── css/
│   └── js/
├── tests/
├── Dockerfile
├── requirements.txt
└── run.py
---

## 🚀  Installation & Usage
### Local (quick)
bash
git clone https://github.com/abdul-0-muheed/newton-calculator.git
cd newton-calculator
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python run.py
# open http://localhost:5000
### Docker
bash
docker build -t newton-calc .
docker run -p 80:80 --env-file=.env newton-calc
### Production (Render)
1. Fork repo → connect to Render web service  
2. Set env vars (see below)  
3. Deploy ✔️

---

## 🔌  API / Integrations
| Method | Endpoint | Body | Response |
|--------|----------|------|----------|
| `POST` | `/api/calc` | `{"expr":"sin(x)","x0":0.5}` | Calculation object |
| `GET`  | `/api/calc/<id>` | — | Same object |
| `GET`  | `/api/history?limit=20` | — | Array of objects |
| `GET`  | `/health` | — | `{"status":"ok"}` |

---

## 🔐  Environment Variables
| Variable | Example | Purpose |
|----------|---------|---------|
| `SECRET_KEY` | `YOUR_SECRET_KEY` | Session encryption |
| `DATABASE_URL` | `sqlite:///calc.db` | DB connection |
| `GOOGLE_CLIENT_ID` | `YOUR_CLIENT_ID` | OAuth (optional) |
| `ALLOWED_DOMAIN` | `university.edu` | Restrict login |
| `MAX_ITER` | `100` | Newton safety cap |

---

## 🧪  Testing & Build
bash
# unit tests
pytest tests/

# coverage
pytest --cov=app tests/

# lint
ruff check app/
mypy app/

# build image
docker buildx build --platform linux/amd64 -t newton-calc .
---

## 📝  Notes
- The solver falls back to numeric derivative if symbolic fails.  
- Convergence is **not** guaranteed — divergence returns helpful message.  
- History is **paginated**; old records are soft-deleted after 90 d (configurable).

---

## 🤝  Contributing
1. Fork & branch (`feature/xyz`)  
2. Write tests for new behaviour  
3. PR against `main` with clear description  
4. CI must be green ✅

---

## 📄  License
MIT © Abdul Muheed

---

## 📬  Contact
Open an issue or start a discussion — responses within 24 h.  
Happy solving! 🚀