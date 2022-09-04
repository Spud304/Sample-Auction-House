from flask import Flask, render_template

class Application(Flask):
    def __init__(self, import_name):
        super().__init__(import_name)
        self._add_routes()

    def _add_routes(self):
        self.add_url_rule('/', 'index', self.index, methods=['GET'])
        self.add_url_rule('/health', 'health', self.health, methods=['GET'])
        self.add_url_rule('/profile', 'profile', self.profile, methods=['GET']) 
        self.add_url_rule('/login', 'login', self.login, methods=['GET'])
        # self.add_url_rule('/signup', 'signup', self.signup, methods=['GET'])

    def index(self):
        return render_template('index.html')

    def profile(self):
        return render_template('profile.html')
    
    def login(self):
        return render_template('login.html')

    # def signup(self):
    #     return render_template('signup.html')

    def health(self) -> str:
        return 'OK'