#!python3

"""
Unit-test for multiple-clock strongly-budget-balanced ascending auction.

Author: Erel Segal-Halevi
Since:  2019-08
"""

from markets import Market
from agents import AgentCategory, MAX_VALUE
import ascending_auction_protocol, prices

import logging
ascending_auction_protocol.logger.setLevel(logging.WARNING)
prices.logger.setLevel(logging.WARNING)

from typing import *
import unittest

class TestAscendingAuction(unittest.TestCase):

    ## Helper functions:

    def _check_market(self, market: Market, ps_recipe:List[int], expected_num_of_deals:int, expected_prices:List[float]):
        trade = ascending_auction_protocol.budget_balanced_ascending_auction(market, ps_recipe)
        self.assertEqual(trade.num_of_deals(), expected_num_of_deals)
        self.assertEqual(trade.prices        , expected_prices      )


    ## Unit-tests:

    def test_market_1_1(self):
        """
        Test a standard buyer-seller market.
        """
        def check_1_1(buyers:List[float], sellers:List[float], expected_num_of_deals:int, expected_prices:List[float]):
            market = Market([
                AgentCategory("buyer", buyers),
                AgentCategory("seller", sellers),
            ])
            ps_recipe = [1,1]
            self._check_market(market, ps_recipe, expected_num_of_deals, expected_prices)

        check_1_1(buyers=[9], sellers=[-4],
            expected_num_of_deals=0, expected_prices=[9,-9])
        check_1_1(buyers=[9,8], sellers=[-4],
            expected_num_of_deals=0, expected_prices=[9,-9])
        check_1_1(buyers=[9], sellers=[-4,-3],
            expected_num_of_deals=1, expected_prices=[4,-4])
        check_1_1(buyers=[9,8], sellers=[-4,-3],
            expected_num_of_deals=1, expected_prices=[8,-8])

        # ALL POSITIVE VALUES:
        check_1_1(buyers=[4,3], sellers=[9,8],
            expected_num_of_deals=1, expected_prices=[3,-3])

        # ALL NEGATIVE VALUES:
        check_1_1(buyers=[-4,-3], sellers=[-9,-8],
            expected_num_of_deals=0, expected_prices=[-3,-8])


    def test_market_1_1_1(self):
        """
        Test a three-category market: buyer, mediator, seller
        """

        def check_1_1_1(buyers: List[float], mediators: List[float], sellers: List[float],
                           expected_num_of_deals: int, expected_prices: List[float]):
            market = Market([
                AgentCategory("buyer", buyers),
                AgentCategory("mediator", mediators),
                AgentCategory("seller", sellers),
            ])
            ps_recipe = [1, 1, 1]
            self._check_market(market, ps_recipe, expected_num_of_deals, expected_prices)

        check_1_1_1(buyers=[9,8], mediators=[-1,-2], sellers=[-4,-3],
            expected_num_of_deals=1, expected_prices=[8,-2,-6])
        check_1_1_1(buyers=[9,8], mediators=[-1,-2], sellers=[-4,-3,-10],
            expected_num_of_deals=1, expected_prices=[8,-2,-6])
        check_1_1_1(buyers=[9,8], mediators=[-1,-2], sellers=[-4,-3,-5],
            expected_num_of_deals=1, expected_prices=[8,-3,-5])
        check_1_1_1(buyers=[9,8], mediators=[-1,-2], sellers=[-4,-3,-2],
            expected_num_of_deals=1, expected_prices=[8,-4,-4])
        check_1_1_1(buyers=[9,8,7], mediators=[-1,-2,-3], sellers=[-4,-3,-2],
            expected_num_of_deals=2, expected_prices=[7,-3,-4])
        check_1_1_1(buyers=[9,8,4], mediators=[-1,-2,-3], sellers=[-4,-3,-2],
            expected_num_of_deals=2, expected_prices=[7,-3,-4])


    def test_market_1_2(self):
        """
        Test a two-category market where each deal requires buyer + two sellers
        """

        def check_1_2(buyers: List[float], sellers: List[float], expected_num_of_deals: int,
                              expected_prices: List[float]):
            market = Market([
                AgentCategory("buyer", buyers),
                AgentCategory("seller", sellers),
            ])
            ps_recipe = [1, 2]
            self._check_market(market, ps_recipe, expected_num_of_deals, expected_prices)

        check_1_2(buyers=[9], sellers=[-4, -3],
            expected_num_of_deals=0, expected_prices=[9,-4.5])
        check_1_2(buyers=[9,8,7,6], sellers=[-6,-5,-4,-3,-2,-1],
            expected_num_of_deals=1, expected_prices=[8,-4])
        check_1_2(buyers=[9,8], sellers=[-4,-3,-2,-1],
            expected_num_of_deals=1, expected_prices=[8,-4])
        check_1_2(buyers=[9,8], sellers=[-6,-3,-2,-1],
            expected_num_of_deals=1, expected_prices=[8,-4])
        check_1_2(buyers=[9,8], sellers=[-4,-3,-2,-1],
            expected_num_of_deals=1, expected_prices=[8,-4])

        # PRICE CROSSES ZERO AT FIRST PHASE
        check_1_2(buyers=list(range(20)), sellers=[-3,-2,-1],
            expected_num_of_deals=1, expected_prices=[18,-9])


    def test_market_1_0_1(self):
        """
        Test a three-category market where the middle category has 0 in the recipe (edge case)
        """

        def check_1_0_1(buyers: List[float], mediators: List[float], sellers: List[float],
                           expected_num_of_deals: int, expected_prices: List[float]):
            market = Market([
                AgentCategory("buyer", buyers),
                AgentCategory("mediator", mediators),
                AgentCategory("seller", sellers),
            ])
            ps_recipe = [1, 0, 1]
            self._check_market(market, ps_recipe, expected_num_of_deals, expected_prices)

        check_1_0_1(buyers=[9,8], mediators=[-5,-7], sellers=[-4,-3],
            expected_num_of_deals=1, expected_prices=[8,-MAX_VALUE,-8])

if __name__ == '__main__':
    unittest.main()


