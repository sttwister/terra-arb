from rich.columns import Columns
from rich.console import Console
from rich.table import Table

from plugins import plugin_manager
from plugins.base import Plugin
from utils.wallet import wallet


@plugin_manager.register
class RichPlugin(Plugin):
    """
    Plugin that provides nicely formatted table output in the console.
    """
    id = 'rich'

    header_style = 'bold magenta'

    def after_simulate(self, groups):
        console = Console()
        console.clear()

        tables = []
        for group in groups:
            table = Table(title=group.name, header_style=self.header_style)

            table.add_column('Protocol', justify='left')
            table.add_column('Strategy', justify='left')
            table.add_column('Min', justify='right')
            table.add_column('Max', justify='right')
            table.add_column('Score', justify='right')

            summary = group.get_summary()
            for strategy_summary in summary:
                row = (
                    strategy_summary['protocol_name'],
                    strategy_summary['name'],
                    '%.2f%%' % strategy_summary['min'],
                    '%.2f%%' % strategy_summary['max'],
                    '%.2f%%' % strategy_summary['score'],
                )

                row_options = {}
                if strategy_summary['score'] < 0:
                    row_options['style'] = 'dim'
                elif strategy_summary['score'] > strategy_summary['strategy'].threshold:
                    row_options['style'] = 'green'
                elif strategy_summary['score'] > 0:
                    row_options['style'] = ''

                table.add_row(*row, **row_options)

            tables.append(table)

        wallet_table = Table(title='Wallet', header_style=self.header_style)
        wallet_table.add_column('Token', justify='left')
        wallet_table.add_column('Balance', justify='right')

        for token, balance in wallet.get_summary():
            wallet_table.add_row(token, balance)

        tables.append(wallet_table)

        console.print(Columns(tables))
