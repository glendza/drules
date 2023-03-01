import json
import pprint
import typing

from durable import engine, lang

RULESET_NAME = "test"


def get_rules_and_actions() -> tuple[dict, dict]:
    with open("ruleset.json") as f:
        content: dict = json.loads(f.read())
    return content.get("ruleset"), content.get("actionsets")


# Dodaj novi fakt
# Izmjeni vrednost postojećeg fakta (bla npr)
# Obriši (reteract) fakt (blaa npr)


def parse_action(action: dict) -> typing.Callable:
    # XXX Factory goes here
    match action.get("action"):
        case "assert_fact":

            def fn(m):
                try:
                    print("Asserting fact!")
                    lang.get_host().assert_fact(
                        RULESET_NAME,
                        *action.get("payload"),
                    )
                except engine.MessageNotHandledException:
                    ...  # TODO: Add logger

            return fn

        case "print":

            def fn(m):
                print("Printing payload!")
                pprint.pprint(*action.get("payload"))

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
        actionset = [
            parse_action(action)
            for action in sorted(
                self.actionsets.get(action_name),
                key=lambda x: x.get("order"),
            )
        ]

        def new_method(m):
            for action in actionset:
                action(m)

        return new_method


def run_rules():
    ruleset, actionsets = get_rules_and_actions()
    lang._main_host = MyHost(ruleset, actionsets)  # XXX Fuck that's ugly
    lang.assert_fact(
        RULESET_NAME,
        {
            "initial_value": 8,
        },
    )


def main() -> None:
    run_rules()


if __name__ == "__main__":
    main()
