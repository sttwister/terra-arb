from protocols import protocol_manager
from strategies.base import Strategy
from utils.wallet import wallet


prism = protocol_manager.get_protocol('prism')


class RefractLunaStrategy(Strategy):
    threshold = 1

    protocol = prism
    name = 'LUNA -> (pLUNA + yLUNA)'
    requires = ['LUNA']

    async def get_score(self):
        amount = await wallet.get('LUNA')

        if not amount:
            return

        luna_to_pluna = await prism.simulate_swap('LUNA', 'pLUNA')
        luna_to_yluna = await prism.simulate_swap('LUNA', 'yLUNA')

        print('1 LUNA == %.2f pLUNA' % luna_to_pluna)
        print('1 LUNA == %.2f yLUNA' % luna_to_yluna)

        pluna_ratio = luna_to_pluna / (luna_to_pluna + luna_to_yluna)
        yluna_ratio = luna_to_yluna / (luna_to_pluna + luna_to_yluna)
        print('pLUNA ratio: %.2f%%' % (pluna_ratio * 100))
        print('yLUNA ratio: %.2f%%' % (yluna_ratio * 100))

        pluna = await prism.simulate_swap('LUNA', 'pLUNA', amount * yluna_ratio)
        yluna = await prism.simulate_swap('LUNA', 'yLUNA', amount * pluna_ratio)
        luna_to_refract = min(pluna, yluna)

        print('%.6f pLUNA -> %.6f LUNA' % (amount * yluna_ratio, pluna))
        print('%.6f yLUNA -> %.6f LUNA' % (amount * pluna_ratio, yluna))

        return (luna_to_refract / amount - 1) * 100

    async def simulate(self):
        amount = await wallet.get('LUNA')

        if not amount:
            return

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

    # def simulate(self):
    #     amount = wallet['LUNA']
    #
    #     luna_to_pluna = prism_swap.simulate_swap('LUNA', 'pLUNA')
    #     luna_to_yluna = prism_swap.simulate_swap('LUNA', 'yLUNA')
    #
    #     print('1 LUNA == %.2f pLUNA' % luna_to_pluna)
    #     print('1 LUNA == %.2f yLUNA' % luna_to_yluna)
    #
    #     pluna_ratio = luna_to_pluna / 2
    #     yluna_ratio = luna_to_yluna / 2
    #     print('pLUNA ratio: %.2f%%' % (pluna_ratio * 100))
    #     print('yLUNA ratio: %.2f%%' % (yluna_ratio * 100))
    #
    #     pluna = prism_swap.simulate_swap('LUNA', 'pLUNA', amount * yluna_ratio)
    #     yluna = prism_swap.simulate_swap('LUNA', 'yLUNA', amount * pluna_ratio)
    #     luna_to_refract = min(pluna, yluna)
    #
    #     print('%.6f pLUNA -> %.6f LUNA' % (amount * yluna_ratio, pluna))
    #     print('%.6f yLUNA -> %.6f LUNA' % (amount * pluna_ratio, yluna))
    #
    #     return (luna_to_refract / amount - 1) * 100


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