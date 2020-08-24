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
from recipetree import RecipeTree

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
        market:Market, ps_recipes: List[Any])->TradeWithMultipleRecipes:
    """
    Calculate the trade and prices using generalized-ascending-auction.
    Allows multiple recipes, but they must be represented by a *recipe tree*.

    :param market:     contains a list of k categories, each containing several agents.
    :param ps_recipes: a nested list of integers. Each integer represents a category-index.
                       The nested list represents a tree, where each path from root to leaf represents a recipe.
                       For example: [0, [1, None]] is a single recipe with categories {0,1}.
                                    [0, [1, None, 2, None]] is two recipes with categories {0,1} and {0,2}.

    :return: Trade object, representing the trade and prices.

    >>> # ONE BUYER, ONE SELLER
    >>> recipe_11 = [0, [1, None]]
    >>>
    >>> market = Market([AgentCategory("buyer", [9.]),  AgentCategory("seller", [-4.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, recipe_11))
    Traders: [buyer: [9.0], seller: [-4.0]]
    No trade

    >>> market = Market([AgentCategory("buyer", [9.,8.]),  AgentCategory("seller", [-4.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, recipe_11))
    Traders: [buyer: [9.0, 8.0], seller: [-4.0]]
    No trade

    >>> logger.setLevel(logging.WARNING)
    >>> market = Market([AgentCategory("buyer", [9.]), AgentCategory("seller", [-4.,-3.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, recipe_11))
    Traders: [buyer: [9.0], seller: [-3.0, -4.0]]
    seller: [-3.0]: all 1 agents trade and pay -4.0
    buyer: [9.0]: all 1 agents trade and pay 4.0

    >>> market = Market([AgentCategory("buyer", [9.,8.]),  AgentCategory("seller", [-4.,-3.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, recipe_11))
    Traders: [buyer: [9.0, 8.0], seller: [-3.0, -4.0]]
    seller: [-3.0, -4.0]: random 1 out of 2 agents trade and pay -8.0
    buyer: [9.0]: all 1 agents trade and pay 8.0
    """
    logger.info("\n#### Multi-Recipe Budget-Balanced Ascending Auction\n")
    logger.info(market)
    logger.info("Procurement-set recipes: {}".format(ps_recipes))

    remaining_market = market.clone()
    recipe_tree = RecipeTree(remaining_market.categories, ps_recipes)
    logger.info("Tree of recipes: {}".format(recipe_tree.paths_to_leaf()))

    optimal_trade, optimal_GFT = recipe_tree.optimal_trade()
    logger.info("For comparison, the optimal trade is: %s, GFT=%f\n", optimal_trade,optimal_GFT)
    # optimal_trade = market.optimal_trade(ps_recipe)[0]

    #### STOPPED HERE

    prices = SimultaneousAscendingPriceVectors(ps_recipes, -MAX_VALUE)
    while True:
        largest_category_size, indices_of_prices_to_increase = recipe_tree.largest_categories()
        logger.info("Largest category indices are %s and their size is %d", indices_of_prices_to_increase, largest_category_size)

        if largest_category_size == 0:
            logger.info("\nThe largest category became empty - no trade!")
            logger.info("  Final price-per-unit vector: %s", prices)
            logger.info(remaining_market)
            return TradeWithMultipleRecipes(remaining_market.categories, ps_recipes, prices.map_category_index_to_price())

        increases = []
        increases.append((main_category_index, main_category.lowest_agent_value(), main_category.name))

        logger.info("Planned price-increases: %s", increases)
        prices.increase_prices(increases)
        map_category_index_to_price = prices.map_category_index_to_price()

        if prices.status == PriceStatus.STOPPED_AT_ZERO_SUM:
            logger.info("\nPrice crossed zero.")
            logger.info("  Final price-per-unit vector: %s", map_category_index_to_price)
            logger.info(remaining_market)
            return TradeWithMultipleRecipes(remaining_market.categories, ps_recipes, map_category_index_to_price)

        for category_index in range(market.num_categories):
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
