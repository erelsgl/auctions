#!python3


class Market:
    """
    Represents a market with several categories of traders,
    and several traders from each category.
    """

    def __init__(self, categories:list):
        """
        :param categories: a list of k AgentCategory objects.
                           Each such object represents a set of traders
                           that belong to a single category.
        """
        self.categories = categories
        self.num_categories = len(categories)
        self.size_of_smallest_category =  min([len(c) for c in self.categories])


    def append_trader(self, category_index:int, value:float):
        """
        Append a trader to the given category in this market.
        The values in the category remain sorted.
        :param ps: a procurement-set - contains one value for each category.
        """
        self.categories[category_index].append(value)

    def append_PS(self, ps:list):
        """
        Append an entire procurement-set to the market.
        :param ps: a procurement-set - contains one value for each category.
        """
        if len(ps)!=len(self.categories):
            raise(ValueError("Market has {} categories but PS has {} values".format(len(self.categories),len(ps))))
        for i in range(len(ps)):
            self.append_trader(i, ps[i])

    def optimal_trade(self)->tuple:
        """
        :return: a list of procurement-sets, and a remaining market.
        Each PS should contain a single agent from each category.
        Each PS should have a positive gain-from-trade.
        The PS are ordered in ascending order of their GFT.

        >>> market2 = Market([AgentCategory("buyer", [9, 7, 11, 5]), AgentCategory("seller",[-4,-6,-8,-2])])
        >>> str(market2)
        'Traders: [buyer: [11, 9, 7, 5], seller: [-2, -4, -6, -8]]'
        >>> (trade,remaining_market)=market2.optimal_trade()
        >>> trade
        [(7, -6), (9, -4), (11, -2)]
        >>> str(remaining_market)
        'Traders: [buyer: [5], seller: [-8]]'
        >>> market3 = Market([AgentCategory("buyer", [15, 12, 9, 6]),AgentCategory("seller",[-2,-5,-8,-11]),AgentCategory("mediator", [-1, -4, -7, -10])])
        >>> (trade,remaining_market)=market3.optimal_trade()
        >>> trade
        [(12, -5, -4), (15, -2, -1)]
        >>> str(remaining_market)
        'Traders: [buyer: [9, 6], seller: [-8, -11], mediator: [-7, -10]]'
        """
        trade = []
        remaining_market = self.clone()
        for _ in range(self.size_of_smallest_category):
            ps = [c.highest_agent_value() for c in remaining_market.categories]
            if sum(ps) > 0:
                trade.append(tuple(ps))
                for c in remaining_market.categories:
                    c.remove_highest_agent()
        trade.sort(key=lambda ps: sum(ps)) # sort in increasing order of GFT
        return (trade, remaining_market)

    def best_containing_PS(self, category_index:int, value:float):
        """
        Find a procurement-set with the highest GFT that contains the given agent.
        :param category_index: the index of the category that this agent belongs to.
        :param value:          the value of this agent.
        :return:               a PS that contains the given agent plus agents from other categories
                                   (different than category_index),
                               such that the GFT of the given agent plus the other agents is highest.

        >>> market2 = Market([AgentCategory("buyer", [7, 5]), AgentCategory("seller", [-8, -10])])
        >>> market2.best_containing_PS(0, 9)
        (9, -8)
        >>> market2.best_containing_PS(1, -6)
        (7, -6)
        """
        best_PS = [None]*self.num_categories
        for i in range(self.num_categories):
            if i == category_index:
                best_PS[i] = value
            else:
                best_PS[i] = self.categories[i].highest_agent_value()
        return tuple(best_PS)


    def calculate_prices_by_external_competition(self, pivot_index:int, pivot_value:float, best_containing_PS:list)->list:
        """
        Determine the prices for the given procurement-set, based on the external competition found.
        :param ps: a procurement-set - contains one agent from each category.
        :return:   a list of prices - a price per agent. The sum of prices should be 0.
                   Returns None if no competition was found.
        """
        prices = [None]*self.num_categories
        for category_index in range(self.num_categories):
            if category_index==pivot_index:
                prices[category_index] = pivot_value - sum(best_containing_PS)
            else:
                prices[category_index] = best_containing_PS[category_index]
        prices = tuple(prices)
        return prices



    def __str__(self)->str:
        return "Traders: {}".format(self.categories)

    def clone(self):
        return Market([c.clone() for c in self.categories])


