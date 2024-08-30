from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(80), nullable=False)
  # id: Mapped[int] = mapped_column(primary_key=True)
  # username: Mapped[str] = mapped_column(unique=True, nullable=False)
  # password: Mapped[str] = mapped_column(nullable=False)