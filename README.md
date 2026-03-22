# 🧮 Newton Calculator  
> A zero-setup, web-based arithmetic engine that stores every calculation in a durable, searchable history.

---

## 🚀 Demo  
🌍 **Live App**: [https://newton-calculator.onrender.com](https://newton-calculator.onrender.com)  
📁 **Source Code**: [https://github.com/abdul-0-muheed/newton-calculator](https://github.com/abdul-0-muheed/newton-calculator)

---

## 📖 Overview  
Doing quick back-of-the-envelope calculations should not require installing software or losing your work.  
**Newton Calculator** is a lightweight, stateless web service that:

* Lets students, scientists & engineers type any arithmetic expression and instantly see the result.  
* Automatically saves every request/response pair in an immutable audit trail.  
* Runs anywhere (SQLite by default, PostgreSQL with one env-var swap).  

The entire application is < 20 k tokens, making it ideal for teaching, embedded demos, or as a starting scaffold for heavier scientific apps.

---

## ✨ Features  
* ⚡ **Instant calculations** – supports `+ - * / ** %` and `math.*` functions  
* 🕰️ **Infinite history** – every calculation is time-stamped and stored  
* 🔍 **Search & replay** – query past results via the REST API  
* 🔄 **Zero-downtime DB swap** – SQLite ↔ PostgreSQL without migrations  
* 🐳 **Container-ready** – 30 MB image, scales horizontally behind any reverse proxy  
* 🧪 **CI/CD included** – GitHub Actions lint, test & build on every push  

---

## 🏗️ Architecture  
Classic **Model-View-Controller**:

Browser  ⇄  Flask (Controller)  ⇄  Service Layer  ⇄  SQL (Model)
                ↓
          Jinja2 Templates (View)
* Stateless Flask workers  
* Single `calculations` table (write-only)  
* Gunicorn WSGI server in production  

---

## 🔑 Key Components  
| Component | Responsibility |
|-----------|----------------|
| `app.py` | Flask entry-point, route registration |
| `calc_service.py` | Sanitises & evaluates expressions |
| `models.py` | SQLAlchemy model for `calculations` |
| `templates/` | Jinja2 UI |
| `static/` | CSS/JS assets |
| `docker/` | Multi-stage build files |
| `.github/workflows/ci.yml` | Lint, test, build & push image |

---

## 🔄 Data Flow  
1. User submits expression via UI or `POST /api/calculate`  
2. Controller validates → Service sanitises → `eval()` computes  
3. Result inserted into `calculations` table  
4. JSON response returned to client  
5. UI polls `/api/history` to display latest rows  

---

## 🧰 Tech Stack  
* **Backend**: Python 3.11, Flask 2.x, SQLAlchemy 2.x  
* **DB**: SQLite (dev) / PostgreSQL (prod)  
* **Server**: Gunicorn  
* **Container**: Docker, distroless python-runtime  
* **CI**: GitHub Actions  
* **IaaS**: Render (live demo)  

---

## 📁 Project Structure  
newton-calculator/
├── app.py
├── calc_service.py
├── models.py
├── requirements.txt
├── templates/
│   ├── index.html
│   └── history.html
├── static/
│   ├── style.css
│   └── app.js
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── tests/
│   └── test_calc.py
├── .env.example
├── .github/
│   └── workflows/
│       └── ci.yml
└── README.md
---

## ⚙️ Installation & Usage  

### Local (SQLite)  
bash
git clone https://github.com/abdul-0-muheed/newton-calculator.git
cd newton-calculator
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # defaults to SQLite
flask --app app.py run
Visit [http://localhost:5000](http://localhost:5000)

### Docker (PostgreSQL)  
bash
docker-compose -f docker/docker-compose.yml up
Set `DATABASE_URL=postgresql://user:pass@db:5432/newton` in `.env`.

---

## 🔌 API / Integrations  
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/calculate` | Body: `{"expr": "sin(pi/2) + 3**2"}` → returns result |
| `GET`  | `/api/history` | Optional query: `?limit=50&offset=0` |
| `GET`  | `/api/history/<id>` | Fetch single calculation |

---

## 🔐 Environment Variables  
| Var | Default | Purpose |
|-----|---------|---------|
| `DATABASE_URL` | `sqlite:///newton.db` | SQLAlchemy connection string |
| `FLASK_ENV` | `production` | Switches debug mode |
| `SECRET_KEY` | `dev-secret-change-me` | Session encryption |
| `LOG_LEVEL` | `INFO` | Stdout granularity |

---

## 🧪 Testing & Build  
bash
pytest tests/                 # unit tests
flake8 app.py calc_service.py  # linting
docker build -t newton:latest -f docker/Dockerfile .
---

## 🤖 AI Documentation Support  
This README is auto-generated and kept in sync with the codebase via AI documentation tools. To regenerate:

bash
python scripts/ai_doc.py
---

## 📝 Notes  
* Expressions are executed in a **whitelisted** namespace (`math` module only).  
* No user accounts—history is globally readable.  
* For true multi-tenancy, add an `owner_id` column and auth layer.

---

## 🤝 Contributing  
1. Fork the repo  
2. Create a feature branch (`git checkout -b feature/amazing`)  
3. Commit & push (`git commit -m 'Add amazing feature'`)  
4. Open a Pull Request—CI must pass ✅

---

## 📄 License  
MIT © Abdul Muheed

---

## 📬 Contact  
For questions, issues or coffee chats:  
GitHub Issues: [https://github.com/abdul-0-muheed/newton-calculator/issues](https://github.com/abdul-0-muheed/newton-calculator/issues)