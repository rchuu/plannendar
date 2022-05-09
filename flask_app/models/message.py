from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
from flask_app.models import user


class Message:
    db_name = 'plannendar_schema'

    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.user_id = data['user_id']
        self.event_id = data['event_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = ''

    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"

    @classmethod
    def get_user_messages(cls, data):
        query = '''SELECT * FROM users
        LEFT JOIN messages
        ON users.id = messages.user_id
        LEFT JOIN events
        ON messages.id = events.id'''
        results = connectToMySQL(cls.db_name).query_db(query, data)
        all_messages = []
        for row in results:
            one_message = cls(row)
            user_data = {
                "id": row["id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": "not telling",
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
            one_message.creator = user.User(user_data)
            print(one_message.creator, "********************")
            all_messages.append(one_message)
        return all_messages

    @classmethod
    def update(cls, data):
        query = """UPDATE messages 
        SET content= %(content)s
        updated_at= NOW()
        WHERE id= %(id)s;"""
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def save(cls, data):
        query = "INSERT INTO messages (content,event_id,user_id) VALUES (%(content)s,%(event_id)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM messages WHERE messages.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
