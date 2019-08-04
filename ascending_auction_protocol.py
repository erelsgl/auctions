#!python3

from agents import AgentCategory
from markets import Market
from trade import Trade, TradeWithSinglePrice

import math

trace = lambda *x: None  # To enable tracing, set trace=print

MAX_VALUE=1000000    # an upper bound (not necessarily tight) on the agents' values.


class PriceCrossesZeroException(Exception):
    pass


class EmptyCategoryException(Exception):
    pass

class PriceVector:
    """
    Represents a vector of prices - one price for each category of agents
    """
    def __init__(self, num_categories:int, ps_recipe:list, initial_price:float):
        self.prices = [initial_price] * num_categories
        self.ps_recipe = ps_recipe

    def __getitem__(self, category_index:int):
        return self.prices[category_index]

    def __setitem__(self, category_index:int, new_price:float):
        self.prices[category_index] = new_price

    def increase_price_up_to_balance(self, category_index:int, new_price:float):
        """
        Increase the price of the given category to the given value.
        BUT, if the sum of prices crosses zero, the price will be increased only
        to the point where the sum is zero, and then an exception will be raised.
        :param key:
        :param value:
        :return:
        """
        category_count = self.ps_recipe[category_index]
        old_price = self.prices[category_index]
        old_sum = sum([price*count for (price,count) in zip(self.prices,self.ps_recipe)])
        new_sum = old_sum + category_count*(new_price-old_price)
        if old_sum < 0 and new_sum >= 0:
            self.prices[category_index] = old_price - old_sum/category_count
            raise PriceCrossesZeroException()
        else:
            self.prices[category_index] = new_price

    def __str__(self):
        return self.prices.__str__()




def budget_balanced_ascending_auction(market:Market, ps_recipe: list):
    """
    Calculate the trade and prices using generalized-ascending-auction.
    :param market:   contains a list of k categories, each containing several agents.
    :param ps_recipe:  a list of integers, one integer per category.
                       Each integer i represents the number of agents of category i
                       that should be in each procurement-set.
    :return: Trade object, representing the trade and prices.


    >>> # ONE BUYER, ONE SELLER
    >>> market = Market([AgentCategory("buyer", [9.]),  AgentCategory("seller", [-4.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [1,1]))
    Traders: [buyer: [9.0], seller: [-4.0]]
    No trade
    >>> market = Market([AgentCategory("buyer", [9.,8.]),  AgentCategory("seller", [-4.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [1,1]))
    Traders: [buyer: [9.0, 8.0], seller: [-4.0]]
    No trade
    >>> market = Market([AgentCategory("seller", [-4.]), AgentCategory("buyer", [9.,8.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [1,1]))
    Traders: [seller: [-4.0], buyer: [9.0, 8.0]]
    seller: [-4.0]: all 1 agents trade and pay -8.0
    buyer: [9.0]: all 1 agents trade and pay 8.0
    >>> market = Market([AgentCategory("seller", [-4.,-3.]), AgentCategory("buyer", [9.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [1,1]))
    Traders: [seller: [-3.0, -4.0], buyer: [9.0]]
    No trade
    >>> market = Market([AgentCategory("buyer", [9.]), AgentCategory("seller", [-4.,-3.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [1,1]))
    Traders: [buyer: [9.0], seller: [-3.0, -4.0]]
    buyer: [9.0]: all 1 agents trade and pay 4.0
    seller: [-3.0]: all 1 agents trade and pay -4.0
    >>> market = Market([AgentCategory("buyer", [9.,8.]),  AgentCategory("seller", [-4.,-3.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [1,1]))
    Traders: [buyer: [9.0, 8.0], seller: [-3.0, -4.0]]
    buyer: [9.0]: all 1 agents trade and pay 8.0
    seller: [-3.0, -4.0]: random 1 out of 2 agents trade and pay -8.0
    >>> market = Market([AgentCategory("seller", [-4.,-3.]), AgentCategory("buyer", [9.,8.])])
    >>> print(budget_balanced_ascending_auction(market, [1,1]))
    seller: [-3.0]: all 1 agents trade and pay -4.0
    buyer: [9.0, 8.0]: random 1 out of 2 agents trade and pay 4.0
    >>> # ALL POSITIVE VALUES
    >>> market = Market([AgentCategory("buyer1", [4.,3.]), AgentCategory("buyer2", [9.,8.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [1,1]))
    Traders: [buyer1: [4.0, 3.0], buyer2: [9.0, 8.0]]
    buyer1: [4.0]: all 1 agents trade and pay 3.0
    buyer2: [9.0, 8.0]: random 1 out of 2 agents trade and pay -3.0
    >>> # ALL NEGATIVE VALUES
    >>> market = Market([AgentCategory("seller1", [-4.,-3.]), AgentCategory("seller2", [-9.,-8.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [1,1]))
    Traders: [seller1: [-3.0, -4.0], seller2: [-8.0, -9.0]]
    No trade
    >>>
    >>> # ONE BUYER, ONE SELLER, ONE MEDIATOR
    >>> market = Market([AgentCategory("seller", [-4.,-3.]), AgentCategory("buyer", [9.,8.]), AgentCategory("mediator", [-1.,-2.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [1,1,1]))
    Traders: [seller: [-3.0, -4.0], buyer: [9.0, 8.0], mediator: [-1.0, -2.0]]
    seller: [-3.0]: all 1 agents trade and pay -4.0
    buyer: [9.0]: all 1 agents trade and pay 8.0
    mediator: [-1.0, -2.0]: random 1 out of 2 agents trade and pay -4.0
    >>> market = Market([AgentCategory("buyer", [9.,8.]), AgentCategory("mediator", [-1.,-2.]), AgentCategory("seller", [-4.,-3.,-10.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [1,1,1]))
    Traders: [buyer: [9.0, 8.0], mediator: [-1.0, -2.0], seller: [-3.0, -4.0, -10.0]]
    buyer: [9.0]: all 1 agents trade and pay 8.0
    mediator: [-1.0]: all 1 agents trade and pay -2.0
    seller: [-3.0, -4.0]: random 1 out of 2 agents trade and pay -6.0
    >>> market = Market([AgentCategory("buyer", [9.,8.]), AgentCategory("mediator", [-1.,-2.]), AgentCategory("seller", [-4.,-3.,-5.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [1,1,1]))
    Traders: [buyer: [9.0, 8.0], mediator: [-1.0, -2.0], seller: [-3.0, -4.0, -5.0]]
    buyer: [9.0]: all 1 agents trade and pay 8.0
    mediator: [-1.0, -2.0]: random 1 out of 2 agents trade and pay -3.0
    seller: [-3.0, -4.0]: random 1 out of 2 agents trade and pay -5.0
    >>> market = Market([AgentCategory("buyer", [9.,8.]), AgentCategory("mediator", [-1.,-2.]), AgentCategory("seller", [-4.,-3.,-2.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [1,1,1]))
    Traders: [buyer: [9.0, 8.0], mediator: [-1.0, -2.0], seller: [-2.0, -3.0, -4.0]]
    buyer: [9.0]: all 1 agents trade and pay 8.0
    mediator: [-1.0, -2.0]: random 1 out of 2 agents trade and pay -4.0
    seller: [-2.0, -3.0]: random 1 out of 2 agents trade and pay -4.0
    >>> market = Market([AgentCategory("buyer", [9.,8.,7.]), AgentCategory("mediator", [-1.,-2.,-3.]), AgentCategory("seller", [-4.,-3.,-2.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [1,1,1]))
    Traders: [buyer: [9.0, 8.0, 7.0], mediator: [-1.0, -2.0, -3.0], seller: [-2.0, -3.0, -4.0]]
    buyer: [9.0, 8.0]: all 2 agents trade and pay 7.0
    mediator: [-1.0, -2.0]: all 2 agents trade and pay -3.0
    seller: [-2.0, -3.0, -4.0]: random 2 out of 3 agents trade and pay -4.0
    >>> market = Market([AgentCategory("buyer", [9.,8.,4.]), AgentCategory("mediator", [-1.,-2.,-3.]), AgentCategory("seller", [-4.,-3.,-2.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [1,1,1]))
    Traders: [buyer: [9.0, 8.0, 4.0], mediator: [-1.0, -2.0, -3.0], seller: [-2.0, -3.0, -4.0]]
    buyer: [9.0, 8.0]: all 2 agents trade and pay 7.0
    mediator: [-1.0, -2.0]: all 2 agents trade and pay -3.0
    seller: [-2.0, -3.0]: all 2 agents trade and pay -4.0
    >>>
    >>> # ONE BUYER, TWO SELLERS
    >>> market = Market([AgentCategory("buyer", [9.]),  AgentCategory("seller", [-4.,-3.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [1,2]))
    Traders: [buyer: [9.0], seller: [-3.0, -4.0]]
    No trade
    >>> market = Market([AgentCategory("buyer", [9.,8.]),  AgentCategory("seller", [-4.,-3.,-2.,-1.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [1,2]))
    Traders: [buyer: [9.0, 8.0], seller: [-1.0, -2.0, -3.0, -4.0]]
    buyer: [9.0]: all 1 agents trade and pay 8.0
    seller: [-1.0, -2.0, -3.0, -4.0]: random 2 out of 4 agents trade and pay -4.0
    >>> market = Market([AgentCategory("buyer", [9.,8.]),  AgentCategory("seller", [-6.,-3.,-2.,-1.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [1,2]))
    Traders: [buyer: [9.0, 8.0], seller: [-1.0, -2.0, -3.0, -6.0]]
    buyer: [9.0]: all 1 agents trade and pay 8.0
    seller: [-1.0, -2.0, -3.0]: random 2 out of 3 agents trade and pay -4.0
    >>> market = Market([AgentCategory("seller", [-4.,-3.,-2.,-1.]), AgentCategory("buyer", [9.,8.])])
    >>> print(market); print(budget_balanced_ascending_auction(market, [2,1]))
    Traders: [seller: [-1.0, -2.0, -3.0, -4.0], buyer: [9.0, 8.0]]
    seller: [-1.0, -2.0]: all 2 agents trade and pay -3.0
    buyer: [9.0, 8.0]: random 1 out of 2 agents trade and pay 6.0
    """
    if len(ps_recipe) != market.num_categories:
        raise ValueError(
            "There are {} categories but {} elements in the PS recipe".
                format(market.num_categories, len(ps_recipe)))

    trace("\n\n### Budget-Balanced Ascending Auction\n")
    trace(market)

    remaining_market = market.clone()
    prices = PriceVector(market.num_categories, ps_recipe, -MAX_VALUE)
    potential_ps = [0] * market.num_categories

    try:
        # trace("\n## Phase 0: calculate number of PS")
        for i in range(remaining_market.num_categories):
            category = remaining_market.categories[i]
            # prices.increase_price_up_to_balance(i, category.lowest_agent_value() - 1)
            potential_ps[i] = math.floor(
                len(category) / ps_recipe[i])  # num of potential PS that can be supported by this category
            # trace("{}: price increases to {}, {} agents remain, {} PS supported".format(category.name, prices[i], len(category), potential_ps[i]))

        min_potential_ps = min(potential_ps)
        trace("\n## Phase 1: balancing the number of PS to {}".format(min_potential_ps))
        for i in range(remaining_market.num_categories):
            category = remaining_market.categories[i]
            if len(category)==0:  raise EmptyCategoryException()
            while math.floor(len(category) / ps_recipe[i]) > min_potential_ps:
                prices.increase_price_up_to_balance(i, category.lowest_agent_value())
                category.remove_lowest_agent()
                trace("{}: price increases to {}, {} agents remain".format(category.name, prices[i], len(category)))
                if len(category) == 0:  raise EmptyCategoryException()
            potential_ps[i] = math.floor(len(category) / ps_recipe[i])
            trace("{}: price is now {}, {} agents remain, {} PS supported".format(category.name, prices[i], len(category), potential_ps[i]))

        trace("\n## Phase 2: balancing the price")
        while True:
            for i in range(remaining_market.num_categories):
                category = remaining_market.categories[i]
                if len(category) == 0:  raise EmptyCategoryException()
                for j in range(ps_recipe[i]):
                    prices.increase_price_up_to_balance(i, category.lowest_agent_value())
                    category.remove_lowest_agent()
                    trace("{}: price increases to {}, {} agents remain".format(category.name, prices[i], len(category)))
                    if len(category) == 0:  raise EmptyCategoryException()
                potential_ps[i] = math.floor(len(category) / ps_recipe[i])
                trace("{}: price is now {}, {} agents remain, {} PS supported".format(category.name, prices[i], len(category), potential_ps[i]))

    except PriceCrossesZeroException:
        trace("\nPrice crossed zero. Final price vector: {}".format(prices))

    except EmptyCategoryException:
        trace("\nOne of the categories became empty. No trade! Final price vector: {}".format(prices))

    trace(remaining_market)
    return TradeWithSinglePrice(remaining_market.categories, ps_recipe, prices.prices)




if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))

    trace = print
    market = Market([AgentCategory("buyer", [9., 8., 7.]), AgentCategory("mediator", [-1., -2., -3.]), AgentCategory("seller", [-4., -3., -2.])])
    print(budget_balanced_ascending_auction(market, [1, 1, 1]))
    exit(0)

    market1 = Market([AgentCategory("buyer", [11, 9, 7, 5]),  AgentCategory("seller", [-2, -4, -6, -6.5])])
    market2 = Market([AgentCategory("buyer", [11, 9, 7, 5]), AgentCategory("seller",  [-2, -4, -6, -8])])
    market3 = Market([
        AgentCategory("buyer",    [17, 14, 13, 9, 6]),  #   Modify the middle number to see interesting phoenomena
        AgentCategory("seller",   [-1, -4, -5, -8, -11]),
        AgentCategory("mediator", [-1, -3, -6, -7, -10])])

    # budget_balanced_ascending_auction(market1, [1,1])   # there is competition - everything is fine. All PS in the optimal trade enter the actual trade, with the same price vector (6.5, -6.5).
    # budget_balanced_ascending_auction(market2, [1,1])   # there is competition - everything is fine. All PS in the optimal trade enter the actual trade, with the same price vector (6.5, -6.5).
    # budget_balanced_ascending_auction(market3, [1,1,1])   # there is competition - everything is fine. All PS in the optimal trade enter the actual trade, with the same price vector (6.5, -6.5).

    print(budget_balanced_ascending_auction(market1, [1,2]))   # 1 buyer,  2 sellers
    # budget_balanced_ascending_auction(market1, [2,1])   # 2 buyers,  1 seller
