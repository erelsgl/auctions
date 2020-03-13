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
from prices import AscendingPriceVector, SimultaneousAscendingPriceVectors, PriceStatus
from typing import *

import logging, sys
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
# To enable tracing, set logger.setLevel(logging.INFO)

class TradeWithMultipleRecipes(Trade):
    """
    Represents the outcome of budget_balanced_ascending_auction.
    See there for details.
    """
    def __init__(self, categories:List[AgentCategory], ps_recipes:List[List[int]], prices:List[float]):
        self.categories = categories
        self.num_categories = len(categories)
        self.ps_recipes = ps_recipes
        self.map_category_index_to_recipe_indices = _map_category_index_to_containing_recipe_indices(self.num_categories, ps_recipes)
        self.prices = prices
        self.num_of_deals_cache = None   # TODO: calculate

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
    num_categories = market.num_categories
    for i, ps_recipe in enumerate(ps_recipes):
        if len(ps_recipe) != num_categories:
            raise ValueError(
                "There are {} categories but {} elements in PS recipe #{}".
                    format(num_categories, len(ps_recipe), i))
        if any(r!=1 for r in ps_recipe):
            raise ValueError("Currently, the multi-recipe protocol supports only recipes of ones; {} was given".format(ps_recipe))


    logger.info("\n#### Budget-Balanced Ascending Auction\n")
    logger.info(market)
    logger.info("Procurement-set recipes: {}".format(ps_recipes))

    map_category_index_to_recipe_indices = _map_category_index_to_containing_recipe_indices(num_categories, ps_recipes)
    relevant_category_indices = [i for i in range(num_categories) if len(map_category_index_to_recipe_indices[i])>0]

    # Calculating the optimal trade with multiple recipes is left for future work.
    # optimal_trade = market.optimal_trade(ps_recipe)[0]
    # logger.info("For comparison, the optimal trade is: %s\n", optimal_trade)

    remaining_market = market.clone()
    price_vectors = [AscendingPriceVector(ps_recipe, -MAX_VALUE) for ps_recipe in ps_recipes]
    prices = SimultaneousAscendingPriceVectors(price_vectors)

    # Functions for calculating the number of potential PS that can be supported by a category:
    # Currently we assume a recipe of ones, so the number of potential PS is simply the category size:
    fractional_potential_ps = lambda category_index: remaining_market.categories[category_index].size()
    integral_potential_ps   = lambda category_index: remaining_market.categories[category_index].size()

    while True:
        # find a category with a largest number of potential PS, and increase its price
        main_category_index = max(relevant_category_indices, key=fractional_potential_ps)
        main_category = remaining_market.categories[main_category_index]
        logger.info("{} before: {} agents remain,  {} PS supported".format(main_category.name, main_category.size(), integral_potential_ps(main_category_index)))

        # TODO: Category that becomes empty rules out only recipes that contain it - other recipes may remain active!
        # if category.size() == 0:
        #     logger.info("\nOne of the categories became empty. No trade!")
        #     logger.info("  Final price-per-unit vector: %s", prices)
        #     break

        increases = _calculate_price_increases(remaining_market, ps_recipes, map_category_index_to_recipe_indices, main_category_index)
        prices.increase_prices(increases)
        map_category_index_to_price = prices.map_category_index_to_price()

        if prices.status == PriceStatus.STOPPED_AT_ZERO_SUM:
            logger.info("\nPrice crossed zero.")
            logger.info("  Final price-per-unit vector: %s", map_category_index_to_price)
            break

        for category_index in relevant_category_indices:
            category = remaining_market.categories[category_index]
            if category.lowest_agent_value() <= map_category_index_to_price[category_index]:
                category.remove_lowest_agent()
                logger.info("{} after: {} agents remain,  {} PS supported".format(category.name, category.size(), integral_potential_ps(category_index)))

    logger.info(remaining_market)
    return TradeWithMultipleRecipes(remaining_market.categories, ps_recipes, map_category_index_to_price)


def _map_category_index_to_containing_recipe_indices(num_categories: int, ps_recipes:List[List]):
    """
    >>> _map_category_index_to_containing_recipe_indices(5, [ [1,1,0,0,0], [1,0,1,1,0] ])
    [[0, 1], [0], [1], [1], []]
    """
    num_recipes = len(ps_recipes)
    return [
        [recipe_index for recipe_index in range(num_recipes) if ps_recipes[recipe_index][category_index] > 0]
        for category_index in range(num_categories)
    ]


def _calculate_price_increases(market:Market, ps_recipes:List[List], map_category_index_to_recipe_indices:List[List], main_category_index:int):
    """
    Calculate the pairs (category_index, new_price) for simultaneous price-increase for different PS recipes.

    >>> market = Market([AgentCategory("buyer", [9,8,7,6]),  AgentCategory("seller", [-1,-2,-3,-4]),  AgentCategory("sel", [-5,-6,-7,-8]),  AgentCategory("ler", [-9,-10,-11,-12])])
    >>> ps_recipes = [[1,1,0,0],[1,0,1,1]]
    >>> map_category_index_to_recipe_indices = _map_category_index_to_containing_recipe_indices(market.num_categories, ps_recipes)
    >>> _calculate_price_increases (market, ps_recipes, map_category_index_to_recipe_indices, main_category_index=0)
    [(0, 6, 'buyer'), (0, 6, 'buyer')]
    >>> _calculate_price_increases (market, ps_recipes, map_category_index_to_recipe_indices, main_category_index=1)
    [(1, -4, 'seller'), (2, -8, 'sel')]
    >>> _calculate_price_increases (market, ps_recipes, map_category_index_to_recipe_indices, main_category_index=2)
    [(1, -4, 'seller'), (2, -8, 'sel')]
    >>> _calculate_price_increases (market, ps_recipes, map_category_index_to_recipe_indices, main_category_index=3)
    [(1, -4, 'seller'), (3, -12, 'ler')]
    """
    increases = []
    main_category = market.categories[main_category_index]
    for (recipe_index, recipe) in enumerate(ps_recipes):
        if recipe[main_category_index] > 0:  # If a recipe contains the maximum-size category - increase the category's price in this recipe's vector.
            increases.append((main_category_index, main_category.lowest_agent_value(), main_category.name))
        else:  # Otherwise, increase some other category, such that the sum of all recipes main_category the same
            possible_other_category_indices = [
                category_index for category_index in range(market.num_categories)
                if map_category_index_to_recipe_indices[category_index] == [recipe_index]
            ]
            if len(possible_other_category_indices)==0:
                raise ValueError("Cannot find a category that is unique to this recipe!")
            other_category_index = possible_other_category_indices[0]
            other_category = market.categories[other_category_index]
            increases.append((other_category_index, other_category.lowest_agent_value(), other_category.name))
    return increases



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
