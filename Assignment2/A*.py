

class SearchNode:

    def __init__(self,pos):
        
        self.pos = pos

        self.g = float('inf')
        self.h = None

        self.solution = False
        self.parent = None
        self.children = []



    def f(self):
        return self.g + self.h     


def A_star(n0):
    closed = []
    open = [n0]

    while True: #Agenda loop
        if not open:  return False #OPEN is empty

        current_node = open.pop()
        closed.append(current_node)

        if current_node.solution : return True # solution is found

        generate_all_successors(current_node, map)

        for child in current_node.children:


            if child not in open and child not in closed:
                attach_and_eval(child,current_node)
                open.append(child)
                open.sort(key = lambda x: x.f, reverse = True)
            elif current_node.g + arc_cost(current_node,child) < child.g:
                attach_and_eval(child,current_node)
                if child in closed : propagate_path_improvements(child)






    pass

def arc_cost(parent,child):
    return 1

def generate_all_successors(parent,map):
    c1 = SearchNode([parent.pos[0] + 1,parent.pos[1]])
    if map.get_cell_value(c1.pos) != -1:
        parent.children.append(c1) 
    c2 = SearchNode([parent.pos[0] -1, parent.pos[1]])
    if map.get_cell_value(c1.pos) != -1:
        parent.children.append(c1)
    c3 = SearchNode([parent.pos[0],parent.pos[1] +1 ])
    if map.get_cell_value(c1.pos) != -1:
        parent.children.append(c1)
    c4 = SearchNode([parent.pos[0],parent.pos[1] -1 ])
    if map.get_cell_value(c1.pos) != -1:
        parent.children.append(c1)




    pass

def attach_and_eval(child,parent):
    child.parent = parent
    child.g = parent.g + arc_cost(parent,child)
    child.h  = manhatten_distance(child,map)
    pass

def propagate_path_improvements(parent):
    for child in parent.children:
        if parent.g + arc_cost(parent, child):
            child.parent = parent
            child.g = parent.g + arc_cost(parent,child)
            child.f = child.g + child.h
            propagate_path_improvements(child)

def manhatten_distance(node,map):
    goal_pos = map.get_goal_pos()
    return abs(goal_pos[0] - node.x) + abs(goal_pos[1]-node.y)






