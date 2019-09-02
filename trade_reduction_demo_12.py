#!python3

"""
Demonstration of a trade-reduction strongly-budget-balanced auction
for a multi-lateral market with buyers, mediators and sellers (type vector: 1,1,1)

Since:  2019-08
"""


from markets import Market
from agents import AgentCategory
import trade_reduction_protocol
from trade_reduction_protocol import budget_balanced_trade_reduction

trade_reduction_protocol.trace = print


# RUNNING EXAMPLE FROM THE PAPER

market = Market([
    AgentCategory("buyer", [17, 14, 13, 9, 6]),
    AgentCategory("seller", [-1, -2, -3, -4, -5, -7, -8, -10, -11]),
])

budget_balanced_trade_reduction(market, [1,2])
