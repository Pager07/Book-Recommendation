# initial setup of Flask
from flask import Flask, render_template, request, redirect, Response
import random, json

app = Flask(__name__)

# setup endpoint
@app.route("/")
def output():
    return render_template("index.html", name="Joe")


#setup endpoint
@app.route('/receiver', methods = ['POST'])
def worker():
    # read json + reply
    data = request.get_json(force = True)
    result = ''
    print(data)
    # for item in data:
    #     # loop over every row
    #     result += str(item['name']) + '\n'
    result += data['name']
    return result

# setup your script to actually run when it is requested:
if __name__ == '__main__':
    app.run()
