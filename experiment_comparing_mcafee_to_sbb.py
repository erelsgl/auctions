#!python3

"""
Simulation experiment for our AAAI 2020 paper, recipe (1,1).
Comparing McAfee's double auction to our SBB auctions.

Since:  2019-11
Author: Erel Segal-Halevi

"""

from experiment import experiment

from mcafee_protocol import mcafee_trade_reduction
from trade_reduction_protocol import budget_balanced_trade_reduction
from ascending_auction_protocol import budget_balanced_ascending_auction

from functools import partial
mcafee_without_heuristic = partial(mcafee_trade_reduction,price_heuristic=False)

recipe = (1,1)

results_file = "results/experiment_comparing_mcafee_to_sbb.csv"

iterations = 50000

experiment(results_file,mcafee_trade_reduction, "McAfee", recipe=recipe,
           value_ranges   = [(1,1000),(-1000,-1)],
           nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           num_of_iterations = iterations
           )

experiment(results_file,budget_balanced_trade_reduction, "SBB External Competition", recipe=recipe,
           value_ranges   = [(1,1000),(-1000,-1)],
           nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           num_of_iterations = iterations
           )

experiment(results_file,budget_balanced_ascending_auction, "SBB Ascending Prices", recipe=recipe,
           value_ranges   = [(1,1000),(-1000,-1)],
           nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           num_of_iterations = iterations
           )

experiment(results_file,mcafee_without_heuristic, "McAfeeWithoutHeuristic", recipe=recipe,
           value_ranges   = [(1,1000),(-1000,-1)],
           nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           num_of_iterations = iterations
           )
