import db

class Post(db.Relation):
    title = db.Column("VARCHAR(100)")
    text = db.Column("TEXT")

print(Post.create())
