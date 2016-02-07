import json
import os
from flask import Flask, render_template, request
app = Flask(__name__)

CURRENT_DIRECTORY = os.getcwd()
BUCKET_NAME = "temp_folder"              #directory to store files
BUCKET_PATH = os.path.join(CURRENT_DIRECTORY, BUCKET_NAME)

@app.route("/")
def main():

    return render_template('index.html')

@app.route("/", methods=['POST'])
def text2File():
    path = os.path.join(BUCKET_PATH, "test.pml")
    file_handle = open(path, "w+")
    text = request.form['text']
    file_handle.write(text)
    file_handle.close()

if __name__ == "__main__":
    app.debug = True
    app.run()
