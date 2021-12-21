# coding: utf-8
try:
    import PyPDF2
    pass
except:
    print("the script need PyPDF2 , script will try to install it by itself for you")
    try:
        import sys
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
        import PyPDF2
        print("PyPDF2 installed successfully")
        del subprocess
        del sys
        pass
    except:
            print("PyPDF2 isn't installed and installing faild try to make sure that you pc connected to internet then run pip install PyPDF2")
            exit(404)
            pass
        

import os
import re
import argparse


# the following pattern is an accurate pattern but works only with full compatible terminales with utf8
sws_req_pattern_4_utf8=r"\[(?P<req_code>(?P<req_module>[A-Z]+)(?P<req_num>\d+))\] [\⌈]?(?P<req_discription>[^\⌋]*)[\⌋]? \(([^\)]*)\)"

# the following pattern 4 cmd and powershell
sws_req_pattern=r"\[(?P<req_code>(?P<req_module>[A-Z]+)(?P<req_num>\d+))\] (?P<req_discription>[^\(]*) \(([^\)]*)\)"
#sws_req_pattern_lite=r"\[(?P<req_code>(?P<req_module>[A-Z]+)(?P<req_num>\d+))\] (?P<req_discription>[^\(]*) \(([^\)]*)\)"

# this support only c comment /**/ as // not allowed by misra rules
default_comment_pattern=r"\/\*[^\]]*\[(?P<req_code>[A-Z]+[\d]+)\][^\*]*[^\/]*\*\/"

# for future using
used_comment_pattern=r''

# for simple extracting module_name
regex_comment_module_pattern=r"(?P<module_name>[\w]+)\.py"



parser = argparse.ArgumentParser(
                                    description="this script helps you to catch autosar requirments you forgot to implement by give the sws_modul.pdf ",
                                    usage="by passing the sws_modul.pdf path , project path and comment_pattern.txt if it used as args to script like the following (any flag like -s not surrounded by[] is required)\npython reqMatcher.py [-h] -s SWSPDF_PATH -d PROJECT_PATH [-p COMMENT_PATTERN][-r REGEX_PATTERN]\n\nnote!!\n\n1- that comment_pattern.txt should be just two line ,first for starting tag and second for ending tag like\n/*[\n]*/\n\n2- you can use default pattern by not pass and it like following\n/*[DIO096] and you comment*/ \n\n "
                                )

parser.add_argument('-s','--swspdf_path',required=True,help='the path of autosar_sws_module.pdf',type=str)
parser.add_argument('-d','--project_path',required=True,help='the path of project directory path',type=str)
parser.add_argument('-p','--comment_pattern',required=False,help='the path of comment_pattern.txt',type=str)
parser.add_argument('-r','--regex_pattern',required=False,help='the path of comment_pattern.py which contains only variable named pattern ',type=str)

args = parser.parse_args()


if(not(os.path.exists(args.swspdf_path))):
    print("%s isn't exist or invalid path"%(args.swspdf_path))
    exit()
    pass
if(not(os.path.isfile(args.swspdf_path))):
    print("%s isn't a file or invalid path"%(args.swspdf_path))
    exit()
    pass
if('.pdf' not in args.swspdf_path):
    print("%s isn't a pdf file"%(args.swspdf_path))
    exit()
    pass
if(not(os.path.exists(args.project_path))):
    print("%s isn't exist or invalid path"%(args.project_path))
    exit()
    pass
if(not(os.path.isdir(args.project_path))):
    print("%s isn't a directory or invalid path"%(args.project_path))
    exit()
    pass

if( bool(args.regex_pattern) ^ bool(args.comment_pattern) ):
    if(args.regex_pattern):
        match=re.search(regex_comment_module_pattern,args.regex_pattern)
        module_dir_path=args.regex_pattern.replace(match["module_name"],'') 
        exec("sys.path.append(%s)"%(module_dir_path))
        exec('from %s import pattern'%match["module_name"])
        exec('sws_req_pattern=pattern')
        pass

    if(bool(args.comment_pattern)):
        #with open(args.comment_pattern,'r') as f:
        print("not supported yet")
        exit()
        pass
elif(bool(args.regex_pattern)):
    print("just regex pattern or comment pattern only")
    print(args.comment_pattern)
    exit(2)
    #raise SystemExit
    pass

#except :
    #default case so do nothing
used_comment_pattern=default_comment_pattern


#scrape all req from swspdf
##open the swspdf and create PdfFileReader instance to interact with pdf file
pdfFileObj = open(args.swspdf_path, 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

#extract whole text in pdf file
data=str()
for page in [ pdfReader.getPage(i) for i in range(pdfReader.numPages)] :
    data=data+page.extractText()
    pass

#extract all requirments 
reqs=re.findall(sws_req_pattern,data)

#scan for all headers and source files in this path and sub directories
filelist = []

for root, dirs, files in os.walk(args.project_path):
	for file in files:
        #append the file name to the list
		filelist.append(os.path.join(root,file))
#filtering only .c .cpp .h .hpp
files=list(
    filter( lambda file : ('.c' in file or '.h' in file) , filelist)
    )
del filelist
all_commented_req=list()
for file in files:
    with open(file,'r') as f:
        code=''
        for line in f.readlines():
            code=code+line
        commented_req=re.findall(used_comment_pattern,code)
        all_commented_req.extend(commented_req)
        pass
    pass

forgot_req=list()
reqs_codes=[req[0] for req in reqs]
for req in reqs_codes:
    if req not in all_commented_req:
        forgot_req.append(req)
        pass
    pass


if len(forgot_req):
    print("forgot %d requirment from %d !"%(len(forgot_req),len(reqs_codes)))
    for req in forgot_req:
        print(req)
    pass
else:
    print("all requirments are mentioned ")
