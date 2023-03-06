import json
import pprint
import typing

from durable import engine
from durable.lang import assert_fact, c, get_facts, get_host, m, post, ruleset, when_all


def printFacts(description, facts):
    print("{0}: {1}".format(description, facts))


with ruleset("risk"):

    @when_all(c.first << m.t == "purchase", c.second << m.location != c.first.location)
    # the event pair will only be observed once
    def fraud(c):
        print("Fraud detected -> {0}, {1}".format(c.first.location, c.second.location))
        c.assert_fact({"second": c.second._d})

    @when_all(+m.second)
    def fraud(c):
        print("FC -> {0}".format(c.m))


post("risk", {"t": "purchase", "location": "US"})
post("risk", {"t": "purchase", "location": "CA"})

# assert_fact("risk", {"t": "purchase", "location": "US"})
# assert_fact("risk", {"t": "purchase", "location": "CA"})

if __name__ == "__main__":
    with open("rulesetEvents.json", "w") as f:
        json.dump(
            get_host().get_ruleset("risk").get_definition(),
            f,
            sort_keys=True,
            indent=4,
        )
