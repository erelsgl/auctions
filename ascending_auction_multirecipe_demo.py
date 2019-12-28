#!python3

"""
Demonstration of a multiple-clock strongly-budget-balanced ascending auction
for a multi-lateral market with one buyer per two sellers (recipe: 1,2)

Author: Erel Segal-Halevi
Since:  2019-08
"""

from markets import Market
from agents import AgentCategory
import ascending_auction_protocol_multirecipe
from ascending_auction_protocol_multirecipe import budget_balanced_ascending_auction_multiple_recipes
import prices

import logging
ascending_auction_protocol_multirecipe.logger.setLevel(logging.INFO)
prices.logger.setLevel(logging.INFO)

print("\n\n###### TEST MULTI RECIPE AUCTION WITH A SINGLE RECIPE (1,2)")

market = Market([
    AgentCategory("buyer", [17, 14, 13, 9, 6]),
    AgentCategory("seller", [-1, -2, -3, -4, -5, -7, -8, -10, -11]),
])

print(budget_balanced_ascending_auction_multiple_recipes(market,[[1,2]]))

