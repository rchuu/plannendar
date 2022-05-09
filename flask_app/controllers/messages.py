from re import L
from flask import render_template, session, flash, redirect, request
# import re
# from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User
from flask_app.models.message import Message


# @app.route('/add/message')
# def add_message():
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data = {
#         "id": session['user_id']
#     }
#     return render_template('view_event.html', user=User.get_from_id(data))


@app.route('/post_message', methods=['POST'])
def post_message():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "event_id":  int(request.form['event_id']),
        "user_id": session['user_id'],
        "content": request.form['content']
    }
    Message.save(data)
    return redirect(f'/event/{request.form["event_id"]}')


@app.route('/destroy/message/<int:id>')
def destroy_message(id):
    data = {
        "id": id
    }
    Message.destroy(data)
    return redirect('/dashboard')
