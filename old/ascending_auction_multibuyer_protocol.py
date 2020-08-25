#!python3

"""
function budget_balanced_ascending_auction
Implementation of a multiple-clock strongly-budget-balanced ascending auction for a multi-lateral market.

Allows multiple recipes, but only of the following kind:

    [ [1,0,0,x], [0,1,0,y], [0,0,1,z] ]

I.e., there are n-1 buyer categories and 1 seller category, and:
* One agent of category 1 buys x units;
* One agent of category 2 buys y units;
* One agent of category 3 buys z units;
etc.

Author: Erel Segal-Halevi
Since:  2019-08
"""

from agents import AgentCategory, EmptyCategoryException, MAX_VALUE
from markets import Market
from trade import Trade
from prices import AscendingPriceVector

import logging, sys
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
# To enable tracing, set logger.setLevel(logging.INFO)

class TradeWithMultipleRecipes(Trade):
    """
    Represents the outcome of budget_balanced_ascending_auction.
    See there for details.
    """
    def __init__(self, categories:list, map_buyer_category_to_seller_count:list, prices:list):
        self.categories = categories
        self.seller_category = categories[-1]
        self.buyer_categories = categories[:-1]
        self.prices = prices
        self.seller_price = prices[-1]
        self.buyer_prices = prices[:-1]
        self.num_units_offered  = len(self.seller_category)
        self.num_units_demanded = sum([len(self.buyer_categories[i])*map_buyer_category_to_seller_count[i] for i in range(len(self.buyer_categories))])
        self.num_of_deals_cache = min(self.num_units_offered, self.num_units_demanded)

    def num_of_deals(self):
        return self.num_of_deals_cache

    def gain_from_trade(self, including_auctioneer=True):
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
        num_of_deals = self.num_of_deals()
        if num_of_deals==0:
            return "No trade"
        s = ""

        category = self.seller_category
        price = self.seller_price
        if self.num_units_offered <= self.num_units_demanded:
            s += "{}: all {} agents trade and pay {}\n".format(category, len(category), price)
        else:
            s += "{}: random {} out of {} agents trade and pay {}\n".format(category, self.num_units_demanded, len(category), price)

        if self.num_units_demanded <= self.num_units_offered:
            for (category,price) in zip(self.buyer_categories, self.buyer_prices):
                s += "{}: all {} agents trade and pay {}\n".format(category, len(category), price)
        else:
            raise ValueError("Too many demanded units - I do not know how to handle this now")

        return s.rstrip()


def budget_balanced_ascending_auction(
        market:Market, ps_recipes: list)->TradeWithMultipleRecipes:
    """
    Calculate the trade and prices using generalized-ascending-auction.
    Allows multiple recipes, but only of the following kind:
    [ [1,0,0,x], [0,1,0,y], [0,0,1,z] ]
    (i.e., there are n-1 buyer categories and 1 seller category.
    One agent of category 1 buys x units; of category 2 buys y units; of category 3 buys z units; etc.)

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

    >>> # ONE BUYER, TWO SELLERS
    >>> market = Market([AgentCategory("buyer", [9.]),  AgentCategory("seller", [-4.,-3.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [[1,2]]))
    Traders: [buyer: [9.0], seller: [-3.0, -4.0]]
    No trade
    >>> market = Market([AgentCategory("buyer", [9., 8., 7., 6.]),  AgentCategory("seller", [-6., -5., -4.,-3.,-2.,-1.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [[1,2]]))
    Traders: [buyer: [9.0, 8.0, 7.0, 6.0], seller: [-1.0, -2.0, -3.0, -4.0, -5.0, -6.0]]
    seller: [-1.0, -2.0, -3.0, -4.0]: random 2 out of 4 agents trade and pay -4.0
    buyer: [9.0]: all 1 agents trade and pay 8.0
    """
    logger.info("\n#### Budget-Balanced Ascending Auction with Multiple Recipes - n-1 buyer categories\n")
    logger.info(market)
    logger.info("Procurement-set recipes: %s", ps_recipes)

    map_buyer_category_to_seller_count = _convert_recipes_to_seller_counts(ps_recipes, market.num_categories)
    logger.info("Map buyer category index to seller count: %s", map_buyer_category_to_seller_count)

    # NOTE: Calculating the optimal trade cannot be done greedily -
    #         it requires solving a restricted instance of Knapsack.
    # optimal_trade = market.optimal_trade(ps_recipe, max_iterations=max_iterations)[0]
    # logger.info("For comparison, the optimal trade is: %s\n", optimal_trade)

    remaining_market = market.clone()
    buyer_categories = remaining_market.categories[:-1]
    num_buyer_categories = market.num_categories-1
    seller_category = remaining_market.categories[-1]


    prices = AscendingPriceVector([1, 1], -MAX_VALUE)
    buyer_price_index = 0
    seller_price_index = 1
    # prices[0] represents the price for all buyer-categories per single unit.
    # prices[1] represents the price for all sellers.
    try:
        num_units_offered  = len(seller_category)
        num_units_demanded = sum([len(buyer_categories[i])*map_buyer_category_to_seller_count[i] for i in range(num_buyer_categories)])
        target_unit_count  = min(num_units_demanded, num_units_offered)
        logger.info("%d units demanded by buyers, %d units offered by sellers, minimum is %d",
            num_units_demanded, num_units_offered, target_unit_count)

        while True:
            logger.info("Prices: %s, Target unit count: %d", prices, target_unit_count)

            price_index = buyer_price_index
            while True:
                num_units_demanded = sum([len(buyer_categories[i]) * map_buyer_category_to_seller_count[i] for i in range(num_buyer_categories)])
                logger.info("  Buyers demand %d units", num_units_demanded)
                if num_units_demanded == 0:                 raise EmptyCategoryException()
                if num_units_demanded <= target_unit_count: break
                map_buyer_category_to_lowest_value = [category.lowest_agent_value() for category in buyer_categories]
                logger.debug("  map_buyer_category_to_lowest_value=%s", map_buyer_category_to_lowest_value)
                map_buyer_category_to_lowest_value_per_unit = [value / count for value,count in zip(map_buyer_category_to_lowest_value,map_buyer_category_to_seller_count)]
                logger.debug("  map_buyer_category_to_lowest_value_per_unit=%s", map_buyer_category_to_lowest_value_per_unit)
                category_index_with_lowest_value_per_unit = min(range(num_buyer_categories), key=lambda i:map_buyer_category_to_lowest_value_per_unit[i])
                category_with_lowest_value_per_unit = buyer_categories[category_index_with_lowest_value_per_unit]
                lowest_value_per_unit = map_buyer_category_to_lowest_value_per_unit[category_index_with_lowest_value_per_unit]
                logger.info("  lowest value per unit is %f, of category %d (%s)", lowest_value_per_unit, category_index_with_lowest_value_per_unit, category_with_lowest_value_per_unit.name)
                prices.increase_price_up_to_balance(price_index, category_with_lowest_value_per_unit.lowest_agent_value()/map_buyer_category_to_seller_count[category_index_with_lowest_value_per_unit], category_with_lowest_value_per_unit.name)
                category_with_lowest_value_per_unit.remove_lowest_agent()

            category    = seller_category
            # logger.info("\n### Step 1a: balancing the sellers (%s)", category.name)
            price_index = seller_price_index
            while True:
                num_units_offered = len(category)
                logger.info("  Sellers offer %d units", num_units_offered)
                if num_units_offered == 0:                 raise EmptyCategoryException()
                if num_units_offered <= target_unit_count: break
                prices.increase_price_up_to_balance(price_index, category.lowest_agent_value(), category.name)
                category.remove_lowest_agent()

            target_unit_count -= 1

    except EmptyCategoryException:
        logger.info("\nOne of the categories became empty. No trade!")
        logger.info("  Final price-per-unit vector: %s", prices)

    # Construct the final price-vector:
    buyer_price_per_unit = prices[buyer_price_index]
    seller_price_per_unit = prices[seller_price_index]
    final_prices = \
        [buyer_price_per_unit * unit_count for unit_count in map_buyer_category_to_seller_count] + \
        [seller_price_per_unit]
    logger.info("  %s", remaining_market)
    return TradeWithMultipleRecipes(remaining_market.categories, map_buyer_category_to_seller_count, final_prices)



def _convert_recipes_to_seller_counts(ps_recipes: list, num_categories:int)->list:
    """
    >>> logger.setLevel(logging.INFO)
    >>> _convert_recipes_to_seller_counts([[1,0,1],[0,1,2]], 3)
    [1, 2]
    >>> _convert_recipes_to_seller_counts([[1,0,0,3],[0,1,0,4],[0,0,1,5]], 4)
    [3, 4, 5]
    """
    map_buyer_category_to_seller_count = [0]*(num_categories-1)
    for ps_recipe in ps_recipes:
        if type(ps_recipe)!=list:
            raise ValueError("Each PS recipe must be a list")
        if len(ps_recipe) != num_categories:
            raise ValueError(
                "There are {} categories but {} elements in the PS recipe {}".
                    format(num_categories, len(ps_recipe), ps_recipe))
        ps_recipe_buyers = ps_recipe[:-1]
        ps_recipe_sellers = ps_recipe[-1]
        nonzero_element_found = False
        for i in range(len(ps_recipe_buyers)):
            if ps_recipe_buyers[i]==0:
                continue
            if nonzero_element_found:
                raise ValueError("i={}: Cannot handle a recipe with many nonzeros: {}".format(i, ps_recipe))
            if ps_recipe_buyers[i]!=1:
                raise ValueError("i={}: Cannot handle a recipe with more than one buyer: {}".format(i, ps_recipe))
            if ps_recipe_buyers[i]==1:
                if map_buyer_category_to_seller_count[i]!=0:
                    raise ValueError("i={}: Cannot handle two recipes with a buyer in the same place: {}".format(i, ps_recipe))
                map_buyer_category_to_seller_count[i] = ps_recipe_sellers
                nonzero_element_found=True
    return map_buyer_category_to_seller_count





if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
