# Flasky Secure App

A small Flask app demonstrating OWASP-aligned secure coding practices:
- Secure password storage with bcrypt
- Input validation and basic sanitization
- CSRF protection and secure session cookies
- Parameterized queries via SQLAlchemy ORM
- Safe error pages (404/500)
- Security headers via Flask-Talisman

## Project structure

```
app.py           # App factory, routes, security config, CLI commands
models.py        # SQLAlchemy models: User, Contact
forms.py         # Flask-WTF forms and validators
templates/       # Jinja2 templates (login, contact, users, contacts, errors)
static/          # CSS
requirements.txt # Dependencies
```

## Setup (Windows PowerShell)

1) Create and activate a virtual environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies
```powershell
pip install -r requirements.txt
```

3) Configure environment (development)
```powershell
$env:FLASK_APP = "app:create_app"
$env:FLASK_ENV = "production"       # Debug is disabled by default in app.py
$env:COOKIE_SECURE = "0"             # For local http; set to 1 when using HTTPS
# Optional: set your own secret key
# $env:SECRET_KEY = "change-me"
```

4) Initialize the database
```powershell
flask create-db
```

5) Create a user securely via environment variables
```powershell
$env:USERNAME = "admin"
$env:EMAIL = "admin@example.com"
$env:PASSWORD = "StrongPassw0rd!"
flask create-user
```

6) Run the app
```powershell
python app.py
# or
# flask run --host 127.0.0.1 --port 5000
```

Visit http://127.0.0.1:5000

## Security notes
- Passwords are hashed with bcrypt using a strong work factor.
- CSRF is enabled globally; forms use `hidden_tag()` tokens.
- Session cookies are `HttpOnly`, `SameSite=Lax`, and optionally `Secure` via `COOKIE_SECURE`.
- All DB operations use SQLAlchemy ORM (no raw SQL).
- Inputs are validated and disallow `<` or `>` to mitigate simple XSS payloads; Jinja auto-escapes output.
- Talisman sets security headers with a restrictive Content Security Policy.

## Creating additional users
Use the `create-user` CLI again with new `USERNAME`, `EMAIL`, and `PASSWORD` env vars.

## Troubleshooting
- If CSS does not load, ensure the `static/` folder exists and `style.css` is present.
- On first run, ensure the virtual environment is activated and packages are installed.
- For HTTPS deployments, set `COOKIE_SECURE=1` and place a strong `SECRET_KEY` in the environment.


