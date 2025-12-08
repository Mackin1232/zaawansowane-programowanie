from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {"id": self.id, "email": self.email}
    
    @classmethod
    def all_users(table):
        users = table.query.all()
        return [u.to_dict() for u in users]
