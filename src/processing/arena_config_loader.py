import os
from typing import Any, Dict, Hashable

import yaml


class ArenaConfigLoader(yaml.SafeLoader):
    """Loader with custom constructors for the custom tags (e.g. !ArenaConfig) in the configuration YAMLs."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.add_constructor("!Arena", self._construct_tag)
        self.add_constructor("!ArenaConfig", self._construct_tag)
        self.add_constructor("!Item", self._construct_tag)
        self.add_constructor("!Vector3", self._construct_tag)
        self.add_constructor("!RGB", self._construct_tag)

    @staticmethod
    def _construct_tag(
        loader: yaml.Loader, node: yaml.MappingNode
    ) -> Dict[Hashable, Any]:
        return loader.construct_mapping(node)


def arena_config_loader_example():
    import pprint

    # Load a configuration yaml file
    config_path = os.path.join("example_configs", "config.yaml")
    with open(config_path) as file:
        config_data = yaml.load(file, Loader=ArenaConfigLoader)

    print("* Entire configuration data:")
    pprint.pprint(config_data)

    print("\n* Configuration items without the Agent item:")
    pprint.pprint(
        [
            element
            for element in config_data["arenas"][0]["items"]
            if element["name"] != "Agent"
        ]
    )


if __name__ == "__main__":
    arena_config_loader_example()
