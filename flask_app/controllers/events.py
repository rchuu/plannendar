from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.event import Event
from flask_app.models.message import Message


@app.route('/add/event')
def add_event():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template('add_event.html', user=User.get_from_id(data))


@app.route('/create/event', methods=['POST'])
def create_event():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Event.validate_event(request.form):
        return redirect('/add/event')
    data = {
        "event": request.form["event"],
        "description": request.form["description"],
        "activities": request.form["activities"],
        "start_date": request.form["start_date"],
        "end_date": request.form["end_date"],
        "location": request.form["location"],
        "user_id": session['user_id']
    }
    Event.save(data)
    return redirect('/dashboard')


@app.route('/edit/event/<int:id>')
def edit_event(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("edit_event.html", edit=Event.get_one(data), user=User.get_from_id(user_data))


@app.route('/update/event', methods=['POST'])
def update_event():
    print(request.form)
    if 'user_id' not in session:
        return redirect('/logout')
    if not Event.validate_event(request.form):
        return redirect('/add/event')
    guest_id = User.get_from_email(request.form['email'])

    data = {
        "event": request.form["event"],
        "description": request.form["description"],
        "activities": request.form["activities"],
        "start_date": request.form["start_date"],
        "end_date": request.form["end_date"],
        "location": request.form["location"],
        "event_id": request.form["event_id"],
        "guest_id": guest_id,
        "user_id": session['user_id']
    }
    Event.update(data)
    return redirect('/dashboard')


@app.route('/event/<int:id>')
def view_event(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("view_event.html", event=Event.get_one(data), events=Event.get_user_events(data), user=User.get_from_id(user_data), messages=Message.get_user_messages(user_data), users=User.get_all())


@app.route('/destroy/event/<int:id>')
def destroy_event(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    Event.destroy(data)
    return redirect('/dashboard')


@app.route('/add_guests', methods=['POST'])
def add_guests():
    if 'user_id' not in session:
        return redirect('/logout')

    guest = User.get_from_email({"email": request.form['email']})
    print(guest, "****************")
    data = {
        "user_id": guest.id,
        "event_id": request.form['event_id']
    }
    Event.add_guests(data)
    return redirect(f'/event/{request.form["event_id"]}')
