import os, sys
from os.path import dirname, join, abspath

sys.path.insert(0, abspath(join(dirname(__file__), '../')))

from flask_app.app import app

if __name__ == "__main__":
    app.run()