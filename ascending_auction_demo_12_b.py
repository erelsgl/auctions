#!python3

"""
An additional example of a multiple-clock strongly-budget-balanced ascending auction
for a multi-lateral market with one buyer per two sellers (recipe: 1,2)

Since:  2019-08
"""

from markets import Market
from agents import AgentCategory
import ascending_auction_protocol
from ascending_auction_protocol import budget_balanced_ascending_auction

ascending_auction_protocol.trace = print

# market = Market([
#     AgentCategory("buyer", [17,15,14,13,6]),
#     AgentCategory("seller", [-1, -2, -3, -4, -5, -7, -8, -10, -11]),
# ])
# print(budget_balanced_ascending_auction(market, [1,2]))


# market = Market([
#     AgentCategory("seller", [-1, -2, -3, -4, -5, -6, -7, -8, -9, -10]),
#     AgentCategory("buyer", [17, 14, 13, 12, 10, 9, 8, 6]),
# ])
# print(budget_balanced_ascending_auction(market, [3,2]))

market = Market([
    AgentCategory("seller",   [-1, -2, -3, -4, -5, -6, -7, -8]),
    AgentCategory("mediator", [-3, -4, -5, -6, -7, -8, -9, -10]),
    AgentCategory("buyer", [17, 16, 15, 14, 13, 12, 10, 6]),
])
print(budget_balanced_ascending_auction(market, [1,1,0]))
