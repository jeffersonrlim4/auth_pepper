from flask import Flask
from database import db
from models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'solomon_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

@app.route('/hello', methods=["GET"])
def hello_word():
  return 'Hello World'

if __name__ == '__main__':
  with app.app_context():
      db.create_all()
  app.run(debug=True)