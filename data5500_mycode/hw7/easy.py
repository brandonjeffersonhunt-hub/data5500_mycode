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
