class Protocol:
    id = None
    name = None

    def __init__(self):
        assert self.id is not None, "Protocol ID is not set for {}".format(self.__class__.__name__)

    def get_name(self):
        return self.name


