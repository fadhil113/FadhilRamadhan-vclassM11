class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
    
    def search(self, target):
        if self.data == target:
            print("Node found")
            return self
        
        if self.left and self.data > target:
            return self.left.search(target)

        if self.right and self.data < target:
            return self.right.search(target)

        print("No Node Found")

    def traversePreorder(self):
        print(self.data)
        if self.left:
            self.left.traversePreorder()
        
        if self.right:
            self.right.traversePreorder()

    def traverseInorder(self):
        if self.left:
            self.left.traverseInorder()
        print(self.data)
        if self.right:
            self.right.traverseInorder()

    def traversePostorder(self):
        if self.left:
            self.left.traversePostorder()
        
        if self.right:
            self.right.traversePostorder()
        
        print(self.data)

    def height(self, h=0):
        leftHeight = self.left.height(h+1) if self.left else h
        rightHeight = self.right.height(h+1) if self.right else h
        return max(leftHeight, rightHeight)

    def getNodeAtDepth(self, depth, nodes=[]):
        if depth==0:
            nodes.append(self)
            return nodes

        if self.left:
            self.left.getNodeAtDepth(depth-1, nodes)
        else:
            nodes.extend([None]*2**(depth-1))

        if self.right:
            self.right.getNodeAtDepth(depth-1, nodes)
        else:
            nodes.extend([None]*2**(depth-1))

        return nodes

    def addNode(self, val):
        if self.data == val:
            return
        
        if val < self.data:
            if self.left is None:
                self.left = Node(val)
                return
            else:
                self.left.addNode(val)
                self.left = self.left.fixImbalance()
        
        if val > self.data:
            if self.right is None:
                self.right = Node(val)
                return
            else:
                self.right.addNode(val)
                self.right = self.right.fixImbalance()

    def findMinNode(self):
        if self.left:
            return self.left.findMinNode()
            
        return self.data

    def delNode(self, target):
        if self.data == target:
            if self.left and self.right:
                #do RTFM
                minNode = self.right.findMinNode()
                self.data = minNode
                self.right = self.right.delNode(minNode)
                return self
            else:
                return self.left or self.right

        if self.right and target > self.data:
            self.right = self.right.delNode(target)
        
        if self.left and target < self.data:
            self.left = self.left.delNode(target)

        return self.fixImbalance()

    def isBalanced(self):
        leftHeight = self.left.height()+1 if self.left else 0
        rightHeight = self.right.height()+1 if self.right else 0
        return abs(leftHeight-rightHeight) < 2

    def unbalanced_indikator(self):
        if not self.isBalanced():
            return str(self.data) + "*"
        
        return str(self.data)

    def leftRightHeightDelta(self):
        leftHeight = self.left.height()+1 if self.left else 0
        rightHeight = self.right.height()+1 if self.right else 0
        return leftHeight-rightHeight

    def fixImbalance(self):
        if self.leftRightHeightDelta() > 1:
            if self.left.leftRightHeightDelta() > 0:
                return rotateRight(self)
            else:
                self.left = rotateLeft(self.left)
                return rotateRight(self)
        elif self.leftRightHeightDelta() < -1:
            if self.right.leftRightHeightDelta() < 0:
                return rotateLeft(self)
            else:
                self.right = rotateRight(self.right)
                return rotateLeft(self)
        
        return self

    def rebalance(self):
        if self.left:
            self.left.rebalance()
            self.left = self.left.fixImbalance()
        if self.right:
            self.right.rebalance()
            self.right = self.right.fixImbalance()

class Tree:
    def __init__(self, root, name=''):
        self.root = root
        self.name = name

    def search(self, target):
        return self.root.search(target)

    def traversePreorder(self):
        self.root.traversePreorder()

    def traverseInorder(self):
        self.root.traverseInorder()

    def traversePostorder(self):
        self.root.traversePostorder()

    def height(self):
        return self.root.height()

    def getNodeAtDepth(self, depth):
        return self.root.getNodeAtDepth(depth)

    def _nodeToChar(self, n, space):
        if n is None:
            return '_' + (' '*space)
        space = space - len(n.unbalanced_indikator())+1
        return n.unbalanced_indikator()+(' '*space)

    def printTree(self, label=''):
        print(self.name + ' ' + label)
        height = self.root.height()
        space = 3
        width = int((2**height-1) * (space+1) +1)

        offset = int((width-1)/2)
        for depth in range(0, height+1):
            if depth>0:
                print(' '*(offset+1) + (' '*(space+2)).join(['/' + (' '*(space-2)) + '\\']*(2**(depth-1))))
            row = self.root.getNodeAtDepth(depth, [])
            print ((' '*offset)+ ''.join([self._nodeToChar(n,space) for n in row]))
            space = offset + 1
            offset = int(offset/2)-1
        print ('')

    def addNode(self, val):
        self.root.addNode(val)
        self.root = self.root.fixImbalance()

    def delNode(self, target):
        self.root = self.root.delNode(target)
        self.root = self.root.fixImbalance()

    def rebalance(self):
        self.root.rebalance()
        self.root = self.root.fixImbalance()

def rotateRight(root):
    pivot = root.left
    reattachNode = pivot.right
    root.left = reattachNode
    pivot.right = root
    return pivot

def rotateLeft(root):
    pivot = root.right
    reattachNode = pivot.left
    root.right = reattachNode
    pivot.left = root
    return pivot

t = Tree(Node(50))
t.addNode(25)
t.addNode(75)
t.addNode(10)
t.addNode(35)
t.addNode(30)
t.addNode(5)
t.addNode(1)
t.printTree()

t.delNode(35)
t.printTree()