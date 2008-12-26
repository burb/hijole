import db
import pgdb

class HijoleRelations(db.Relation):
    relation_update_time = db.TimestampColumn(default = 'CURRENT_TIMESTAMP', primary_key = True)
    relation_name = db.VarCharColumn(length = 100, primary_key = True)
    relation_pickle = db.TextColumn()

if __name__ == '__main__':
    s = HijoleRelations.create()
    connection = pgdb.connect(database = 'blog', user = 'postgres', password = 'sasa166')
    cursor = connection.cursor()
    # print(HijoleRelations.create())
    # cursor.execute(HijoleRelations.create())
    # HijoleRelations.save_to_db(cursor)
    # last_hijole_relations = HijoleRelations.last_from_db(cursor)
    # print(HijoleRelations.update(last_hijole_relations))
    # cursor.execute(HijoleRelations.update(last_hijole_relations))
    connection.commit()
    connection.close()
