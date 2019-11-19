#!python3

"""
Perform a simulation experiment similar to the one described by McAfee (1992), Table I (page 448).

The experiment is performed both on McAfee's original auction, and on our new strongly-budget-balanced auctions.

The results are printed to results/aaai20.csv. The columns are:

* auction_name - Either McAfee, or one of our SBB auctions.
* recipe - for McAfee it is always 1:1 =  one buyer and one seller.
*          for our SBB External Competition auction it is either 1:1 or 1:1:1 - buyer, seller and mediator.
*          for our SBB Ascending Prices auction it is either 1:1 or 1:1:1 or 1:2.
* num_of_agents - n = total number of agents in each category (e.g. if n=100 and recipe=[1,2] then there are 100 buyers and 100 sellers).
* mean_optimal_count - k = number of deals in the optimal trade, averaged over all iterations.
                       Note that k <= n. E.g., there may be 100 buyers and 100 sellers, but only 50 procurement-sets with positive GFT, so k=50.
* mean_auction_count - number of deals done by our auction,  averaged over all iterations.
                       Theoretically it is either k or k-1.
                       In the results, the mean value is mean(k)-1/2.
* count_ratio  = mean_auction_count / mean_optimal_count  * 100%.
* mean_optimal_gft - OPT = gain-from-trade in the optimal trade, 	averaged over all iterations.
* mean_auction_gft - GFT = gain-from-trade in the auction, averaged over all iterations.
* gft_ratio  = mean_auction_gft / mean_optimal_gft * 100%.
              Theoretically it should be at least 1 - 1/k.
              In the results, it is usually higher.

Since:  2019-11
Author: Erel Segal-Halevi

"""

from experiment import  experiment

from mcafee_protocol import mcafee_trade_reduction
from trade_reduction_protocol import budget_balanced_trade_reduction
from ascending_auction_protocol import budget_balanced_ascending_auction
results_file = "results/aaai20.csv"

experiment(results_file,mcafee_trade_reduction, "McAfee", recipe=(1,1),
           value_ranges   = [(1,1000),(-1000,-1)],
           nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           # nums_of_agents = (2, 3, 4, 5, 10),
           num_of_iterations = 50
           # num_of_iterations = 50
           )

experiment(results_file,budget_balanced_trade_reduction, "SBB External Competition", recipe=(1,1),
           value_ranges   = [(1,1000),(-1000,-1)],
           nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           num_of_iterations = 50
           )

experiment(results_file,budget_balanced_trade_reduction, "SBB External Competition", recipe=(1,1,1),
           value_ranges   = [(1,2000),(-1000,-1),(-1000,-1)],
           nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           num_of_iterations = 50
           )

experiment(results_file,budget_balanced_ascending_auction, "SBB Ascending Prices", recipe=(1,1),
           value_ranges   = [(1,1000),(-1000,-1)],
           nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           num_of_iterations = 50
           )

experiment(results_file,budget_balanced_ascending_auction, "SBB Ascending Prices", recipe=(1,1,1),
           value_ranges   = [(1,2000),(-1000,-1),(-1000,-1)],
           nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           num_of_iterations = 50
           )


experiment(results_file,budget_balanced_ascending_auction, "SBB Ascending Prices", recipe=(2,1),
           value_ranges   = [(1,1000),(-1000,-1)],
           nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           num_of_iterations = 50
           )

