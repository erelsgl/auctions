#!python3 -m transcrypt -b -m -n -k


import agents

def output(x):
    document.getElementById("output").value += str(x) + "\n"

def test_agents():
    name = document.getElementById("name-box").value
    output("Hello, " + name)
    a = agents.AgentCategory("buyer", [7,9,3,5])
    output(a)
    a.remove_highest_agent()
    output(a)
    a = agents.AgentCategory("buyer", [7,19,3,5])
    output(a)
    a.remove_highest_agent()
    output(a)

document.getElementById("run-button").addEventListener('click', test_agents)
