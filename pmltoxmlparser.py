from xml.etree import ElementTree as ET
import  os, itertools, json
import subprocess


# Read in a pml file and save to an xml file
def translate_pml_file(pml_file):

    pml_path = os.path.abspath(pml_file)
    basename, ext = os.path.splitext(pml_path)
    xml_path = os.path.abspath(basename+'.xml')

    args = ["parser/Pmlxml", xml_path, pml_file]
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result, error = process.communicate()

    if process.returncode > 0:
        return error

    return result



def getAgents(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    final = []
    for child in root.iter('SpecAgent'):
        for agent in child.iter('ID'):
            res = ( agent.attrib)
            final.append(res)

    return final

def getNames(agents):
    result = []
    for d in agents:
        if 'value' in d:
          result.append( d['value'])

    return result

# if __name__ == "__main__":
#     #translate_pml_file('simple.pml')
#     agents =  getAgents('simple.xml')
#     names = getNames(agents)
#     print (names)




