#!python3

"""
Demonstration of a multiple-clock strongly-budget-balanced ascending auction
for a multi-lateral market with one buyer per two sellers (recipe: 1,2)

Author: Erel Segal-Halevi
Since:  2019-08
"""

from markets import Market
from agents import AgentCategory
import ascending_auction_multirecipe_protocol
from ascending_auction_multirecipe_protocol import budget_balanced_ascending_auction
import prices

import logging
ascending_auction_multirecipe_protocol.logger.setLevel(logging.INFO)
prices.logger.setLevel(logging.INFO)

print("\n\n###### TEST MULTI RECIPE AUCTION WITH TWO EQUIVALENT RECIPES: [1,0,1] [1,1,0]")

market = Market([
    AgentCategory("buyer", [17, 14, 13, 9, 6]),
    AgentCategory("sellerA", [-1, -3, -4, -5, -8, -10]),
    AgentCategory("sellerB", [-2, -7, -11]),
])

# print(budget_balanced_ascending_auction(market, [[1, 1, 0], [1, 0, 1]]))


print("\n\n###### TEST MULTI RECIPE AUCTION WITH TWO DIFFERENT RECIPES: [1,1,0,0] [1,0,1,1]")

market = Market([
    AgentCategory("buyer", [17, 14, 13, 9, 6]),
    AgentCategory("seller", [-1, -3, -4, -5, -8, -10]),
    AgentCategory("producerA", [-1, -3, -5]),
    AgentCategory("producerB", [-1, -4, -6]),
])

# print(budget_balanced_ascending_auction(market,[[1,1,0,0],[1,0,1,1]]))



print("\n\n###### TEST MULTI RECIPE AUCTION - RICA'S EXAMPLE")

market = Market([
    AgentCategory("buyer",   [15, 16, 17, 18, 19, 20]),
    AgentCategory("oneseller",   [-1, -2, -5, -6, -9, -10]),
    AgentCategory("twoseller", [-4, -8]),
    AgentCategory("threeseller", [-3, -7]),
])

print(budget_balanced_ascending_auction(market, [[1, 1, 0, 0], [1, 0, 1, 1]]))
