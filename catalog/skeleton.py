# Skeleton Flask Project
from flask import Flask
app = Flask(__name__)  # Pass in default file name as parameter


# Decorators for methods to execute based on route(s)
@app.route('/')
@app.route('/hello')
def HelloWorld():
    return "Hello World."

# __main__ is the default name given to the application run by the Python
# interpreter. The below if statement only runs if this file is being executed
# by it explicitly. If it's imported, the below won't run
if __name__ == '__main__':
    app.debug = True  # Will reload automatically when code changes
    app.run(host='0.0.0.0', port=5000)  # Run on public IP, port 5000
