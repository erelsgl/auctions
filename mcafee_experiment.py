#!python3

"""
The simulation experiment described by McAfee (1992), Table I (page 448).

Since:  2019-11

Author: Erel Segal-Halevi
"""


from markets import Market
from agents import AgentCategory
from mcafee_protocol import mcafee_trade_reduction

recipe = [1,1]
min_value = 1
max_value = 1000
# nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000)
nums_of_agents = (2, 3, 4, 5, 10)
# num_of_iterations = 50000
num_of_iterations = 5000


for num_of_agents_per_category in nums_of_agents:
    print("\n\n### McAfee's experiment: n={}".format(num_of_agents_per_category))
    count_max_gft = 0  # count the number of times the max GFT was attained
    sum_max_gft = sum_gft = 0
    for _ in range(num_of_iterations):
        market = Market([
            AgentCategory.uniformly_random("buyer", num_of_agents_per_category, min_value, max_value),
            AgentCategory.uniformly_random("seller", num_of_agents_per_category, -max_value, -min_value),
        ])
        (optimal_trade, _) = market.optimal_trade(recipe)
        mcafee_trade = mcafee_trade_reduction(market, recipe)
        optimal_count = len(optimal_trade)
        mcafee_count  = mcafee_trade.number_of_ps
        if optimal_count==mcafee_count:
            count_max_gft += 1
        elif optimal_count==mcafee_count+1:
            pass
        else:
            raise ValueError("Deals: {} out of {}".format(mcafee_count, optimal_count))
    print("Max GFT: {} / {} = {}%".format(count_max_gft, num_of_iterations, count_max_gft*100 / num_of_iterations))