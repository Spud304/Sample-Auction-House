from models import db

from application import Application
from listings_manager import ListingBlueprint

app = Application(__name__)

db_name = 'auction_db'

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
db.create_all(app=app)

listing_bp = ListingBlueprint('listings', __name__)
app.register_blueprint(listing_bp)

if __name__ == '__main__':
    app.run(host='localhost', port = 8080, debug=True)


"""
Possibly use user id in headers?

Call to buy an item
post /listing/buy/<item_id>

Class to create a new listing
class CreateListingBlueprint(Blueprint):
"""

