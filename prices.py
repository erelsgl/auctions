#!python3

"""
Defines classes related to price-vectors.

Author: Erel Segal-Halevi
Since:  2019-12
"""

import logging, sys
from typing import *

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

from enum import Enum
class PriceStatus(Enum):
    STOPPED_AT_AGENT_VALUE = 1
    STOPPED_AT_ZERO_SUM = 2


class PriceCrossesZeroException(Exception):
    pass

class AscendingPriceVector:
    """
    Represents a vector of prices - one price for each category of agents.
    The vector is used in ascending-prices auctions: the price can be increased until the price-sum hits zero.
    """
    def __init__(self, ps_recipe:list, initial_price:float):
        self.num_categories = len(ps_recipe)
        self.ps_recipe = ps_recipe
        self.prices = [initial_price] * self.num_categories
        self.status = None  # status of the latest price-increase operation. Of type PriceStatus.

    def __getitem__(self, category_index:int):
        return self.prices[category_index]

    def __setitem__(self, category_index:int, new_price:float):
        self.prices[category_index] = new_price

    def price_sum(self):
        return dot(self.prices, self.ps_recipe)

    def price_sum_without_category(self, category_index:int):
        return self.price_sum() - self.ps_recipe[category_index]*self.prices[category_index]

    def price_sum_after_increase(self, category_index:int, new_price:float):
        """
        :return: the sum of prices after a hypothetical increase of the price in category_index to new_price.
        >>> p = AscendingPriceVector([1, 1, 0, 0], -1000)
        >>> p.price_sum_after_increase(0, 10)
        -990
        >>> p = AscendingPriceVector([1, 0, 1, 1], -1000)
        >>> p.price_sum_after_increase(0, 10)
        -1990
        """
        return self.price_sum_without_category(category_index) + self.ps_recipe[category_index]*new_price

    def increase_price_up_to_balance(self, category_index:int, new_price:float, description:str, sum_upper_bound:float=0):
        """
        Increase the price of the given agent-category to the given value.
        BUT, if the sum of prices crosses zero, the price will be increased only
        to the point where the sum is zero, and the status will be changed to STOPPED_AT_ZERO_SUM.
        :param category_index: index of price to increase.
        :param new_price: the target price.
        :param description: a textual description for logging (e.g. category name).
        :param sum_upper_bound: an upper bound to the price-sum; the increase stops when the sum hits this bound (default is 0).

        >>> # Simple recipe
        >>> p = AscendingPriceVector([1, 1], -1000)
        >>> p.increase_price_up_to_balance(0, 10., "buyer")
        >>> str(p.status)
        'PriceStatus.STOPPED_AT_AGENT_VALUE'
        >>> p.increase_price_up_to_balance(1, -100., "seller")
        >>> str(p.status), p.price_sum()
        ('PriceStatus.STOPPED_AT_AGENT_VALUE', -90.0)
        >>> p.increase_price_up_to_balance(0, 90., "buyer")
        >>> str(p.status), p.price_sum()
        ('PriceStatus.STOPPED_AT_AGENT_VALUE', -10.0)
        >>> p.increase_price_up_to_balance(1, -80., "seller")
        >>> str(p.status), p.price_sum(), p[1]
        ('PriceStatus.STOPPED_AT_ZERO_SUM', 0.0, -90.0)

        >>> # More complex recipe
        >>> p = AscendingPriceVector([2, 1, 0], -1000)
        >>> p.increase_price_up_to_balance(0, 10., "buyer")
        >>> p.status
        <PriceStatus.STOPPED_AT_AGENT_VALUE: 1>
        >>> p.increase_price_up_to_balance(1, -100., "seller")
        >>> str(p.status), p.price_sum()
        ('PriceStatus.STOPPED_AT_AGENT_VALUE', -80.0)
        >>> p.increase_price_up_to_balance(2, 1000., "watcher")
        >>> str(p.status), p.price_sum()
        ('PriceStatus.STOPPED_AT_AGENT_VALUE', -80.0)
        >>> p.increase_price_up_to_balance(0, 60., "buyer")
        >>> str(p.status), p.price_sum(), p[0]
        ('PriceStatus.STOPPED_AT_ZERO_SUM', 0.0, 50.0)

        """
        category_count_in_recipe = self.ps_recipe[category_index]
        sum_without_category = self.price_sum_without_category(category_index)
        new_sum = sum_without_category + category_count_in_recipe*new_price
        if new_sum >= sum_upper_bound:
            fixed_new_price = (sum_upper_bound - sum_without_category) / category_count_in_recipe
            logger.info("{}: while increasing price towards {}, stopped at {} where the price-sum crossed {}".format(description, new_price, fixed_new_price, sum_upper_bound))
            self.prices[category_index] = fixed_new_price
            self.status = PriceStatus.STOPPED_AT_ZERO_SUM
        else:
            logger.info("{}: price increases to {}".format(description, new_price))
            self.prices[category_index] = new_price
            self.status = PriceStatus.STOPPED_AT_AGENT_VALUE

    def __str__(self):
        return self.prices.__str__()


class SimultaneousAscendingPriceVectors:
    """
    Represents a collection of tied price-vectors, corresponding to different PS recipes in the same market.
    All price-vectors must have the same number of categories.
    During price-increases, all price-vectors retain the same sum.


    >>> p1 = AscendingPriceVector([1, 1, 0, 0], -1000)
    >>> p2 = AscendingPriceVector([1, 0, 1, 1], -1000)
    >>> pv = SimultaneousAscendingPriceVectors([p1, p2])
    >>> str(pv)
    "['[-1000, -1000, -1000, -1000]', '[-1000, -1000, -1000, -1000]']"
    """
    def __init__(self, vectors:List[AscendingPriceVector]):
        if len(vectors)==0:
            raise ValueError("Empty list of price-vectors")

        num_categories = vectors[0].num_categories
        price_sum = vectors[0].price_sum()
        for v in vectors:
            if v.num_categories != num_categories:
                raise ValueError("Different category counts: {} vs {}".format(num_categories, v.num_categories))
            if v.price_sum() != price_sum:
                raise ValueError("Different initial price-sum counts: {} vs {}".format(price_sum, v.price_sum()))

        self.vectors = vectors
        self.num_categories = num_categories
        self.status = None  # status of the latest price-increase operation

    def price_sum(self):
        return self.vectors[0].price_sum()

    def __getitem__(self, vector_index:int):
        return self.vectors[vector_index]

    def increase_prices(self, increases:List[Tuple[int,float,str]]):
        """
        Simultaneously increase the prices of all vectors, keeping their sum equal.
        :param increases: a list of tuples; each tuple contains arguments to the increase_prices method of AscendingPriceVector:
            (category_index, new_price, description)

        >>> logger.setLevel(logging.DEBUG)
        >>> p1 = AscendingPriceVector([1, 1, 0, 0], -1000)
        >>> p2 = AscendingPriceVector([1, 0, 1, 1], -1000)
        >>> p2[2] = p2[3] = -500
        >>> pv = SimultaneousAscendingPriceVectors([p1, p2])
        >>> pv.increase_prices ([(0,10,"buyer"), (0,10,"buyer")])
        >>> str(pv)
        "['[10.0, -1000, -1000, -1000]', '[10.0, -1000, -500, -500]'] PriceStatus.STOPPED_AT_AGENT_VALUE"
        >>> pv.increase_prices ([(1,-80, "seller"), (2,-80,"halfseller-A")])
        >>> str(pv)
        "['[10.0, -580.0, -1000, -1000]', '[10.0, -1000, -80.0, -500]'] PriceStatus.STOPPED_AT_AGENT_VALUE"
        >>> pv.increase_prices ([(1,-80, "seller"), (3,-80,"halfseller-B")])
        >>> str(pv)
        "['[10.0, -160.0, -1000, -1000]', '[10.0, -1000, -80.0, -80.0]'] PriceStatus.STOPPED_AT_AGENT_VALUE"
        """
        new_sums = [0]*len(self.vectors)
        for vector_index, vector in enumerate(self.vectors):
            (category_index, new_price, _) = increases[vector_index]
            new_sums[vector_index] = vector.price_sum_after_increase(category_index, new_price)
        min_new_sum = min(0, min(new_sums))
        logger.info("New sums: %s.  Price-increase upper-bounded by %f", new_sums, min_new_sum)

        for vector_index, vector in enumerate(self.vectors):
            (category_index, new_price, description) = increases[vector_index]
            vector.increase_price_up_to_balance(category_index, new_price, description, sum_upper_bound=min_new_sum)

        self.status = PriceStatus.STOPPED_AT_ZERO_SUM if min_new_sum==0 else PriceStatus.STOPPED_AT_AGENT_VALUE


    def __str__(self):
        return str([str(v) for v in self.vectors]) + " " + str(self.status)


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))

