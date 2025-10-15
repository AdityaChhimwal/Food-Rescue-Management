
# Its only job is to create and run our Flask app.

from project import create_app

# We call the create_app function (our "app factory") from the 'project' folder.
# This function will build our application for us.
app = create_app()

# This is a standard Python line that runs the web server.
# The 'if __name__ == "__main__":' part means this code will only run
# when you execute "python run.py" directly.
if __name__ == '__main__':

    app.run(debug=True)

