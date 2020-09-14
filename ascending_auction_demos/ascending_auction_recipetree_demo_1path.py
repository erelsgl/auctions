#!python3

"""
Demonstration of a multiple-clock strongly-budget-balanced ascending auction
for a multi-lateral market with a recipe tree. Single path demos.

Author: Erel Segal-Halevi
Since:  2020-09
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

print("\n\n###### TEST MULTI RECIPE AUCTION WITH A SINGLE PATH: [1,1,1]")
market = Market([
    AgentCategory("buyer", [9, 8]),
    AgentCategory("sellerA", [-1, -2]),
    AgentCategory("sellerB", [-4, -3]),
])
recipes_111 = [1, [2, [0, None]]] # buyer <- sellerB <- sellerA; [1,1,1]
print(budget_balanced_ascending_auction(market, recipes_111))
