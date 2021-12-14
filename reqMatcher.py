# coding: utf-8
import PyPDF2
import re
import argparse


parser = argparse.ArgumentParser(
    description=
    """
    this script helps you to catch autosar requirments you forgot to implement it
    by give the sws_modul.pdf , project path and pattern.txt as args to script 
    """)
# the following pattern is an accurate pattern but works only with full compatible terminales with utf8
sws_req_pattern_4_utf8=r"\[(?P<req_code>(?P<req_module>[A-Z]+)(?P<req_num>\d+))\] [\⌈]?(?P<req_discription>[^\⌋]*)[\⌋]? \(([^\)]*)\)"

# the following pattern 4 cmd and powershell
sws_req_pattern_lite=r"\[(?P<req_code>(?P<req_module>[A-Z]+)(?P<req_num>\d+))\] (?P<req_discription>[^\(]*) \(([^\)]*)\)"



pdfFileObj = open('AUTOSAR_SWS_DIODriver.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
data=str()
for page in [ pdfReader.getpage(i) for i in range(pdfReader.numPages)] :
    data=data+page.extractText()
    
    
sws_req_pattern=r"\[(?P<req_code>(?P<req_module>[A-Z]+)(?P<req_num>\d+))\] (?P<req_discription>[^\(]*) \(([^\)]*)\)"
reqs=re.findall(sws_req_pattern,data)
reqs
for page in [ pdfReader.getPage(i) for i in range(pdfReader.numPages)] :
    data=data+page.extractText()
    
reqs=re.findall(sws_req_pattern,data)
reqs
