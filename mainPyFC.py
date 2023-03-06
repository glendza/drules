import json
import pprint
import typing

from durable import engine
from durable.lang import assert_fact, get_facts, get_host, m, ruleset, when_all


def printFacts(description, facts):
    print("{0}: {1}".format(description, facts))


with ruleset("animal"):
    # will be triggered by 'Kermit eats flies'
    @when_all((m.predicate == "eats") & (m.object == "flies"))
    def frog(c):
        print("Triger rule 1:")
        printFacts("Facts that trigers the rule", c.m)
        printFacts("All facts before assert", get_host().get_facts("animal"))
        c.assert_fact({"subject": c.m.subject, "predicate": "is", "object": "frog"})
        printFacts("All facts", get_host().get_facts("animal"))

    @when_all((m.predicate == "eats") & (m.object == "worms"))
    def bird(c):
        print("Triger rule 2:")
        printFacts("Facts that trigers the rule", c.m)
        c.assert_fact({"subject": c.m.subject, "predicate": "is", "object": "bird"})
        printFacts("All facts", get_host().get_facts("animal"))

    # will be chained after asserting 'Kermit is frog'
    @when_all((m.predicate == "is") & (m.object == "frog"))
    def green(c):
        print("Triger rule 3:")
        printFacts("Facts that trigers the rule", c.m)
        c.assert_fact({"subject": c.m.subject, "predicate": "is", "object": "green"})
        printFacts("All facts", get_host().get_facts("animal"))

    @when_all((m.predicate == "is") & (m.object == "bird"))
    def black(c):
        print("Triger rule 4:")
        printFacts("Facts that trigers the rule", c.m)
        c.assert_fact({"subject": c.m.subject, "predicate": "is", "object": "black"})
        printFacts("All facts", get_host().get_facts("animal"))

    @when_all(+m.subject)
    def output(c):
        print("Fact: {0} {1} {2}".format(c.m.subject, c.m.predicate, c.m.object))


assert_fact("animal", {"subject": "Kermit", "predicate": "eats", "object": "flies"})
assert_fact("animal", {"subject": "Twity", "predicate": "eats", "object": "worms"})

if __name__ == "__main__":
    with open("rulesetFC.json", "w") as f:
        json.dump(
            get_host().get_ruleset("animal").get_definition(),
            f,
            sort_keys=True,
            indent=4,
        )
