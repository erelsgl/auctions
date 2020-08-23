#!python3

"""
Additional examples of a multiple-clock strongly-budget-balanced ascending auction.

Author: Erel Segal-Halevi
Since:  2019-11
"""

from markets import Market
from agents import AgentCategory
import ascending_auction_protocol
from ascending_auction_protocol import budget_balanced_ascending_auction

import logging
ascending_auction_protocol.logger.setLevel(logging.INFO)

print("\n\n###### RUNNING EXAMPLE 3 FROM THE PAPER FOR TYPE (2,2,3)")

market = Market([
    AgentCategory("buyer", [17, 16, 15, 14, 13, 12, 10, 6]),
    AgentCategory("mediator", [-3, -4, -5, -6, -7, -8, -9, -10]),
    AgentCategory("seller",   [-1, -2, -3, -4, -5, -6, -7, -8]),
])
# print(budget_balanced_ascending_auction(market, [2,2,3]))

print("\n\n###### OTHER EXAMPLES FOR (2,2,3)")

market = Market([
    AgentCategory("buyer", [17, 16, 15, 14, 13, 12, 10, 6]),
    AgentCategory("mediator", [-3, -4, -5, -6, -7, -8, -9, -10]),
    AgentCategory("seller",   [-1, -2, -3, -4, -5, -6, -7, -8]),
])
print(budget_balanced_ascending_auction(market, [2,2,3]))
