from flask import Flask, request, jsonify
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user
from models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'solomon_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

loggin_manager = LoginManager()

db.init_app(app)
loggin_manager.init_app(app)

#view login
loggin_manager.login_view = 'login'

@loggin_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

@app.route('/login', methods=["POST"])
def login():
  data = request.json
  
  username = data.get("username")
  password = data.get("password")
  
  if username and password:
    user = User.query.filter_by(username=username).first()
    
    if user and user.password == password:
      login_user(user)
      return jsonify({"user": current_user.username})
    
    return jsonify({"message": "Invalid credentials"})
  
  return jsonify({"message": "User invalid"}), 400

@app.router('/logout', methods=["GET"])
def logout(user_id):
  logout_user()
  return jsonify({"message", "Logout successfully"})

@app.route('/hello', methods=["GET"])
def hello_word():
  return 'Hello World'

if __name__ == '__main__':
  with app.app_context():
      db.create_all()
  app.run(debug=True)