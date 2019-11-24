#!python3

"""
Demonstration of a multiple-clock strongly-budget-balanced ascending auction
for a multi-lateral market with one buyer per two sellers (recipe: 1,2)

Author: Erel Segal-Halevi
Since:  2019-08
"""

from markets import Market
from agents import AgentCategory
import ascending_auction_protocol
from ascending_auction_protocol import budget_balanced_ascending_auction

import logging
ascending_auction_protocol.logger.setLevel(logging.INFO)


print("\n\n###### RUNNING EXAMPLE FROM THE PAPER FOR TYPE (1,2)")

market = Market([
    AgentCategory("buyer", [17, 14, 13, 9, 6]),
    AgentCategory("seller", [-1, -2, -3, -4, -5, -7, -8, -10, -11]),
])

print(budget_balanced_ascending_auction(market, [1,2]))


print("\n\n###### RUNNING EXAMPLE FROM THE PAPER, WITH DIFFERENT CATEGORY ORDER")

market = Market([
    AgentCategory("seller", [-1, -2, -3, -4, -5, -7, -8, -10, -11]),
    AgentCategory("buyer", [17, 14, 13, 9, 6]),
])

print(budget_balanced_ascending_auction(market, [2,1]))


print("\n\n###### ADDITIONAL EXAMPLES")

print("\n\n###### k=3, price-increase stops before first seller")
market = Market([
    AgentCategory("seller", [-1, -2, -3, -4, -5, -8, -10, -11]),
    AgentCategory("buyer", [20, 19, 18, 17, 9, 6]),
])
print(budget_balanced_ascending_auction(market, [2,1]))

print("\n\n###### k=3, price-increase stops before second seller")
market = Market([
    AgentCategory("seller", [-1, -2, -3, -4, -5, -8, -10, -11]),
    AgentCategory("buyer", [17, 15, 14, 11, 9, 6]),
])
print(budget_balanced_ascending_auction(market, [2,1]))

print("\n\n###### k=2!!, price-increase stops before second seller")
market = Market([
    AgentCategory("seller", [-1, -2, -3, -4, -5, -8, -10, -11]),
    AgentCategory("buyer", [17, 15, 12, 11, 9, 6]),
])
print(budget_balanced_ascending_auction(market, [2,1]))

print("\n\n###### k=3, price-increase stops before buyer")
market = Market([
    AgentCategory("seller", [-1, -2, -3, -4, -5, -8, -10, -11]),
    AgentCategory("buyer", [17, 15, 14, 9.5, 9, 6]),
])
print(budget_balanced_ascending_auction(market, [2,1]))

print("\n\n###### k=2!!, price-increase stops before buyer")
market = Market([
    AgentCategory("seller", [-1, -2, -3, -4, -5, -8, -10, -11]),
    AgentCategory("buyer", [17, 15, 12, 9.5, 9, 6]),
])
print(budget_balanced_ascending_auction(market, [2,1]))


