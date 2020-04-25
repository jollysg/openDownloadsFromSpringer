# Created by Jasprit S Gill, April 25, 2020
# email: jaspritsgill@gmail.com
# Copyright (c) 2020, Jasprit Singh Gill
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of Jasprit, nor the names of any organizers linked
#      to him may be used to endorse or promote products derived from
#       this software without specific prior written permis sion.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

'''
This file was developed as a crude way of downloading some open pdf documents for educational purpose. The script has been
tested with Python version 2.7.12 on MacOS.

It requires following python libraries to be installed (using pip or sudo apt-get):
xlrd, urllib2, urllib, urlparse, os.

Steps for using this script, assuming that Python 2.7+ and the above python packages are installed:
1. Place this python script in the same folder as the accompanying excel sheet.
2. Run the script using:
    python fetchFronSpringer.py
3. The files will be downloaded in the pdf format to a folder called "springer_books" in he same
    directory as this script.
'''

import urllib2
import urllib
import xlrd
from urlparse import urlsplit
from urlparse import urlunsplit
import os

def createDirectory(dirPath):
    if dirPath == '':
        return
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    else:
        print('Directory "' + dirPath + '" already exists.')

def downloadFileFromURL(downloadURL, filenameForSaving):
    if not os.path.exists(filenameForSaving):
        print('Downloading...' + downloadURL + ' and saving as: ' + filenameForSaving)
        urllib.urlretrieve(downloadURL, filenameForSaving)
        print('Downloaded complete.')
    else:
        print('File "' + filenameForSaving + '" found locally. Skipping the download')

# Crude way of Exracting the book page url from springers url response
def extractURLFromText(htmlLine):
    searchString = '"canonical" href="'
    startIndex = htmlLine.find(searchString)
    endIndex = -1
    if (startIndex != -1):
        endIndex = htmlLine[startIndex+len(searchString):].find('"')
    return htmlLine[startIndex+len(searchString):startIndex+len(searchString)+endIndex]

# Crude way of Exracting the book name from springers url response
def extractNameFromText(htmlLine):
    searchString = '<title>'
    startIndex = htmlLine.find(searchString)
    endIndex = -1
    if (startIndex != -1):
        endIndex = htmlLine[startIndex+len(searchString):].find('|')
    return htmlLine[startIndex+len(searchString):startIndex+len(searchString)+endIndex-1]

#
# Caution: The springer links are links to the book webpage and not to the pdf documents.
# This routine is a crude way of handling these links and may work only for springer
# links. Following are the steps to the work around:
#   1. Fetch the response from the springer webpage urls for the books. The responses
#       to these links are redirections to the link to the book webpage.
#   2. Extract the bookname and urlname from the reponse. For eg, a link such as
#           http://link.springer.com/openurl?genre=book&isbn=978-0-306-48048-5
#       in the spreadsheet for a book redirects to the book webpage:
#           https://link.springer.com/book/10.1007%2Fb100747
#       The response gives the name of the book and the redirectd url in the html format,
#       and both can be searched using a simple sring query, as their field/tag names are
#       pretty consistent across all the links provided. Again, this redirected link is
#       the link to the webpage of the book and not the download link to the pdf of book.
#   3. However, finding the pdf document link has an easy work around. Apparently, the
#       book names and the urls for the pdf documents are mapped in a pretty consistent
#       (read dumb) manner on springer. For ex:  the link book page link:
#           https://link.springer.com/book/10.1007%2Fb100747
#       maps to the document link
#           https://link.springer.com/content/pdf/10.1007%2Fb100747.pdf
#       So all that is needed is a simple string manipulation to get the pdf url.
#   4. Once we have the pdf url, download it using urllib2 and urllib

def fetchContentFromURL(urlStr, baseURL=''):

    # Step 1
    req = urllib2.Request(urlStr)
    response = urllib2.urlopen(req)
    html = response.read()

    # Step 2
    bookURL = extractURLFromText(html)
    bookName = extractNameFromText(html)

    # Step 3
    urlobj = urlsplit(bookURL)
    urlPathList = urlobj.path.split('/', 2)
    doiName = urlPathList[2] + '.pdf';
    newUrlPath = '/content/pdf/' + doiName;
    newUrlObj = list(urlobj)
    newUrlObj[2] = newUrlPath
    downloadURL = urlunsplit(newUrlObj)
    bookName = bookName.replace('/', ' ') + ' ' + doiName.replace('/', ' ')

    # Step 4
    downloadFileFromURL(downloadURL, baseURL+ '/' +bookName)

if __name__ == "__main__":
    # create a base directory to download the file in
    baseURL = 'springer_books'
    createDirectory(baseURL)

    # Read the spreadsheets for links
    workBook = xlrd.open_workbook('springer_links.xlsx')
    worksheet = workBook.sheet_by_index(0)
    links = worksheet.col_values(6, 7, worksheet.nrows)
    validLinks = [link for link in links if link != u'']

    # Start downloading the pdfs from the links one by one.
    for link in validLinks:
        fetchContentFromURL(link, baseURL)
