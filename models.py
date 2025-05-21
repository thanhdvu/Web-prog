from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class LostItem(db.Model):
    __tablename__ = 'lost_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # sẽ là current_user.id
    category = db.Column(db.String(255), nullable=False)
    date_found = db.Column(db.Date, nullable=False)
    item_name = db.Column(db.String(255), nullable=False)
    building_found = db.Column(db.String(255), nullable=False)
    image_filename = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

