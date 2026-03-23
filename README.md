# 🧮 Newton Calculator  
A lightweight web app that finds real roots of polynomials with the Newton-Raphson method, stores every step, and renders the full convergence history in your browser.

🌐 **Live Demo:** [https://newton-calculator.onrender.com](https://newton-calculator.onrender.com)  
📁 **Source:** [https://github.com/abdul-0-muheed/newton-calculator](https://github.com/abdul-0-muheed/newton-calculator)

---

## 🚀 Overview
Students and instructors often need quick, repeatable numerical solutions but don’t want to install heavy math suites. Newton Calculator solves this by wrapping the classic Newton-Raphson algorithm in a dead-simple web form. Enter any polynomial, pick a starting guess, and watch every iteration appear instantly—no installs, no spreadsheets, no black boxes.

---

## ✨ Features
- ⚡ **Instant solving** – type `x**3 - 2*x - 5`, hit Solve, see the root.  
- 📊 **Full history table** – every xₙ, f(xₙ), f'(xₙ) and error is persisted and displayed.  
- 🔁 **Experiment-friendly** – change the initial guess and compare convergence speeds.  
- 💾 **Persistent storage** – SQLite by default, PostgreSQL one-env-var away.  
- 🎓 **Instructor mode** – replay any past calculation via shareable ID.  
- 🪶 **Zero JS** – works with cookies off, loads in milliseconds.  

---

## 🏗️ Architecture
Strict MVC monolith designed for clarity, not micro-service sprawl.

Browser (View)  ⇄  Flask Controller  ⇄  SQL Model (calculations table)
### Key Components
- `app.py` – Flask controller; handles form POST, calls solver, redirects.  
- `solver.py` – Newton-Raphson service; returns list of iteration dicts.  
- `templates/index.html` – Jinja2 view; renders form + history table.  
- `schema.sql` – single `calculations` table; ANSI-SQL compliant.  

### Data Flow
1. User submits polynomial `P(x)` and guess `x₀`.  
2. Controller passes to solver.  
3. Solver iterates until `|P(x)| < ε` (default 1e-10).  
4. Each tuple `(xₙ, f(xₙ), f'(xₙ), err)` stored in DB.  
5. Controller redirects to `/` which renders the full history.

---

## 🧰 Tech Stack
- **Backend:** Python 3.11, Flask 2.x, SQLAlchemy 2.x  
- **DB:** SQLite (dev) / PostgreSQL (prod)  
- **WSGI:** Gunicorn (workers = CPU × 2 + 1)  
- **Template:** Jinja2 (no JS frameworks)  
- **Deployment:** Render, Heroku, or any POSIX box with systemd.

---

## 📁 Project Structure
.
├── app.py              # Flask entry-point
├── solver.py           # Newton-Raphson core
├── requirements.txt
├── schema.sql
├── templates/
│   └── index.html
└── README.md
---

## ⚙️ Installation & Usage
### 1. Clone
bash
git clone https://github.com/abdul-0-muheed/newton-calculator.git
cd newton-calculator
### 2. Virtualenv
bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
### 3. DB (SQLite default)
bash
sqlite3 newton.db < schema.sql
# or
createdb newton && psql newton < schema.sql   # PostgreSQL
### 4. Run
bash
export FLASK_APP=app.py
flask run
# or production
gunicorn -w 4 -b 0.0.0.0:8000 app:app
Visit [http://localhost:8000](http://localhost:8000) and start solving!

---

## 🔌 API / Integrations
There is no JSON API—every interaction is a synchronous POST followed by server-side redirect.  
To embed the solver in another service, import `solver.py`:

python
from solver import newton_raphson
steps = newton_raphson("x**3 - 2*x - 5", x0=2, eps=1e-10, max_iter=50)
---

## 🔐 Environment Variables
| Variable | Default | Purpose |
| -------- | ------- | ------- |
| `DATABASE_URL` | `sqlite:///newton.db` | SQLAlchemy URI |
| `SECRET_KEY` | `dev-secret-change-me` | Flask sessions |
| `EPSILON` | `1e-10` | Convergence tolerance |
| `MAX_ITER` | `100` | Safety cap |

---

## 🧪 Testing & Build
No unit-tests yet—manual QA via browser.  
To add tests:

bash
pip install pytest
pytest tests/
Linting:
bash
pip install flake8 black
black app.py solver.py
flake8
---

## 📝 Notes
- Polynomial syntax follows Python `sympy` – `x**2 + 3*x + 2` ✅  
- Only real roots; complex ones return “did not converge”.  
- History is forever; delete rows manually or add a purge cronjob.

---

## 🤝 Contributing
PRs welcome!  
1. Fork, branch `feature/foo`.  
2. Keep the MVC monolith spirit—no new micro-services.  
3. Update this README if you change env vars or schema.

---

## 📄 License
MIT © Abdul Muheed

---

## 📬 Contact
Open an issue on GitHub for bugs or feature requests.