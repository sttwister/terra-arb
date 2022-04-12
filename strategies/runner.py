import asyncio
from dateutil import parser

import config
from plugins import plugin_manager
from strategies import strategy_manager
from utils import network
from utils.wallet import wallet


class StrategyRunner:

    def __init__(self):
        self.current_block_height = None
        self.current_block_time = None

    async def run(self):
        await plugin_manager.dispatch('init')

        groups = strategy_manager.get_strategy_groups()

        current_block = await network.get_current_block()
        self.current_block_height = current_block['height']
        self.current_block_time = parser.parse(current_block['time'])

        while True:
            await plugin_manager.dispatch('loop_start')

            populate_wallet_cache = wallet.populate_cache()
            run_strategies = asyncio.gather(*(
                group.run() for group in groups
            ))

            await asyncio.gather(populate_wallet_cache, run_strategies)

            await plugin_manager.dispatch('after_scoring')

            if config.EXECUTE:
                for group in groups:
                    await group.execute()

            await plugin_manager.dispatch('wait_for_next_block')

            # Wait for the next block
            new_block = await network.get_current_block()
            while new_block['height'] <= self.current_block_height:
                await asyncio.sleep(0.1)  # 100 ms
                new_block = await network.get_current_block()

            self.current_block_height = new_block['height']
            self.current_block_time = parser.parse(new_block['time'])


strategy_runner = StrategyRunner()
