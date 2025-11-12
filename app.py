import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from flask_talisman import Talisman
from extensions import db, bcrypt, csrf, login_manager


def create_app() -> Flask:
    app = Flask(__name__)

    # Secure configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(32))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', f"sqlite:///{os.path.join(app.root_path, 'app.db')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Session & cookie hardening
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    # Set SECURE cookies when running behind HTTPS; keep configurable for local dev
    app.config['SESSION_COOKIE_SECURE'] = os.environ.get('COOKIE_SECURE', '1') == '1'
    app.config['REMEMBER_COOKIE_SECURE'] = app.config['SESSION_COOKIE_SECURE']
    app.config['REMEMBER_COOKIE_HTTPONLY'] = True

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Security headers via Talisman
    csp = {
        'default-src': ["'self'"],
        'style-src': ["'self'", "'unsafe-inline'"],
        'script-src': ["'self'"],
    }
    Talisman(app, content_security_policy=csp, frame_options='DENY', force_https=False)

    login_manager.login_view = 'login'
    login_manager.session_protection = 'strong'

    from models import User, Contact  # noqa: WPS433 (local import to avoid cycles)
    from forms import LoginForm, ContactForm, SignupForm  # noqa

    @login_manager.user_loader
    def load_user(user_id: str):  # type: ignore[override]
        try:
            return User.query.get(int(user_id))
        except Exception:
            return None

    # Routes
    @app.route('/')
    def index():
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash('Logged in successfully.', 'success')
                next_url = request.args.get('next')
                return redirect(next_url or url_for('contacts'))
            flash('Invalid username or password.', 'danger')
        return render_template('login.html', form=form)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        form = SignupForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Account created. You can now log in.', 'success')
            return redirect(url_for('login'))
        return render_template('signup.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        form = ContactForm()
        if form.validate_on_submit():
            contact = Contact(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                message=form.message.data,
            )
            db.session.add(contact)
            db.session.commit()
            flash('Thank you! Your message has been received.', 'success')
            return redirect(url_for('contact'))
        return render_template('contact.html', form=form)

    @app.route('/contacts')
    @login_required
    def contacts():
        items = Contact.query.order_by(Contact.created_at.desc()).all()
        return render_template('contacts.html', contacts=items)

    @app.route('/users')
    @login_required
    def users():
        items = User.query.order_by(User.created_at.desc()).all()
        return render_template('users.html', users=items)

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):  # noqa: ANN001
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):  # noqa: ANN001
        return render_template('500.html'), 500

    # CLI commands for safe DB setup
    @app.cli.command('create-db')
    def create_db():
        """Create database tables."""
        with app.app_context():
            db.create_all()
        print('Database tables created.')

    @app.cli.command('create-user')
    def create_user():
        """Create a user via environment variables for safety.

        Set USERNAME, EMAIL, PASSWORD env vars before running.
        """
        username = os.environ.get('USERNAME')
        email = os.environ.get('EMAIL')
        password = os.environ.get('PASSWORD')
        if not all([username, email, password]):
            print('USERNAME, EMAIL, PASSWORD env vars are required.')
            return
        if User.query.filter((User.username == username) | (User.email == email)).first():
            print('User already exists.')
            return
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print('User created.')

    # Ensure DB exists (safe for SQLite)
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=False)


