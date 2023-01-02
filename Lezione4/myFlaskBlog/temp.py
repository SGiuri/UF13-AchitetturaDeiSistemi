# Lezione 4 Finita

from run import app, db, User, Post

with app.app_context():

    # db.create_all()
    # user3 = User(username="paperino", password="paperino123",
    #              email="paperino.giuri@gmail.com")
    # db.session.add(user3)
    # db.session.commit()

    # post1 = Post(title="primo post", post_content="Questo e' il contenuto del primo post di Paperino",
    #              user_id=3)

    # post2 = Post(title="secondo post", post_content="Questo e' il contenuto del secondo post di Paperino",
    #              user_id=3)
    # post3 = Post(title="terzo post", post_content="Questo e' il contenuto del primo post di Pippo",
    #              user_id=2)
    # post4 = Post(title="quarto post", post_content="Questo e' il contenuto del quarto post di Paperino",
    #              user_id=3)
    # db.session.add(post1)
    # db.session.add(post2)
    # db.session.add(post3)
    # db.session.add(post4)
    # db.session.commit()
    # tutti
    users = db.session.execute(
        db.select(User).order_by(User.id)).all()
    print(users)
    # # lultimo:
    # user = db.session.execute(
    #     db.select(User).order_by(User.id)).scalar()

    # post1 = user.posts[0]
    # print(post1)

    # print(post1.author)

    # db.drop_all()
