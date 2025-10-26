'''
when deleting a node in a binary search tree, one must follow important rules. This is because you have to maintain the structure
of the tree after the deletion. That structure being that for every node values on the left must be smaller and those on the
right must be larger. If a node has no children, you can just delete the target value without consequence. If the node has a
single child, you delete the target value and move that single child up to take its place. if a node has two children you must
look for the smallest value in the right subtree of the target value. That value will be moved up to take the place of the target
value you wish to delete.

Some potential edge cases or challenges might include duplicates. The easiest way to handle this is to just prevent the
insertion of duplicates. Another would be if you were trying to delete the root node. To combat this your code should return
the root at the end always.
'''
print('Hello World')