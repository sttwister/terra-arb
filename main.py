#!/usr/bin/env python
import asyncio

import click as click
from rich.traceback import install

import config


# Nice prety colored tracebacks
install(show_locals=True)


async def run_loop(summary_callback=None):
    """
    Main entry point for the bot.
    """
    from strategies import STRATEGY_GROUPS
    from utils.wallet import wallet

    while True:
        groups = STRATEGY_GROUPS

        populate_wallet_cache = wallet.populate_cache()
        run_strategies = asyncio.gather(*(
            group.run() for group in groups
        ))

        await asyncio.gather(populate_wallet_cache, run_strategies)

        if summary_callback:
            summary_callback(groups)

        if config.EXECUTE:
            for group in groups:
                group.execute()

        await asyncio.sleep(config.SLEEP_INTERVAL)


def tabulate_summary(groups):
    """
    Prints a summary of the current state of the bot using tabulate.
    """
    from tabulate import tabulate

    headers = ['Protocol', 'Strategy', 'Score', 'Min', 'Max']
    for group in groups:
        table = []
        summary = group.get_summary()
        for strategy_summary in summary:
            table.append([
                strategy_summary['protocol'],
                strategy_summary['name'],
                strategy_summary['score'],
                strategy_summary['min'],
                strategy_summary['max'],
            ])
        print(tabulate(table, headers=headers, floatfmt='.2f'))
        print()


def rich_summary(groups):
    """
    Prints a rich summary of the current state of the bot using rich.
    """
    from rich.columns import Columns
    from rich.console import Console
    from rich.table import Table

    from utils.wallet import wallet

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


@click.command()
@click.option('--summary', type=click.Choice(['tabulate', 'rich']), default='rich')
def main(summary):
    summary_callback = {
        'tabulate': tabulate_summary,
        'rich': rich_summary,
    }.get(summary)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_loop(summary_callback=summary_callback))


if __name__ == '__main__':
    main()
