#!python3

"""
Perform the simulation experiment described by McAfee (1992), Table I (page 448).

Since:  2019-11

Author: Erel Segal-Halevi
"""

from markets import Market
from agents import AgentCategory
from typing import Callable

def experiment(auction_function:Callable, title:str, recipe:tuple, value_ranges:list, nums_of_agents:list, num_of_iterations:int):
    """
    Run McAfee's experiment on the given auction.

    :param auction_function: the function for executing the auction under consideration.
    :param title: title of the experiment, for printouts.
    :param nums_of_agents: a list of the numbers of agents with which to run the experiment.
    :param value_ranges: for each category, a pair (min_value,max_value). The value for each agent in this category is selected uniformly at random between min_value and max_value.
    :param num_of_iterations: how many times to repeat the experiment for each num of agents.
    """
    for num_of_agents_per_category in nums_of_agents:
        print("\n\n### {}: n={}".format(title, num_of_agents_per_category))
        count_optimal_gft = 0  # count the number of times the maximum GFT was attained
        sum_optimal_gft = sum_auction_gft = 0
        for _ in range(num_of_iterations):
            market = Market([
                AgentCategory.uniformly_random("agent", num_of_agents_per_category, min_value, max_value)
                for (min_value, max_value) in value_ranges
            ])
            (optimal_trade, _) = market.optimal_trade(recipe)
            auction_trade = auction_function(market, recipe)

            optimal_count = optimal_trade.num_of_deals()
            mcafee_count  = auction_trade.num_of_deals()
            if optimal_count==mcafee_count:
                count_optimal_gft += 1
            elif optimal_count==mcafee_count+1:
                pass
            else:
                raise ValueError("Deals: {} out of {}".format(mcafee_count, optimal_count))

            sum_optimal_gft +=  optimal_trade.gain_from_trade()
            sum_auction_gft  += auction_trade.gain_from_trade()

        print("Num of times {} attains the maximum GFT: {} / {} = {:.2f}%".format(title, count_optimal_gft, num_of_iterations, count_optimal_gft * 100 / num_of_iterations))
        print("GFT of {}: {:.2f} / {:.2f} = {:.2f}%".format(title, sum_auction_gft, sum_optimal_gft, sum_auction_gft * 100 / sum_optimal_gft))


from mcafee_protocol import mcafee_trade_reduction
experiment(mcafee_trade_reduction, "McAfee", recipe=(1,1),
           value_ranges   = [(1,1000),(-1000,-1)],
           # nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           nums_of_agents = (2, 3, 4, 5, 10),
           # num_of_iterations = 50000
           num_of_iterations = 50
           )

from trade_reduction_protocol import budget_balanced_trade_reduction
experiment(budget_balanced_trade_reduction, "BudgetBalancedTradeReduction11", recipe=(1,1),
           value_ranges   = [(1,1000),(-1000,-1)],
           # nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           nums_of_agents = (2, 3, 4, 5, 10),
           # num_of_iterations = 50000
           num_of_iterations = 50
           )


experiment(budget_balanced_trade_reduction, "BudgetBalancedTradeReduction111", recipe=(1,1,1),
           value_ranges   = [(1,1000),(-1000,-1),(-1000,-1)],
           # nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           nums_of_agents = (2, 3, 4, 5, 10),
           # num_of_iterations = 50000
           num_of_iterations = 5000
           )



from ascending_auction_protocol import budget_balanced_ascending_auction
experiment(budget_balanced_ascending_auction, "BudgetBalancedAscendingAuction11", recipe=(1,1),
           value_ranges   = [(1,1000),(-1000,-1)],
           # nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           nums_of_agents = (2, 3, 4, 5, 10),
           # num_of_iterations = 50000
           num_of_iterations = 50
           )


experiment(budget_balanced_ascending_auction, "BudgetBalancedAscendingAuction111", recipe=(1,1,1),
           value_ranges   = [(1,1000),(-1000,-1),(-1000,-1)],
           # nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           nums_of_agents = (2, 3, 4, 5, 10),
           # num_of_iterations = 50000
           num_of_iterations = 5000
           )


experiment(budget_balanced_ascending_auction, "BudgetBalancedAscendingAuction23", recipe=(2,3),
           value_ranges   = [(1,1000),(-1000,-1)],
           # nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           nums_of_agents = (2, 3, 4, 5, 10),
           # num_of_iterations = 50000
           num_of_iterations = 5000
           )

