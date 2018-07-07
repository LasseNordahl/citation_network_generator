import PyPDF2
import os

def main():

	for filename in os.listdir('research_pdfs'):
		print_pdf_contents('research_pdfs/' + filename)

def print_pdf_contents(o_file):

	pdf_object = open(o_file, 'rb')

	pdf_reader = PyPDF2.PdfFileReader(pdf_object)

	for page_number in range(pdf_reader.numPages):
		page_object = pdf_reader.getPage(page_number)
		print(page_object.extractText())

if __name__ == "__main__":

	main()