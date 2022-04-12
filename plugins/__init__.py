import asyncio

from autodiscover import AutoDiscover
from pathlib import Path


class PluginManager:

    def __init__(self):
        # Maps plugin id to plugin class
        self.registry = {}

        # Maps plugin id to plugin instance
        self.plugins = {}

        # Stores the order in which plugins should be called, dependencies first
        self.plugins_order = []

    def autodiscover(self):
        """
        Autodiscover all sections in order to automatically register with section_manager
        """
        AutoDiscover(Path('plugins'))()

    def register(self, plugin):
        self.registry[plugin.id] = plugin

    def enable(self, plugin_id, update_order=True):
        if plugin_id not in self.plugins:
            self.plugins[plugin_id] = self.registry[plugin_id]()

        if update_order:
            self.update_plugins_order()

    def update_plugins_order(self):
        import networkx as nx

        # Build dependency graph as a DAG
        g = nx.DiGraph()

        # Add dependencies to the graph
        for plugin_id in self.plugins.keys():
            for dependency in self.registry[plugin_id].depends_on:
                g.add_edge(dependency, plugin_id)

        # Use topological sort to ensure dependencies are always first
        self.plugins_order = list(nx.topological_sort(g))

        # Enable all plugins in order to include all dependencies
        for plugin_id in self.plugins_order:
            self.enable(plugin_id, update_order=False)

    def get_plugin(self, plugin_id):
        return self.plugins[plugin_id]

    async def dispatch(self, event, *args, **kwargs):
        for plugin_id in self.plugins_order:
            plugin = self.get_plugin(plugin_id)
            method = getattr(plugin, event, None)
            if method:
                if asyncio.iscoroutinefunction(method):
                    await method(*args, **kwargs)
                else:
                    method(*args, **kwargs)


plugin_manager = PluginManager()
plugin_manager.autodiscover()