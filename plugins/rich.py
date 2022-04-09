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

    def after_simulate(self, groups):
        console = Console()
        console.clear()

        tables = []
        for group in groups:
            table = Table(title=group.name)

            table.add_column('Protocol', justify='left')
            table.add_column('Strategy', justify='left')
            table.add_column('Score', justify='right')
            table.add_column('Min', justify='right')
            table.add_column('Max', justify='right')

            summary = group.get_summary()
            for strategy_summary in summary:
                row = (
                    strategy_summary['protocol'],
                    strategy_summary['name'],
                    '%.2f%%' % strategy_summary['score'],
                    '%.2f%%' % strategy_summary['min'],
                    '%.2f%%' % strategy_summary['max'],
                )
                table.add_row(*row)

            tables.append(table)

        wallet_table = Table(title='Wallet')
        wallet_table.add_column('Token', justify='left')
        wallet_table.add_column('Balance', justify='right')

        for token, balance in wallet.get_summary():
            wallet_table.add_row(token, balance)

        tables.append(wallet_table)

        console.print(Columns(tables))
