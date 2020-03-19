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


# @unittest.skip("save time")
class TestAscendingAuctionWithSingleRecipe(ascending_auction_test.TestAscendingAuction):
# class TestAscendingAuctionWithSingleRecipe(unittest.TestCase):
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
        self.assertEqual(trade.prices, expected_prices)


    # Override the test of [1,2] recipe, since currently only binary recipes are supported.
    def test_market_1_2(self):
        pass



class TestAscendingAuctionWithTwoRecpies(unittest.TestCase):
    """
    This TestCase class runs all the unittests written for the single-recipe ascending_auction_protocol,
    on the multi-recipe ascending_auction protocol.
    The results should be the same.
    """


    def _check_market(self, market: Market, ps_recipes:List[List[int]], expected_num_of_deals:int, expected_prices:List[float]):
        trade = ascending_auction_multirecipe_protocol.budget_balanced_ascending_auction(market, ps_recipes)
        self.assertEqual(trade.num_of_deals(), expected_num_of_deals)
        # for i, price in enumerate(trade.prices):
        #     if price==None:
        #         trade.prices[i]=-MAX_VALUE
        for i, price in enumerate(expected_prices):
            if price is not None:
                self.assertEqual(trade.prices[i], expected_prices[i])


    def test_market_110_101(self):
        """
        Unit-tests with two recipes: [1,1,0] and [1,0,1].
        Note that the two latter categories are equivalent,
        so we expect the results to be identical to a single recipe [1,1].
        :return:
        """

        def check_110_101(buyers: List[float], sellersA: List[float], sellersB: List[float],
                           expected_num_of_deals: int, expected_prices: List[float]):
            market = Market([
                AgentCategory("buyer", buyers),
                AgentCategory("sellerA", sellersA),
                AgentCategory("sellerB", sellersB),
            ])
            ps_recipes = [[1, 1, 0], [1, 0, 1]]
            self._check_market(market, ps_recipes, expected_num_of_deals, expected_prices)

        check_110_101(buyers=[9,8], sellersA=[-4], sellersB=[-3],
            expected_num_of_deals=1, expected_prices=[8,-8,-8])

        # The following checks are based on the following:
        # check_1_1(buyers=[19,17,15,13,11,9], sellers=[-12,-10,-8,-6,-4,-2],
        #     expected_num_of_deals=4, expected_prices=[11,-11])

        check_110_101(buyers=[19,17,15,13,11,9], sellersA=[], sellersB=[-12,-10,-8,-6,-4,-2],
            expected_num_of_deals=4, expected_prices=[11,None,-11])
        check_110_101(buyers=[19,17,15,13,11,9], sellersA=[-12], sellersB=[-10,-8,-6,-4,-2],
            expected_num_of_deals=4, expected_prices=[11,None,-11])
        check_110_101(buyers=[19,17,15,13,11,9], sellersA=[-4,-2], sellersB=[-12,-10,-8,-6],
            expected_num_of_deals=4, expected_prices=[11,-11,-11])
        check_110_101(buyers=[19,17,15,13,11,9], sellersA=[-10,-4], sellersB=[-12,-8,-6,-2],
            expected_num_of_deals=4, expected_prices=[11,-11,-11])
        check_110_101(buyers=[19,17,15,13,11,9], sellersA=[-12,-10,-8,-6,-4,-2], sellersB=[],
            expected_num_of_deals=4, expected_prices=[11,-11,None])


    def test_market_1100_1011(self):
        """
        Unit-tests with two recipes: [1,1,0,0] and [1,0,1,1].
        This is the smallest case in which multi-recipe substantially differs than single-recipe.
        :return:
        """

        def check_1100_1011(buyers: List[float], sellers: List[float], producers: List[float], movers: List[float],
                           expected_num_of_deals: int, expected_prices: List[float]):
            market = Market([
                AgentCategory("buyer", buyers),
                AgentCategory("seller", sellers),
                AgentCategory("producer", producers),
                AgentCategory("mover", movers),
            ])
            ps_recipes = [[1, 1, 0, 0], [1, 0, 1, 1]]
            self._check_market(market, ps_recipes, expected_num_of_deals, expected_prices)

        # ascending_auction_multirecipe_protocol.logger.setLevel(logging.INFO)
        # prices.logger.setLevel(logging.INFO)
        check_1100_1011(buyers=[19, 17, 15, 13, 11, 9], sellers=[-12, -10, -8, -6, -4, -2], producers=[], movers=[],
            expected_num_of_deals=4, expected_prices=[11.0, -11.0, None, None])
        ascending_auction_multirecipe_protocol.logger.setLevel(logging.WARNING)
        prices.logger.setLevel(logging.WARNING)
        check_1100_1011(buyers=[19, 17, 15, 13, 11, 9], sellers=[], producers=[-6,-5,-4,-3,-2,-1], movers=[-6,-5,-4,-3,-2,-1],
            expected_num_of_deals=4, expected_prices=[11, None, -5, -6])


if __name__ == '__main__':
    unittest.main()

