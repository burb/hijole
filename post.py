import db

class Post(db.Relation):
    post_id = db.Column(type = "INTEGER")
    title = db.VarCharColumn(length = 100)
    text = db.TextColumn()
    pk = db.PrimaryKey("post_id")

class Comment(db.Relation):
    post_id = db.ReferenceColumn(Post.post_id)
    text = db.TextColumn()

print(Post.create())
print(Comment.create())
