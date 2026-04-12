# auth/routes.py
from flask import (
    render_template, 
    redirect, 
    url_for, 
    flash, 
    session, 
    request, 
    current_app
)
from werkzeug.security import (
    generate_password_hash, 
    check_password_hash
)
from . import mft_AuthBP
from .forms import (
    mft_LoginForm, 
    mft_SignupForm
)
from .models import (
    User, 
    db # SQLAlchemy instance (or any ORM)
) 

# --------------------------------------------------------------
# Wrapper that mimics Flask‑Login's login_required function
# --------------------------------------------------------------
def mft_LoginRequired(view_func):
    """Replaces flask_login.login_required"""
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("You must be logged in to view that page.", "warning")
            return redirect(url_for("auth.mft_LoginPage", next=request.endpoint))
        return view_func(*args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper

# --------------------------------------------------------------
# /authenticate – gatekeeper
# --------------------------------------------------------------
@mft_AuthBP.route("/authenticate")
def mft_AuthenticationPage():
    """
    * If the visitor already owns a valid session, send to dashboard.
    * If not, redirect to login page
    """
    if session.get("user_id"):
        return redirect(url_for("dashboard.mft_DashPage"))

    flash("Please log in or create an account.", "info")
    return redirect(url_for("auth.mft_LoginPage"))


# --------------------------------------------------------------
# /login using GET & POST
# --------------------------------------------------------------
@mft_AuthBP.route("/login", methods=["GET", "POST"])
def mft_LoginPage():
    form = mft_LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            # If login was SUCCESSFUL
            session["user_id"] = user.id
            session["username"] = user.username
            flash(f"Welcome back, {user.username}!", "success")
            # Preserve a "next" param if the user was redirected here
            next_endpoint = request.args.get("next")
            return redirect(url_for(next_endpoint) if next_endpoint else url_for("auth.mft_DashPage"))
        else:
            flash("Invalid e-mail or password.", "danger")
    return render_template("auth/login.html", form=form)


# --------------------------------------------------------------
# /signup using GET & POST
# --------------------------------------------------------------
@mft_AuthBP.route("/signup", methods=["GET", "POST"])
def mft_SignupPage():
    form = mft_SignupForm()
    if form.validate_on_submit():
        # Creates user in database
        user = User(
            email=form.email.data.lower(),
            username=form.username.data,
            password_hash=generate_password_hash(form.password.data),
        )
        db.session.add(user)
        db.session.commit()

        # Automatically log in after signup process
        session["user_id"] = user.id
        session["username"] = user.username
        flash("Account created. You are now logged in!", "success")
        return redirect(url_for("auth.mft_DashPage"))
    return render_template("auth/signup.html", form=form)


# --------------------------------------------------------------
# /logout simple clear token session
# --------------------------------------------------------------
@mft_AuthBP.route("/logout")
def mft_LogoutPage():
    session.clear()
    flash("You have successfully been logged out.", "info")
    return redirect(url_for("auth.mft_LoginPage"))


# --------------------------------------------------------------
# FIXME: /dashboard – just a placeholder for testing purposes
# --------------------------------------------------------------
# Below is a minimal example that uses the local `mft_LoginRequired` helper.
@mft_AuthBP.route("/dashboard")
@mft_LoginRequired
def mft_DashPage():
    # Grab the user object if you’d like to display extra info.
    user = User.query.get(session["user_id"])
    return render_template("dashboard/user_dash.html", user=user)
