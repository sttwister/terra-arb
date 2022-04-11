from aiohttp import web

from plugins import plugin_manager
from plugins.base import Plugin
from strategies import strategy_manager


@plugin_manager.register
class WebPlugin(Plugin):
    id = "web"

    def __init__(self):
        self.scores = {}

    async def init(self, **kwargs):
        """
        Initialize an async webserver.
        """
        app = web.Application()
        app.add_routes([web.get('/', self.index)])

        runner = web.AppRunner(app)
        await runner.setup()

        site = web.TCPSite(runner)
        await site.start()

    async def after_scoring(self, **kwargs):
        for group in strategy_manager.get_strategy_groups():
            summary = group.get_summary()
            for strategy_summary in summary:
                self.scores[
                    (strategy_summary['protocol_name'], strategy_summary['name'])
                ] = round(strategy_summary['score'], 2)

        self.scores = dict(sorted(self.scores.items(), key=lambda x: x[1], reverse=True))

    async def index(self, request):
        import pprint
        return web.Response(text=pprint.pformat(self.scores, sort_dicts=False))


