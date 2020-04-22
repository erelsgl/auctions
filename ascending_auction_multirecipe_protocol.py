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

import logging, sys, math
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
# To enable tracing, set logger.setLevel(logging.INFO)


EPSILON = 0.00001

class TradeWithMultipleRecipes(Trade):
    """
    Represents the outcome of budget_balanced_ascending_auction.
    See there for details.
    """
    def __init__(self, categories:List[AgentCategory], ps_recipes:List[List[int]], prices:List[float]):
        self.categories = categories
        self.num_categories = len(categories)
        self.ps_recipes = ps_recipes
        self.num_recipes = len(ps_recipes)
        map_category_index_to_recipe_indices, common_category_indices, map_recipe_index_to_unique_category_indices = \
            _analyze_recipes(self.num_categories, ps_recipes)
        self.prices = prices
        self.map_category_index_to_recipe_indices = map_category_index_to_recipe_indices

        ps_supported_by_common_categories = min([self.categories[i].size() for i in common_category_indices]) \
            if len(common_category_indices) > 0 \
            else MAX_VALUE

        map_recipe_index_to_ps_supported_by_unique_categories = [
            min([self.categories[i].size() for i in unique_category_indices])
            for unique_category_indices in map_recipe_index_to_unique_category_indices
        ]
        ps_supported_by_unique_categories = sum(map_recipe_index_to_ps_supported_by_unique_categories)

        self.num_of_deals_cache = min(ps_supported_by_unique_categories, ps_supported_by_common_categories)

    def num_of_deals(self):
        return self.num_of_deals_cache

    def gain_from_trade(self, including_auctioneer:bool=True):
        """
        Calculate the total gain-from-trade.
        :param including_auctioneer:  If true, the result includes the profit of the auctioneer.
        If false, the result includes only the profit of the traders.
        This may be smaller when the auction has a surplus, or larger when the auction has a deficit.
        :return:
        """
        if self.num_of_deals_cache==0:
            return 0
        raise NotImplementedError("TradeWithMultipleRecipes.gain_from_trade is not implemented yet")

    def __repr__(self):
        if self.num_of_deals_cache==0:
            return "No trade"
        s = ""
        for category_index in range(self.num_categories):
            recipe_indices = self.map_category_index_to_recipe_indices[category_index]
            if len(recipe_indices)>0:
                category = self.categories[category_index]
                existing_agents = len(category)
                price = self.prices[category_index]
                s += "{}: some of the {} agents trade and pay {}\n".format(category, existing_agents, price)
                # required_agents = self.ps_recipe[i]*self.num_of_deals_cache
                # existing_agents = len(category)
                # if existing_agents == required_agents:
                #     s += "{}: all {} agents trade and pay {}\n".format(category, existing_agents, price)
                # else:   # existing_agents > required_agents
                #     s += "{}: random {} out of {} agents trade and pay {}\n".format(category, required_agents, existing_agents, price)
        return s.rstrip()


def budget_balanced_ascending_auction(
        market:Market, ps_recipes: List[List])->TradeWithMultipleRecipes:
    """
    Calculate the trade and prices using generalized-ascending-auction.
    Allows multiple recipes, but they must all be binary, and must all start with 1. E.g.:
    [ [1,1,0,0], [1,0,1,1] ]
    I.e., there is 1 buyer category and n-1 seller categories.
    Each buyer may wish to buy a different combination of products.

    :param market:     contains a list of k categories, each containing several agents.
    :param ps_recipes: a list of lists of integers, one integer per category.
                       Each integer i represents the number of agents of category i
                       that should be in each procurement-set.
    :return: Trade object, representing the trade and prices.

    >>> # ONE BUYER, ONE SELLER
    >>> market = Market([AgentCategory("buyer", [9.]),  AgentCategory("seller", [-4.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [[1,1]]))
    Traders: [buyer: [9.0], seller: [-4.0]]
    No trade

    >>> market = Market([AgentCategory("buyer", [9.,8.]),  AgentCategory("seller", [-4.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [[1,1]]))
    Traders: [buyer: [9.0, 8.0], seller: [-4.0]]
    No trade

    >>> logger.setLevel(logging.WARNING)
    >>> market = Market([AgentCategory("buyer", [9.]), AgentCategory("seller", [-4.,-3.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [[1,1]]))
    Traders: [buyer: [9.0], seller: [-3.0, -4.0]]
    seller: [-3.0]: all 1 agents trade and pay -4.0
    buyer: [9.0]: all 1 agents trade and pay 4.0

    >>> market = Market([AgentCategory("buyer", [9.,8.]),  AgentCategory("seller", [-4.,-3.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [[1,1]]))
    Traders: [buyer: [9.0, 8.0], seller: [-3.0, -4.0]]
    seller: [-3.0, -4.0]: random 1 out of 2 agents trade and pay -8.0
    buyer: [9.0]: all 1 agents trade and pay 8.0
    """

    num_recipes = len(ps_recipes)
    if num_recipes<1:
        raise ValueError("Empty list of recipes")

    num_categories = market.num_categories
    for i, ps_recipe in enumerate(ps_recipes):
        if len(ps_recipe) != num_categories:
            raise ValueError(
                "There are {} categories but {} elements in PS recipe #{}".
                    format(num_categories, len(ps_recipe), i))
        if any((r!=1 and r!=0) for r in ps_recipe):
            raise ValueError("Currently, the multi-recipe protocol supports only recipes of zeros and ones; {} was given".format(ps_recipe))


    logger.info("\n#### Multi-Recipe Budget-Balanced Ascending Auction\n")
    logger.info(market)
    logger.info("Procurement-set recipes: {}".format(ps_recipes))

    map_category_index_to_recipe_indices, common_category_indices, map_recipe_index_to_unique_category_indices = \
        _analyze_recipes(num_categories, ps_recipes)

    # Calculating the optimal trade with multiple recipes is left for future work.
    # optimal_trade = market.optimal_trade(ps_recipe)[0]
    # logger.info("For comparison, the optimal trade is: %s\n", optimal_trade)

    remaining_market = market.clone()
    prices = SimultaneousAscendingPriceVectors(ps_recipes, -MAX_VALUE)

    # Functions for calculating the number of potential PS that can be supported by a category:
    # Currently we assume a recipe of ones, so the number of potential PS is simply the category size:
    fractional_potential_ps = lambda category_index: remaining_market.categories[category_index].size()
    integral_potential_ps   = lambda category_index: remaining_market.categories[category_index].size()

    while True:
        # find a category with a largest number of potential PS, and increase its price

        largest_common_category_index = max(common_category_indices, key=fractional_potential_ps) \
            if len(common_category_indices)>0 \
            else None
        largest_common_category_size  = fractional_potential_ps(largest_common_category_index) \
            if len(common_category_indices) > 0 \
            else 0
        logger.info("Largest common category is %d and its size is %d", largest_common_category_index, largest_common_category_size)

        map_recipe_index_to_largest_unique_category_index = [
            max(unique_category_indices, key=fractional_potential_ps)
            for unique_category_indices in map_recipe_index_to_unique_category_indices]
        if len(map_recipe_index_to_largest_unique_category_index)==0:
            raise ValueError("No unique categories")
        unique_categories_size = sum([
            fractional_potential_ps(largest_unique_category_index)
            for largest_unique_category_index in map_recipe_index_to_largest_unique_category_index
        ])
        logger.info("Largest unique categories are %s and their total size is %d", map_recipe_index_to_largest_unique_category_index, unique_categories_size)

        if unique_categories_size == 0:
            logger.info("\nThe unique categories %s became empty - no trade!", map_recipe_index_to_largest_unique_category_index)
            logger.info("  Final price-per-unit vector: %s", prices)
            logger.info(remaining_market)
            return TradeWithMultipleRecipes(remaining_market.categories, ps_recipes, prices.map_category_index_to_price())

        if largest_common_category_size >= unique_categories_size:
            logger.info("Raising price of the largest common category (%d) in all recipes", largest_common_category_index)
            main_category_index = largest_common_category_index
            main_category = remaining_market.categories[main_category_index]
            logger.info("%s before: %d agents remain", main_category.name, main_category.size())
            increases = [(main_category_index, main_category.lowest_agent_value(), main_category.name)] * num_recipes

        else:  # largest_common_category_size < unique_categories_size
            logger.info("Raising price of the largest unique categories in each recipe: %s", map_recipe_index_to_largest_unique_category_index)
            increases = []
            for recipe_index, main_category_index in enumerate(map_recipe_index_to_largest_unique_category_index):
                main_category = remaining_market.categories[main_category_index]
                logger.info("%s before: %d agents remain", main_category.name, main_category.size())
                if main_category.size() == 0:
                    logger.info("\nThe %s category became empty - no trade in recipe %d", main_category.name, recipe_index)
                    del ps_recipes[recipe_index]
                    if len(ps_recipes)>0:
                        return budget_balanced_ascending_auction(market, ps_recipes)
                    else:
                        logger.info("\nNo recipes left - no trade!")
                        logger.info("  Final price-per-unit vector: %s", prices)
                        logger.info(remaining_market)
                        return TradeWithMultipleRecipes(remaining_market.categories, ps_recipes, map_category_index_to_price)
                increases.append( (main_category_index, main_category.lowest_agent_value(), main_category.name) )
            if len(increases)==0:
                raise ValueError("No increases!")


        logger.info("Planned increases: %s", increases)
        prices.increase_prices(increases)
        map_category_index_to_price = prices.map_category_index_to_price()
        if prices.status == PriceStatus.STOPPED_AT_ZERO_SUM:
            logger.info("\nPrice crossed zero.")
            logger.info("  Final price-per-unit vector: %s", map_category_index_to_price)
            logger.info(remaining_market)
            return TradeWithMultipleRecipes(remaining_market.categories, ps_recipes, map_category_index_to_price)

        for category_index in range(num_categories):
            category = remaining_market.categories[category_index]
            if map_category_index_to_price[category_index] is not None \
                and category.size()>0 \
                and category.lowest_agent_value() <= map_category_index_to_price[category_index]:
                    category.remove_lowest_agent()
                    logger.info("{} after: {} agents remain,  {} PS supported".format(category.name, category.size(), integral_potential_ps(category_index)))


def _analyze_recipes(num_categories: int, ps_recipes:List[List]):
    """
    >>> map_category_to_recipe, common_categories, map_recipe_to_unique_categories = _analyze_recipes(3, [ [1,1,0] ])
    >>> map_category_to_recipe
    [[0], [0], []]
    >>> common_categories
    set()
    >>> map_recipe_to_unique_categories
    [{0, 1}]
    >>> map_category_to_recipe, common_categories, map_recipe_to_unique_categories = _analyze_recipes(3, [ [1,1,0], [1,0,1] ])
    >>> map_category_to_recipe
    [[0, 1], [0], [1]]
    >>> common_categories
    {0}
    >>> map_recipe_to_unique_categories
    [{1}, {2}]
    >>> map_category_to_recipe, common_categories, map_recipe_to_unique_categories = _analyze_recipes(5, [ [1,1,0,0,0], [1,0,1,1,0] ])
    >>> map_category_to_recipe
    [[0, 1], [0], [1], [1], []]
    >>> common_categories
    {0}
    >>> map_recipe_to_unique_categories
    [{1}, {2, 3}]
    """
    num_recipes = len(ps_recipes)
    map_category_index_to_recipe_indices = []
    common_category_indices = set()
    map_recipe_index_to_unique_category_indices = [set() for _ in ps_recipes]
    for category_index in range(num_categories):
        containing_recipe_indices = [recipe_index for recipe_index in range(num_recipes) if ps_recipes[recipe_index][category_index] > 0]
        map_category_index_to_recipe_indices.append(containing_recipe_indices)
        if len(containing_recipe_indices) == 0:
            pass   # irrelevant category
        elif len(containing_recipe_indices)==1:
            map_recipe_index_to_unique_category_indices[containing_recipe_indices[0]].add(category_index)
        elif len(containing_recipe_indices) == num_recipes:
            common_category_indices.add(category_index)
        else:
            raise ValueError("Category #{} is not common nor unique; it appears in recipes {}".format(category_index, containing_recipe_indices))
    return map_category_index_to_recipe_indices, common_category_indices, map_recipe_index_to_unique_category_indices




if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
