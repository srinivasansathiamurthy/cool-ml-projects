from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go

class HTMLExtractor:
    def __init__(self, url):
        self.url = url

    def get_html(self):
        options = Options()
        options.headless = True
        service = Service(webdriver.Chrome().service.path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(self.url)
        page_source = driver.page_source
        driver.quit()
        return page_source

class DOMBuilder:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, "html.parser")

    def add_nodes_edges(self, graph, parent, soup_element, level):
        if level > 10: return
        level += 1
        for child in soup_element.children:
            if child.name:
                child_id = f"{parent}/{child.name}"
                graph.add_node(child_id, label=child.name)
                graph.add_edge(parent, child_id)
                self.add_nodes_edges(graph, child_id, child, level)

    def build_dom_tree(self):
        G = nx.DiGraph()
        root_id = self.soup.name
        G.add_node(root_id, label=self.soup.name)
        self.add_nodes_edges(G, root_id, self.soup, 0)
        return G

def main(url):
    extractor = HTMLExtractor(url)
    html_content = extractor.get_html()
    
    builder = DOMBuilder(html_content)
    dom_tree = builder.build_dom_tree()
    
    pos = nx.spring_layout(dom_tree)
    labels = nx.get_node_attributes(dom_tree, 'label')
    
    x_nodes = [pos[node][0] for node in dom_tree.nodes()]
    y_nodes = [pos[node][1] for node in dom_tree.nodes()]
    text_nodes = [labels[node] for node in dom_tree.nodes()]
    
    edge_x = []
    edge_y = []
    for edge in dom_tree.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='black'),
        hoverinfo='none',
        mode='lines'
    ))
    
    fig.add_trace(go.Scatter(
        x=x_nodes, y=y_nodes,
        mode='markers+text',
        text=text_nodes,
        textposition='top center',
        marker=dict(size=10, color='lightgreen'),
        hoverinfo='text'
    ))
    
    fig.update_layout(
        title="DOM Structure of the Website",
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )
    
    fig.show()

if __name__ == "__main__":
    test_url = "https://en.wikipedia.org/wiki/Kanye_West"
    main(test_url)