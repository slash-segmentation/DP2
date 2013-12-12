from tree import *

def makeTestTree(value, rootFolderPath):
    rootNode = DataNode('rootNodeName', 'type of node', None, value)
    
    rootNode.addChildren((DataNode('A', 'type of node', None, value),
                         DataNode('B', 'type of node', None, value)))
    
    A = getNode(rootNode, ('A',))
    B = getNode(rootNode, ('B',))
    
    B.addChildren((DataNode('B1', 'type of node', None, value),
                   DataNode('B2', 'type of node', None, value),
                   DataNode('B3', 'type of node', None, value)))
    return PersistentDataTree(rootNode, rootFolderPath)

tree = makeTestTree('testTree1', 'c:\\temp\\')

print tree.rootNode

tree.writeSubtree(('B', 'B1'))
tree.writeSubtree(('B', 'B2'))

print nodeExists(tree.rootNode, ('B',))
print nodeExists(tree.rootNode, ('B_',))


print "testing reading a node from a file and creating parent nodes if needed"
tree2 = PersistentDataTree(DataNode('rootNodeName', 'type of node', None, None), 'c:\\temp\\') 

#readPersistentSubtree(rootNode2, ('C', 'C1'), 'c:\\temp\\'):

tree2.readSubtree(('B', 'B1'))
tree2.readSubtree(('B', 'B2'))

print tree2.rootNode


print "testing reading a node from file that should overwrite an existing node"
tree3 = makeTestTree('testTree3', 'c:\\temp\\')
print tree3.rootNode
print getNode(tree3.rootNode, ('B', 'B2')).object

tree3.readSubtree(('B', 'B2'))
print tree3.rootNode
print getNode(tree3.rootNode, ('B', 'B2')).object


print "testing reading an invalid filename"
try:
    tree2.readSubtree(('X', 'X1'))
except IOError:
    print "file not found"

print "testing getting a node that does exist in the tree"
print tree.getSubtree(('B', 'B1'))

tree4 = PersistentDataTree(DataNode('rootNodeName', 'type of node', None, None), 'c:\\temp\\')
print "testing getting a node that has to be read from file"
print tree4.getSubtree(('B', 'B1'))

print "testing trying to get a node that does not exist (in a file or in memory)"
try:
    tree2.readSubtree(('X', 'X1'))
    print tree2.getSubtree(('B', 'B3'))
except IOError:
    print "file not found"


