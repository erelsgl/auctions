#!python3

"""
A tree in which each node is an agent category,
and each path from root to leaf is a recipe.
"""


"""
For more information on tree implementations in Python, see here:
https://stackoverflow.com/q/2358045/827927
"""

from anytree import Node, NodeMixin, RenderTree
from agents import AgentCategory
import logging, sys

logger = logging.getLogger(__name__)

class Tree (NodeMixin):
    def __init__(self, category, parent=None, children=None):
        self.category = category
        if isinstance(category, AgentCategory):
            self.name = category.name
        else:
            self.name = category
        self.parent = parent
        if children is not None:
            self.children = children


    def paths_to_leaf(self, prefix = []):
        """
        Get all paths from this node to a leaf.

        >>> tree = Tree(1)
        >>> tree.paths_to_leaf()
        [[1]]

        >>> tree = Tree(1, children = [Tree(2), Tree(3)])
        >>> tree.paths_to_leaf()
        [[1, 2], [1, 3]]

        >>> tree = Tree(1, children = [Tree(2), Tree(3, children=[Tree(4), Tree(5)])])
        >>> tree.paths_to_leaf()
        [[1, 2], [1, 3, 4], [1, 3, 5]]
        """
        if len(self.children)==0:
            paths = [prefix + [self.name]]
        else:
            paths = []
            for child in self.children:
                paths_from_child_to_leaf = child.paths_to_leaf(prefix = prefix + [self.name])
                paths += paths_from_child_to_leaf
        return paths

    def combined_values(self) -> int:
        """
        >>> buyer = AgentCategory("buyer", [60,40,20,-30])
        >>> seller = AgentCategory("seller", [-10,-30,-50])
        >>> producerA = AgentCategory("producerA", [-1, -3, -5])
        >>> producerB = AgentCategory("producerB", [-2, -4, -6])

        >>> tree = Tree(buyer)
        >>> tree.combined_values()
        [60, 40, 20, -30]

        >>> tree = Tree(buyer, children=[Tree(seller)])
        >>> tree.combined_values()
        [50, 10, -30]

        >>> tree = Tree(buyer, children=[Tree(seller)])
        >>> tree.combined_values()
        [50, 10, -30]

        >>> tree = Tree(buyer, children=[Tree(producerA), Tree(producerB)])
        >>> tree.combined_values()
        [59, 38, 17, -34]

        >>> tree = Tree(buyer, children=[Tree(seller), Tree(producerA, children=[Tree(producerB)])])
        >>> tree.combined_values()
        [57, 33, 10, -41]
        """
        self_values = self.category.values
        if len(self.children) == 0:
            values = self_values
        else:
            children_values = sum([child.combined_values() for child in self.children], [])
            children_values.sort(reverse=True)
            values = [a+b for (a,b) in zip(self_values, children_values)]
        return values

    def maximum_GFT(self) -> int:
        """
        Calculate the maximum possible GFT for the given category tree.

        >>> buyer = AgentCategory("buyer", [60,40,20,-30])
        >>> seller = AgentCategory("seller", [-10,-30,-50])
        >>> producerA = AgentCategory("producerA", [-1, -3, -5])
        >>> producerB = AgentCategory("producerB", [-2, -4, -6])

        >>> tree = Tree(buyer)
        >>> tree.maximum_GFT()
        120

        >>> tree = Tree(buyer, children=[Tree(seller)])
        >>> tree.maximum_GFT()
        60

        >>> tree = Tree(buyer, children=[Tree(producerA), Tree(producerB)])
        >>> tree.maximum_GFT()
        114

        >>> tree = Tree(buyer, children=[Tree(seller), Tree(producerA, children=[Tree(producerB)])])
        >>> tree.maximum_GFT()
        100
        """
        return sum([v for v in self.combined_values() if v > 0])






if __name__=="__main__":
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.DEBUG)

    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("doctest: {} failures, {} tests".format(failures,tests))

    buyer = AgentCategory("buyer", [17, 14, 13, 9, 6])
    seller = AgentCategory("seller", [-1, -3, -4, -5, -8, -10])
    producerA = AgentCategory("producerA", [-1, -3, -5])
    producerB = AgentCategory("producerB", [-1, -4, -6])

    tree = Tree(buyer,
                children=[Tree(seller,
                               children=None),
                          Tree(producerA,
                               children=[Tree(producerB)])])

    for pre, fill, node in RenderTree(tree):
        print("{}{}".format(pre,node.name))

    print(tree.paths_to_leaf())

