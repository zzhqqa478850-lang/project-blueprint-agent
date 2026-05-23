# app.py - 示例应用入口

from flask import Flask
from app.controllers import main_controller
from app.models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

app.register_blueprint(main_controller.bp)

if __name__ == '__main__':
    app.run(debug=True)
