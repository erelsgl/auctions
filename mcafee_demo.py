#!python3

"""
Demonstration of McAfee's trade-reduction auction
for a bilateral market with buyers and sellers.

Since:  2019-08

Author: Erel Segal-Halevi
"""


from markets import Market
from agents import AgentCategory
import mcafee_protocol
from mcafee_protocol import mcafee_trade_reduction


import logging
mcafee_protocol.logger.setLevel(logging.INFO)

recipe = [1,1]


print("\n\n### Example without trade reduction")
market = Market([
    AgentCategory("buyer",    [17, 14, 13, 9, 6]),
    AgentCategory("seller",   [-1, -4, -5, -8, -11]),
])
print(mcafee_trade_reduction(market, recipe))


print("\n\n### Example with trade reduction")
market = Market([
    AgentCategory("buyer",    [17, 14, 13, 9, 6]),
    AgentCategory("seller",   [-1, -4, -5, -8, -13]),
])
print(mcafee_trade_reduction(market, recipe))
