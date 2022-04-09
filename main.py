#!/usr/bin/env python
import asyncio

import click as click
from rich.traceback import install

import config
from plugins import plugin_manager


# Nice pretty colored tracebacks
install(show_locals=True)


async def run_loop():
    """
    Main entry point for the bot.
    """
    from strategies import STRATEGY_GROUPS
    from utils.wallet import wallet

    while True:
        groups = [
            STRATEGY_GROUPS.get(strategy_group)
            for strategy_group in config.ENABLED_STRATEGY_GROUPS
        ]

        populate_wallet_cache = wallet.populate_cache()
        run_strategies = asyncio.gather(*(
            group.run() for group in groups
        ))

        await asyncio.gather(populate_wallet_cache, run_strategies)

        plugin_manager.after_simulate(groups)

        if config.EXECUTE:
            for group in groups:
                group.execute()

        await asyncio.sleep(config.SLEEP_INTERVAL)


@click.command()
def main():
    for plugin in config.ACTIVE_PLUGINS:
        plugin_manager.activate(plugin)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_loop())


if __name__ == '__main__':
    main()
