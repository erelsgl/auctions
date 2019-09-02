#!python3

"""
Demonstration of a multiple-clock strongly-budget-balanced ascending auction
for a multi-lateral market with one buyer per two sellers (type vector: 1,2)

Author: Erel Segal-Halevi
Since:  2019-08
"""

from markets import Market
from agents import AgentCategory
import ascending_auction_protocol
from ascending_auction_protocol import budget_balanced_ascending_auction

ascending_auction_protocol.trace = print

market = Market([
    AgentCategory("buyer", [20., 18., 16., 14.]),
    AgentCategory("seller", [-2., -4., -6., -8.]),
])

budget_balanced_ascending_auction(market, [1,2])  # 1 buyer,  2 sellers
# Here, the final trade involves 1 buyer and 4 sellers (so 2 sellers should be selected at random).

budget_balanced_ascending_auction(market, [2,1])  # 2 buyers,  1 seller
# Here, the final trade involves 4 buyers and 2 sellers (so no lottery is needed).


market = Market([
    AgentCategory("buyer", [10., 8., 6., 4.]),
    AgentCategory("seller", [-2., -4., -6., -8.]),
])

budget_balanced_ascending_auction(market, [1,2])  # 1 buyer,  2 sellers
# Here, there is no trade at all

budget_balanced_ascending_auction(market, [2,1])  # 2 buyers,  1 seller
# Here, the final trade involves 4 buyers and 2 sellers (so no lottery is needed).


market = Market([
    AgentCategory("buyer", [13., 8., 6., 4.]),
    AgentCategory("seller", [-2., -4., -6., -8.]),
])

budget_balanced_ascending_auction(market, [1,2])  # 1 buyer,  2 sellers
# Here, the final trade involves 1 buyer and 2 sellers (so no lottery is needed).
