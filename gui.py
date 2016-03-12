import json
import os, sys, tempfile, stat, shutil
import subprocess
import uuid
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import pygraphviz as pgv
import test

reload(sys)
sys.setdefaultencoding("utf-8")

CURRENT_DIRECTORY = os.getcwd()
BUCKET_NAME = "temp_folder/"  # directory to store files
BUCKET_PATH = os.path.join(CURRENT_DIRECTORY, BUCKET_NAME)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = BUCKET_PATH
app.config['ALLOWED_EXTENSIONS'] = set(['pml'])


def __init__():
    if not os.path.exists('temp_folder'):
        os.mkdir('temp_folder')


@app.route('/')
def main():
    __init__()
    return render_template('index1.html')


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


#return location of the svg graph file
@app.route('/temp_folder/<filename>')
def uploaded_file(filename):
    return send_from_directory(BUCKET_PATH, filename)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files['file']
        if files and allowed_file(files.filename):
            out_data = files.read()
            # global filename
            filename = secure_filename(files.filename)
            # global path
            path = os.path.join(BUCKET_PATH, filename)

            file_handle = open(path, "w")
            # write data to file
            file_handle.write(out_data)
            file_handle.close()

            return render_template("index1.html", output=out_data)
        else:
            return redirect("/")


@app.route("/pmlcheck", methods=['POST'])
def pmlcheck():
    #global text
    text = request.form["text"]

    if text:

        #global filename

        filename = 'test.pml'  # + random.choice("1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ") + '.pml'

        # save pml file
        file_handle = open(BUCKET_PATH + filename, "w")
        file_handle.write(text)
        file_handle.close()

        #global path
        path = os.path.join(BUCKET_PATH, filename)

        file = open(path, 'r')

        process = subprocess.Popen(["peos/pml/check/pmlcheck", file.name], stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #global output_res
        output_res, err = process.communicate()
        output_res = output_res.strip().replace(path, filename)

        output_res = "No errors detected"

        err = err.strip().replace(path + ':', "Line number ")
        if process.returncode > 0:
            return render_template('index1.html', result=err, output=text)
        return render_template('graph.html', result=output_res, output=text)


def flushPath():
    #removes files in temp_folder
    folder = BUCKET_PATH
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e

#analysis colored actions
@app.route("/graph", methods=['GET', 'POST'])
def graph():
    text = request.form["text"]
    if text:
        with tempfile.NamedTemporaryFile(mode='w+t', suffix='.pml') as file:#open(path) as file:
            name = file.name
            basename, ext = os.path.splitext(name)
            path = os.path.join(basename + '.pml')

            file.write(text)
            file.flush()
            try:

                #check for error to avoid dot error later on
                process = subprocess.Popen(["peos/pml/check/pmlcheck", name], stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output_res, error = process.communicate()
                output_res = output_res.strip().replace(path, name)
                
                # create analysis file
                fname, ext = os.path.splitext(name)
                path2 = os.path.join(fname + ".analysis")
                analysis_file = open(path2, "w")
                analysis_file.write(output_res)
                analysis_file.close()

                error = error.strip().replace(name + ':', "Line number ")
                if process.returncode > 0:
                    return render_template('index1.html', result=error, output=text)
                finalgraph = test.graph_analysis(pmlfile=name, flag='-n')
                
                # create graph
                Graph = pgv.AGraph(finalgraph)
                Graph.draw(BUCKET_PATH +'graph'+'.svg', prog="dot")

                #return graph
                listFiles = url_for('uploaded_file' , filename= 'graph.svg')

                output_res = 'No Errors Detected'

                return render_template('graph.html', result=output_res, output=text, imgpath=listFiles)

            except subprocess.CalledProcessError as err:
                return err.output.decode(), 400




if __name__ == "__main__":
    app.debug = True
    app.run()