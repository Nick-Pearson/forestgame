from flask import *

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def root_html():
    return send_from_directory('../dist', 'index.html')

@app.route('/game.js')
def static_script():
    return send_from_directory('../dist', 'game.js')

if __name__ == "__main__":
    print("Starting server");

    app.testing = True;
    app.run(debug=True);