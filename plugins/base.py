

class Plugin:
    id = None

    def __init__(self):
        assert self.id is not None, "Plugin ID is not set for {}".format(self.__class__.__name__)
