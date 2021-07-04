#!python3

"""
Demonstration of a multiple-clock strongly-budget-balanced ascending auction
for a multi-lateral market with a recipe tree

Author: Erel Segal-Halevi
Since:  2020-08
"""

import sys, os; sys.path.insert(0, os.path.abspath('..'))

from markets import Market
from agents import AgentCategory
import ascending_auction_recipetree_protocol
from ascending_auction_recipetree_protocol import budget_balanced_ascending_auction
import prices
import numpy as np

import logging
ascending_auction_recipetree_protocol.logger.setLevel(logging.INFO)
prices.logger.setLevel(logging.INFO)

recipes_110_101 = [0, [1, None, 2, None]]  # buyer -> sellerA, buyer -> sellerB;   [[1, 1, 0], [1, 0, 1]]
recipes_1100_1011 = [0, [1, None, 2, [3, None]]]  # buyer -> seller, buyer -> producerA -> producerB;   [[1,1,0,0],[1,0,1,1]]
recipes_11100_10011 = [0, [1, [2, None], 3, [4, None]]]


# print("\n\n###### TEST TWO EQUIVALENT RECIPES: [1,0,1] [1,1,0]")
# market = Market([
#     AgentCategory("buyer", [17, 14, 13, 9, 6]),
#     AgentCategory("sellerA", [-1, -3, -4, -5, -8, -10]),
#     AgentCategory("sellerB", [-2, -7, -11]),
# ])
# market = Market([
#     AgentCategory("buyer", [400, 300, 200, 100]),
#     AgentCategory("sellerA", [-3, -14]),
#     AgentCategory("sellerB", [-9, -50]),
# ])
# print(budget_balanced_ascending_auction(market, recipes_110_101))

#
#
print("\n\n###### TEST TWO DIFFERENT RECIPES: [1,1,0,0] [1,0,1,1]. PAPER EXAMPLE")
market = Market([
    AgentCategory("buyer", [17, 14, 13, 9, 6, 2]),
    AgentCategory("seller", [-4, -5, -8, -10]),
    AgentCategory("producerA", [-1, -3, -5]),
    AgentCategory("producerB", [-1, -4, -6]),
])
print(budget_balanced_ascending_auction(market, recipes_1100_1011))
#
#
# print("\n\n###### TEST TWO DIFFERENT RECIPES - RICA'S EXAMPLE")
# market = Market([
#     AgentCategory("buyer",   [20, 19, 18, 17, 16, 15]),
#     AgentCategory("seller",   [-1, -2, -5, -6, -9, -10]),
#     AgentCategory("producerA", [-4, -8]),
#     AgentCategory("producerB", [-3, -7]),
# ])
# print(budget_balanced_ascending_auction(market, recipes_1100_1011))





# print("\n\n###### EXAMPLE WITH A LARGE CATEGORY AND SEVERAL SMALL ONES")
# market = Market([
#     AgentCategory("buyer",     np.arange(100,1100,100)),
#     AgentCategory("sellerA",   np.arange(-41,-46,-1)),
#     AgentCategory("sellerB",   np.arange(-31,-36,-1)),
#     AgentCategory("producerA", np.arange(-81,-86,-1)),
#     AgentCategory("producerB", np.arange(-1,-21,-1)),
# ])

# print("\n\n###### EXAMPLE WITH UNBALANCED CATEGORIES")
# market = Market([
#     AgentCategory("buyer",     np.arange(100,1100,100)),
#     AgentCategory("sellerA",   np.arange(-41,-48,-1)),
#     AgentCategory("sellerB",   np.arange(-31,-38,-1)),
#     AgentCategory("producerA", np.arange(-81,-88,-1)),
#     AgentCategory("producerB", np.arange(-1,-8,-1)),
# ])



# print("\n\n###### EXAMPLE OF LOSING 2 OPTIMAL DEALS")
# market = Market([
#     AgentCategory("buyer", [400, 300, 200, 100]),  # C0
#     AgentCategory("seller1", [-1, -11]),             # C1
#     AgentCategory("seller2", [-2, -3]),             # C2 u C3
#     AgentCategory("producer1", [-4, -44]),             # C4
#     AgentCategory("producer2", [-5, -6]),             # C5 u C6
# ])
#
# print(budget_balanced_ascending_auction(market, recipes_11100_10011))
#
#
# In the third round there is a problem!
# The price-increase makes a seller2 leave, instead of a producer1!
# This means that we lose a second optimal deal (-3, -11), instead of losing the remainder of the first optimal deal (-44).
#
# For comparison, the optimal trade has k=4, GFT=924.000000: [(400, -1, -2), (300, -4, -5), (200, -11, -3), (100, -44, -6)]
#
# Traders: [buyer: [400, 300, 200],   seller1: [-1, -11], seller2: [-2, -3],   producer1: [-4, -44], producer2: [-5]]
# Largest category indices are [2, 3]. Largest category size = 2, combined category size = 3
# Planned price-increases: [(2, -3, 'seller2'), (3, -44, 'producer1')]
#   Prices before increase: [100.0, -1000000.0, -6.0, -1000000.0, -6.0]
#   Planned increase: [(2, -3, 'seller2'), (3, -44, 'producer1')]
#   Increases per recipe: [1, 1]
# seller2: price increases to -3
# producer1: while increasing price towards -44, stopped at -999997.0 where an agent from another category left
# seller2 after: 1 agents remain
#

# print("\n\n###### EXAMPLE OF PRICE-INCREASES")
# market = Market([
#     AgentCategory("buyer", [400, 300, 200, 100]),
#     AgentCategory("seller1", [-1, -2]),
#     AgentCategory("seller2", [-3, -4]),
#     AgentCategory("producer1", [-5, -6]),
#     AgentCategory("producer2", [-7, -8]),
# ])
# print(budget_balanced_ascending_auction(market, recipes_11100_10011))


#
# print("\n\n###### GFT CHALLENGE 1")
# market = Market([
#     AgentCategory("buyer", [300, 200, 100]),
#     AgentCategory("seller1", [-6, -5]),
#     AgentCategory("seller2", [-6, -5]),
#     AgentCategory("producer1", [-98,-97]),
#     AgentCategory("producer2", [-1,-2]),
# ])
# print(budget_balanced_ascending_auction(market, recipes_11100_10011))
#


# print("\n\n###### GFT CHALLENGE - EASY")
# market = Market([
#     AgentCategory("buyer", [400,300,200,100]),  # k = 4
#     AgentCategory("seller1", [-5, -7, -11]),     # k = 3
#     AgentCategory("producer1", [-9, -13, -15]),  # k = 1
# ])
# print(budget_balanced_ascending_auction(market, recipes_110_101))
#
#
# print("\n\n###### GFT CHALLENGE - MEDIUM")
# market = Market([
#     AgentCategory("buyer", [400,300,200,100]),  # k = 4
#     AgentCategory("seller1", [-5, -7, -11]),     # k = 3
#     AgentCategory("seller2", [-5, -7, -11]),         # k = 3
#     AgentCategory("producer1", [-9, -13, -15]),          # k = 1
#     AgentCategory("producer2", [-9, -13, -15]),        # k = 1
# ])
# print(budget_balanced_ascending_auction(market, recipes_11100_10011))
#
#
# print("\n\n###### GFT CHALLENGE - HARD")
# market = Market([
#     AgentCategory("buyer", [400,300,200,100]),     # k = 4
#     AgentCategory("seller1", [-5, -7, -11]),     # k = 3
#     AgentCategory("seller2", [-5, -7, -11]),         # k = 3
#     AgentCategory("producer1", [-9, -13, -15]),          # k = 1
#     AgentCategory("producer2", [-3, -10, -15]),        # k = 1
# ])
# print(budget_balanced_ascending_auction(market, recipes_11100_10011))

