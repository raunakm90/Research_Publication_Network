import plotly.plotly as py
from plotly.graph_objs import *


def scatter_nodes(G,pos, labels=None, color=None, size=20, opacity=1,size_flag = 0):
    # pos is the dict of node positions
    # labels is a list  of labels of len(pos), to be displayed when hovering the mouse over the nodes
    # color is the color for nodes. When it is set as None the Plotly default color is used
    # size is the size of the dots representing the nodes
    #opacity is a value between [0,1] defining the node color opacity
    #L=len(pos)
    L = pos.keys()
    trace = Scatter(
        x=[], y=[], 
        text=[],
        mode='markers', 
        hoverinfo='text',
        marker=Marker(
            showscale=True,
            # colorscale options
            # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
            # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
            colorscale='Jet',
            reversescale=True,
            color=[], 
            size = [],
            colorbar=dict(thickness=15,
                          title='Node Connections',
                          xanchor='left',
                          titleside='right'),
            line=dict(width=2)))
    
    for k in L:
        trace['x'].append(pos[k][0])
        trace['y'].append(pos[k][1])
        
    
    attrib=dict(name='', text=labels , hoverinfo='text', opacity=opacity) # a dict of Plotly node attributes
    trace=dict(trace, **attrib)# concatenate the dict trace and attrib

    
    for node, adjacencies in enumerate(G.adjacency_list()):
        
        if size_flag == 0:
            trace['marker']['size'].append(len(adjacencies))
        else:
            trace['marker']['size'].append(G.degree(node)+10)
        trace['marker']['color'].append(len(adjacencies))
        #node_info = '# of connections: '+str(len(adjacencies))
        #trace['text'].append(node_info)
    return trace 

def scatter_edges(G, pos, line_color=None, line_width=1):
    trace = Scatter(
        x=[], 
        y=[], 
        text = [],
        line=Line(width=[],color='#888'),
        hoverinfo='text',
        mode='lines')
    for edge in G.edges():
        trace['x'] += [pos[edge[0]][0],pos[edge[1]][0], None]
        trace['y'] += [pos[edge[0]][1],pos[edge[1]][1], None]  
        n1 = edge[0]
        n2 = edge[1]
        trace['line']['width'].append(0.5 + G.get_edge_data(n1,n2).values()[0])
    return trace      