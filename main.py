#!/usr/bin/env python
import asyncio

import config
from plugins import plugin_manager
from strategies.runner import strategy_runner


def main():
    for plugin in config.ACTIVE_PLUGINS:
        plugin_manager.enable(plugin)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(strategy_runner.run())


if __name__ == '__main__':
    main()
