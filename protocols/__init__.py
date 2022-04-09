from pathlib import Path

from autodiscover import AutoDiscover


class ProtocolManager:
    def __init__(self):
        self.registry = {}

    def autodiscover(self):
        """
        Autodiscover all sections in order to automatically register with section_manager
        """
        AutoDiscover(Path('protocols'))()

    def register(self, protocol):
        self.registry[protocol.id] = protocol()

    def get_protocol(self, protocol_id):
        return self.registry[protocol_id]


protocol_manager = ProtocolManager()
protocol_manager.autodiscover()
