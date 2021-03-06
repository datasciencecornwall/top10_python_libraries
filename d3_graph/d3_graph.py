import os
import pandas
import IPython.core.display
import networkx
import networkx.readwrite.json_graph
import random


# force-directed graph
def plot_force_directed_graph(node1_node1_weight):
    # column names for node source and target, and edge attributes
    node_source_name = node1_node1_weight.columns.values[0]
    node_target_name = node1_node1_weight.columns.values[1]
    link_edge_name = node1_node1_weight.columns.values[2]

    # convert node1_node1_weight to graph
    graph = networkx.from_pandas_edgelist(node1_node1_weight, source=node_source_name, target=node_target_name, edge_attr=link_edge_name)

    # convert graph nodes and inks to json, ready for d3
    graph_json = networkx.readwrite.json_graph.node_link_data(graph)
    graph_json_nodes = graph_json['nodes']
    graph_json_links = graph_json['links']
    #print(str(graph_json_nodes))
    #print(str(graph_json_links))

    # read html template
    html_template_file = os.path.join(os.path.dirname(__file__), 'd3_graph.html')
    with open(html_template_file, mode='r') as f:
        html = f.read()
        pass

    # read javascript template
    js_template_file = os.path.join(os.path.dirname(__file__), 'd3_graph.js')
    with open(js_template_file, mode='r') as f:
        js = f.read()
        pass

    # generate random identifier for SVG element, to avoid name clashes if used multiple times in a notebook
    random_id_string = str(random.randrange(1000000,9999999))
    # replace placeholder in both html and js templates
    html = html.replace('%%unique-id%%', random_id_string)
    js = js.replace('%%unique-id%%', random_id_string)

    # substitute links and data
    js = js.replace('%%links%%', str(graph_json_links))
    js = js.replace('%%nodes%%', str(graph_json_nodes))
    js = js.replace('%%edge_attribute%%', link_edge_name)
    #print(html)
    #print(js)

    # display html in notebook cell
    IPython.core.display.display_html(IPython.core.display.HTML(html))
    # display (run) javascript in notebook cell
    IPython.core.display.display_javascript(IPython.core.display.Javascript(data=js))
    pass