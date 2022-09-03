from src.models import db

from src.application import Application
from src.listings_manager import ListingBlueprint
from src.user_manager import UserBlueprint

app = Application(__name__)

db_name = 'auction_db'

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
db.create_all(app=app)

listing_bp = ListingBlueprint('listings', __name__)
app.register_blueprint(listing_bp)

user_bp = UserBlueprint()
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(host='localhost', port = 8080, debug=True)


"""
Possibly use user id in headers?

Call to buy an item
post /listing/buy/<item_id>

Class to create a new listing
class CreateListingBlueprint(Blueprint):
"""

