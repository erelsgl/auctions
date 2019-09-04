#!python3

"""
Demonstration of a multiple-clock strongly-budget-balanced ascending auction
for a multi-lateral market with one buyer per two sellers (type vector: 1,2)

Since:  2019-08
"""

from markets import Market
from agents import AgentCategory
import ascending_auction_protocol
from ascending_auction_protocol import budget_balanced_ascending_auction

ascending_auction_protocol.trace = print

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
