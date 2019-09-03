#!python3

"""
Demonstration of a multiple-clock strongly-budget-balanced ascending auction
for a multi-lateral market with buyers, mediators and sellers (type vector: 1,1,1)

Since:  2019-08
"""

from markets import Market
from agents import AgentCategory
import ascending_auction_protocol
from ascending_auction_protocol import budget_balanced_ascending_auction

ascending_auction_protocol.trace = print

ps_recipe = [1,1,1]

print("\n\n###### RUNNING EXAMPLE FROM THE PAPER FOR TYPE (1,1,1)")

# Price stops between buyers, k=3:
market = Market([
    AgentCategory("buyer",    [17, 14, 13, 9, 6]),
    AgentCategory("seller",   [-1, -4, -5, -5.5, -11]),
    AgentCategory("mediator", [-1, -3, -6, -7, -10])])
print(budget_balanced_ascending_auction(market, ps_recipe))

# Price stops between sellers, k=3:
market = Market([
    AgentCategory("buyer",    [17, 14, 13, 9, 6]),
    AgentCategory("seller",   [-1, -4, -5, -8, -11]),
    AgentCategory("mediator", [-1, -3, -6, -7, -10])])
print(budget_balanced_ascending_auction(market, ps_recipe))

# Price stops between mediators, k=3:
market = Market([
    AgentCategory("buyer",    [17, 14, 13, 9, 6]),
    AgentCategory("seller",   [-1, -4, -6.5, -8, -11]),
    AgentCategory("mediator", [-1, -3, -6, -7, -10])])
print(budget_balanced_ascending_auction(market, ps_recipe))

# Price stops between buyers, k=2:
market = Market([
    AgentCategory("buyer",    [17, 14, 13, 9, 6]),
    AgentCategory("seller",   [-1, -4, -7.5, -8, -11]),
    AgentCategory("mediator", [-1, -3, -6, -7, -10])])
print(budget_balanced_ascending_auction(market, ps_recipe))

exit(1)



# OTHER EXAMPLES

# Here, the final trade involves 2 buyers and 2 mediators and 3 sellers - seller-lottery is needed.
market = Market([
    AgentCategory("buyer",    [17., 14., 13., 9., 6.]),
    AgentCategory("mediator", [-1., -3., -6., -7., -10., -13., -16.]),
    AgentCategory("seller",   [-1., -4., -5., -8., -11.]),
])
budget_balanced_ascending_auction(market, ps_recipe)


# Here, there is no trade at all.
market = Market([
    AgentCategory("buyer",    [7., 4., 3., 2., 1.]),
    AgentCategory("mediator", [-3., -6., -7., -10., -13., -16.]),
    AgentCategory("seller",   [-4., -5., -8., -11.]),
])
budget_balanced_ascending_auction(market, ps_recipe)


# Here, the final trade involves 3 buyers and 3 mediators and 3 sellers -  no lottery is needed.
market = Market([
    AgentCategory("buyer",    [17., 16.5, 16., 9., 6.]),
    AgentCategory("mediator", [-1., -3., -6., -7., -10., -13., -16.]),
    AgentCategory("seller",   [-1., -4., -5., -8., -11.]),
])
budget_balanced_ascending_auction(market, ps_recipe)
