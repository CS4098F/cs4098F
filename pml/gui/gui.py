import json
import os
import subprocess
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

    text = request.form['text']
    path = os.path.join(BUCKET_PATH, "test.pml")
    file_handle = open(path, "w")
    #save input file to local temp file
    file_handle.write(text)
    file_handle.close()

    try:
        process = subprocess.Popen(["C:/Users/sunil/Desktop/cs4098F/pml/check/pmlcheck",path],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    except OSError as error:
        return error

    output_res, err = process.communicate()
    if process.returncode > 0:
        return err
    return output_res


if __name__ == "__main__":
    app.debug = True
    app.run()
