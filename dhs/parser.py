import PyPDF2

# read the file
reader = PyPDF2.PdfFileReader(
    '4300A Sensitive-Systems-Handbook-v12_0-508Cs.pdf')

# output document info
print(reader.documentInfo)

# determine the number of pages
num_of_pages = reader.numPages
print('Number of pages: ' + str(num_of_pages))

# loop through the pages
pIndex = 0
strText = ""
while pIndex < num_of_pages:
    page = reader.getPage(pIndex)
    strText += page.extractText()
    pIndex += 1

# fix encodings
strText = strText.encode('utf-8').decode('ascii', 'ignore')

# output the result
txtFile = open("4300a.txt", "a")
txtFile.write(strText)
txtFile.close()