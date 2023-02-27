import json

from durable import engine

RULES = """
{
  "test": {
    "r_0": {
      "all": [
        {
          "m": {
            "subject": "World"
          }
        }
      ],
      "run": "approved"
    }
  }
}
"""


class Actions:  # NOTE: just one way of doing stuff
    def approved(self, m):
        print("Approved!")

    def bla(self, m):
        print("nja")


class MyHost(engine.Host):
    def __init__(self):
        self.actions = Actions()
        super().__init__(None)

    def get_action(self, action_name):
        if hasattr(self.actions, action_name):
            return getattr(self.actions, action_name)
        return super().get_action(action_name)


def main() -> None:
    host = MyHost()
    host.set_rulesets(json.loads(RULES))
    host.post("test", {"subject": "World"})


if __name__ == "__main__":
    main()
