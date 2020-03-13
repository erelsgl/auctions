#!python3

"""
Unit-test for multiple-clock strongly-budget-balanced ascending auction.

Author: Erel Segal-Halevi
Since:  2019-08
"""

from markets import Market
from agents import AgentCategory, MAX_VALUE
import ascending_auction_multirecipe_protocol, ascending_auction_test, prices
from ascending_auction_multirecipe_protocol import budget_balanced_ascending_auction

import logging
ascending_auction_multirecipe_protocol.logger.setLevel(logging.WARNING)
prices.logger.setLevel(logging.WARNING)

from typing import *
import unittest

class TestAscendingAuctionWithSingleRecipe(ascending_auction_test.TestAscendingAuction):
    """
    This TestCase class runs all the unittests written for the single-recipe ascending_auction_protocol,
    on the multi-recipe ascending_auction protocol.
    The results should be the same.
    """


    # Override the check_market function so that it uses the multi-recipe protocol instead of the single-recipe protocol.
    def _check_market(self, market: Market, ps_recipe:List[int], expected_num_of_deals:int, expected_prices:List[float]):
        ps_recipes = [ps_recipe]  # a recipe-vector with a single recipe
        trade = ascending_auction_multirecipe_protocol.budget_balanced_ascending_auction(market, ps_recipes)
        self.assertEqual(trade.num_of_deals(), expected_num_of_deals)

        for i, price in enumerate(trade.prices):
            if price==None:
                trade.prices[i]=-MAX_VALUE
        self.assertEqual(trade.prices        , expected_prices      )


    # Override the test of [1,2] recipe, since currently only binary recipes are supported.
    def test_market_1_2(self):
        pass


if __name__ == '__main__':
    unittest.main()


