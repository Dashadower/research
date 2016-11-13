#function search() which returns a list of list of the possible ways from node A to node B in a 3x8 grid.

def GenerateCyclicGraph():
    Graph = {}
    width = 6
    height = 3
    for w in range(0,width+1):
        for h in range(0,height+1):
            if w != 6: RightPath = (h,w+1)
            else: RightPath = None
            if h != 2: DownPath = (h+1,w)
            else: DownPath = None
            Graph["("+str(h)+", "+str(w)+")"] = [RightPath,DownPath]
    return Graph

def search(goal,graph):
    paths = [[],[],[]]
    for h in range(0,3):
        for w in range(0,7):
            table = []
            findpath([(0,0)],(h,w), table, graph)
            paths[h].append(len(table))
    return paths

def findpath(pos,goal, pathlist, graph):
    location = pos[-1]

    if location == goal: pathlist.append(pos)
    for items in graph[str(location)]:
        if items == None: pass
        elif items not in pos:
            findpath(pos+[items],goal,pathlist,graph)