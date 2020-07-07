from micro import app

from micro.api import callback


@app.route('/')
def home():
    return callback()