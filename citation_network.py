import PyPDF2
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import networkx as nx
import os
import csv 

plotly.tools.set_credentials_file(username='lassenordahl', api_key='xsorGpccQaRkt0JVAXec')

PDF_DIRECTORY = 'smaller_sample_pdfs/'
CSV_DIRECTORY = 'node_csvs/'
NODE_CSV_NAME = 'smaller_sample_nodes.csv'


def main():

	testNetworkGraph()

	research_node = create_nodes_from_csv(CSV_DIRECTORY + NODE_CSV_NAME)

	for filename in os.listdir(PDF_DIRECTORY):
		if filename != '.DS_Store':
			# print_pdf_contents(PDF_DIRECTORY, filename)
			map_citation_network(research_node, PDF_DIRECTORY, filename)

	# print_research_node(research_node)


def print_pdf_contents(directory_name, filename):

	pdf_object = open(directory_name + filename, 'rb')

	try:
		pdf_reader = PyPDF2.PdfFileReader(pdf_object)
		for page_number in range(pdf_reader.numPages):
			page_object = pdf_reader.getPage(page_number)
			print(page_object.extractText())
	except:
		print('unsupported file')

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
		if contains_citation(author_date, author_name, file_text, paper_date):
			print('found ', author_name, ' in ', filename)
		 	research_node[filename[:-4]]['references'].update({key: True})


def contains_citation(checking_author_date, checking_author_name, file_text, file_date):
	return checking_author_date < int(file_date) and checking_author_name in file_text


def create_nodes_from_csv(csv_filename):

	research_node = {}

	with open(csv_filename, 'rb') as csv_file:

		csv_reader = csv.reader(csv_file)

		for row in csv_reader:
			research_node[row[1].rstrip()] = {'year': row[1][:4], 'id': row[0], 'references': {}}
		
		return research_node


def print_research_node(research_node):
	for key, value in research_node.iteritems():
		print(key, ' references ')
		print(value['references'])
		print()


def testNetworkGraph():
	G=nx.random_geometric_graph(200,0.125)
	pos=nx.get_node_attributes(G,'pos')

	dmin=1
	ncenter=0
	for n in pos:
		x,y=pos[n]
		d=(x-0.5)**2+(y-0.5)**2
		if d<dmin:
			ncenter=n
			dmin=d

	p=nx.single_source_shortest_path_length(G,ncenter)

	edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')

	for edge in G.edges():
		x0, y0 = G.node[edge[0]]['pos']
		x1, y1 = G.node[edge[1]]['pos']
		# print(x0, y0)
		edge_trace['x'] = [x0, x1, None]
		edge_trace['y'] = [y0, y1, None]

	node_trace = go.Scatter(
		x=[],
		y=[],
		text=[],
		mode='markers',
		hoverinfo='text',
		marker=dict(
			showscale=True,
			# colorscale options
			# 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
			# Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
			colorscale='Greys',
			reversescale=True,
			color=[],
			size=10,
			colorbar=dict(
				thickness=15,
				title='Node Connections',
				xanchor='left',
				titleside='right'
			),
			line=dict(width=2)))

	for node in G.nodes():
		x, y = G.node[node]['pos']
		# print(x, y)
		# node_trace['x'].append(x)
		# node_trace['y'].append(y)
		node_trace['x'] += (x,)
		node_trace['y'] += (y,)

	for node, adjacencies in enumerate(G.adjacency()):
		# node_trace['marker']['color'].append(len(adjacencies))
		node_trace['marker']['color'] += (len(adjacencies), )
		node_info = '# of connections: '+str(len(adjacencies))
		# node_trace['text'].append(node_info)
		node_trace['text'] = (node_info, )


	fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Network graph made with Python',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Test Graph haha",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

	py.plot(fig, filename='networkx')


if __name__ == "__main__":
	main()