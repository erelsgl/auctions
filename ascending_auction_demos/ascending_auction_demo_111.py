#!python3

"""
Demonstration of a multiple-clock strongly-budget-balanced ascending auction
for a multi-lateral market with buyers, mediators and sellers (recipe: 1,1,1)

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

ps_recipe = [1,1,1]

print("\n\n###### RUNNING EXAMPLE FROM THE PAPER FOR TYPE (1,1,1)")
# Price stops between buyers, k=3:
market = Market([
    AgentCategory("buyer",    [17, 14, 13, 9, 6]),
    AgentCategory("seller",   [-1, -4, -5, -8, -11]),
    AgentCategory("mediator", [-1, -3, -4, -7, -10])])
print(budget_balanced_ascending_auction(market, ps_recipe))


print("\n\n###### SIMILAR EXAMPLE, WHERE PRICE STOPS BETWEEN SELLERS:")
market = Market([
    AgentCategory("buyer",    [17, 14, 13, 9, 6]),
    AgentCategory("seller",   [-1, -4, -5, -8, -11]),
    AgentCategory("mediator", [-1, -3, -6, -7, -10])])
print(budget_balanced_ascending_auction(market, ps_recipe))

print("\n\n###### SIMILAR EXAMPLE, WHERE PRICE STOPS BETWEEN MEDIATORS:")
market = Market([
    AgentCategory("buyer",    [17, 14, 13, 9, 6]),
    AgentCategory("seller",   [-1, -4, -6.5, -8, -11]),
    AgentCategory("mediator", [-1, -3, -6, -7, -10])])
print(budget_balanced_ascending_auction(market, ps_recipe))

print("\n\n###### SIMILAR EXAMPLE, WHERE PRICE STOPS BETWEEN BUYERS:")
market = Market([
    AgentCategory("buyer",    [17, 14, 13, 9, 6]),
    AgentCategory("seller",   [-1, -4, -7.5, -8, -11]),
    AgentCategory("mediator", [-1, -3, -6, -7, -10])])
print(budget_balanced_ascending_auction(market, ps_recipe))
