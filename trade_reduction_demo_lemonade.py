#!python3

"""
Demonstration of the lemonade-industry markets in
Babaioff and Nisan (2004), "Concurrent Auctions Across The Supply Chain",
https://jair.org/index.php/jair/article/view/10379, example in Section 2.

In their market, there are 3 agent categories.
Instead of a single multilateral auction for the entire market,
they create 3 sub-markets, one per category,
and run an independent double-auction in each sub-market

Here, we use our trade-reduction SBB protocol as the double-auction in each sub-market.
It can be seen that, even though a SBB protocol is used in each sub-market,
the combined outcome is not SBB.

Author: Erel Segal-Halevi
Since:  2019-09
"""

from markets import Market
from agents import AgentCategory
import trade_reduction_protocol
from trade_reduction_protocol import budget_balanced_trade_reduction

trade_reduction_protocol.trace = print

pickers = [-3, -6, -7]
squeezers = [-1, -3, -6]
drinkers = [+12, +11, +7]

print("\n\n###### ONE AUCTION FOR THE ENTIRE INDUSTRY")

market = Market([
    AgentCategory("squeezer", squeezers),
    AgentCategory("picker", pickers),
    AgentCategory("drinker", drinkers),
])
print(budget_balanced_trade_reduction(market, [1, 1, 1]))

virtual_lemon_buyers = [x+y for (x,y) in zip(drinkers,squeezers)]
virtual_squeezing_buyers = [x+y for (x,y) in zip(drinkers,pickers)]
virtual_juice_sellers = [x+y for (x,y) in zip(pickers,squeezers)]


print("\n\n###### THREE DIFFERENT AUCTIONS FOR THE SUB-MARKETS")

buyerFirst = True

if buyerFirst:
    print("\n\n###### LEMON SUB-MARKET")
    market = Market([
        AgentCategory("virtual-lemon-buyer", virtual_lemon_buyers),
        AgentCategory("picker", pickers),
    ])
    print(budget_balanced_trade_reduction(market, [1,1]))

    print("\n\n###### SQUEEZING SUB-MARKET")
    market = Market([
        AgentCategory("virtual-squeezing-buyer", virtual_squeezing_buyers),
        AgentCategory("squeezer", squeezers),
    ])
    print(budget_balanced_trade_reduction(market, [1,1]))

    print("\n\n###### JUICE SUB-MARKET")
    market = Market([
        AgentCategory("drinker", drinkers),
        AgentCategory("virtual-juice-seller", virtual_juice_sellers),
    ])
    print(budget_balanced_trade_reduction(market, [1,1]))

else:  # seller first

    print("\n\n###### LEMON SUB-MARKET")
    market = Market([
        AgentCategory("picker", pickers),
        AgentCategory("virtual-lemon-buyer", virtual_lemon_buyers),
    ])
    print(budget_balanced_trade_reduction(market, [1,1]))

    print("\n\n###### SQUEEZING SUB-MARKET")
    market = Market([
        AgentCategory("squeezer", squeezers),
        AgentCategory("virtual-squeezing-buyer", virtual_squeezing_buyers),
    ])
    print(budget_balanced_trade_reduction(market, [1,1]))

    print("\n\n###### JUICE SUB-MARKET")
    market = Market([
        AgentCategory("virtual-juice-seller", virtual_juice_sellers),
        AgentCategory("drinker", drinkers),
    ])
    print(budget_balanced_trade_reduction(market, [1,1]))

