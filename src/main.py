import re
from src.models import db, User

from src.application import Application
from src.listings_manager import ListingBlueprint
from src.user_manager import UserBlueprint
from src.auth import AuthBlueprint
from flask_login import LoginManager

app = Application(__name__)

db_name = 'auction_db'

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'secret'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db.create_all(app=app)

listing_bp = ListingBlueprint('listings', __name__)
app.register_blueprint(listing_bp)

user_bp = UserBlueprint()
app.register_blueprint(user_bp)

auth_bp = AuthBlueprint()
app.register_blueprint(auth_bp)


if __name__ == '__main__':
    app.run(host='localhost', port = 8080, debug=True)


"""
Possibly use user id in headers?

Call to buy an item
post /listing/buy/<item_id>

Class to create a new listing
class CreateListingBlueprint(Blueprint):
"""

