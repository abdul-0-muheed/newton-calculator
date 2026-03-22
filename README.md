# 🧮 Newton Calculator  
> A lightweight web app that solves non-linear equations with Newton’s method and remembers every step.

---

## 🚀 Demo
🌍 **Live Site:** [https://newton-calculator.onrender.com](https://newton-calculator.onrender.com)  
📁 **Source:** [https://github.com/abdul-0-muheed/newton-calculator](https://github.com/abdul-0-muheed/newton-calculator)

---

## 📖 Overview
Solving transcendental or polynomial equations numerically is a daily task for students, teachers, and lab researchers.  
Newton Calculator gives you **instant convergence feedback** in the browser and **persists every attempt** so you can revisit earlier work—no installs, no spreadsheets, no MATLAB license required.

---

## ✨ Features
- ⚡ **Single-page** Newton–Raphson solver  
- 🧠 **Symbolic derivative** generation—no external math libs  
- 🕰️ **Automatic history**—every run is stored locally  
- 📱 **Responsive UI**—works on phones, tablets, and Raspberry Pi  
- 🔐 **Zero-config** SQLite backend—no ORM, no migrations  
- 🚀 **CI/CD ready**—GitHub Actions build & push container images  

---

## 🏗️ Architecture
Classic **MVC** pattern, intentionally thin layers:

┌-------------┐     ┌-------------┐     ┌-------------┐
│   Browser   │ <---> │   Flask     │ <---> │   SQLite    │
│   (View)    │       │(Controller) │       │  (Model)    │
└-------------┘     └-------------┘     └-------------┘
---

## 🔑 Key Components
| File / Module | Purpose |
|---------------|---------|
| `app.py` | Flask factory & route registration |
| `solver.py` | Symbolic diff + Newton iteration engine |
| `schema.sql` | Single `calculations` table definition |
| `templates/` | Jinja2 UI (home + result) |
| `static/` | CSS, favicon, client-side JS |
| `Dockerfile` | Slim Python image, Gunicorn entrypoint |

---

## 📡 Data Flow
1. User enters `f(x)=…` and initial guess `x₀`  
2. Server symbolically computes `f'(x)`  
3. Newton loop runs until `|f(x)| < ε` or max iterations  
4. Result (`root`, `iterations`, `converged`) inserted into SQLite  
5. Browser receives rendered result page & history table

---

## 🧰 Tech Stack
- **Backend:** Python 3.11, Flask 2.x, Gunicorn  
- **Frontend:** Jinja2, vanilla CSS, ES5 JS  
- **Database:** SQLite (file-based)  
- **Container:** Docker, GitHub Container Registry  
- **CI/CD:** GitHub Actions (lint → test → build → push)  

---

## 📁 Project Structure
newton-calculator/
├── app.py
├── solver.py
├── db.py
├── requirements.txt
├── Dockerfile
├── .github/workflows/ci.yml
├── templates/
│   ├── index.html
│   └── result.html
├── static/
│   └── style.css
└── tests/
    └── test_solver.py
---

## ⚙️ Installation & Usage
### Local Development
bash
git clone https://github.com/abdul-0-muheed/newton-calculator.git
cd newton-calculator
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
flask --app app.py --debug run
Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Docker (Recommended)
bash
docker build -t newton-calc .
docker run -p 8000:8000 newton-calc
Gunicorn serves on port **8000**.

---

## 🔌 API / Integrations
**POST** `/solve`  
**Body (JSON):**
json
{
  "expression": "x**3 - 2*x - 5",
  "initial_guess": 2.0
}
**Response:**
json
{
  "root": 2.0945514815423265,
  "iterations": 5,
  "converged": true
}
---

## 🔐 Environment Variables
| Var | Default | Purpose |
|-----|---------|---------|
| `PORT` | `8000` | Gunicorn bind port |
| `DATABASE_URL` | `sqlite:///calculations.db` | SQLite file path |
| `FLASK_ENV` | `production` | Flask config profile |

---

## 🧪 Testing & Build
bash
pytest tests/
GitHub Actions automatically lints (`ruff`), tests, builds, and pushes the image to **ghcr.io** on every push to `main`.

---

## 📝 Notes
- No authentication—history is local to the container volume.  
- Designed for **single-user** or **classroom** demos.  
- Swap SQLite for Postgres by changing `DATABASE_URL`.

---

## 🤝 Contributing
1. Fork & branch (`git checkout -b feature/amazing`)  
2. Commit & push  
3. Open a PR—CI must pass ✅

---

## 📄 License
MIT © Abdul Muheed

---

## 📬 Contact
For questions or feature requests, open an issue or reach out via GitHub Discussions.