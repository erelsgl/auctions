#!python3

"""
Demonstration of a multiple-clock strongly-budget-balanced ascending auction
for a multi-lateral market with one buyer per two sellers (recipe: 1,2)

Since:  2019-08
"""

from markets import Market
from agents import AgentCategory
import ascending_auction_protocol
from ascending_auction_protocol import budget_balanced_ascending_auction

ascending_auction_protocol.trace = print


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
