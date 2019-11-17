#!python3


"""
class TradeWithSinglePrice

Represents a set of deals done in a multi-lateral market.

See also: Market

Author: Erel Segal-Halevi
Since: 2019-08
"""


import math
from agents import AgentCategory



class TradeWithoutPrice:
    """
    Represents a set of deals done in the market, without a particular price.

    >>> t = TradeWithoutPrice([(7,-1),(6,-3),(5,-4)])
    >>> t
    3 deals: [(7, -1), (6, -3), (5, -4)]
    >>> t.num_of_deals()
    3
    >>> t.gain_from_trade()
    10
    """
    def __init__(self, procurement_sets:list):
        self.procurement_sets = procurement_sets

    def num_of_deals(self):
        return len(self.procurement_sets)


    def gain_from_trade(self):
        return sum([sum(ps) for ps in self.procurement_sets])

    def __repr__(self):
        return "{} deals: {}".format(self.num_of_deals(), self.procurement_sets)



class TradeWithSinglePrice:
    """
    Represents the set of deals done in the market,
    assuming there is a single price-vector (one price per category).
    This is the output of the auction mechanisms.

    self.categories: a vector of k AgentCategory objects.
    self.prices:     a vector of k floats - one  per category - representing the price paid by traders of that category.
    self.ps_recipe:  a vector of k integers - one per category - representing the number of traders from this category in each PS.

    >>> t = TradeWithSinglePrice([AgentCategory("buyer", [7,4,2]), AgentCategory("seller",[-1,-3,-5])], [1,1], [0,0])
    >>> print(t)
    buyer: [7, 4, 2]: all 3 agents trade and pay 0
    seller: [-1, -3, -5]: all 3 agents trade and pay 0
    >>> t.num_of_deals()
    3
    >>> t.gain_from_trade()
    4
    """
    def __init__(self, categories:list, ps_recipe:list, prices:list):
        self.categories = categories
        self.num_categories = len(categories)
        self.prices = prices
        self.ps_recipe = ps_recipe

    def num_of_deals(self):
        return min([math.floor(len(category) / count)
             for (category, count) in zip(self.categories, self.ps_recipe)
             if count > 0])

    def gain_from_trade(self):
        return sum([sum(c.values) for c in self.categories])

    def __str__(self):
        num_of_deals = self.num_of_deals()
        if num_of_deals==0:
            return "No trade"
        s = ""
        for i in range(self.num_categories):
            if self.ps_recipe[i]>0:
                category = self.categories[i]
                price = self.prices[i]
                required_agents = self.ps_recipe[i]*num_of_deals
                existing_agents = len(category)
                if existing_agents == required_agents:
                    s += "{}: all {} agents trade and pay {}\n".format(self.categories[i], existing_agents, self.prices[i])
                else:   # existing_agents > required_agents
                    s += "{}: random {} out of {} agents trade and pay {}\n".format(self.categories[i], required_agents, existing_agents, self.prices[i])
        return s.rstrip()





class TradeWithManyPrices:
    """
    Represents a general set of deals done in the market,
    where different agents in the same category may have different prices.

    This general trade scheme is currently not in use.

    self.procurement_sets: a vector of sets of traders. Each set in this vector is responsible to a single "trade-unit".
    self.price_vectors:    price-vector i contains the prices by which the traders in procurement-set i trade.
    self.num_categories:   number of different trader-categories in the market.
    self.category_counts:  for each category, the number of traders from this category that participate in the trade.
    """

    def __init__(self, num_categories:int):
        self.procurement_sets = []
        self.price_vectors = []
        self.num_categories = num_categories
        self.category_counts =[0]*num_categories


    def append(self, ps:list, prices:list):
        self.procurement_sets.append(ps)
        self.price_vectors.append(prices)
        for i in range(self.num_categories):
            if ps[i] is not None:
                self.category_counts[i] += 1

    def __str__(self):
        s = ""
        for i in range(len(self.procurement_sets)):
            s += "  {} trades using price-vector {}\n".format(self.procurement_sets[i], self.price_vectors[i])
        smallest_category_size = min(self.category_counts)
        for i in range(self.num_categories):
            if self.category_counts[i] > smallest_category_size:
                s += "  In category {} there is a lottery: {} out of {} trade\n".format(i, smallest_category_size, self.category_counts[i])
            else:
                s += "  In category {} all {} agents trade\n".format(i, smallest_category_size)
        return s



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
