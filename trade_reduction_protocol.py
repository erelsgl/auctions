#!python3

from agents import AgentCategory
from markets import Market
from trade import Trade

trace = lambda *x: None  # To enable tracing, set trace=print


def budget_balanced_trade_reduction(market:Market):
    """
    Calculate the trade and prices using generalized-trade-reduction
    :return:
    """
    trace("\n\n### Budget-Balanced Trade Reduction\n")
    trace(market)
    (optimal_trade, remaining_market) = market.optimal_trade()
    trace("Optimal trade, by increasing GFT, is: {}".format(optimal_trade))
    trace("Remaining market is: {}".format(remaining_market))
    actual_trade = Trade(market.num_categories)

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

    print("\nActual trade is:\n{}".format(actual_trade))
    return actual_trade



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    # print ("{} failures, {} tests".format(failures,tests))

    trace = print
    market1 = Market([AgentCategory("buyer", [11, 9, 7, 5]),  AgentCategory("seller", [-2, -4, -6, -6.5])])
    market2 = Market([AgentCategory("buyer", [11, 9, 7, 5]), AgentCategory("seller",  [-2, -4, -6, -8])])
    market3 = Market([
        AgentCategory("buyer",    [17, 14, 13, 9, 6]),  #   Modify the middle number to see interesting phoenomena
        AgentCategory("seller",   [-1, -4, -5, -8, -11]),
        AgentCategory("mediator", [-1, -3, -6, -7, -10])])

    # budget_balanced_trade_reduction(market1)   # there is competition - everything is fine. All PS in the optimal trade enter the actual trade, with the same price vector (6.5, -6.5).
    # budget_balanced_trade_reduction(market2)   # no competition - reduction required
    budget_balanced_trade_reduction(market3)     # no competition - reduction required
