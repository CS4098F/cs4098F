import json
import os, sys, tempfile
import subprocess
import uuid
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from graphviz import Source
#import pydot
#import pyparsing 
import pygraphviz as pgv

CURRENT_DIRECTORY = os.getcwd()
BUCKET_NAME = "temp_folder"              #directory to store files
BUCKET_PATH = os.path.join(CURRENT_DIRECTORY, BUCKET_NAME)

app = Flask(__name__)
app.config['BUCKET_PATH'] = BUCKET_PATH
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'svg', 'pml'])




@app.route('/')
def main():
    return render_template('index1.html')


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


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
            path = os.path.join(BUCKET_PATH, filename)

            file_handle = open(path, "w")
            #write data to file
            file_handle.write(out_data)
            file_handle.close()

            return render_template("index1.html", output = out_data)
        else:
            return redirect("/")

@app.route("/graph", methods=['GET', 'POST'])
def graph():
	     with tempfile.NamedTemporaryFile(mode='w+t', suffix='.dot') as file_handle:
        	fname = file_handle.name

       		file_handle.write(request.form["text"])
       		file_handle.flush()

       		process = subprocess.Popen(["peos/pml/graph/traverse" , '-n',fname],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
       		output_dot = process.communicate()[0]
    
       		dot_file = open(path, "w")
       		dot_file.write(output_dot)
       		dot_file.close()

       		A=pgv.AGraph(output_dot)
       		A.write('temp_folder/'+filename+".dot") # write to simple.dot
        	A.draw('temp_folder/'+ filename+'.svg',prog="circo") # draw to png using circo
        

       		listFiles = url_for('uploaded_file',filename=filename + '.svg')

        	return render_template('graph.html', result = output_res, output = text, imgpath = listFiles)
       	 



@app.route("/pmlcheck", methods=['POST'])
def pmlcheck():
	global text
 	text = request.form["text"]
	if text:
		global filename
		filename = str(uuid.uuid4())
		global path
		path = os.path.join(BUCKET_PATH, filename)

    	file_handle = open(path, "w")
    	#save input file to local temp file
    	file_handle.write(text)
    	file_handle.close()


    	process = subprocess.Popen(["peos/pml/check/pmlcheck",path],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  	
	global output_res
    	output_res, err = process.communicate()
    	
	output_res = "No errors detected"
        
	err = err.strip().replace(path +':', "Line number ")
    	if process.returncode > 0:
        	return render_template('index1.html', result = err, output = text)
    	return render_template('graph.html', result = output_res, output = text)

        	
    	


if __name__ == "__main__":
    app.debug = True
    app.run()
