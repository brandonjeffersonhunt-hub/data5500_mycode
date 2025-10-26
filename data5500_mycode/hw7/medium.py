def search(root, value):
    if root is None:                    #the base case is if the tree is empty or if the value is found
        return False
    elif root.val == value:                 #whent he value is found
        return True 
    elif value < root.val:
        return search(root.left, value)     #search for smaller values int he tree. I had this one mixed up
    else:
        return search(root.right, value)        #larger values in the tree


class TreeNode:                             #set up the class
    def __init__(self, val):                #give the structure
        self.val = val
        self.left = None
        self.right = None

def insert(root, value):
    if root is None:
        return TreeNode(value)

    elif value < root.val:                          #if the value is larger than the root go to the left
        root.left = insert(root.left, value)

    elif value > root.val:
        root.right = insert(root.right, value)      #if it is smaller than the root go rught

    return root 

root = TreeNode(8)
root = insert(root, 3)
root = insert(root, 8)
root = insert(root, 9)
root = insert(root, 1)

print(search(root, 6))
print(search(root, 3))
print(search(root, 10))
print(search(root, 9))


#I put this first draft into chat and asked why it didnt work
'''
def search(root, value):
    if root is None:                    #the base case is if the tree is empty or if the value is found
        return False
    elif root.val == value:
        return True
    elif root > value:
        return search(root.right, value)
    else:
        return search(root.left, value)


class TreeNode:                             #set up the class
    def __init__(self, val):                #give the structure
        self.val = val
        self.left = None
        self.right = None

def insert(root, value):
    if root is None:
        return TreeNode(value)

    elif value < root.val:                          #if the value is larger than the root go to the left
        root.left = insert(root.left, value)

    elif value > root.val:
        root.right = insert(root.right, value)      #if it is smaller than the root go rught

    return root 

root = TreeNode(8)
root = insert(root, 3)
root = insert(root, 8)
root = insert(root, 9)
root = insert(root, 1)

print(search(root, 6))
print(search(root, 3))
print(search(root, 10))
print(search(root, 9))
'''

