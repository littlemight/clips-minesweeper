from flask import Flask, send_from_directory,request
import random

app = Flask(__name__)

# Path for our main Svelte page

@app.route("/",methods=["GET","POST"])
def base():
    if (request.method =="GET"):
        return send_from_directory('client/public', 'index.html')
    else:
        # board_states =  start_game(args)
        return send_from_directory('client/public')


# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

@app.route("/rand")
def hello():
    return str(random.randint(0, 100))

if __name__ == "__main__":
    app.run(debug=True)