from micro import app

from micro.offers_api import get_offers


@app.route('/')
def home():
    return 'Hello app'


@app.route('/<id>/offers')
def list(id):
    return '%s' % get_offers(id).json()


@app.route('/add', methods=['POST'])
def add():
    pass


@app.route('/update', methods=['PUT'])
def update():
    pass


@app.delete('<id>/del', methods=['DELETE'])
def delete():
    pass
