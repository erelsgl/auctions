#!python3

"""
function budget_balanced_ascending_auction
Implementation of a multiple-clock strongly-budget-balanced ascending auction for a multi-lateral market.

Allows multiple recipes, but only of the following kind:

    [1, x, y, z, ...]

where x, y, z, etc. are either 0 or 1.

I.e., there is a single buyer category and n-1 seller categories, and
a single buyer may wish to buy different combinations or products.

The smallest interesting example is:

    [ [1, 1, 0, 0], [1, 0, 1, 1] ]

Author: Erel Segal-Halevi
Since:  2020-03
"""

from agents import AgentCategory, EmptyCategoryException, MAX_VALUE
from markets import Market
from trade import Trade, TradeWithSinglePrice
from prices import SimultaneousAscendingPriceVectors, PriceStatus
from typing import *
from math import ceil,floor

import logging, sys
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
# To enable tracing, set logger.setLevel(logging.INFO)


EPSILON = 0.00001

class TradeWithMultipleRecipes(Trade):
    """
    Represents the outcome of budget_balanced_ascending_auction_twolevels.
    See there for details.
    """
    def __init__(self, categories:List[AgentCategory], ps_recipe_counts, prices:List[float]):
        self.categories = categories
        category_sizes = [len(category) for category in categories]
        supported_PS = [floor(category_size/count) for category_size,count in zip(category_sizes,ps_recipe_counts)]
        self.num_categories = len(categories)
        self.prices = prices
        self.ps_recipe_counts = ps_recipe_counts
        self.num_of_deals_cache = None
        self.num_of_deals_explanation_cache = \
            f"Final traders: {categories}\nFinal prices: {prices}\nFinal category sizes: {category_sizes}\nSupported PSs: {supported_PS}"
        self.gft_cache = None

    def num_of_deals(self):
        return self.num_of_deals_cache

    def gain_from_trade(self, including_auctioneer:bool=True):
        return self.gft_cache

    def __repr__(self):
        if self.num_of_deals_cache==0:
            return "No trade"
        return self.num_of_deals_explanation_cache.rstrip()


def budget_balanced_ascending_auction_twolevels(
        market:Market, ps_recipe_counts: List[Any])->TradeWithMultipleRecipes:
    """
    Calculate the trade and prices using generalized-ascending-auction.
    Allows multiple non-binary recipes, but they must be represented by a *recipe tree* with two levels.

    :param market:           contains a list of k categories, each containing several agents.
                             category 0 is the root; the others are its children.
    :param ps_recipe_counts: Required number r_g for each category g.

    :return: Trade object, representing the trade and prices.

    >>> logger.setLevel(logging.INFO)
    >>> # ONE BUYER, ONE SELLER
    >>> recipe_11 = [1, 1]
    >>>
    >>> market = Market([AgentCategory("buyer", [9.]),  AgentCategory("seller", [-4.])])
    >>> print(market); print(budget_balanced_ascending_auction_twolevels(market, recipe_11))
    Traders: [buyer: [9.0], seller: [-4.0]]
    No trade

    >>> market = Market([AgentCategory("buyer", [9.,8.]),  AgentCategory("seller", [-4.])])
    >>> print(market); print(budget_balanced_ascending_auction_twolevels(market, recipe_11))
    Traders: [buyer: [9.0, 8.0], seller: [-4.0]]
    seller: 1 potential deals, price=-8.0
    buyer: all 1 traders selected, price=8.0
    seller: all 1 traders selected
    1 deals overall

    >>> logger.setLevel(logging.WARNING)
    >>> market = Market([AgentCategory("buyer", [9.]), AgentCategory("seller", [-4.,-3.])])
    >>> print(market); print(budget_balanced_ascending_auction_twolevels(market, recipe_11))
    Traders: [buyer: [9.0], seller: [-3.0, -4.0]]
    No trade

    >>> logger.setLevel(logging.WARNING)
    >>> market = Market([AgentCategory("buyer", [9.,8.]),  AgentCategory("seller", [-4.,-3.])])
    >>> print(market); print(budget_balanced_ascending_auction_twolevels(market, recipe_11))
    Traders: [buyer: [9.0, 8.0], seller: [-3.0, -4.0]]
    seller: 1 potential deals, price=-4.0
    buyer: 1 out of 2 traders selected, price=4.0
    seller: all 1 traders selected
    1 deals overall
    """
    logger.info("\n#### Multi-Recipe Budget-Balanced Ascending Auction\n")
    logger.info(market)

    root_count = ps_recipe_counts[0]
    logger.info("Root category required count:   %d", root_count)
    child_counts = ps_recipe_counts[1:]
    num_recipes = len(child_counts)
    logger.info("Child category required counts: %s", child_counts)
    ps_recipes = [
        [root_count] + recipe_index*[0] + [child_counts[recipe_index]] + (num_recipes-recipe_index-1)*[0]
        for recipe_index in range(num_recipes)]
    logger.info("PS recipes: %s", ps_recipes)
    prices = SimultaneousAscendingPriceVectors(ps_recipes, -MAX_VALUE)

    remaining_market = market.clone()
    while True:
        root_category = remaining_market.categories[0]
        root_category_size = len(root_category)
        normalized_root_category_size = root_category_size / root_count

        child_category_sizes = [len(category) for category in remaining_market.categories[1:]]
        normalized_child_category_size = sum([floor(child_category_size/child_count) for child_category_size,child_count in zip(child_category_sizes,child_counts)])

        logger.info("Root category size: %g, normalized: %g", root_category_size, normalized_root_category_size)
        logger.info("Child category sizes: %s, normalized: %g", child_category_sizes, normalized_child_category_size)

        if normalized_root_category_size > normalized_child_category_size: # increase only the root price
            prices_to_increase = [0]
        else: # increase the children prices
            prices_to_increase = range(1,market.num_categories)

        increases = []
        for category_index in prices_to_increase:
            category = remaining_market.categories[category_index]
            target_price = category.lowest_agent_value() if category.size()>0 else MAX_VALUE
            increases.append((category_index, target_price, category.name))
        
        logger.info("\n")
        # logger.info(remaining_market)
        # logger.info("Largest category indices are %s. Largest category size = %d, combined category size = %d", indices_of_prices_to_increase, largest_category_size, combined_category_size)

        # if combined_category_size == 0:
        #     logger.info("\nCombined category size is 0 - no trade!")
        #     logger.info("  Final price-per-unit vector: %s", prices)
        #     logger.info(remaining_market)
        #     return TradeWithMultipleRecipes(remaining_market.categories, recipe_tree, prices.map_category_index_to_price())

        logger.info("Planned price-increases: %s", increases)
        prices.increase_prices(increases)
        map_category_index_to_price = prices.map_category_index_to_price()

        if prices.status == PriceStatus.STOPPED_AT_ZERO_SUM:
            logger.info("\nPrice crossed zero.")
            logger.info("  Final price-per-unit vector: %s", map_category_index_to_price)
            logger.info(remaining_market)
            return TradeWithMultipleRecipes(remaining_market.categories, ps_recipe_counts, map_category_index_to_price)

        else: # Remove agents who do not want to trade in the new prices:
            for category_index in prices_to_increase:
                category = remaining_market.categories[category_index]
                if map_category_index_to_price[category_index] is not None \
                    and category.size()>0 \
                    and category.lowest_agent_value() <= map_category_index_to_price[category_index]:
                        category.remove_lowest_agent()
                        logger.info("{} after: {} agents remain".format(category.name, category.size()))




if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
