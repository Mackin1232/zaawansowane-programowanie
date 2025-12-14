from db.modele import db, User, newUser
import bcrypt


def add_user(data: newUser): # pewnie to wsadzimy do endpointa
    user = User(username=data.username, password=bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()), email=data.email, role=data.role)
    db.session.add(user)
    db.session.commit()



def load_data(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        us1 = {
            "username": "user1",
            "password": "123",
            "email": "user1@gmail.com"}
        us2 = {
            "username": "user2",
            "password": "123",
            "email": "user2@gmail.com"}
        adm = {
            "username": "admin",
            "password": "admin123",
            "email": "admin@gmail.com",
            "role": "admin"}
        
        users = [us1,us2,adm]
        if User.query.count() == 0:
            for us in users:
                add_user(data=newUser(**us))
