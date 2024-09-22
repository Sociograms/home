import pandas as pd

nodes = pd.read_excel('Sociograms.xlsx', sheet_name="Nodes")
edges = pd.read_excel('Sociograms.xlsx', sheet_name="Edges")
quotes = pd.read_excel('Sociograms.xlsx', sheet_name="Quotes")
person = pd.read_excel('Sociograms.xlsx', sheet_name="Persons")

# set level by distance from 'Me'

# edges
edgecols = ['source', 'target']
edges.drop(['id','relationship','platform'],axis=1,inplace=True)
edges.drop_duplicates(subset=edgecols, keep="first",inplace=True,ignore_index=True)
edgeToMe = list(edges[edges['source']=="Me"]['target'])
truncatedEdges = list(edges[edges['source'].isin(edgeToMe)]['target'].unique())
nextlevelEdges = list(edges[edges['source'].isin(truncatedEdges)]['target'].unique())
nextnextlevelEdges = list(edges[edges['source'].isin(nextlevelEdges)]['target'].unique())
print(edgeToMe)
print(truncatedEdges)
print(nextlevelEdges)
print("nodes with next level Edges as source - think about dropping them")
print(nextnextlevelEdges)
print("are there another level again? - think about dropping them")
print(list(edges[edges['source'].isin(nextnextlevelEdges)]['target'].unique()))

# fix up data with edge from "Me" to "TikTok"
d = {'source': ['Me'],'target': ['TikTok']}
newEdge =pd.DataFrame(data=d)
edges = pd.concat([edges[edgecols],newEdge],axis=0).reset_index()

# testing, just drop the outer node links (so they'll be orphans)
#edges[~edges['source'].isin(nextlevelEdges)][edgecols].to_json("edges.json",indent=2, mode='w',orient='index')

edges[edgecols].to_json("edges.json",indent=2, mode='w',orient='index')

# nodes
nodes['label'] = nodes['name']
levels_map = {'Image': 4, 'Person': 1, 'Platform' : 2, 'Recipients': 3, 'Video': 4}
nodes['level'] = nodes['type'].map(levels_map)

color_map = {
    'Image': '#8dd3c7',
    'Person': '#fb8072',
    'Platform': '#8da0cb',
    'Recipients': '#ffffb3',
    'Video': '#8dd3c7'}
nodes['color'] = nodes['type'].map(color_map)
nodes.set_index('name', inplace=True)
nodes['name'] = nodes['label']

nodecols = ['name','type','label','level','color']

# just save a simple view of the nodes
#nodes[nodes['level']<3][nodecols].to_json("nodes.json",indent=2, mode='w',orient='index')

# save all the nodes
nodes[nodecols].to_json("nodes.json",indent=2, mode='w',orient='index')

# save the quotes
quotecols = ['Node', 'Quote', 'File']
quotes[quotecols].to_json("quotes.json",indent=2,mode='w',orient='index')



