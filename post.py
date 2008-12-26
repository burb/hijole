import db
import pgdb

class Post(db.Relation):
    post_id = db.Column(type = "INTEGER", primary_key = True)
    # todo!! ugly quoting - rewrite it
    title = db.VarCharColumn(length = 400, default = "'ho'")
    text = db.TextColumn(can_be_null = True)

class Comment(db.Relation):
    post_id = db.ReferenceColumn(Post.post_id)
    text = db.TextColumn()

connection = pgdb.connect(database = 'blog', user = 'postgres', password = 'sasa166')
cursor = connection.cursor()
# Post.save_to_db(cursor)
# Comment.save_to_db(cursor)
Post.db_action(cursor)
Comment.db_action(cursor)
connection.commit()
connection.close()
