#!python3

"""
Perform the simulation experiment described by McAfee (1992), Table I (page 448).

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
           num_of_iterations = 50000
           # num_of_iterations = 50
           )

experiment(results_file,budget_balanced_trade_reduction, "SBB-Cmp", recipe=(1,1),
           value_ranges   = [(1,1000),(-1000,-1)],
           nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           num_of_iterations = 50000
           )

experiment(results_file,budget_balanced_trade_reduction, "SBB-Cmp", recipe=(1,1,1),
           value_ranges   = [(1,2000),(-1000,-1),(-1000,-1)],
           nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           num_of_iterations = 50000
           )

experiment(results_file,budget_balanced_ascending_auction, "SBB-Asc", recipe=(1,1),
           value_ranges   = [(1,1000),(-1000,-1)],
           nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           num_of_iterations = 50000
           )

experiment(results_file,budget_balanced_ascending_auction, "SBB-Asc", recipe=(1,1,1),
           value_ranges   = [(1,2000),(-1000,-1),(-1000,-1)],
           nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           num_of_iterations = 50000
           )


experiment(results_file,budget_balanced_ascending_auction, "SBB-Asc", recipe=(2,1),
           value_ranges   = [(1,1000),(-1000,-1)],
           nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           num_of_iterations = 50000
           )

