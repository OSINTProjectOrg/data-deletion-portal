from flask import Flask, Blueprint, render_template
import os

# ----------------------------------------------------------
# Doing initial setup for certain aspects of the project.
# ----------------------------------------------------------
dir_path = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)


@app.route('/')
def indexPage():
    return render_template('index.html')


# ----------------------------------------------------------
# Creates parameters for the application to run.
# ----------------------------------------------------------
if __name__ == '__main__':
	app.run(
          debug=False,
          host='0.0.0.0',
          port=8080
          )