import networkx as nx
from collections import namedtuple
from math import sqrt
import bokeh
from bokeh.models import HoverTool
from bokeh.plotting import show, figure
from bokeh.colors import RGB
import random

#corresponding package on pypi is confusingly called python-louvain
import community


def create_bokeh_graph(graph):
    
    def gen_edge_coordinates(graph, layout):
        xs = []
        ys = []
        val = namedtuple("edges", "xs ys")
        for edge in graph.edges():
            from_node = layout[edge[0]]
            to_node = layout[edge[1]]
            xs.append([from_node[0],to_node[0]])
            ys.append([from_node[1], to_node[1]])
        return val(xs=xs, ys=ys)

    def gen_node_coordinates(layout):
        names, coords = zip(*layout.items())
        xs, ys = zip(*coords)
        val = namedtuple("nodes", "names xs ys")
        return val(names=names, xs=xs, ys=ys)
    
    #Calc Layout - Slowest Part
    plot_layout = nx.spring_layout(graph,
                                k=1/(sqrt(graph.number_of_nodes() * 0.75)),
                                iterations=60,
                                scale = 2)
    
    _nodes = gen_node_coordinates(plot_layout)
    _edges = gen_edge_coordinates(graph, plot_layout)
    
    #Prepare Bokeh-Figure
    hover = HoverTool(tooltips=[('name', '@name'), 
                                ('node_id', '$index'),
                                ('degree', '@degree'),
                                ('betweenness centrality', '@betweenness'),
                                ('clustering', '@clustering'),
                                ('cluster_nr', '@community_nr')], names=["show_hover"])

    fig = figure(width=800, height=600, 
                 tools=[hover, 'box_zoom', 'reset', 'wheel_zoom', 'pan', 'lasso_select'],
                logo = None)
    fig.toolbar.logo = None
    fig.axis.visible = False                            
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None
    
    #Draw Edges
    source_edges = bokeh.models.ColumnDataSource(dict(xs=_edges.xs, ys=_edges.ys))
    fig.multi_line('xs', 'ys', line_color='navy', source=source_edges, alpha=0.17)
    
    #Calc numbers
    degrees = list(nx.degree(graph).values())
    clustering = list(nx.clustering(graph).values())
    communs = community.best_partition(graph)
    nodes, communities = zip(*communs.items())
    betw = list(nx.betweenness_centrality(graph).values())
    
    #create Colormaps
    colormap_coms = {x : RGB(random.randrange(0,256),random.randrange(0,256),random.randrange(0,256)) 
                     for x in list(set(communities))}
    community_color_list, community_nr = zip(*[(colormap_coms[communs[node]], communs[node]) for node in nodes])

    
    graph_nodes = graph.number_of_nodes()
    
    colors = ['firebrick' for node in range(graph_nodes)]
    
    #Draw circles
    source_nodes = bokeh.models.ColumnDataSource(dict(xs=_nodes.xs, ys=_nodes.ys, name=_nodes.names, 
                                                      single_color = colors,
                                                      color_by_community = community_color_list, 
                                                      degree=degrees, 
                                                      clustering=clustering, community_nr=community_nr,
                                                      betweenness = betw))
    
    r_circles = fig.circle('xs', 'ys', fill_color='single_color', line_color='single_color', 
                           source = source_nodes, alpha=0.7, size=9, name="show_hover")
    
    #Create Color-Selector    
    colorcallback = bokeh.models.callbacks.CustomJS(args=dict(source=source_nodes, circles=r_circles), code="""
        var value = cb_obj.get('value');
        circles.glyph.line_color.field = value;
        circles.glyph.fill_color.field = value;
        source.trigger('change')
    """)  
    
    button = bokeh.models.widgets.Select(title="Color", value="single_color", 
                                         options=["single_color", "color_by_community"], 
                                         callback=colorcallback)
    
    #Create grid and save
    layout_plot = bokeh.layouts.gridplot([[fig, button]])
    
    #if file is wanted
    #bokeh.io.output_file(f"graph.html")
    #bokeh.io.save(layout_plot)
    
    show(layout_plot)


#working example
graph = nx.barbell_graph(5,6)
create_bokeh_graph(graph)
