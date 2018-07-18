import PyPDF2
import os
import csv 

PDF_DIRECTORY = 'smaller_sample_pdfs/'
CSV_DIRECTORY = 'node_csvs/'
NODE_CSV_NAME = 'smaller_sample_nodes.csv'


def main():

	research_node = create_nodes_from_csv(CSV_DIRECTORY + NODE_CSV_NAME)

	for filename in os.listdir(PDF_DIRECTORY):
		if filename != '.DS_Store':
			# print_pdf_contents(PDF_DIRECTORY, filename)
			map_citation_network(research_node, PDF_DIRECTORY, filename)

	print(research_node)


def print_pdf_contents(directory_name, filename):

	pdf_object = open(directory_name + filename, 'rb')

	try:
		pdf_reader = PyPDF2.PdfFileReader(pdf_object)
		for page_number in range(pdf_reader.numPages):
			page_object = pdf_reader.getPage(page_number)
			print(page_object.extractText())
	except:
		print(o_file, 'broken file') 


def map_citation_network(research_node, directory_name, filename):

	pdf_object = open(directory_name + filename, 'rb')

	try:
		pdf_reader = PyPDF2.PdfFileReader(pdf_object)

		paper_date = filename[:4]

		for page_number in range(pdf_reader.numPages):
			page_object = pdf_reader.getPage(page_number)
			calculate_references(research_node, page_object.extractText(), filename, paper_date)

	except TypeError:
		print('Invalid PDF: ', filename)
	except:
		print ('Pdf Read Error', filename)


def calculate_references(research_node, file_text, filename, paper_date):
	for key, value in research_node.iteritems():
		author_name = key[5:]
		author_date = int(key[:4])
		if author_date < int(paper_date) and author_name in file_text:
			print('found ', author_name, ' in ', filename)
		 	research_node[filename[:-4]]['references'].update({key: True});


def create_nodes_from_csv(csv_filename):

	research_node = {}

	with open(csv_filename, 'rb') as csv_file:

		csv_reader = csv.reader(csv_file)

		for row in csv_reader:
			research_node[row[1].rstrip()] = {'year': row[1][:4], 'id': row[0], 'references': {}}
		
		return research_node


if __name__ == "__main__":
	main()