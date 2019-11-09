#!python3 -m transcrypt -b -m -n -k

from markets import Market
from agents import AgentCategory
import ascending_auction_protocol
from ascending_auction_protocol import budget_balanced_ascending_auction

def output(*args):
    for arg in args:
        document.getElementById("output").value += str(arg) + "\n"

ascending_auction_protocol.set_trace(output)

def demo():
    name = document.getElementById("name-box").value
    output("Hello, " + name)
    market = Market([
        AgentCategory("buyer", [17, 14, 13, 9, 6]),
        AgentCategory("seller", [-1, -2, -3, -4, -5, -7, -8, -10, -11]),
    ])
    output(market)
    output(budget_balanced_ascending_auction(market, [1, 2], max_iterations=1000))


document.getElementById("run-button").addEventListener('click', demo)
