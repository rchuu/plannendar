from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import message


class Event:
    db = "plannendar_schema"

    def __init__(self, data):
        self.id = data['id']
        self.event = data['event']
        self.description = data['description']
        self.activities = data['activities']
        self.start_date = data['start_date']
        self.end_date = data['end_date']
        self.location = data['location']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO events (event, description, activities, start_date, end_date, location, user_id) VALUES (%(event)s,%(description)s,%(activities)s,%(start_date)s,%(end_date)s,%(location)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def add_guests(cls, data):
        query = 'INSERT INTO guests (event_id, user_id) VALUES (%(event_id)s,%(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = '''SELECT * FROM events
        JOIN users
        ON events.user_id = users.id;'''
        results = connectToMySQL(cls.db).query_db(query)
        all_events = []
        for row in results:
            one_event = cls(row)
            user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": "not telling",
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            one_event.guests = user.User.get_event_guests(
                {"event_id": one_event.id})
            one_event.creator = user.User(user_data)
            all_events.append(one_event)
        return all_events

    @classmethod
    def get_user_events(cls, data):
        query = """SELECT * FROM events
        JOIN users
        ON events.user_id = users.id
        WHERE events.id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        for row in results:
            one_event = cls(row)
            user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": "not telling",
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            one_event.creator = user.User(user_data)
        return one_event

    @classmethod  # get by the ID, appending the messages into empty list
    def get_one(cls, data):
        query = """SELECT * FROM events
        LEFT JOIN messages
        ON events.id = messages.event_id
        WHERE events.id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        event = cls(results[0])
        event.guests = user.User.get_event_guests({"event_id": event.id})
        event.messages = []
        for row in results:
            message_row = {
                "id": row['messages.id'],
                "content": row['content'],
                "user_id": row['messages.user_id'],
                "event_id": row['event_id'],
                "created_at": row['messages.created_at'],
                "updated_at": row['messages.updated_at']
            }
            one_message = message.Message(message_row)
            one_message.creator = user.User.get_from_id(
                {"id": row["messages.user_id"]})  # grabbing events user_id
            event.messages.append(one_message)
        return event

    @classmethod  # upate function
    def update(cls, data):
        query = """UPDATE events 
        SET event= %(event)s,
        description= %(description)s,
        activities= %(activities)s,
        start_date= %(start_date)s,
        end_date= %(end_date)s,
        location= %(location)s,
        updated_at= NOW()
        WHERE id= %(id)s;"""
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod  # delete function
    def destroy(cls, data):
        query = """DELETE FROM events
        WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod  # validating event details
    def validate_event(event):
        is_valid = True
        if len(event['event']) < 2:
            is_valid = False
            flash("The event name is too short", "event")
        if len(event['activities']) < 2:
            is_valid = False
            flash("The activities is too short", "event")
        if len(event['description']) < 2:
            is_valid = False
            flash("The description is too short", "event")
        if len(event['start_date']) == "":
            is_valid = False
            flash("missing a date", "event")
        if len(event['end_date']) == "":
            is_valid = False
            flash("missing a date", "event")
        if len(event['location']) < 2:
            is_valid = False
            flash("Location is too short", "event")
        return is_valid
