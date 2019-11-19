#!python3

"""
The simulation experiment described by McAfee (1992), Table I (page 448).

Since:  2019-11

Author: Erel Segal-Halevi
"""


from markets import Market
from agents import AgentCategory
from mcafee_protocol import mcafee_trade_reduction

from experiment import experiment

experiment("results/mcafee_experiment.csv", mcafee_trade_reduction, "McAfee", recipe=(1,1),
           value_ranges   = [(1,1000),(-1000,-1)],
           # nums_of_agents = (2, 3, 4, 5, 10, 15, 25, 50, 100, 500, 1000),
           nums_of_agents = (2, 3, 4, 5, 10),
           # num_of_iterations = 50000
           num_of_iterations = 5000
           )


