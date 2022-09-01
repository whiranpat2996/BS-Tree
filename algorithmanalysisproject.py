from math import ceil, floor
from random import randint
import random
import sys, getopt


# The rightmost branch of a Binomial Search Tree (now to be refered to BS-Tree) is a linked list. This also helps on merging.
class Node:
    def __init__(node, key):
        node.tree = None
        node.nextNode = None
        node.nodeCount = 1
        node.key = key

    def display(node):
        lines, *_ = node._display_aux()
        for line in lines:
            print(line)

    def _display_aux(node):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if node.nextNode is None and node.tree is None:
            line = '%s' % node.key
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if node.nextNode is None:
            lines, n, p, x = node.tree._display_aux()
            s = '%s' % node.key
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if node.tree is None:
            lines, n, p, x = node.nextNode._display_aux()
            s = '%s' % node.key
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = node.tree._display_aux()
        right, m, q, y = node.nextNode._display_aux()
        s = '%s' % node.key
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, min(p, q) + 2, n + u // 2
        
# The root of a Binary Search Tree (now to be refered to as a BST). These are the left branches of the linked list.
class Root:
    def  __init__(root, key):
        root.left = None
        root.right = None
        root.key = key
    
    def display(root):
        lines, *_ = root._display_aux()
        for line in lines:
            print(line)

    def _display_aux(root):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if root.right is None and root.left is None:
            line = '%s' % root.key
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if root.right is None:
            lines, n, p, x = root.left._display_aux()
            s = '%s' % root.key
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if root.left is None:
            lines, n, p, x = root.right._display_aux()
            s = '%s' % root.key
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = root.left._display_aux()
        right, m, q, y = root.right._display_aux()
        s = '%s' % root.key
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, min(p, q) + 2, n + u // 2



# Inserts a node for the right most branch of a BS-Tree.
def insertNode(node1, node2):
    if node1.nextNode is None:
        node1.nextNode = node2
        node1.nodeCount += 1
    else:
        insertNode(node1.nextNode, node2)

# Starts a BST for the right most branch of a BS-Tree.
def startTree(node, key):
    if node is None:
        node = Node(key)
    elif node.tree is None:
        node.tree = Root(key)
    else:
        insertBST(node.tree, key)

# Inserts a node at the next open spot of a BST.
def insertBST(root, key):
    if root is None:
        root = Root(key)
    else:
        if key < root.key:
            if root.left is None:
                root.left = Root(key)
            elif root.left is not None and root.right is None:
                rightrotate(root, key)
            else:
                insertBST(root.left,key)
        elif key > root.key:
            if root.right is None:
                root.right = Root(key)
            elif root.right is not None and root.left is None:
                leftrotate(root, key)
            else:
                insertBST(root.right,key)
        
def leftrotate(root, key):
    temp = Root(root.key)
    root.left = temp
    root.key = key

def rightrotate(root, key):
    temp = Root(root.key)
    root.right = temp
    root.key = key


# Searches for a particular node.
def search(root, key):
    if root is None:
        print("root not found")
        return root

    if root.key == key:
        print("key found")
        print(root.key)
        return root
    
    if root.key < key:
        return search(root.right,key)

    return search(root.left, key)

# Prints a BS-Tree.
def printBSTree(Node):
    if Node is None:
        pass
    print(Node.key)
    if(Node.tree is not None):
        printBST(Node.tree)
    if(Node.nextNode is not None):    
        printBSTree(Node.nextNode)
    else:
        pass

# Prints out all of the nodes of a BST.
def printBST(root):
    if root.left:
        printBST(root.left)
    print(root.key),
    if root.right:
        printBST(root.right)

# Converts a BST to an array for processing.
def arrBST(root, arr):
    if root is None:
        return arr
    if root.left:
        arrBST(root.left, arr)
    arr.append(root.key),
    if root.right:
        arrBST(root.right, arr)

# Converts a BS-Tree to an array for processing.
def arrBSTree(Node):
    arr = []
    if Node is None:
        pass
    arr.append(Node.key)
    arrBST(Node.tree, arr)
    if(Node.nextNode is not None):    
        arrBSTree(Node.nextNode)
    else:
        pass
    return arr

# Populates a tree.
def populate(arr):
    for i in range(0, len(arr)):
        arr[i] = random.randint(0, 10000)
    return arr

# Shuffles the tree.
def rand(arr):
    # Start from the last element and swap one by one. We don't
    # need to run for the first element that's why i > 0
    for i in range(1, len(arr)):
        # Pick a random index from 0 to i
        j = randint(0,i)
        # Swap arr[i] with the element at random index
        arr[i],arr[j] = arr[j],arr[i]
    return arr

# Merges two subarrays of arr. 
def merge(arr, l, m, r, cnt):
    n1 = m - l + 1
    n2 = r - m

    # Create temporary arrays.
    L = [0] * (n1)
    R = [0] * (n2)

    # Copy data from main array to the temporary arrays.
    for i in range(0, n1):
        L[i] = arr[l + i]

    for j in range(0, n2):
        R[j] = arr[m + 1 + j]

    # Merge the temporary arrays back into the main array
    i = 0
    j = 0
    k = l
    
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        cnt += 1
        k += 1

    # Copy the remaining elements of the L array, if there are any.
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    
    
    # Copy the remaining elements of the R array, if there are any.
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1
        
    return cnt

# Standard Mergesort.
# Has a worst case of O(n*lgn).
def mergesort(node, arr, l, r, res):
    cnt = 0
    x = 0
    if l < r:
        m = l + (r - l)//2

        mergesort(node, arr, l, m, 1)
        mergesort(node, arr, m+1, r, 1)
        cnt = merge(arr, l, m, r, cnt)

    if res == 0:
        print("Number of comparisons:" + str(cnt))
        return res

    return arr

# Post-sorting operation. Converts an array to a BS-Tree.
def postsort(arr):
    newNode = Node(min(arr))
    arr.remove(min(arr))
    for x in range(1, len(arr)):
        startTree(newNode, arr[x])
    return newNode

# The algorithm in question. 
# Apparently has a worst case of O(2^(k+1)).
def UBmergesort(node1, node2, res):
    if(node1.nodeCount == node2.nodeCount) and (node1.nodeCount or node2.nodeCount == 1):
        return couple(node1, node2, res)
    else:
        n1 = arrBSTree(node1)
        n2 = arrBSTree(node2)
        newNode1 = Node(min(n1))
        newNode2 = Node(min(n2))
        insertNode(newNode1, newNode2)
        n1.remove(min(n1))
        n2.remove(min(n2))
        cnt = UBmerge(newNode1, newNode2, n1, n2)
        if res == 0:
            print("Number of comparisons:" + str(cnt))
            return res
        return newNode1

# The unbalanced merging.
def UBmerge(node1, node2, arr1, arr2):
    x = 0
    h1 = len(arr1)
    h2 = len(arr2)
    finarr = arr1.extend(arr2)
    
    for x in range(h1):
        startTree(node1, finarr[floor(h1/2)])
        finarr.remove(finarr[floor(h1/2)])
        cnt += 1

    for x in range(h2):
        startTree(node2, finarr[floor(h2/2)])
        finarr.remove(finarr[floor(h2/2)])
        cnt += 1
    
    return cnt

# The special procedure listed out in the paper.
# Converts two BS-Trees into arrays and then merge them into one larger BS-Tree.
def couple(node1, node2, res):
    n1 = arrBSTree(node1)
    n2 = arrBSTree(node2)
    cnt = 0
    n1.extend(n2)
    newNode = Node(min(n1))
    n1.remove(min(n1))

    while len(n1) != 0:
        startTree(newNode, n1[floor(len(n1)/2)])
        n1.remove(n1[floor(len(n1)/2)])
        cnt += 1
    
    if res == 0:
        print("Number of comparisons:" + str(cnt))
        return res

    return newNode

# Just a quick set of code to populate and shuffle data.
def test(n):
    arr = [None] * n
    arr = populate(arr)
    arr = rand(arr)
    return arr

# Driver Code.
results = [None] * 6
ubtest1 = test(5)
ubtest1pt2 = test(5)
test1 = test(10)
test2 = test(100)
ubtest2 = test(50)
ubtest2pt2 = test(50)
test3 = test(1000)
ubtest3 = test(500)
ubtest3pt2 = test(500)

node1 = postsort(test1)
node2 = postsort(test2)
node3 = postsort(test3)
node4 = postsort(ubtest1)
node5 = postsort(ubtest1pt2)
node6 = postsort(ubtest2)
node7 = postsort(ubtest2pt2)
node8 = postsort(ubtest3)
node9 = postsort(ubtest3pt2)

print("Input:")
print(test1)
nres1 = mergesort(node1, test1, 0, len(test1) - 1, 0)
print("Sorted Input:")
print(mergesort(node1, test1, 0, len(test1) - 1, 1))
nres2 = mergesort(node2, test2, 0, len(test2) - 1, 0)
nres3 = mergesort(node3, test3, 0, len(test3) - 1, 0)

print("Input:")
print(ubtest1 + ubtest1pt2)
ubres1 = UBmergesort(node4, node5, 0)
print("Sorted Input:")
print(arrBSTree(UBmergesort(node4, node5, 1)))
ubres2 = UBmergesort(node6, node7, 0)
ubres3 = UBmergesort(node8, node9, 0)
