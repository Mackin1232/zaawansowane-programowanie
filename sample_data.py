from db.modele import db, User

def load_data(app):
    with app.app_context():
        db.create_all()

        sample_users = [
            User(email="anna@gmail.com"),
            User(email="bartek@outlook.com"),
            User(email="czarek@interia.pl"),
        ]

        if User.query.count() == 0:
            db.session.add_all(sample_users)
            db.session.commit()
