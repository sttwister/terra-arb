import time

from rich.columns import Columns
from rich.console import Console
from rich.table import Table

import config
from plugins import plugin_manager
from plugins.base import Plugin
from strategies import strategy_manager
from utils import network
from utils.wallet import wallet


@plugin_manager.register
class RichPlugin(Plugin):
    """
    Plugin that provides nicely formatted table output in the console.
    """
    id = 'rich'

    depends_on = ['history']

    header_style = 'bold magenta'

    config_keys = [
        'EXECUTE',
        'BROADCAST_TX',
        'USE_WALLET_FOR_SIMULATE',
    ]

    def __init__(self):
        from rich.traceback import install

        # Nice pretty colored tracebacks
        install(show_locals=True)

        self.console = Console()
        self.start_time = None

    def init(self, **kwargs):
        self.console.print('Starting [bold magenta]terra-arb[/bold magenta]!')
        self.console.print()

        if config.NETWORK == 'mainnet':
            style = 'bold green'
        else:
            style = 'bold yellow'
        self.console.print(f'Using network [{style}]{config.NETWORK}[/]')
        self.console.print(f'Chain ID: [bold magenta]{network.lcd.chain_id}[/]')
        self.console.print(f'LCD URL: [bold magenta]{network.lcd.url}[/]')
        self.console.print()

        plugins = ', '.join('[bold magenta]{}[/]'.format(plugin) for plugin in config.ACTIVE_PLUGINS)
        self.console.print(f'[underline]Active plugins[/]: {plugins}')
        self.console.print()

        self.console.print('[underline]Active strategy groups:')
        for group_id, group in strategy_manager.strategy_groups.items():
            self.console.print(f'  [bold yellow]{group_id}[/] - [bold magenta]{group.name}[/]')
        self.console.print()

        self.console.print('[underline]Config options:')
        for key in self.config_keys:
            self.console.print(f'  [bold magenta]{key}[/] = [bold green]{getattr(config, key)}[/]')
        self.console.print()

    def loop_start(self, **kwargs):
        self.start_time = time.time()

    def after_scoring(self, **kwargs):
        history = plugin_manager.get_plugin('history')
        self.console.clear()

        # Create a table for each strategy group
        tables = []
        for group in strategy_manager.get_strategy_groups():
            table = Table(title=group.name, header_style=self.header_style)

            table.add_column('Protocol', justify='left')
            table.add_column('Strategy', justify='left')
            table.add_column('Min', justify='right')
            table.add_column('Max', justify='right')
            table.add_column('Score', justify='right')

            rows = []

            for strategy in group.strategies:
                min = history.min(strategy)
                max = history.max(strategy)
                score = group.last_run[strategy]

                row_options = {}
                if score < 0:
                    row_options['style'] = 'dim'
                elif score == min != max:
                    # New minimum
                    row_options['style'] = 'red'
                elif score == max != min:
                    # New maximum
                    row_options['style'] = 'green'
                elif score > strategy.threshold:
                    # Over threshold
                    row_options['style'] = 'bold'

                rows.append({
                    'protocol': strategy.protocol.get_name() if hasattr(strategy.protocol, 'get_name') else '',
                    'name': strategy.get_name(),
                    'min': min,
                    'max': max,
                    'score': score,
                    'row_options': row_options,
                })

            # Sort desc by score
            rows.sort(key=lambda row: row['score'], reverse=True)

            for row in rows:
                table.add_row(
                    row['protocol'],
                    row['name'],
                    '%.2f' % row['min'],
                    '%.2f' % row['max'],
                    '%.2f' % row['score'],
                    **row['row_options']
                )

            tables.append(table)

        # Create a table with wallet balances
        wallet_table = Table(title='Wallet', header_style=self.header_style)
        wallet_table.add_column('Token', justify='left')
        wallet_table.add_column('Balance', justify='right')

        for token, balance in wallet.get_summary():
            wallet_table.add_row(token, balance)

        self.console.print(wallet_table)
        self.console.print()

        self.console.print(Columns(tables))
        self.console.print()

        scoring_time = time.time() - self.start_time
        self.console.print('Strategy scoring time: [bold yellow]{:.2f}s[/]'.format(scoring_time))

    def before_strategy_execute(self, strategy=None, score=None, **kwargs):
        self.console.print(f'Executing strategy [bold magenta]{strategy.get_name()}[/] with score [bold green]{score}[/]')
        self.console.print()

    def before_call_contract(self, contract=None, msg=None, coins=None, **kwargs):
        self.console.print(f'Calling contract: [bold magenta]{contract}[/]')
        self.console.print('Msg:')
        self.console.print(msg)
        if coins:
            self.console.print(f'Coins:\n  [green]{coins}')
        self.console.print()

    def before_broadcast_tx(self, **kwargs):
        self.console.print(f'Broadcasting tx...')
        self.console.print()

    def wait_for_next_block(self, **kwargs):
        self.console.print('Waiting for next block...')