from typing import Union

import matplotlib.figure
import yaml
from dash import Dash

from src.app.callback_registrar import CallbackRegistrar
from src.app.setup import set_up_app_layout
from src.core.checker import Checker
from src.core.visualiser import Visualiser
from src.processing.loader import Loader
from src.processing.preprocessor import Preprocessor


class AppManager:
    """The AppManager orchestrates the lifecycle of the Dash application."""

    PORT_NUMBER = 8000
    ITEM_PARAMETERS_FILE_PATH = "src/definitions/item_default_parameters.yaml"
    INITIAL_ARENA_INDEX = 0
    INITIAL_ITEM_INDEX = 0

    def __init__(self, config_path: Union[str, None] = None) -> None:
        """Loads the default parameters, creates arenas objects, and instantiates dependencies.

        Args:
            config_path (str or None): Path to the YAML configuration file to load or None if starting app from scratch.
        """
        # Get the default item parameters
        with open(self.ITEM_PARAMETERS_FILE_PATH, "r") as file:
            self.default_item_parameters = yaml.safe_load(file)
        self.all_aai_item_names = list(self.default_item_parameters.keys())

        preprocessor = Preprocessor(
            self.default_item_parameters, self.all_aai_item_names
        )

        if config_path is None:
            self.arenas = preprocessor.create_default_arenas_list()
        else:
            yaml_config_data = Loader.load_config_data(config_path)
            self.arenas = preprocessor.create_arenas_list(yaml_config_data)

        # Instantiate required classes
        self.checker = Checker()
        self.visualiser = Visualiser()

        self.curr_arena_ix = self.INITIAL_ARENA_INDEX
        self.curr_item_to_move_ix = self.INITIAL_ARENA_INDEX

    def run_app(self) -> None:
        """Launches the Animal-AI Assistant (Level Editor) Dash application."""
        app = Dash(__name__)
        app.layout = set_up_app_layout(self._get_fig_init(), self.all_aai_item_names)
        CallbackRegistrar(app_manager=self).register_callbacks()
        app.run(port=self.PORT_NUMBER)

    def _get_fig_init(self) -> matplotlib.figure.Figure:
        """Generates the initial arena figure to display at application start-up.

        Returns:
            (matplotlib.figure.Figure): The arena figure to display at application start-up.
        """
        cuboids = self.arenas[self.curr_arena_ix].physical_items
        names_items_with_overlap = self.checker.check_overlaps_between_cuboids(cuboids)
        fig_init = self.visualiser.visualise_cuboid_bases(
            cuboids, list(names_items_with_overlap)
        )
        return fig_init


def app_manager_example() -> None:
    """Executes a typical usage of the AppManager."""
    application_manager = AppManager("example_configs/config.yaml")
    application_manager.run_app()


if __name__ == "__main__":
    app_manager_example()
