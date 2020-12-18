# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
from flask import Flask, request, redirect
import flask_sqlalchemy
import flask_socketio
import models
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse


ITEMS_RECEIVED_CHANNEL = "items received"

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), "secret_tokens.env")
load_dotenv(dotenv_path)

database_uri = os.environ["DATABASE_URL"]
twilio_sid = os.environ["TWILIO_SID"]
twilio_auth = os.environ["TWILIO_AUTH"]

# the following line needs your Twilio Account SID and Auth Token
client = Client(twilio_sid, twilio_auth)

app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app


db.create_all()
db.session.commit()


def emit_all_items(channel):
    all_items = [db_item.item for db_item in db.session.query(models.Grocerylist).all()]

    socketio.emit(channel, {"allItems": all_items})


@socketio.on("connect")
def on_connect():
    print("Someone connected!")
    socketio.emit("connected", {"test": "Connected"})

    client.messages.create(
        to="+19733921387", from_="+12516640317", body="Welcome to my Grocery List app!"
    )

    emit_all_items(ITEMS_RECEIVED_CHANNEL)


@socketio.on("disconnect")
def on_disconnect():
    print("Someone disconnected!")


@socketio.on("new item input")
def on_new_item(data):
    print("Got an event for new item input with data:", data)

    db.session.add(models.Grocerylist(data["item"]))
    db.session.commit()

    emit_all_items(ITEMS_RECEIVED_CHANNEL)


@socketio.on("remove item")
def on_new_remove(data):
    print("Got an event for removal with data:", data)

    db.session.query(models.Grocerylist).filter_by(item=data["item"]).delete()
    db.session.commit()

    emit_all_items(ITEMS_RECEIVED_CHANNEL)


@app.route("/", methods=["GET", "POST"])
def index():
    emit_all_items(ITEMS_RECEIVED_CHANNEL)
    body = request.values.get("Body", None)
    print(body)
    if body[:3] == "add":
        db.session.add(models.Grocerylist(body[4:]))
        db.session.commit()
    elif body[:6] == "remove":
        db.session.query(models.Grocerylist).filter_by(item=body[7:]).delete()
        db.session.commit()
    else:
        print("we doing nothing")

    return flask.render_template("index.html")


if __name__ == "__main__":
    socketio.run(
        app,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
