# os is needed for environment variables, to set up our IP address and PORT number
import os
from flask import Flask

# Create an instance of flask, or a flask app. And we store it in the app variable 
app = Flask(__name__)

# The '/' refers to the default route
@app.route('/')
def hello():
    return 'Hello world .... again'

# set up our IP address and our port number so that Gitpod knows how to run and where to run our application.
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),  
            port=int(os.environ.get('PORT')),
            # Setting debug to true  allows the changes to be picked up automatically in the browser. And produce debug statements
            debug=True)
