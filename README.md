
# Description

**this script helps you to catch autosar requirements you forgot to implement**

  

# Dependencies

only PyPDF2 by running the following command `pip install PyPDF2` before running the script or the script will install PyPDF2 by itself 

  

# Usage

by passing the sws_modul.pdf path , project path and comment_pattern.txt if it used as args to script like the following (any flag like -s not surrounded by[] is required)

`python reqMatcher.py [-h] -s SWSPDF_PATH -d PROJECT_PATH [-p COMMENT_PATTERN][-r REGEX_PATTERN]`

  

**note!!**

  

1- you can use default pattern by not passing `-r` or `-p` and the default pattern would be like following

`/*your comment[DIO096] or even here */` or just like this `/*[DIO096]*/`

  

2- if you know regex and python and want to use a different pattern just create a python file and create single variable named pattern and the pattern contains first named groups called "req_code" and the script will do its job


3-  if you don't know regex or python and want use another simple comment you can use --starting_tag and --ending_tag like the following:
`python reqMatcher.py -s SWSPDF_PATH -d PROJECT_PATH --starting_tag '[' --ending_tag ']'`
and the supported comments would be like this only `/*[DIO090]*/`

4- if you don't know regex or python and that comment_pattern.txt should be just two line ,first for starting tag and second for ending tag like

`[`
`]`

and this would lock for comments like this only `/*[DIO090]*/`
but can't see comments like this `/*your comment[DIO096] or even here */` nor this `/*[DIO096]*/` nor this `//[DIO096]`
