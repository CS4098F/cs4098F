import os, sys
import subprocess
import pygraphviz as pgv
import os.path

CURRENT_DIRECTORY = os.getcwd()
#BUCKET_NAME = "temp_folder/"  # directory to store files
BUCKET_PATH = os.path.join(CURRENT_DIRECTORY)#,BUCKET_NAME)

def getAnalysisFile(filenameA):

    basename, ext = os.path.splitext(filenameA)
    path = os.path.join(BUCKET_PATH, basename + '.analysis')

    analysis_file = open(path, 'r')

    return analysis_file.read()#.split('/')[-1]


def pmlCheckT(pmlfile):

    basename, ext = os.path.splitext(pmlfile)
    path = os.path.join(BUCKET_PATH, basename + '.analysis')

    args = ["peosModified/pml/check/pmlcheck", pmlfile]
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pmlOutput, error = process.communicate()

    #write the output from pmlcheck to an analysis file
    write2AnaFile = open(path, 'w')
    write2AnaFile.write(pmlOutput)
    write2AnaFile.close()


    return  pmlOutput,error

#traverse to create dot file
def traverse(pmlfile, flag):

    basename, ext = os.path.splitext(pmlfile)
    path = os.path.join(BUCKET_PATH, basename + '.dot')

    args = ["peosModified/pml/graph/traverse", flag, pmlfile]
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    dotOutput, error = process.communicate()

    #write the output from traverse to a dot file
    write2DotFile = open(path, 'w')
    write2DotFile.write(dotOutput)
    write2DotFile.close()

    if process.returncode > 0:
        return error

    return  write2DotFile.name

#awk to create sed color file
def awk(analysis_file):

    args = ["awk", '-f', "peosModified/pml/graph/color-pml.awk"]
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)

    awkOutput, error = process.communicate(input=analysis_file)
    process.wait()

    if process.returncode > 0:
        return error
    return awkOutput


#combine sed and dot to create colored dot file
def graph_analysis(pmlfile, flag):

    if not os.path.isfile(pmlfile):
        raise IOError("File does not exist")

    basename, ext = os.path.splitext(pmlfile)

    DOT_FILE = traverse(pmlfile=pmlfile, flag = flag)
    ANA_FILE = getAnalysisFile(filenameA=pmlfile)
    AWK_FILE = awk(analysis_file=ANA_FILE)


    COLOR_DOT_FILE = os.path.join(BUCKET_PATH, DOT_FILE)

    args = ['sed', '-i', '-e',AWK_FILE, COLOR_DOT_FILE]
    process = subprocess.Popen(args, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE )
    process.wait()
    output_color_dot, error = process.communicate()

    final_colored_dot = open(COLOR_DOT_FILE, 'r')
    analysisColored = final_colored_dot.read()

    if process.returncode > 0:
        return error
    return analysisColored


# def main():

#      filename = 'simple.pml'
#      final = graph_analysis(filename, '-n')
#      #ANA_FILE = getAnalysisFile(filenameA=filename)
#      #AWK_FILE = awk(analysis_file=ANA_FILE)

#      print final

  
# if __name__ == "__main__":
#       main()