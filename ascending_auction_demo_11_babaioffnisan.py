#!python3

"""
Demonstration of a strongly-budget-balanced ascending auction
for the double-sided lemonade-industry markets in
Babaioff and Nisan (2004), "Concurrent Auctions Across The Supply Chain",
https://jair.org/index.php/jair/article/view/10379.
Example in Section 2.

It can be seen that, even though there is strong-budget-balance in each market,
the total trade is not always strongly-budget-balanced.

Since:  2019-09
"""

from markets import Market
from agents import AgentCategory
import ascending_auction_protocol
from ascending_auction_protocol import budget_balanced_ascending_auction

ascending_auction_protocol.trace = print


pickers = [-3, -6, -7]
squeezers = [-1, -3, -6]
drinkers = [+12, +11, +7]

virtual_lemon_buyers = [x+y for (x,y) in zip(drinkers,squeezers)]
virtual_squeezing_buyers = [x+y for (x,y) in zip(drinkers,pickers)]
virtual_juice_sellers = [x+y for (x,y) in zip(pickers,squeezers)]

buyerFirst = True

if buyerFirst:
    print("\n\n###### LEMON MARKET")
    market = Market([
        AgentCategory("virtual-lemon-buyer", virtual_lemon_buyers),
        AgentCategory("picker", pickers),
    ])
    print(budget_balanced_ascending_auction(market, [1,1]))

    print("\n\n###### SQUEEZING MARKET")
    market = Market([
        AgentCategory("virtual-squeezing-buyer", virtual_squeezing_buyers),
        AgentCategory("squeezer", squeezers),
    ])
    print(budget_balanced_ascending_auction(market, [1,1]))

    print("\n\n###### JUICE MARKET")
    market = Market([
        AgentCategory("drinker", drinkers),
        AgentCategory("virtual-juice-seller", virtual_juice_sellers),
    ])
    print(budget_balanced_ascending_auction(market, [1,1]))

else:  # seller first

    print("\n\n###### LEMON MARKET")
    market = Market([
        AgentCategory("picker", pickers),
        AgentCategory("virtual-lemon-buyer", virtual_lemon_buyers),
    ])
    print(budget_balanced_ascending_auction(market, [1,1]))

    print("\n\n###### SQUEEZING MARKET")
    market = Market([
        AgentCategory("squeezer", squeezers),
        AgentCategory("virtual-squeezing-buyer", virtual_squeezing_buyers),
    ])
    print(budget_balanced_ascending_auction(market, [1,1]))

    print("\n\n###### JUICE MARKET")
    market = Market([
        AgentCategory("virtual-juice-seller", virtual_juice_sellers),
        AgentCategory("drinker", drinkers),
    ])
    print(budget_balanced_ascending_auction(market, [1,1]))

