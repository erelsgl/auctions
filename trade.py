#!python3

from agents import AgentCategory
import math

class TradeWithSinglePrice:
    """
    Represents the set of deals done in the market,
    assuming there is a single price-vector (one price per category).
    This is the output of the auction mechanisms.

    self.categories: a vector of k AgentCategory objects.
    self.prices:     a vector of k floats - one  per category - representing the price paid by traders of that category.
    self.ps_recipe:  a vector of k integers - one per category - representing the number of traders from this category in each PS.
    """
    def __init__(self, categories:list, ps_recipe: list, prices:list):
        self.categories = categories
        self.num_categories = len(categories)
        self.prices = prices
        self.ps_recipe = ps_recipe
        self.number_of_ps = min([math.floor(len(category) / count)
                                 for (category,count) in zip(self.categories,self.ps_recipe)])

    def __str__(self):
        if self.number_of_ps==0:
            return "No trade"
        s = ""
        for i in range(self.num_categories):
            category = self.categories[i]
            price = self.prices[i]
            required_agents = self.ps_recipe[i]*self.number_of_ps
            existing_agents = len(category)
            if existing_agents == required_agents:
                s += "{}: all {} agents trade and pay {}\n".format(self.categories[i], existing_agents, self.prices[i])
            else:   # existing_agents > required_agents
                s += "{}: random {} out of {} agents trade and pay {}\n".format(self.categories[i], required_agents, existing_agents, self.prices[i])
        return s.rstrip()



class Trade:
    """
    Represents the set of deals done in the market.
    This is the output of the auction mechanisms.

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

