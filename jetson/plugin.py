"""Plugin interface for Bloopy tasks.

Plugins provide additional behaviors for the robot. Each plugin must inherit
from :class:`BloopyPlugin` and implement the ``run`` method. Plugins can be
placed in a ``plugins`` directory and loaded dynamically by ``PluginManager``.
"""

from importlib import import_module
from pathlib import Path
from typing import List, Type


class BloopyPlugin:
    """Base class for all plugins."""

    name: str = "Unnamed"

    def run(self) -> None:
        """Execute the plugin's behavior."""
        raise NotImplementedError


class PluginManager:
    """Loads and executes Bloopy plugins."""

    def __init__(self, plugin_dir: Path) -> None:
        self.plugin_dir = plugin_dir
        self.plugins: List[BloopyPlugin] = []

    def load_plugins(self) -> None:
        for file in self.plugin_dir.glob("*.py"):
            if file.name.startswith("_"):
                continue
            module_name = file.stem
            module = import_module(f"plugins.{module_name}")
            for obj in module.__dict__.values():
                if isinstance(obj, type) and issubclass(obj, BloopyPlugin) and obj is not BloopyPlugin:
                    self.plugins.append(obj())

    def run_all(self) -> None:
        for plugin in self.plugins:
            plugin.run()
