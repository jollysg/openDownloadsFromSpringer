# Download Open Publications From Springer
This package is a crude way of downloading some open pdf documents from Springer publications for educational purpose. The script has been tested with Python version 2.7.12 on MacOS/Unix. It has NOT been tested on Python 3.x.

It requires following python libraries to be installed (using 'pip install xxx' or 'sudo apt-get install' ):
xlrd, urllib2, urllib, urlparse, os.

Steps for using this script, assuming that Python 2.7+ and the above python packages are installed:
1. Place this python script in the same folder as the accompanying excel sheet.
2. Run the script using:
    python fetchFronSpringer.py
3. The files will be downloaded in the pdf format to a folder called "springer_books" in he same
    directory as this script.

### Acknowledgement
The accompanying file "Springer Ebooks.pdf" was from Whatsapp University ( yup, that's right). The pdf was converted to the spreadsheet format thanks to the folks at https://pdf2docx.com/.

### Correspondence
For any queries, please contact Jasprit at jaspritsgill@gmail.com
