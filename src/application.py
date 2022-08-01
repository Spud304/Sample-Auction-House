from flask import Flask

class Application(Flask):
    def __init__(self, import_name):
        super().__init__(import_name)
        self._add_routes()

    def _add_routes(self):
        self.add_url_rule('/', 'index', self.index, methods=['GET'])
        self.add_url_rule('/health', 'health', self.health, methods=['GET'])

    def index(self) -> str:
        return 'Hello, World!'
    
    def health(self) -> str:
        return 'OK'