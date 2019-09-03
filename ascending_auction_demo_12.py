#!python3

"""
Demonstration of a multiple-clock strongly-budget-balanced ascending auction
for a multi-lateral market with one buyer per two sellers (type vector: 1,2)

Since:  2019-08
"""

from markets import Market
from agents import AgentCategory
import ascending_auction_protocol
from ascending_auction_protocol import budget_balanced_ascending_auction

ascending_auction_protocol.trace = print


print("\n\n###### RUNNING EXAMPLE FROM THE PAPER FOR TYPE (1,2)")

market = Market([
    AgentCategory("buyer", [17, 14, 13, 9, 6]),
    AgentCategory("seller", [-1, -2, -3, -4, -5, -7, -8, -10, -11]),
])

print(budget_balanced_ascending_auction(market, [1,2]))


print("\n\n###### RUNNING EXAMPLE FROM THE PAPER, WITH DIFFERENT CATEGORY ORDER")

market = Market([
    AgentCategory("seller", [-1, -2, -3, -4, -5, -7, -8, -10, -11]),
    AgentCategory("buyer", [17, 14, 13, 9, 6]),
])

print(budget_balanced_ascending_auction(market, [2,1]))



market = Market([
    AgentCategory("seller", [-1, -2, -3, -4, -5, -8,  -10, -11]),
    AgentCategory("buyer", [17, 15, 12, 11, 9, 6]),
])

print(budget_balanced_ascending_auction(market, [2,1]))

exit(1)



# OTHER EXAMPLES

market = Market([
    AgentCategory("buyer", [20., 18., 16., 14.]),
    AgentCategory("seller", [-2., -4., -6., -8.]),
])

budget_balanced_ascending_auction(market, [1,2])  # Here, the final trade involves 1 buyer and 4 sellers (so 2 sellers should be selected at random).
budget_balanced_ascending_auction(market, [2,1])  # Here, the final trade involves 4 buyers and 2 sellers (so no lottery is needed).


market = Market([
    AgentCategory("buyer", [10., 8., 6., 4.]),
    AgentCategory("seller", [-2., -4., -6., -8.]),
])

budget_balanced_ascending_auction(market, [1,2])  # Here, there is no trade at all
budget_balanced_ascending_auction(market, [2,1])  # Here, the final trade involves 4 buyers and 2 sellers (so no lottery is needed).

market = Market([
    AgentCategory("buyer", [13., 8., 6., 4.]),
    AgentCategory("seller", [-2., -4., -6., -8.]),
])

budget_balanced_ascending_auction(market, [1,2])  # Here, the final trade involves 1 buyer and 2 sellers (so no lottery is needed).

market = Market([
    AgentCategory("buyer", [23., 18., 16., 14., 12.]),
    AgentCategory("seller", range(-20,-1)),
])

budget_balanced_ascending_auction(market, [2,1])  # Here, the final trade involves 5 buyers and 2 sellers, so we have to pick 4 buyers at random.
