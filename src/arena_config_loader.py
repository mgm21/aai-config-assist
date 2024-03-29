import yaml
import os


class ArenaConfigLoader(yaml.SafeLoader):
    """Loader with custom constructors for the custom tags (e.g. !ArenaConfig) in the configuration YAMLs."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_constructor('!Arena', self.construct_arena)
        self.add_constructor('!ArenaConfig', self.construct_arena_config)
        self.add_constructor('!Item', self.construct_item)
        self.add_constructor('!Vector3', self.construct_vector3)
        self.add_constructor('!RGB', self.construct_rgb)

    @staticmethod
    def construct_arena(loader, node):
        return loader.construct_mapping(node)

    @staticmethod
    def construct_arena_config(loader, node):
        return loader.construct_mapping(node)

    @staticmethod
    def construct_item(loader, node):
        return loader.construct_mapping(node)

    @staticmethod
    def construct_vector3(loader, node):
        return loader.construct_mapping(node)

    @staticmethod
    def construct_rgb(loader, node):
        return loader.construct_mapping(node)


if __name__ == "__main__":
    import pprint

    # Load a configuration yaml file
    config_path = os.path.join("example_configs", "config.yaml")
    with open(config_path) as file:
        config_data = yaml.load(file, Loader=ArenaConfigLoader)

    print("* Entire configuration data:")
    pprint.pprint(config_data)

    print("\n* Configuration items without the Agent item:")
    pprint.pprint([element for element in config_data["arenas"][0]["items"] if element["name"] != "Agent"])
