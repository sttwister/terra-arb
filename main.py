#!/usr/bin/env python
import asyncio

import click as click

import config
from plugins import plugin_manager
from utils import network


async def run_loop():
    """
    Main entry point for the bot.
    """
    from strategies import strategy_manager
    from utils.wallet import wallet

    plugin_manager.dispatch('init')

    groups = strategy_manager.get_strategy_groups()

    current_block = await network.get_current_block_height()

    while True:
        plugin_manager.dispatch('loop_start', current_block=current_block)

        populate_wallet_cache = wallet.populate_cache()
        run_strategies = asyncio.gather(*(
            group.run() for group in groups
        ))

        await asyncio.gather(populate_wallet_cache, run_strategies)

        plugin_manager.dispatch('after_scoring')

        if config.EXECUTE:
            for group in groups:
                await group.execute()

        plugin_manager.dispatch('wait_for_next_block')

        # Wait for the next block
        new_block = await network.get_current_block_height()
        while new_block <= current_block:
            await asyncio.sleep(0.1)  # 100 ms
            new_block = await network.get_current_block_height()

        current_block = new_block


@click.command()
def main():
    for plugin in config.ACTIVE_PLUGINS:
        plugin_manager.activate(plugin)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_loop())


if __name__ == '__main__':
    main()
