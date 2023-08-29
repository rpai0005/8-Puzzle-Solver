#Purpose: Efficient and Optimal Implementation of a Queue Data Structure
class Queue:
    def __init__(self):
        self._head = 0                                  #Head holds the index value of the first element of the list
        self._L = []                                    #list holding the queue elements
        self._S = set()                                 #set holding the elements/items in the queue

    def enqueue(self, item):                            #Purpose: adds item to end of queue
        self._L.append(item)                            #Adds item to end of List
        self._S.add(item)                               #Adds the element to the set

    def dequeue(self):                                  #Purpose: returns the first element of the queue
        item = self._L[self._head]                      #item holds first element of the queue
        self._head += 1                                 #moves the head pointer to the next element of the list (the new first ele)
        self._S.remove(item)                            #removes the item var in the set (O(1) because order doesnt matter in a set)
        return item                                     #returns the element that was in the first position of the queue

    def __len__(self):                                  #Purpose: returns the length of the queue
        return len(self._L) - self._head                #returns the current length of the list 

    def isempty(self):                                  #Purpose: determines if the queue has no elements 
        return len(self._L) - self._head == 0           #returns true if there are no elements in L, false otherwise

    def in_queue(self, item):                           #Purpose: determines if a certain item in currently in the queue
        return item in self._S                          #returns True if item is in the set of items -- O(1) for a set structure

#----------------------------------------------------------------------------------------------------------------------------------------------
#Purpose: Implements a graph for the specific case of an 8 Puzzle
class PuzzleGraph:
    def __init__(self, V, E):                           #Purpose: creates an initial graph with any given vertices and edges
        self._V = set()                                 #Holds the vertices 
        self._nbrs = dict()                             #Holds vertex and children of the vertex for all vertices as a dictionary
        for v in V:                                     #Adds all inputted vertices to the graph (which are each puzzle states)
            self.addvertex(v)
        for u, v in E:                                  #Adds all inputted edges to the graph if there are any
            self.addedge(u, v)

    def vertices(self):                                 #Purpose: Returns an iterator over all the vertices in the graph
        return iter(self._V)

    def edges(self):                                    #Purpose: Returns an iterator over all edges in the graph 
        for u in self._V:
            for v in self.nbrs(u):                      #Goes through each vertex in the dictionary
                yield(u, v)                             #Outputs (vertex, child)

    def addvertex(self, v):                             #Purpose: Adds a vertex to the graph
        if not(v in self._V):                           #Checks if the vertex is already in the graph
            self._V.add(v)                              #If not, the vertex is added to the vertex set
            self._nbrs[v] = set()                       #The vertex is addes to the dictionary, a child set is created as the value

    def addedge(self, u, v):                            #Purpose: Adds an edge to the graph (a connection btw two nodes)
        self._nbrs[u].add(v)                            #Finds the vertex in the dict, and adds the connected node to the nbrs set

    def isValidSwap(self, direc, v):                    #Purpose: Checks if the desireds swap is valid based on where the space is in the puz
        ind = v.index(0)                                #Finds the posiiton of the space in the inputted puzzle
        size = 9                                        #fixed size of an 8 puzzle

        if(direc == "right"):                                      #If inputted direction is right
            if(((ind + 1) < size) and (((ind + 1) % 3) != 0)):     #checks if space is on right boundery or space will go out of bounds
                return True
        elif(direc == "left"):                                     #If inputted direction is left
            if(((ind - 1) >= 0) and ((ind % 3) != 0)):             #checks if space is on left boundery or if space will go out of bounds
                return True                                     
        elif(direc == "up"):                                       #If inputted direction is up
            if((ind - 3) >= 0):                                    #checks if space is on the top boundery
                return True 
        elif(direc == "down"):                                     #If inputted direction is down
            if((ind + 3) < size):                                  #checks if space is on bottom boundery
                return True
        
        return False                                               #returns false otherwise

    def explore(self, v):                               #Purpose: moves the space in all valid directions, adds them to the nbrs of v
        space = v.index(0)                              #Finds the index of the space in the current v puzzle

        if(self.isValidSwap("right", v)):               #Create child of a swap to the right if it is valid
            puz1 = list(v)                              #creates a copy of the puzzle v into a list to have ability to swap 
            temp = puz1[space]                          #Start of swap algorithm
            puz1[space] = puz1[space + 1]
            puz1[space + 1] = temp                      #End of swap algorithm

            puz1 = tuple(puz1)                          #Makes the puzzle into a tuple

            self.addedge(v, puz1)                       #Adds the child puzzle to nbrs by adding it to the edges of v

        if(self.isValidSwap("left", v)):                #Create child of a swap to the left if it is valid
            puz2 = list(v)                              #creates a copy of the puzzle v into a list to have ability to swap
            
            temp = puz2[space]                          #start of swap algorithm
            puz2[space] = puz2[space - 1]
            puz2[space - 1] = temp                      #end of swap algorithm
            
            puz2 = tuple(puz2)                          #Makes puzzle into a tuple

            self.addedge(v, puz2)                       #adds the puzzle to the edges of v

        if(self.isValidSwap("up", v)):                  #Create child of a swap to the up if it is valid
            puz3 = list(v)                              #creates a copy of the puzzle v into a list to have ability to swap
            
            temp = puz3[space]                          #start of swap algorithm 
            puz3[space] = puz3[space - 3]               #minus 3 in 1D list is equiv to moving down in 2D array
            puz3[space - 3] = temp                      #End of swap aglorthm

            puz3 = tuple(puz3)                          #Makes puzzle into a tuple

            self.addedge(v, puz3)                       #Adds the puzzle as a edge of v in nbrs

        if(self.isValidSwap("down", v)):                #Create child of a swap to the down if it is valid
            puz4 = list(v)                              #creates a copy of the puzzle v into a list to have the ability to swap
            
            temp = puz4[space]                          #start of swap algorithm
            puz4[space] = puz4[space + 3]               #plus 3 in 1D array is equiv to moving down in 2D array
            puz4[space + 3] = temp                      #end of swap algorithm

            puz4 = tuple(puz4)                          #Makes puzzle into a tuple

            self.addedge(v, puz4)                       #Adds the puzzle as a neighbor of the current vertex v

    def displaystate(self, result):                     #Purpose: displays the 8 puzzle as a 2D matrix, used when printing the solution
        print("******************")                     

        for i in range(0, 3):                           #prints the first row
            print("%4d" % result[i], end = ' ')
        print()

        for i in range(3, 6):                           #prints the second row
            print("%4d" % result[i], end = ' ')
        print()

        for i in range(6, 9):                           #prints the third row
            print("%4d" % result[i], end = ' ')
        print()
        print("******************")                     #end of the printing

    def nbrs(self, v):                                  #Purpose: creates all children of v, returns iterator over those neighbors
        self.addvertex(v)                               #adds the current vertex to the puzzle graph
        self.explore(v)                                 #creates all children of v by caling moveSpace
        return iter(self._nbrs[v])                      #returns iterator over the created children
    
    def bfs(self, v):                                   #Purpose: implements the BFS algorithm on the first inputted puzzle state
            tree = {}                                   #creates the ongoing tree being made for the spacific intiial state -- dictionary

            end = [i + 1 for i in range(8)]             #intiializes the end state (a constant state no matter the input)
            end.append(0)
            end = tuple(end)                            #makes the end state a tuple

            tovisit = Queue()                           #creates a queue of all nodes that still need to be visisted and checked
            tovisit.enqueue((None, v))                  #adds element to the queue, form of input: (child, parent)
            while tovisit:                              #while keeps going until the to visit queue is empty (should never happen)
                a, b = tovisit.dequeue()                #takes first element off of the queue, a = child, b = parent
                if b not in tree:                       #checks if b is already a vertex in the tree (to avoid infinite loops)
                    tree[b] = a                         #makes child the key, and parent the value to trace back the path later

                    if b == end:                        #checks if the current state = end state, quits bfs if this is true
                        return tree
                    for n in self.nbrs(b):                  #creates all children of current state by calling nbrs function
                        if not tovisit.in_queue((b, n)):    #checks if the (child, parent) is already in the to visit set
                            tovisit.enqueue((b, n))         #if not, adds the tuple to the queue
            return tree                                     #returns the tree if not returned before (which is should have)

    def solve(self, u):                                 #Purpose: Calls bfs and traces the path from end to beginning
        tree = self.bfs(u)                              #calls bfs function to get the tree that was created

        end = [i + 1 for i in range(8)]                 #initializes the end state of the puzzle
        end.append(0)
        end = tuple(end)                                #makes the end state a tuple

        v = end
        result = [v]                                    #adds the end state to result, which will hold the path from end to beginning
        edgecount = 0                                   #Counts the number of edges (number of moves)

        while not(v == u):                              #will keep adding until the current element 
            edgecount += 1                              #add one the the edgecount (number of moves)
            v = tree[v]                                 #v now holds the parent of the current v
            result.append(v)                            #adds the parent to the result list
        result.reverse()                                #reverses the order of result to go from initial to end state
        print("Solution: ")                             
        for i in range(len(result)):                    #for loop to print each of the states from beginning to end
            print("Step", i, ":")
            self.displaystate(result[i])                #calls display state to display the current puzzle state

#-----------------------------------------------------------------------------------------------------------------------------------------------
def validInput(input):                                  #Purpose: determines if the current puzzle is a valid input
    s = set(input)                                      #makes the input list a set (more optimal)
    compareList = {0, 1, 2, 3, 4, 5, 6, 7, 8}           #all valid numbers in an 8 puzzle

    if (len(s) != 9):                                   #checks if the length of the puzzle is not
        return False
    
    for value in compareList:                           #Checks if there are any doubles of a number
        if not(value in compareList):
            return False
    
    for val in s:                                       #checks if each value in the input is in the range of 0-8
        if (val < 0) or (val > 8):
            return False
    
    return True
    
def puzzle(startList):                                  #Purpose: starts the puzzle graph for an inputted initial state

    validity = validInput(startList)                    #checks if the input is valid
    if not(validity):
        print("This is not a valid 8 puzzle input!")
        return validity

    start = tuple(startList)                            #makes the input list a tuple
    
    V = set()                                           #creates the vertex set
    V.add(start)                                        #adds the intiial state to the vertex set
    E = set()                                           #creates an empty edge set
    pgraph = PuzzleGraph(V, E)                          #creates a puzzle graph with set V and E

    pgraph.solve(start)                                 #solves the puzzle graph 

#Testing Section ----------------------------------------------------------------------
test = [1, 0, 7, 2, 4, 8, 6, 5, 3] #25 Moves

puzzle(test)   

#test = [0, 1, 2, 3, 4, 5, 6, 7, 8] #0 moves - Edge Case
#test = [0, 1, 3, 4, 8, 5, 2, 7, 6] #10 Moves
#test = [1, 3, 5, 4, 7, 8, 2, 0, 6] #15 Moves
#test = [1, 7, 8, 2, 4, 3, 0, 6, 5] #20 Moves
#test = [0, 1, 3, 6, 2, 5, 7, 8, 6] #Case with a double number (6)
#test = [0, 1, 3, 4, 2, 5, 7, 9, 6] #Case with out of bounds number
#test = [0, 1, 3, 4, 2, 5, 7, 8] #Case with less elements than expected
#test = [8, 7, 6, 5, 4, 3, 2, 1, 0] #Goal Case
#test = [0, 1, 3, 4, 2, 5, 7, 8, 6] #4 Moves