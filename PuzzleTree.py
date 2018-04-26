GOAL_STATE = [[1,2,3],[4,5,6],[7,8,0]]
AVERAGE = 26.9
class Node:
    def __init__(self, data=None, val=None):
        self.val =  Node.getVal(data) if not val else val
        self.children = []
        self.data = data
        self.parent = None
    
    def addChild(self, child):
        if type(child) is type(self):
            child.setParent(self)
            self.children.append(child)
        else:
            print("only append nodes")    
    
    def setParent(self, parent):
        if type(parent) is type(self):
            self.parent = parent
        else:
            print("parent is not a node")
    
    def getParent(self):
        if self.parent:
            return self.parent
        else:
            return None
        
    def countChildren(self):
        if not self.children:
            return 0
        else:
            return len(self.children)
        
    def getChild(self, index):
        if index<self.countChildren():
            return self.children[index]
        else:
            return "child "+str(index)+" does not exist"
    
    def __str__(self):
        return "{} \n {}".format(self.val, self.data)
    
    def get_rev_children(self):
        children = self.children
        children.reverse()
        return children   

    @classmethod
    def getVal(cls,data):
        #manhattan distance
        val = 0 
        for row in range(len(data)):
            for col in range(len(data[row])):
                tile = data[row][col]
                if tile ==0:
                    continue
                x0 = (tile-1)//3
                y0 = (tile-1)%3
                val += abs(row-x0) + abs(col-y0)  
                
        return val
    
class Tree:
    #for 8 puzzle
    
    def __init__(self, data= None):
        self.root = Node(data=data)
        
 
    def __str__(self):
        buf, out = [self.root], []
        count = 0 
        while buf:
            count +=1
            kids = []
            group = []
            for node in buf:
                group.append(node.val)
                for index in range(node.countChildren()):
                    child = node.getChild(index)
                    kids.append(child)
            output = self.niceOutPut(len(group))
            out.append(output.format(d=group))
            out.append(" generation {}".format(count))
            buf = kids
        return "\n".join(out)
    
    @staticmethod        
    def niceOutPut(length):
        output = ""
        for n in range(length):
            output += " _{d["+str(n)+"]}_ "
        return output
    
    
        