from flask import (
    Flask, 
    Blueprint, 
    render_template, 
    redirect, 
    url_for, 
    flash
)
from flask_login import (
    LoginManager, 
    current_user, 
    login_required
)
import os
from auth import mft_AuthBP # the blueprint we defined above
from auth.models import (
    db, 
    User
) # DB instance
from config import mft_Config


# ----------------------------------------------------------
# Setting up initial aspects for the project.
# ----------------------------------------------------------
def create_app():
    app = Flask(__name__)
    app.mft_Config.from_object(mft_Config)

    # Initialise extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(mft_AuthBP) # all auth routes under /

    # ----------------------------------------------------------------
    # FIXME: Create DB tables on first run (only for development, replace with Alembic for prod)
    # ----------------------------------------------------------------
    @app.before_first_request
    def create_tables():
        db.create_all()

    return app


@create_app().route('/')
def indexPage():
    print(os.getenv("OSINTPROJECT_KEY"))
    return render_template('index.html')


# ----------------------------------------------------------
# Creates parameters for the application to run.
# ----------------------------------------------------------
if __name__ == '__main__':
	create_app().run(
          debug=False,
          host='0.0.0.0',
          port=8080
          )