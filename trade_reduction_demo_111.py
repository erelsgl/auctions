#!python3

"""
Demonstration of a trade-reduction strongly-budget-balanced auction
for a multi-lateral market with buyers, mediators and sellers (recipe: 1,1,1)

Since:  2019-08

Author: Erel Segal-Halevi
"""


from markets import Market
from agents import AgentCategory
import trade_reduction_protocol
from trade_reduction_protocol import budget_balanced_trade_reduction

import logging
trade_reduction_protocol.logger.setLevel(logging.INFO)


print("\n\n###### RUNNING EXAMPLE FROM THE PAPER FOR TYPE (1,1,1): buyers-sellers-mediators")

buyers = [17, 14, 13, 9, 6]
sellers = [-1, -4, -5, -8, -11]
mediators = [-1, -3, -4, -7, -10]
recipe = [1,1,1]

market = Market([
    AgentCategory("buyer",    buyers),
    AgentCategory("seller",   sellers),
    AgentCategory("mediator", mediators),
])
print(budget_balanced_trade_reduction(market, recipe))


print("\n\n###### SAME EXAMPLE WITH DIFFERENT ORDER: buyers-mediators-sellers")
market = Market([
    AgentCategory("buyer",    buyers),
    AgentCategory("mediator", mediators),
    AgentCategory("seller",   sellers),
])
print(budget_balanced_trade_reduction(market, recipe))


print("\n\n###### SAME EXAMPLE WITH DIFFERENT ORDER: sellers-buyers-mediators")
market = Market([
    AgentCategory("seller",   sellers),
    AgentCategory("buyer",    buyers),
    AgentCategory("mediator", mediators),
])
print(budget_balanced_trade_reduction(market, recipe))



print("\n\n###### SAME EXAMPLE WITH DIFFERENT ORDER: sellers-mediators-buyers")
market = Market([
    AgentCategory("seller",   sellers),
    AgentCategory("mediator", mediators),
    AgentCategory("buyer", buyers),
])
print(budget_balanced_trade_reduction(market, recipe))


print("\n\n###### SAME EXAMPLE WITH DIFFERENT ORDER: mediators-sellers-buyers")
market = Market([
    AgentCategory("mediator", mediators),
    AgentCategory("seller",   sellers),
    AgentCategory("buyer", buyers),
])
print(budget_balanced_trade_reduction(market, recipe))


print("\n\n###### SAME EXAMPLE WITH DIFFERENT ORDER: mediators-buyers-sellers")
market = Market([
    AgentCategory("mediator", mediators),
    AgentCategory("buyer", buyers),
    AgentCategory("seller",   sellers),
])
print(budget_balanced_trade_reduction(market, recipe))




