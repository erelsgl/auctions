#!python3

"""
Simulation experiment for our AAAI 2020 paper, with recipes of size 2.
Comparing McAfee's double auction to our SBB auctions.

Since:  2019-11
Author: Erel Segal-Halevi

"""

from experiment import  experiment
from ascending_auction_protocol import budget_balanced_ascending_auction

results_file = "results/experiment_sbb_with_two_categories.csv"
iterations = 50000

for num_of_sellers_per_deal in (2,4,8,16):
    experiment(results_file,budget_balanced_ascending_auction, "SBB Ascending Prices", recipe=(1,num_of_sellers_per_deal),
               value_ranges   = [(1,1000*num_of_sellers_per_deal),(-1000,-1)],
               nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
               num_of_iterations = iterations
               )
