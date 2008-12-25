import db

class Post(db.Relation):
    post_id = db.Column(type = "INTEGER", primary_key = True)
    title = db.VarCharColumn(length = 100)
    text = db.TextColumn()

class Comment(db.Relation):
    post_id = db.ReferenceColumn(Post.post_id, primary_key = True)
    text = db.TextColumn(primary_key = True)

print(Post.create())
print(Comment.create())
