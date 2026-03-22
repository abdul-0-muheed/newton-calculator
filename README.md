# 🧮 Newton Calculator  
> A lightweight, web-based scientific calculator that remembers every calculation—perfect for physics, chemistry, and every STEM field that needs quick, auditable math.

---

## 🚀 Demo  
🌍 Live site: [https://newton-calculator.onrender.com](https://newton-calculator.onrender.com)  
📦 Repo: [https://github.com/abdul-0-muheed/newton-calculator](https://github.com/abdul-0-muheed/newton-calculator)

---

## 📖 Overview  
Doing quick back-of-the-envelope calculations is part of every scientist’s workflow, but browser tabs get lost and paper gets tossed. Newton Calculator solves this by giving you a single-page web app that:

* Evaluates any arithmetic expression instantly  
* Stores every result in a durable SQL ledger so you can scroll back, audit, or resume work  
* Runs anywhere—laptop, lab PC, or phone—without installs or sign-ups  

Target users: students, researchers, TAs, and hobbyists who want **fast, traceable math**.

---

## ✨ Features  
* 🧪 **Multi-disciplinary**: arithmetic, physics, chem, stats—anything Python can parse  
* 🕰️ **Infinite history**: every expression + result auto-saved to SQLite  
* 🔄 **Chained calculations**: reuse previous answers by referencing their line number  
* 🌐 **Responsive**: works on mobile, tablet, and desktop  
* 🛡️ **Zero cookies**: no tracking, no accounts, no session state  
* 🚀 **Deploy in 60 s**: single container, 20 MB image, runs on free Render tier  

---

## 🏗️ Architecture  
Classic **Model-View-Controller** inside one Flask process.

Browser  ⇄  Flask (Controller)  ⇄  Python eval()  ⇄  SQLite (Model)
                ↓
           Jinja2 (View) → HTML
---

## 🔑 Key Components  
| Component | Responsibility |
|---|---|
| `app.py` | Flask dispatcher, routes `/` and `/api/eval` |
| `calculator.py` | Thin service wrapper around Python `ast` for safe evaluation |
| `models.py` | SQLAlchemy model for `calculations` table |
| `templates/index.html` | Single-page UI with history sidebar |
| `static/style.css` | 3 kB vanilla CSS for light/dark mode |

---

## 📡 Data Flow  
1. User types expression → hits **Enter**  
2. JS posts JSON `{ "expr": "2+2" }` to `/api/eval`  
3. Flask validates → `calculator.py` evaluates → result stored in `calculations`  
4. Server returns `{ "result": 4, "id": 42 }`  
5. JS appends row to history; no page reload  

---

## 🧰 Tech Stack  
* **Backend**: Python 3.11, Flask 2.3, Gunicorn 21  
* **DB**: SQLite (dev) / PostgreSQL (prod) via SQLAlchemy 2.0  
* **Frontend**: vanilla ES5, no build tools  
* **Infra**: Docker, GitHub Actions, Render  

---

## 📁 Project Structure  
newton-calculator/
├── app.py
├── calculator.py
├── models.py
├── requirements.txt
├── Dockerfile
├── .github/workflows/ci.yml
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── tests/
    └── test_calculator.py
---

## ⚙️ Installation & Usage  

### Local (no Docker)
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
docker run -p 80:8000 newton-calc
---

## 🔌 API / Integrations  
**POST** `/api/eval`  
Body: `{ "expr": "sqrt(2)*pi" }`  
Response: `{ "result": 4.442882938, "id": 123 }`  

**GET** `/api/history?limit=50`  
Returns array of previous expressions and results.

---

## 🔐 Environment Variables  
| Var | Default | Purpose |
|---|---|---|
| `DATABASE_URL` | `sqlite:///calc.db` | SQLAlchemy connection string |
| `FLASK_ENV` | `production` | Controls debug mode |
| `PORT` | `8000` | Port Gunicorn listens on |

---

## 🧪 Testing & Build  
bash
pytest tests/                 # unit tests
flake8 *.py                   # linting
docker buildx bake             # multi-arch image
GitHub Actions runs the above on every push; tagged releases auto-deploy to Render.

---

## 🤖 AI Documentation Support  
This README was auto-generated with the help of LLM-assisted technical writers. For updates, open an issue or PR—our bot will re-generate docs on demand.

---

## 📝 Notes  
* No symbolic algebra (yet); expressions must evaluate to a float/int  
* History is stored **forever** unless you manually delete the DB file  
* For **true** persistence across container restarts, supply an external Postgres URI  

---

## 🤝 Contributing  
1. Fork & branch (`feat/whatever`)  
2. Add tests for new logic  
3. Push and open a PR; CI must be green  
4. Tag maintainer for review

---

## 📄 License  
MIT © Abdul Muheed

---

## 📬 Contact  
For questions, feature requests, or bug reports:  
[GitHub Issues](https://github.com/abdul-0-muheed/newton-calculator/issues) or [abdul.muheed@example.com](mailto:abdul.muheed@example.com)