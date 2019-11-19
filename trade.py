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

class Trade:
    """
    An abstract base class.
    Represents a set of deals done in a market.
    This may be the output of an auction mechanism, or an algorithm for computing optimal trade.
    """

    def num_of_deals(self) -> int:
        """
        :return: the number of deals done in this Trade.
        """
        pass

    def gain_from_trade(self)->float:
        """
        :return: the expected gain-from-trade resulting from doing the deals in this Trade.
        """
        pass




class TradeWithMaterialBalance (Trade):
    """
    A materially-balanced trade - a whole number of deals  done in the market.
    Represented by a list of tuples, where each tuple represents the valuations of agents in a particular deal.

    This is the output of an algorithm for finding the optimal trade.

    >>> t = TradeWithMaterialBalance([(7,-1),(6,-3),(5,-4)])
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



class TradeWithSinglePrice (Trade):
    """
    Represents a set of agents trading in the market,
    assuming there is a single price-vector (one price per agent-category).

    This is the output of an auction mechanisms.

    self.categories: a vector of k AgentCategory objects.
    self.prices:     a vector of k floats - one  per category - representing the price paid by traders of that category.
    self.ps_recipe:  a vector of k integers - one per category - representing the number of traders from this category in each PS.

    >>> t = TradeWithSinglePrice([AgentCategory("buyer", [7,4,2]), AgentCategory("seller",[-1,-3,-5])], [1,1], [0,0])
    >>> t
    buyer: [7, 4, 2]: all 3 agents trade and pay 0
    seller: [-1, -3, -5]: all 3 agents trade and pay 0
    >>> t.num_of_deals()
    3
    >>> t.gain_from_trade()
    4.0
    >>> t = TradeWithSinglePrice([AgentCategory("buyer", [7,4,3,2]), AgentCategory("seller",[-1,-3,-5])], [1,1], [0,0])
    >>> t
    buyer: [7, 4, 3, 2]: random 3 out of 4 agents trade and pay 0
    seller: [-1, -3, -5]: all 3 agents trade and pay 0
    >>> t.gain_from_trade()
    3.0
    """
    def __init__(self, categories:list, ps_recipe:list, prices:list):
        self.categories = categories
        self.num_categories = len(categories)
        self.prices = prices
        self.ps_recipe = ps_recipe
        self.num_of_deals_cache = min([math.floor(len(category) / count)
             for (category, count) in zip(self.categories, self.ps_recipe)
             if count > 0])

    def num_of_deals(self):
        return self.num_of_deals_cache

    def gain_from_trade(self):
        if self.num_of_deals_cache==0:
            return 0
        gft = 0
        for i in range(self.num_categories):
            category = self.categories[i]
            agents_per_deal = self.ps_recipe[i]
            gft += sum(category.values)/len(category.values)*self.num_of_deals_cache*agents_per_deal
        return gft

    def __repr__(self):
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



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))