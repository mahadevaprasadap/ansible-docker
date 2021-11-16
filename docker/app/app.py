#!venv/bin/python
from flask import Flask, render_template, url_for, redirect, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os
import socket


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://{0}:{1}@{3}:27017/{2}?authSource=admin&ssl=false".\
    format(os.environ.get('MONGO_USER'), os.environ.get('MONGO_PASSWORD'), os.environ.get('MONGO_DB_NAME'), os.environ.get('MONGO_HOST'))

print("mongodb://{0}:{1}@172.19.0.2:27017/{2}?authSource=admin&ssl=false".format(os.environ.get('MONGO_USER'), os.environ.get('MONGO_PASSWORD'), os.environ.get('MONGO_DB_NAME')))
mongo = PyMongo(app)

todos = mongo.db.get_collection(os.environ.get('MONGO_COLLECTION'))


@app.route('/')
def index():
    docker_short_id = socket.gethostname()
    toDoList = todos.find()
    return render_template('index.html', toDoList=toDoList, docker_short_id=docker_short_id)

@app.route('/add', methods=['POST'])
def add(): 
    new_todo = request.form.get('new-todo')
    todos.insert_one({'text' : new_todo, 'complete' : False})
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete(id):
    todos.delete_one({'_id' : ObjectId(id)})
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()