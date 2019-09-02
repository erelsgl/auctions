#!python3

"""
class AgentCategory

Represents a category of traders in a multi-lateral market,
such as "buyers", "sellers", etc.

Since: 2019-08
"""

class AgentCategory:
    """
    Represents a category of single-parametric agents in a market, for example: "buyers".
    The agents are sorted in descending order of their value.

    >>> a = AgentCategory("buyer", [1,6,3,7])
    >>> str(a)
    'buyer: [7, 6, 3, 1]'
    """
    def __init__(self, name:str, values:list):
        self.name = name
        self.values = list(values)
        self.values.sort(reverse=True)

    def __len__(self):
        return len(self.values)

    def __str__(self)->str:
        return "{}: {}".format(self.name, self.values)

    def __repr__(self)->str:
        return self.__str__()

    def append(self, value:float):
        """
        Adds an agent with the given value to the category.
        Keeps the values sorted in descending order.
        :param value: the value of the new agent.
        """
        self.values.append(value)
        self.values.sort(reverse=True)

    def highest_agent_value(self)->float:
        """
        :return: the highest value of an agent in this category.
        """
        return self.values[0]  # Assumes the values are sorted

    def lowest_agent_value(self)->float:
        """
        :return: the lowest value of an agent in this category.
        """
        return self.values[-1]  # Assumes the values are sorted

    def remove_highest_agent(self):
        """
        Removes the highest-valued agent from this category.
        :return:
        """
        del self.values[0]

    def remove_lowest_agent(self):
        """
        Removes the lowest-valued agent from this category.
        :return:
        """
        del self.values[-1]

    def clone(self):
        return AgentCategory(self.name, self.values)


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
