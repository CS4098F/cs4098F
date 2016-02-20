import json
import os, sys
import subprocess
import uuid
from flask import Flask, render_template, request, redirect, url_for, send_from_directory



CURRENT_DIRECTORY = os.getcwd()
BUCKET_NAME = "temp_folder"              #directory to store files
BUCKET_PATH = os.path.join(CURRENT_DIRECTORY, BUCKET_NAME)

app = Flask(__name__)
app.config['BUCKET_PATH'] = BUCKET_PATH


@app.route('/')
def main():

    return render_template('index1.html')


@app.route('/temp_folder/<filename>')
def uploaded_file(filename):
    return send_from_directory(BUCKET_PATH, filename)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files['file']
        if files:
            out_data = files.read()
            filename = files.filename
            paths = os.path.join(BUCKET_PATH, filename)

            file_handle = open(paths, "w")
            #write data to file
            file_handle.write(out_data)
            file_handle.close()

            process = subprocess.Popen(["peos/pml/graph/traverse",filename],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output_dot = process.communicate()[0]

            filename2, file_extension = os.path.splitext(filename)
            paths2 = os.path.join(BUCKET_PATH, filename2 + ".dot")
            dot_file = open(paths2, "w")
            dot_file.write(str(output_dot))
            dot_file.close()

            return render_template('/editor.html', output = out_data, output_dot = output_dot)
        else:
            return redirect('/')


# @app.route('/editor', methods=['GET', 'POST'])
# def edit_file():
#     if request.method == 'POST':
#         files = request.form["file"]
#         filename = files.filename
#         path = os.path.join(BUCKET_PATH, filename)
#         file_handle = open(path, "r")
#
#     return render_template("editor.html", output = file_handle.read() )


@app.route("/text2File", methods=['POST'])
def text2File():
    text = request.form["text"]
    if text:
        filename = str(uuid.uuid4())
        path = os.path.join(BUCKET_PATH, filename)

        file_handle = open(path, "w")
        #save input file to local temp file
        file_handle.write(text)
        file_handle.close()

        process = subprocess.Popen(["peos/pml/check/pmlcheck",path],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        #except OSError as error:
        #    return error

        output_res, err = process.communicate()
        if process.returncode > 0:
            return err
        return render_template('result.html', output = output_res)


if __name__ == "__main__":
    app.debug = True
    app.run()
