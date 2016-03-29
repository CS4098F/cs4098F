import json
import os, sys, tempfile, stat, shutil, re, nltk
import subprocess
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import pygraphviz as pgv
import graph as test
import pmltoxmlparser as test2
from xml.etree import ElementTree as ET


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

    return render_template('graph2.html')


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


#return location of the svg graph file
@app.route('/temp_folder/<filename>' )
def uploaded_file(filename):
    return send_from_directory(BUCKET_PATH, filename)


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files['file']
        if files and allowed_file(files.filename):
            out_data = files.read()
            global filename
            filename = secure_filename(files.filename)
            # global path
            path = os.path.join(BUCKET_PATH, filename)

            file_handle = open(path, "w")
            # write data to file
            file_handle.write(out_data)
            file_handle.close()

            return render_template("graph2.html", output=out_data)
        else:
            return redirect("/")



def flushPath(filename):
    #removes files in temp_folder
    folder = BUCKET_PATH
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e


@app.route("/graph" , methods=['GET','POST'])
def swimLaneDiagram():
    text = request.form["code"]
    if text :
        path = os.path.join(BUCKET_PATH, 'test.pml')
        file_handle = open(path, "w")
        # write data to file
        file_handle.write(text)
        file_handle.close()

        test2.translate_pml_file('temp_folder/test.pml')
        agents =  test2.getAgents('temp_folder/test.xml')
        names = test2.getNames(agents)
        #print (names)

        return render_template("graph.html", agent=names)#, agent2=ag2, agent3=ag3, agent4=ag4, agent5=ag5, agent6=ag6)
    else:
        return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run()
