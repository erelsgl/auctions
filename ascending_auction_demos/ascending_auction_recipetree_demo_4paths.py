#!python3

"""
Demonstration of a multiple-clock strongly-budget-balanced ascending auction
for a multi-lateral market with a recipe tree. Demos with 4 paths.

Author: Erel Segal-Halevi
Since:  2020-08
"""

import sys, os; sys.path.insert(0, os.path.abspath('..'))


from markets import Market
from agents import AgentCategory
import ascending_auction_recipetree_protocol
from ascending_auction_recipetree_protocol import budget_balanced_ascending_auction
import prices

import logging
ascending_auction_recipetree_protocol.logger.setLevel(logging.INFO)
prices.logger.setLevel(logging.INFO)

print("\n\n###### TEST MULTI RECIPE AUCTION - 4 PATHS")

# market = Market([
#     AgentCategory("C0", [400, 300, 200, 100]),
#     AgentCategory("C1", [-1, -11]),
#     AgentCategory("C2", [-2, -22]),
#     AgentCategory("C3", [-3, -33]),
#     AgentCategory("C4", [-4, -44]),
#     AgentCategory("C5", [-5, -55]),
#     AgentCategory("C6", [-6, -66]),
# ])

market = Market([
    AgentCategory("C0", [400, 300, 200, 100]),
    AgentCategory("C1", [-1, -11]),
    AgentCategory("C2", [-2]),
    AgentCategory("C3", [-3]),
    AgentCategory("C4", [-4, -44]),
    AgentCategory("C5", [-5]),
    AgentCategory("C6", [-6]),
])


recipes_4paths = [0, [1, [2, None, 3, None], 4, [5, None, 6, None]]]
# The recipes are:
#     1,1,1,0,0,0,0   [C0, C1, C2]
#     1,1,0,1,0,0,0   [C0, C1, C3]
#     1,0,0,0,1,1,0   [C0, C4, C5]
#     1,0,0,0,1,0,1   [C0, C4, C6]

print(budget_balanced_ascending_auction(market, recipes_4paths))
