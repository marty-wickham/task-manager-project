# os is needed for environment variables, to set up our IP address and PORT number
import os
import env
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
# MongoDB stores its data in a JSON like format called BSON.
from bson.objectid import ObjectId

# Create an instance of flask, or a flask app. And we store it in the app variable 
app = Flask(__name__)

# Add some configuration to our Flask application, the Mongo database
# name and the URL linking to that database.
MONGO_URI = os.getenv('MONGO_URI')

app.config["MONGO_DBNAME"] = 'task-manager'
app.config["MONGO_URI"] = MONGO_URI

print("Your Mongo URI is " + str(MONGO_URI))

# Create an instance of PyMongo. We'll add the app into that with what's called a constructor method.
# Our app object is the argument.
mongo = PyMongo(app)

'''
The '/' refers to the default route. To make our connection to the database, 
create a function with a decorator that includes a route to that function. 
The routing is a string that, when attached to a URL, will redirect to a 
particular function in our Flask application. Two decorators  '/' and a string 
with 'get_tasks'. When the application is run, then the default function that 
will be called will be get_ tasks because of that single '/' decorator that's in place. 
'''
@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    # supply a tasks collection, which will be returned from making a call directly to Mongo.  
    # mongo.db.tasks is our collection.
    # The find() method will return everything in our tasks collection. 
    return render_template("tasks.html", tasks=mongo.db.tasks.find())

# set up our IP address and our port number so that Gitpod knows how to run and where to run our application.
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),  
            port=int(os.environ.get('PORT')),
            # Setting debug to true  allows the changes to be picked up automatically in the browser. And produce debug statements
            debug=True)
