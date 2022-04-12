

class Plugin:
    id = None

    # A list of plugin IDs that this plugin depends on.
    #
    # These plugins will be automatically enabled and triggered before this plugin.
    depends_on = []

    def __init__(self):
        assert self.id is not None, "Plugin ID is not set for {}".format(self.__class__.__name__)
