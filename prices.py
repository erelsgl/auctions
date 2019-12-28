#!python3

"""
Defines classes related to price-vectors.

Author: Erel Segal-Halevi
Since:  2019-12
"""

import logging, sys

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
# To enable tracing, set logger.setLevel(logging.INFO)


def dot(xx:list,yy:list):
    """
    Dot product of two lists.
    >>> dot([1,2,3],[4,5,6])
    32
    """
    return sum([x*y for (x,y) in zip(xx,yy)])

class PriceCrossesZeroException(Exception):
    pass

class AscendingPriceVector:
    """
    Represents a vector of prices - one price for each category of agents.
    The vector is used in ascending-prices auctions: the price can be increased until the price-sum hits zero.
    """
    def __init__(self, num_categories:int, ps_recipe:list, initial_price:float):
        self.prices = [initial_price] * num_categories
        self.ps_recipe = ps_recipe

    def __getitem__(self, category_index:int):
        return self.prices[category_index]

    def __setitem__(self, category_index:int, new_price:float):
        self.prices[category_index] = new_price

    def increase_price_up_to_balance(self, category_index:int, new_price:float, description:str):
        """
        Increase the price of the given category to the given value.
        BUT, if the sum of prices crosses zero, the price will be increased only
        to the point where the sum is zero, and then an exception will be raised.
        :param key:
        :param value:
        :return:
        """
        category_count_in_recipe = self.ps_recipe[category_index]
        old_price = self.prices[category_index]
        old_sum = dot(self.prices,self.ps_recipe)
        new_sum = old_sum + category_count_in_recipe*(new_price-old_price)
        if old_sum < 0 and new_sum >= 0:
            fixed_new_price = old_price - old_sum/category_count_in_recipe
            logger.info("{}: while increasing price towards {}, stopped at {} where the price-sum crossed zero".format(description, new_price, fixed_new_price))
            self.prices[category_index] = fixed_new_price
            raise PriceCrossesZeroException()
        else:
            logger.info("{}: price increases to {}".format(description, new_price))
            self.prices[category_index] = new_price

    def __str__(self):
        return self.prices.__str__()




if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    p = AscendingPriceVector(2, [1, 1], -1000)
    try:
        p.increase_price_up_to_balance(0, 10., "buyer")
        p.increase_price_up_to_balance(1, -100., "seller")
        p.increase_price_up_to_balance(0, 90., "buyer")
        p.increase_price_up_to_balance(1, -80., "seller")
        p.increase_price_up_to_balance(0, 110., "buyer")
    except PriceCrossesZeroException:
        print(p)  # should be [90, -90]
        assert(p[0]==90.0)
        assert(p[1]==-90.0)

