import db

class OldPost(db.Relation):
    title = db.VarCharColumn(length = 10)
    text = db.TextColumn()
    haha = db.TextColumn()

class Post(db.Relation):
    post_id = db.Column(type = "INTEGER", primary_key = True)
    title = db.VarCharColumn(length = 100, default = "kuku")
    text = db.TextColumn(can_be_null = True)

class Comment(db.Relation):
    post_id = db.ReferenceColumn(Post.post_id)
    text = db.TextColumn()

print(Post.create())
print(Comment.create())
print(Post.update(OldPost))
