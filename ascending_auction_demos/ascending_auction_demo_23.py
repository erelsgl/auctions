#!python3

"""
Demonstration of a multiple-clock strongly-budget-balanced ascending auction
for a multi-lateral market with two buyers per three sellers (recipe: 2,3)

Author: Erel Segal-Halevi
Since:  2019-08
"""
import sys, os; sys.path.insert(0, os.path.abspath('..'))

from markets import Market
from agents import AgentCategory
import ascending_auction_protocol
from ascending_auction_protocol import budget_balanced_ascending_auction

import logging
ascending_auction_protocol.logger.setLevel(logging.INFO)

market = Market([
    AgentCategory("buyer",  [20., 18., 16., 9., 2., 1.]),
    AgentCategory("seller", [-2., -4., -6., -8., -10., -12., -14.]),
])

print(budget_balanced_ascending_auction(market, [2,3]))
    # Here, k=1, and the final trade involves 2 buyers and 5 sellers
    # (so 3 sellers should be selected at random).

print(budget_balanced_ascending_auction(market, [3,2]))
    # Here, k=1, and the final trade involves 5 buyers and 3 sellers
    #  (so 3 buyers and 2 sellers should be selected at random).
