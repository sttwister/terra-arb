

class Plugin:
    id = None

    def __init__(self):
        assert self.id

    def after_simulate(self, groups):
        """
        Called after all strategies in a strategy group have been simulated.
        """
        pass

