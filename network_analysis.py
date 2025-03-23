import networkx as nx
import matplotlib.pyplot as plt
import sys

def create_interaction_graph(df):
    G = nx.Graph()
    df = df[df['user'] != 'notification']
    user_interactions = df['user'].value_counts().to_dict()
    for user, count in user_interactions.items():
        G.add_node(user, size=count)
        
    for _, row in df.iterrows():
        G.add_edge(row['user'], "Group", weight=1)
        
    for node in G.nodes:
        node_data = G.nodes.get(node, {})
        if 'size' not in node_data:
            G.nodes[node]['size'] = 1  
    return G


def plot_graph(G, output_path=None):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42) 

    node_sizes = [G.nodes[n].get('size', 1) * 50 for n in G.nodes]

    nx.draw(
        G, pos, with_labels=True, node_color='lightblue', edge_color='gray',
        node_size=node_sizes, alpha=0.8
    )
    
    plt.title("WhatsApp Group Interaction Network")

    if output_path:
        plt.savefig(output_path, dpi=300)
        print(f"Graph saved as {output_path}")
    else:
        plt.show()
