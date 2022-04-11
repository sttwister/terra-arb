import asyncio

from autodiscover import AutoDiscover
from pathlib import Path


class PluginManager:

    def __init__(self):
        self.registry = {}
        self.enabled_plugins = []

    def autodiscover(self):
        """
        Autodiscover all sections in order to automatically register with section_manager
        """
        AutoDiscover(Path('plugins'))()

    def register(self, plugin):
        self.registry[plugin.id] = plugin

    def activate(self, plugin_id):
        self.enabled_plugins.append(self.registry[plugin_id]())

    async def dispatch(self, event, *args, **kwargs):
        for plugin in self.enabled_plugins:
            method = getattr(plugin, event, None)
            if method:
                if asyncio.iscoroutinefunction(method):
                    await method(*args, **kwargs)
                else:
                    method(*args, **kwargs)


plugin_manager = PluginManager()
plugin_manager.autodiscover()