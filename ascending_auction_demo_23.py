#!python3

"""
Demonstration of a multiple-clock strongly-budget-balanced ascending auction
for a multi-lateral market with two buyers per three sellers (type vector: 2,3)

Since:  2019-08
"""

from markets import Market
from agents import AgentCategory
import ascending_auction_protocol
from ascending_auction_protocol import budget_balanced_ascending_auction

ascending_auction_protocol.trace = print

market = Market([
    AgentCategory("buyer", [20., 18., 16., 14., 12.]),
    AgentCategory("seller", [-2., -4., -6., -8., -10., -12., -14.]),
])

budget_balanced_ascending_auction(market, [2,3])  # Here, the final trade involves 2 buyers and 5 sellers (so 3 sellers should be selected at random).
budget_balanced_ascending_auction(market, [3,2])  # Here, the final trade involves 5 buyers and 3 sellers (so 3 buyers and 2 sellers should be selected at random).
