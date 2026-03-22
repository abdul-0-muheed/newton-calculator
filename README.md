# 🧮 Newton-Calculator  
> A lightweight web solver that finds roots of any expression with one click—no installs, no spreadsheets, just answers.

---

## 🚀 Demo
Live site: [https://newton-calculator.onrender.com](https://newton-calculator.onrender.com)  
GitHub repo: [https://github.com/abdul-0-muheed/newton-calculator](https://github.com/abdul-0-muheed/newton-calculator)

---

## 📖 Overview
Students, engineers and researchers often need quick numeric solutions to equations in physics, chemistry, biology, economics—any field that reduces to *f(x)=0*.  
Newton-Calculator wraps the classic Newton-Raphson algorithm in a friendly web UI: type an expression, give an initial guess, get the root plus a full convergence history. Every run is saved, so you can search, replay or audit previous work.

---

## ✨ Features
- 🧠 Symbolic math engine (parses, differentiates, evaluates)  
- ⚡ Sub-second convergence for most expressions  
- 🕰️ Persistent history (SQLite locally, PostgreSQL in prod)  
- 🔍 Search & filter past calculations  
- 📱 Responsive UI (works on phone, tablet, desktop)  
- 🌍 No install—runs in any modern browser  
- 🔒 Stateless API—easy to embed in Jupyter, MATLAB, Excel, etc.  
- 🚀 CI/CD pipeline with CVE scanning & zero-downtime deploys  

---

## 🏗️ Architecture
Clean MVC monolith:  
Browser ↔ Nginx ↔ Gunicorn ↔ Flask ↔ Service Layer ↔ SQL DB

### Key Components
| Layer | Responsibility |
|-------|----------------|
| Controller (`app.py`) | HTTP routing, input validation |
| Service (`solver.py`) | Symbolic differentiation + Newton iteration |
| Model (`models.py`) | Single `calculations` table (ANSI-SQL) |
| View (`templates/`) | Jinja2 pages, minimal JS for UX sugar |

### Data Flow
1. User posts expression + guess  
2. Controller delegates to Service  
3. Service compiles symbolic derivative, iterates until `|f(x)|<ε` or `iter>max`  
4. Result (root, steps, expression, timestamp) written to DB  
5. Controller returns HTML (or JSON if `Accept: application/json`)

---

## 🧰 Tech Stack
- **Backend**: Python 3.11, Flask 2.x, Gunicorn  
- **Math**: SymPy (symbolic), NumPy (numeric)  
- **DB**: SQLite (dev), PostgreSQL (prod) via SQLAlchemy  
- **Frontend**: Jinja2, vanilla JS, Pico.css  
- **Infra**: Docker, Nginx, GitHub Actions, Kubernetes (optional)  

---

## 📁 Project Structure
newton-calculator/
├── app.py                 # Flask entry point
├── solver.py              # Newton-Raphson engine
├── models.py              # SQLAlchemy model
├── requirements.txt
├── Dockerfile
├── .github/
│   └── workflows/
│       └── ci.yml         # lint → test → build → deploy
├── templates/
│   ├── index.html
│   └── history.html
├── static/
│   └── style.css
└── tests/
    └── test_solver.py
---

## ⚙️ Installation & Usage

### Local Quick-Start
bash
git clone https://github.com/abdul-0-muheed/newton-calculator.git
cd newton-calculator
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py
# open http://localhost:5000
### Docker
bash
docker build -t newton-calc .
docker run -p 80:8000 --env DATABASE_URL=sqlite:///local.db newton-calc
### Production (Render)
1. Fork repo  
2. Create Web Service → connect GitHub repo  
3. Set env vars (see below)  
4. Deploy → automatic rolling updates on push

---

## 🔌 API / Integrations
All browser routes also speak JSON:

| Method | Endpoint | Body | Response |
|--------|----------|------|----------|
| POST | `/solve` | `{"expr":"sin(x)-0.1*x","guess":2.0}` | `{"root":2.8523,"steps":5,"id":42}` |
| GET | `/history` | `?q=sin&limit=20` | `[{...},{...}]` |

Embed in Python:
python
import requests, json
r = requests.post("https://newton-calculator.onrender.com/solve",
                json={"expr":"x**3 - 2*x - 5", "guess":2})
print(r.json()["root"])  # 2.0945514815423265
---

## 🔐 Environment Variables
| Var | Default | Purpose |
|-----|---------|---------|
| `DATABASE_URL` | `sqlite:///app.db` | SQLAlchemy connection string |
| `ITERATION_LIMIT` | `100` | Max Newton steps |
| `TOLERANCE` | `1e-10` | Convergence threshold |
| `SECRET_KEY` | *(required)* | Flask sessions |
| `GUNICORN_WORKERS` | `4` | Worker count (prod) |

---

## 🧪 Testing & Build
bash
# lint
flake8 app.py solver.py models.py tests/
# unit tests
pytest tests/
# coverage
pytest --cov=solver tests/
# build image
docker buildx build --platform linux/amd64 -t newton-calc .
CI runs the above on every push; tagged releases auto-deploy.

---

## 🤖 AI Documentation Support
This README is auto-generated and kept in sync with the codebase via AI-assisted documentation tools. Contributions that update logic or API surface should regenerate docs (`make docs`) to ensure consistency.

---

## 📝 Notes
- Expressions use Python/SymPy syntax: `sin(x)`, `exp(x)`, `x**2`, etc.  
- Multiple roots? Try different initial guesses.  
- History is append-only—perfect for lab notebooks or compliance trails.

---

## 🤝 Contributing
1. Fork & branch (`feature/short-desc`)  
2. Add tests for new logic  
3. Ensure `pytest` and `flake8` pass  
4. Open PR → maintainer review → squash merge

---

## 📄 License
MIT © Abdul Muheed

---

## 📬 Contact
Issues & feature requests: [GitHub Issues](https://github.com/abdul-0-muheed/newton-calculator/issues)  
Email: muheed.abdul0@gmail.com