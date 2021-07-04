#!python3

"""
Demonstration of a multiple-clock strongly-budget-balanced ascending auction
for a multi-lateral market with a two-level recipe tree with integers.

Author: Erel Segal-Halevi
Since:  2020-08
"""

from markets import Market
from agents import AgentCategory
import ascending_auction_recipetree_twolevels_protocol
from ascending_auction_recipetree_twolevels_protocol import budget_balanced_ascending_auction_twolevels
import prices

import logging
ascending_auction_recipetree_twolevels_protocol.logger.setLevel(logging.WARNING)
prices.logger.setLevel(logging.WARNING)

# print("\n\n###### TWO BINARY RECIPES: [1,1,0], [1,0,1]")
# market = Market([
#     AgentCategory("buyer", [19,18,17,16,15,14,13]),
#     AgentCategory("sellerA", [-1, -2]),
#     AgentCategory("sellerB", [-3, -4]),
# ])
# print(budget_balanced_ascending_auction_twolevels(market, [1, 1 ,1]))



# print("\n\n###### TWO NON-BINARY RECIPES: [1,2,0], [1,0,2]")
# market = Market([
#     AgentCategory("buyer", [19,18,17,16,15,14,13]),
#     AgentCategory("sellerA", [-1, -2]),
#     AgentCategory("sellerB", [-3, -4]),
# ])
# print(budget_balanced_ascending_auction_twolevels(market, [1, 2, 2]))


print("\n\n###### COUNTER-EXAMPLE FOR CEILING CHILDREN")
num_of_seller_categories = 8
market = Market(
    [AgentCategory("buyer", [101]*10*(num_of_seller_categories+1))] +
    [AgentCategory("producer", [-50]*20)] +
    [AgentCategory("seller", [-100]+[-2]*21)] * num_of_seller_categories
)
# print(budget_balanced_ascending_auction_twolevels(market, [1, 2] + [2] * num_of_seller_categories))


print("\n\n###### DVIR'S EXAMPLE BINARY")
num_of_seller_categories = 8
market = Market(
    [AgentCategory("buyer", [100]*num_of_seller_categories)] +
    [AgentCategory("seller", [-80+i]) for i in range(num_of_seller_categories)]
)
print(budget_balanced_ascending_auction_twolevels(market, [1] + [1]*num_of_seller_categories))



ascending_auction_recipetree_twolevels_protocol.logger.setLevel(logging.INFO)
prices.logger.setLevel(logging.INFO)
print("\n\n###### DVIR'S EXAMPLE")
num_of_seller_categories = 8
market = Market(
    [AgentCategory("buyer", [100+i for i in range(num_of_seller_categories)])] +
    [AgentCategory("seller", [-80+i,-10-i]) for i in range(num_of_seller_categories)]
)
print(budget_balanced_ascending_auction_twolevels(market, [1] + [2]*num_of_seller_categories))

