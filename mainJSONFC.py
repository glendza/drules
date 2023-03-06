import json
import pprint
import typing

from durable import engine, lang

RULESET_NAME = "animal"


def printFacts(description, facts):
    print("{0}: {1}".format(description, facts))


def get_rules_and_actions() -> tuple[dict, dict]:
    with open("rulesetJSONFC.json") as f:
        content: dict = json.loads(f.read())
    return content.get("ruleset"), content.get("actionsets")


# Dodaj novi fakt
# Izmjeni vrednost postojećeg fakta (bla npr)
# Obriši (reteract) fakt (blaa npr)


def parse_action(action: dict) -> typing.Callable:
    # XXX Factory goes here
    match action.get("action"):
        case "assert_fact":

            def fn(c):
                try:
                    print("Asserting fact!!!!!!!!!!!!!!!!!!!!!!!")
                    printFacts("Facts that trigers the rule", c.m)
                    c.assert_fact(
                        RULESET_NAME,
                        action.get("payload")[0],
                    )
                    printFacts("Facts", lang.get_host().get_facts(RULESET_NAME))
                except engine.MessageNotHandledException:
                    print("Exceprion add facts")

            return fn

        case "print":

            def fn(c):
                try:
                    print("Printing fact!!!!!!!!!!!!!!!!!!!!!!!")
                    # print(*action.get("payload"))
                    print(c.m)
                except engine.MessageNotHandledException:
                    ...  # TODO: Add logger
                    print("Exceprion print")

            return fn

        case "print_all":

            def fn(c):
                print("Printing ALL fact!!!!!!!!!!!!!!!!!!!!!!!")
                # print(*action.get("payload"))
                print(lang.get_host().get_facts(RULESET_NAME))

            return fn

        case _:
            raise Exception("E jbg sad")


class MyHost(engine.Host):
    def __init__(
        self,
        ruleset_definitions=None,
        actionsets: dict = [],
    ):
        self.actionsets = actionsets
        super().__init__(ruleset_definitions)

    def get_action(self, action_name: str):

        sorted_actions = sorted(
            self.actionsets.get(action_name),
            key=lambda x: x.get("order"),
        )

        actionset = [parse_action(action) for action in sorted_actions]

        def new_method(m):
            for action in actionset:
                action(m)

        return new_method


def run_rules():
    ruleset, actionsets = get_rules_and_actions()
    lang._main_host = MyHost(ruleset, actionsets)  # XXX Fuck that's ugly
    print(lang.get_host().get_ruleset(RULESET_NAME).get_definition())
    lang.assert_fact(
        RULESET_NAME, {"subject": "Kermit", "predicate": "eats", "object": "flies"}
    )
    lang.assert_fact(
        RULESET_NAME, {"subject": "Twity", "predicate": "eats", "object": "worms"}
    )


def main() -> None:
    run_rules()


if __name__ == "__main__":
    main()
