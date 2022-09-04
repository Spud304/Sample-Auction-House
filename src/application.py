from contextlib import redirect_stderr
from flask import Flask, render_template
from flask_login import login_required, current_user

class Application(Flask):
    def __init__(self, import_name):
        super().__init__(import_name)
        self._add_routes()

    def _add_routes(self):
        self.add_url_rule('/', 'index', self.index, methods=['GET'])
        self.add_url_rule('/health', 'health', self.health, methods=['GET'])
        self.add_url_rule('/profile', 'profile', self.profile, methods=['GET']) 

    def index(self):
        return render_template('index.html')

    @login_required
    def profile(self):
        return render_template('profile.html', name=current_user.username)


    def health(self) -> str:
        return 'OK'