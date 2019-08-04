#!python3

from agents import AgentCategory
from markets import Market
from trade import Trade, TradeWithSinglePrice

trace = lambda *x: None  # To enable tracing, set trace=print

MAX_VALUE=1000000    # an upper bound (not necessarily tight) on the agents' values.


def budget_balanced_trade_reduction(market:Market, ps_recipe:list):
    """
    Calculate the trade and prices using generalized-trade-reduction.
    :param market:   contains a list of k categories, each containing several agents.
    :param ps_recipe:  a list of integers, one integer per category.
                       Each integer i represents the number of agents of category i
                       that should be in each procurement-set.
    :return: Trade object, representing the trade and prices.

    >>> # ONE BUYER, ONE SELLER
    >>> market = Market([AgentCategory("buyer", [9.]),  AgentCategory("seller", [-4.])])
    >>> print(market); print(budget_balanced_trade_reduction(market, [1,1]))
    Traders: [buyer: [9.0], seller: [-4.0]]
    No trade
    >>> market = Market([AgentCategory("buyer", [9.,8.]),  AgentCategory("seller", [-4.])])
    >>> print(market); print(budget_balanced_trade_reduction(market, [1,1]))
    Traders: [buyer: [9.0, 8.0], seller: [-4.0]]
    No trade
    >>> market = Market([AgentCategory("seller", [-4.]), AgentCategory("buyer", [9.,8.])])
    >>> print(market); print(budget_balanced_trade_reduction(market, [1,1]))
    Traders: [seller: [-4.0], buyer: [9.0, 8.0]]
    seller: [-4.0]: all 1 agents trade and pay -8.0
    buyer: [9.0]: all 1 agents trade and pay 8.0
    >>> market = Market([AgentCategory("seller", [-4.,-3.]), AgentCategory("buyer", [9.])])
    >>> print(market); print(budget_balanced_trade_reduction(market, [1,1]))
    Traders: [seller: [-3.0, -4.0], buyer: [9.0]]
    No trade
    >>> market = Market([AgentCategory("buyer", [9.]), AgentCategory("seller", [-4.,-3.])])
    >>> print(market); print(budget_balanced_trade_reduction(market, [1,1]))
    Traders: [buyer: [9.0], seller: [-3.0, -4.0]]
    buyer: [9.0]: all 1 agents trade and pay 4.0
    seller: [-3.0]: all 1 agents trade and pay -4.0
    >>> market = Market([AgentCategory("buyer", [9.,8.]),  AgentCategory("seller", [-4.,-3.])])
    >>> print(market); print(budget_balanced_trade_reduction(market, [1,1]))
    Traders: [buyer: [9.0, 8.0], seller: [-3.0, -4.0]]
    buyer: [9.0]: all 1 agents trade and pay 8.0
    seller: [-3.0, -4.0]: random 1 out of 2 agents trade and pay -8.0
    >>> market = Market([AgentCategory("seller", [-4.,-3.]), AgentCategory("buyer", [9.,8.])])
    >>> print(budget_balanced_trade_reduction(market, [1,1]))
    seller: [-3.0]: all 1 agents trade and pay -4.0
    buyer: [9.0, 8.0]: random 1 out of 2 agents trade and pay 4.0
    >>> # ALL POSITIVE VALUES
    >>> market = Market([AgentCategory("buyer1", [4.,3.]), AgentCategory("buyer2", [9.,8.])])
    >>> print(market); print(budget_balanced_trade_reduction(market, [1,1]))
    Traders: [buyer1: [4.0, 3.0], buyer2: [9.0, 8.0]]
    buyer1: [4.0]: all 1 agents trade and pay 3.0
    buyer2: [9.0, 8.0]: random 1 out of 2 agents trade and pay -3.0
    >>> # ALL NEGATIVE VALUES
    >>> market = Market([AgentCategory("seller1", [-4.,-3.]), AgentCategory("seller2", [-9.,-8.])])
    >>> print(market); print(budget_balanced_trade_reduction(market, [1,1]))
    Traders: [seller1: [-3.0, -4.0], seller2: [-8.0, -9.0]]
    No trade
    >>>
    >>> # ONE BUYER, ONE SELLER, ONE MEDIATOR
    >>> market = Market([AgentCategory("seller", [-4.,-3.]), AgentCategory("buyer", [9.,8.]), AgentCategory("mediator", [-1.,-2.])])
    >>> print(market); print(budget_balanced_trade_reduction(market, [1,1,1]))
    Traders: [seller: [-3.0, -4.0], buyer: [9.0, 8.0], mediator: [-1.0, -2.0]]
    seller: [-3.0]: all 1 agents trade and pay -4.0
    buyer: [9.0]: all 1 agents trade and pay 8.0
    mediator: [-1.0, -2.0]: random 1 out of 2 agents trade and pay -4.0
    >>> market = Market([AgentCategory("buyer", [9.,8.]), AgentCategory("mediator", [-1.,-2.]), AgentCategory("seller", [-4.,-3.,-10.])])
    >>> print(market); print(budget_balanced_trade_reduction(market, [1,1,1]))
    Traders: [buyer: [9.0, 8.0], mediator: [-1.0, -2.0], seller: [-3.0, -4.0, -10.0]]
    buyer: [9.0]: all 1 agents trade and pay 8.0
    mediator: [-1.0]: all 1 agents trade and pay -2.0
    seller: [-3.0, -4.0]: random 1 out of 2 agents trade and pay -6.0
    >>> market = Market([AgentCategory("buyer", [9.,8.]), AgentCategory("mediator", [-1.,-2.]), AgentCategory("seller", [-4.,-3.,-5.])])
    >>> print(market); print(budget_balanced_trade_reduction(market, [1,1,1]))
    Traders: [buyer: [9.0, 8.0], mediator: [-1.0, -2.0], seller: [-3.0, -4.0, -5.0]]
    buyer: [9.0]: all 1 agents trade and pay 8.0
    mediator: [-1.0, -2.0]: random 1 out of 2 agents trade and pay -3.0
    seller: [-3.0, -4.0]: random 1 out of 2 agents trade and pay -5.0
    >>> market = Market([AgentCategory("buyer", [9.,8.]), AgentCategory("mediator", [-1.,-2.]), AgentCategory("seller", [-4.,-3.,-2.])])
    >>> print(market); print(budget_balanced_trade_reduction(market, [1,1,1]))
    Traders: [buyer: [9.0, 8.0], mediator: [-1.0, -2.0], seller: [-2.0, -3.0, -4.0]]
    buyer: [9.0]: all 1 agents trade and pay 8.0
    mediator: [-1.0, -2.0]: random 1 out of 2 agents trade and pay -4.0
    seller: [-2.0, -3.0]: random 1 out of 2 agents trade and pay -4.0
    >>> market = Market([AgentCategory("buyer", [9.,8.,7.]), AgentCategory("mediator", [-1.,-2.,-3.]), AgentCategory("seller", [-4.,-3.,-2.])])
    >>> print(market); print(budget_balanced_trade_reduction(market, [1,1,1]))
    Traders: [buyer: [9.0, 8.0, 7.0], mediator: [-1.0, -2.0, -3.0], seller: [-2.0, -3.0, -4.0]]
    buyer: [9.0, 8.0]: all 2 agents trade and pay 7.0
    mediator: [-1.0, -2.0]: all 2 agents trade and pay -3.0
    seller: [-2.0, -3.0]: all 2 agents trade and pay -4.0
    >>> market = Market([AgentCategory("buyer", [9.,8.,4.]), AgentCategory("mediator", [-1.,-2.,-3.]), AgentCategory("seller", [-4.,-3.,-2.])])
    >>> print(market); print(budget_balanced_trade_reduction(market, [1,1,1]))
    Traders: [buyer: [9.0, 8.0, 4.0], mediator: [-1.0, -2.0, -3.0], seller: [-2.0, -3.0, -4.0]]
    buyer: [9.0, 8.0]: all 2 agents trade and pay 7.0
    mediator: [-1.0, -2.0]: all 2 agents trade and pay -3.0
    seller: [-2.0, -3.0]: all 2 agents trade and pay -4.0
    """
    if len(ps_recipe) != market.num_categories:
        raise ValueError(
            "There are {} categories but {} elements in the PS recipe".
                format(market.num_categories, len(ps_recipe)))

    trace("\n\n### Budget-Balanced Trade Reduction\n")
    trace(market)
    (optimal_trade, remaining_market) = market.optimal_trade()
    for category in remaining_market.categories:
        if len(category)==0:
            category.append(-MAX_VALUE)
    trace("Optimal trade, by increasing GFT, is: {}".format(optimal_trade))
    trace("Remaining market is: {}".format(remaining_market))
    actual_trade = Trade(market.num_categories)
    actual_traders = [None] * market.num_categories
    for i in range(market.num_categories):
        actual_traders[i] = AgentCategory(market.categories[i].name, [])

    latest_prices = None
    for ps in optimal_trade:
        ps = list(ps)
        if latest_prices is None:
            trace("\nCalculating prices for PS {}:".format(ps))
            for pivot_index in range(len(ps)):
                pivot_value = ps[pivot_index]
                pivot_category = market.categories[pivot_index]
                trace("  Looking for external competition to {} with value {}:".
                      format(pivot_category.name, pivot_value))
                best_containing_PS = remaining_market.best_containing_PS(pivot_index, pivot_value)
                best_containing_GFT = sum(best_containing_PS)
                if best_containing_GFT > 0:  # EXTERNAL COMPETITION - KEEP TRADER
                    trace("    best PS is {} with GFT {}. It is positive so it is an external competition.".
                          format(best_containing_PS, best_containing_GFT))
                    prices = market.calculate_prices_by_external_competition(pivot_index, pivot_value, best_containing_PS)
                    trace("    Prices are {}".format(prices))
                    latest_prices = prices
                    actual_trade.append(ps, prices)
                    for i in range(market.num_categories):
                        if ps[i] is not None:
                            actual_traders[i].append(ps[i])
                    break  # done with current PS - move to next PS
                else:  # NO EXTERNAL COMPETITION - REMOVE TRADER
                    trace("    Best PS is {} with GFT {}. It is negative so it is not an external competition.".
                          format(best_containing_PS, best_containing_GFT))
                    trace("    Remove {} {} from trade and add to remaining market".
                          format(pivot_category.name, pivot_value))
                    ps[pivot_index] = None
                    remaining_market.append_trader(pivot_index, pivot_value)
                    trace("    Remaining market is now: {}".format(remaining_market))
        else:
            trace("\nPrices for PS {} are {}".format(ps, latest_prices))
            actual_trade.append(ps, latest_prices)
            for i in range(market.num_categories):
                if ps[i] is not None:
                    actual_traders[i].append(ps[i])

    trace("\nActual trade is:\n{}".format(actual_trade))
    # return actual_trade

    return TradeWithSinglePrice(actual_traders, ps_recipe, latest_prices)


if __name__ == "__main__":
    # import doctest
    # (failures,tests) = doctest.testmod(report=True)
    # print ("{} failures, {} tests".format(failures,tests))

    trace = print
    # market = Market([AgentCategory("buyer", [9., 8., 7.]), AgentCategory("mediator", [-1., -2., -3.]), AgentCategory("seller", [-4., -3., -2.])])
    market = Market([AgentCategory("buyer", [9.]),  AgentCategory("seller", [-4.])])
    print(budget_balanced_trade_reduction(market, [1, 1]))
    exit(0)


    market1 = Market([AgentCategory("buyer", [11, 9, 7, 5]),  AgentCategory("seller", [-2, -4, -6, -6.5])])
    market2 = Market([AgentCategory("buyer", [11, 9, 7, 5]), AgentCategory("seller",  [-2, -4, -6, -8])])
    market3 = Market([
        AgentCategory("buyer",    [17, 14, 13, 9, 6]),  #   Modify the middle number to see interesting phoenomena
        AgentCategory("seller",   [-1, -4, -5, -8, -11]),
        AgentCategory("mediator", [-1, -3, -6, -7, -10])])

    # budget_balanced_trade_reduction(market1, [1,1])   # there is competition - everything is fine. All PS in the optimal trade enter the actual trade, with the same price vector (6.5, -6.5).
    # budget_balanced_trade_reduction(market2, [1,1])   # no competition - reduction required
    budget_balanced_trade_reduction(market3, [1,1])     # no competition - reduction required
