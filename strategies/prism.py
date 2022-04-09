import config
from protocols import protocol_manager
from strategies.base import Strategy
from utils import network
from utils.wallet import wallet


prism = protocol_manager.get_protocol('prism')


class RefractLunaStrategy(Strategy):
    protocol = prism
    name = 'LUNA -> (pLUNA + yLUNA)'
    requires = ['LUNA']

    threshold = 4

    async def get_score(self):
        if config.USE_WALLET_FOR_SIMULATE:
            amount = await wallet.get('LUNA')
        else:
            amount = 10 ** 6

        # At least 0.001 LUNA
        if not amount or amount < 1000:
            return 0

        luna_to_pluna = await prism.simulate_swap('LUNA', 'pLUNA', amount)
        luna_to_yluna = await prism.simulate_swap('LUNA', 'yLUNA', amount)

        # print('%d LUNA == %.2f pLUNA' % (amount, luna_to_pluna))
        # print('%d LUNA == %.2f yLUNA' % (amount, luna_to_yluna))

        pluna_ratio = luna_to_pluna / (luna_to_pluna + luna_to_yluna)
        yluna_ratio = luna_to_yluna / (luna_to_pluna + luna_to_yluna)
        # print('pLUNA ratio: %.2f%%' % (pluna_ratio * 100))
        # print('yLUNA ratio: %.2f%%' % (yluna_ratio * 100))

        pluna = await prism.simulate_swap('LUNA', 'pLUNA', int(amount * yluna_ratio))
        yluna = await prism.simulate_swap('LUNA', 'yLUNA', int(amount * pluna_ratio))
        luna_to_refract = min(pluna, yluna)

        # print('%.6f pLUNA -> %.6f LUNA' % (amount * yluna_ratio, pluna))
        # print('%.6f yLUNA -> %.6f LUNA' % (amount * pluna_ratio, yluna))

        return (luna_to_refract - amount) / amount * 100

    async def execute(self):
        amount = await wallet.get('LUNA')

        # At least 0.001 LUNA
        if not amount or amount < 1000:
            return 0

        luna_to_pluna = await prism.simulate_swap('LUNA', 'pLUNA', amount)
        luna_to_yluna = await prism.simulate_swap('LUNA', 'yLUNA', amount)

        pluna_ratio = luna_to_pluna / (luna_to_pluna + luna_to_yluna)
        yluna_ratio = luna_to_yluna / (luna_to_pluna + luna_to_yluna)

        contract_calls = [
            await prism.get_swap_native_coin_contract_call('LUNA', 'pLUNA', int(amount * yluna_ratio)),
            await prism.get_swap_native_coin_contract_call('LUNA', 'yLUNA', int(amount * pluna_ratio)),
        ]

        return await wallet.call_contracts_multiple(contract_calls)


class PrismWithdrawLunaStrategy(Strategy):
    protocol = prism
    name = 'Withdraw LUNA'

    threshold = 0

    async def get_score(self):
        return await prism.withdrawable_luna() / 10 ** 6

    async def execute(self):
        await prism.withdraw_luna()


class PrismUnbondCLunaStrategy(Strategy):
    protocol = prism
    name = 'Unbond cLUNA'

    threshold = 0

    async def get_score(self):
        return await wallet.get('cLUNA') / 10 ** 6

    async def execute(self):
        await prism.unbond_cluna()


class PrismUnstakeXPrismStrategy(Strategy):
    protocol = prism
    name = 'Unstake xPRISM'

    threshold = 0

    async def get_score(self):
        return await wallet.get('xPRISM') / 10 ** 6

    async def execute(self):
        await prism.unstake_xprism()


class PrismMergeLunaStrategy(Strategy):
    protocol = prism
    name = 'Merge pLUNA + yLUNA'

    threshold = 0

    async def get_score(self):
        yluna = await wallet.get('yLUNA') or 0
        pluna = await wallet.get('pLUNA') or 0

        return min(yluna, pluna) / 10 ** 6

    async def execute(self):
        yluna = await wallet.get('yLUNA') or 0
        pluna = await wallet.get('pLUNA') or 0

        to_merge = min(yluna, pluna)

        if to_merge < 1000:
            return

        prism_luna_vault_contract = network.CONTRACTS['PRISM_LUNA_VAULT']

        msgs = [
            {
                'contract': network.TOKENS['pLUNA'],
                'msg': {
                    'increase_allowance': {
                        'amount': str(to_merge),
                        'spender': prism_luna_vault_contract,
                    }
                },
            },
            {
                'contract': network.TOKENS['yLUNA'],
                'msg': {
                    'increase_allowance': {
                        'amount': str(to_merge),
                        'spender': prism_luna_vault_contract,
                    }
                },
            },
            {
                'contract': prism_luna_vault_contract,
                'msg': {
                    'merge': {
                        'amount': str(to_merge),
                    }
                },
            },
        ]

        return await wallet.call_contracts_multiple(msgs)
