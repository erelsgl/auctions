#!python3

"""
Perform a simulation experiment with the ascending auction, similar to the one described by McAfee (1992), Table I (page 448).

Since:  2019-11
Author: Erel Segal-Halevi
"""

from experiment import  experiment

from ascending_auction_protocol import budget_balanced_ascending_auction
import sys

results_file = "results/ascending_auction.csv"

experiment(results_file,budget_balanced_ascending_auction, "SBB Ascending Prices", recipe=(1,1),
           value_ranges   = [(1,1000),(-1000,-1)],
           # nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           nums_of_agents = (100,1000),
           num_of_iterations = 50
           )

experiment(results_file,budget_balanced_ascending_auction, "SBB Ascending Prices", recipe=(1,1,1),
           value_ranges   = [(1,2000),(-1000,-1),(-1000,-1)],
           nums_of_agents = (100,1000),
           num_of_iterations = 50
           )

experiment(results_file,budget_balanced_ascending_auction, "SBB Ascending Prices", recipe=(2,1),
           value_ranges   = [(1,500),(-1000,-1)],
           nums_of_agents = (100,1000),
           num_of_iterations = 50
           )

