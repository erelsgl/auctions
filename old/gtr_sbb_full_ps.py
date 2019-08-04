"""
Implementation of GTR SBB mechanisms.
"""

trace = print


class AgentCategory:
    """
    ‎This class represents a category of single-parametric agents, for example: buyers.
    The agents are sorted in descending order of their value.

    >>> AgentCategory("buyer", [1,6,3,7])
    buyer: [7, 6, 3, 1]
    """
    def __init__(self, name:str, values:list):
        self.name = name
        self.values = values
        self.values.sort(reverse=True)

    def __len__(self):
        return len(self.values)

    def __repr__(self)->str:
        return "{}: {}".format(self.name, self.values)

    def append(self, value:float):
        self.values.append(value)
        self.values.sort(reverse=True)

    def clone(self):
        return AgentCategory(self.name, list(self.values))


class Market:
    def __init__(self, categories:list):
        """
        :param categories: a list of AgentCategory objects.
        """
        self.categories = categories
        self.size_of_smallest_category =  min([len(c) for c in self.categories])


    def optimal_trade(self)->tuple:
        """
        :return: a list of procurement-sets, and a remaining market.
        Each PS should contain a single agent from each category.
        Each PS should have a positive gain-from-trade.
        The PS are ordered in ascending order of their GFT.

        >>> market2 = Market([AgentCategory("buyer", [9, 7, 11, 5]), AgentCategory("seller",[-4,-6,-8,-2])])
        >>> market2
        [buyer: [11, 9, 7, 5], seller: [-2, -4, -6, -8]]
        >>> (trade,remaining_market)=market2.optimal_trade()
        >>> trade
        [(7, -6), (9, -4), (11, -2)]
        >>> remaining_market
        [buyer: [5], seller: [-8]]
        >>> market3 = Market([AgentCategory("buyer", [15, 12, 9, 6]),AgentCategory("seller",[-2,-5,-8,-11]),AgentCategory("mediator", [-1, -4, -7, -10])])
        >>> (trade,remaining_market)=market3.optimal_trade()
        >>> trade
        [(12, -5, -4), (15, -2, -1)]
        >>> remaining_market
        [buyer: [9, 6], seller: [-8, -11], mediator: [-7, -10]]
        """
        trade = []
        remaining_market = Market([c.clone() for c in self.categories])
        for _ in range(self.size_of_smallest_category):
            ps = [c.values[0] for c in remaining_market.categories]
            if sum(ps) > 0:
                trade.append(tuple(ps))
                for c in remaining_market.categories:
                    del c.values[0]
        trade.sort(key=lambda ps: sum(ps)) # sort in increasing order of GFT
        return (trade, remaining_market)

    def append_PS(self, ps:list):
        """
        Append procurement-set to the market.
        :param ps: a procurement-set - contains one value for each category.
        """
        if len(ps)!=len(self.categories):
            raise(ValueError("Market has {} categories but PS has {} values".format(len(self.categories),len(ps))))
        for i in range(len(ps)):
            self.categories[i].append(ps[i])

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
        best_PS = [None]*len(self.categories)
        for i in range(len(self.categories)):
            if i == category_index:
                best_PS[i] = value
            else:
                best_PS[i] = self.categories[i].values[0]
        return tuple(best_PS)


    def calculate_prices(self, ps:list)->list:
        """
        Determine the prices for the given procurement-set.
        :param ps: a procurement-set - contains one agent from each category.
        :return:   a list of prices - a price per agent. The sum of prices should be 0.
                   Returns None if no competition was found.
        """
        trace("\nCalculating prices for PS {}:".format(ps))
        trace("  Remaining market is: {}".format(self))
        ps = list(ps)
        for pivot_index in range(len(ps)):
            pivot_value = ps[pivot_index]
            pivot_category = self.categories[pivot_index]
            trace("  Looking for external competition to {} with value {}:".format(pivot_category.name, pivot_value))
            best_containing_PS = self.best_containing_PS(pivot_index, pivot_value)
            best_containing_GFT = sum(best_containing_PS)
            if best_containing_GFT>0:
                trace("    best PS is {} with GFT {}. It is positive so it is an external competition.".format(best_containing_PS, best_containing_GFT))
                prices = [None]*len(ps)
                for category_index in range(len(ps)):
                    if category_index==pivot_index:
                        prices[category_index] = pivot_value - best_containing_GFT
                    else:
                        prices[category_index] = best_containing_PS[category_index]
                prices = tuple(prices)
                return prices
            else:
                trace("    Best PS is {} with GFT {}. It is negative so it is not an external competition.".format(best_containing_PS, best_containing_GFT))
                trace("    Remove {} {} from trade and add him to remaining market".format(pivot_category.name, pivot_value))
                pivot_category.append(pivot_value)
                trace("    Remaining market is: {}".format(self))
                ps[pivot_index] = None
        return None  # could not find appropriate prices


    def calculate_trade(self):
        """
        Calculate the trade and prices using generalized-trade-reduction
        :return:
        """
        trace("Market is: {}".format(self))
        (optimal_trade, remaining_market) = self.optimal_trade()
        trace("Optimal trade is: {}".format(optimal_trade))
        actual_trade = []

        for ps in optimal_trade:
            prices = remaining_market.calculate_prices(ps)
            if prices is None:
                trace("Could not find prices - removing PS")
                remaining_market.append_PS(ps)
            else:
                trace("Prices are {}".format(prices))
                actual_trade.append((ps, prices))
        print("\nActual trade is: {}".format(actual_trade))
        return actual_trade


    def __repr__(self)->str:
        return str(self.categories)



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    # print ("{} failures, {} tests".format(failures,tests))

    market1 = Market([AgentCategory("buyer", [11, 9, 7, 5]),  AgentCategory("seller", [-2, -4, -6, -6.5])])
    market2 = Market([AgentCategory("buyer", [11, 9, 7, 5]), AgentCategory("seller",  [-2, -4, -6, -8])])
    market3 = Market([AgentCategory("buyer", [15, 12, 9, 6]), AgentCategory("seller", [-2, -5, -8, -11]), AgentCategory("mediator", [-1, -4, -7, -10])])

    # market1.budget_balanced_trade_reduction()   # there is competition - everything is fine
    market2.calculate_trade()  # There is no competition - how to proceed?
