from flask import Flask, request, jsonify
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
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
  
  return jsonify({"message": "User invalid"}), 401

@app.route('/logout', methods=["GET"])
@login_required
def logout():
  logout_user()
  return jsonify({"message": "Logout successfully"})

@app.route('/user', methods=["POST"])
def create_user():
  data = request.json
  
  username = data.get("username")
  password = data.get("password")
  
  if username and password:
    user = User(username=username, password=password)
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": "User created successfully"}), 201 
  
  return jsonify({"message": "Invalid credentials"}), 400

@app.route('/user/<int:id_user>', methods=["GET"])
def get_user_by_id(id_user):
  user = User.query.get(id_user)
  
  if user:
    return jsonify({"user": user.username})
  
  return jsonify({"message": "User not found"}), 404

@app.route('/user/<int:id_user>', methods=["PUT"])
@login_required
def update_user(id_user):
  data = request.json
  
  user = User.query.get(id_user)
  password = data.get("password")
  
  if user and password:
    user.password = password
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": "User updated successfully"})
    
  return jsonify({"message": "User not found"}), 404

@app.route('/user/<int:id_user>', methods=["DELETE"])
@login_required
def delete_user(id_user):
  user = User.query.get(id_user)
  
  if user:
    logout_user()
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message": "User deleted successfully"})
  
  return jsonify({"message": "User not found"}), 404

@app.route('/hello', methods=["GET"])
def hello_word():
  return 'Hello World'

if __name__ == '__main__':
  with app.app_context():
      db.create_all()
  app.run(debug=True)