import json
import pprint
import typing

from durable import engine
from durable.lang import (
    assert_fact,
    c,
    get_facts,
    get_host,
    m,
    ruleset,
    s,
    update_state,
    when_all,
)


def printFacts(description, facts):
    print("{0}: {1}".format(description, facts))


with ruleset("flow"):
    # state condition uses 's'
    @when_all(s.status == "start")
    def start(c):
        # state update on 's'
        c.s.status = "next"
        print("start")

    @when_all(s.status == "next")
    def next(c):
        c.s.status = "last"
        print("next")

    @when_all(s.status == "last")
    def last(c):
        c.s.status = "end"
        print("last")
        # deletes state at the end
        c.delete_state()


update_state("flow", {"status": "start"})
print("New update set from start")
update_state("flow", {"status": "start"})

if __name__ == "__main__":
    with open("rulesetState.json", "w") as f:
        json.dump(
            get_host().get_ruleset("flow").get_definition(),
            f,
            sort_keys=True,
            indent=4,
        )
