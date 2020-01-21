# os is needed for environment variables, to set up our IP address and PORT number
import os
from os import path 
if path.exists("env.py"):
    import env
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
# MongoDB stores its data in a JSON like format called BSON.
from bson.objectid import ObjectId

# Create an instance of flask, or a flask app. And we store it in the app variable 
app = Flask(__name__)

# Add some configuration to our Flask application, the Mongo database
# name and the URL linking to that database.

app.config["MONGO_DBNAME"] = 'task-manager'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

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


@app.route('/add_task')
def add_task():
    return render_template("add-task.html", categories=mongo.db.categories.find())


# Because we are submitting a form, we must refer to the HHTP method that will be used to deliver the form data
# The default is 'GET'. It's only if 'POST' submisiion format is used we must specify.
@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.tasks
    # When information is submitted to some web location, it is submitted in the form of a request object.
    # Converting form to a dictionary so it can be understood by mongo
    tasks.insert_one(request.form.to_dict())

    return redirect(url_for('get_tasks'))


@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories = mongo.db.categories.find()

    return render_template("edit-task.html", task=the_task, categories=all_categories)


@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update(
        {'_id': ObjectId(task_id)},
        {'task_name': request.form.get('task_name'),
         'category_name': request.form.get('category_name'),
         'task_description': request.form.get('task_description'),
         'due_date': request.form.get('due_date'),
         'is_urgent': request.form.get('is_urgent')})

    return redirect(url_for('get_tasks'))


@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})

    return redirect(url_for('get_tasks'))


@app.route('/get_categories')
def get_categories():

    return render_template('categories.html', categories=mongo.db.categories.find())


@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    
    return render_template('edit-category.html', category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))


@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})

    return redirect(url_for('get_categories'))


@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})

    return redirect(url_for('get_categories'))


@app.route('/add_category')
def add_category():
    return render_template('add-category.html')


@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories = mongo.db.categories.find()
    new_doc = {'category_name': request.form.get('category_name')}
    mongo.db.categories.insert(new_doc)

    return redirect(url_for('get_categories'))


# set up our IP address and our port number so that Gitpod knows how to run and where to run our application.
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),  
            port=int(os.environ.get('PORT')),
            # Setting debug to true  allows the changes to be picked up automatically in the browser. And produce debug statements
            debug=True)