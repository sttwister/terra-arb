from apps.base import DexProtocol


class Astroport(DexProtocol):
    name = 'Astroport'

    PAIRS_IDENTIFIER = 'ASTROPORT_PAIRS'


astroport = Astroport()
