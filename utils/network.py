import config

from terra_sdk.client.lcd import AsyncLCDClient


class TerraNetwork:
    chain_id = None
    url = None

    NATIVE_COINS = {
        'LUNA': 'uluna',
        'UST': 'uusd',
    }

    def __init__(self):
        assert self.chain_id
        assert self.url

        self.lcd = AsyncLCDClient(chain_id=self.chain_id, url=self.url)


class Mainnet(TerraNetwork):
    chain_id = 'columbus-5'
    url = 'https://lcd.terra.dev'

    CONTRACTS = {
        'ANCHOR_BLUNA_HUB': 'terra1mtwph2juhj0rvjz7dy92gvl6xvukaxu8rfv8ts',
        'PRISM_LUNA_VAULT': 'terra1xw3h7jsmxvh6zse74e4099c6gl03fnmxpep76h',
        'PRISM_SWAP_ROUTER': 'terra1yrc0zpwhuqezfnhdgvvh7vs5svqtgyl7pu3n6c',
        'PRISM_GOVERNANCE': 'terra1h4al753uvwmhxwhn2dlvm9gfk0jkf52xqasmq2',
        'ASTROPORT_PAIRS': {
            ('LUNA', 'bLUNA'): 'terra1j66jatn3k50hjtg2xemnjm8s7y8dws9xqa5y8w',
            ('LUNA', 'LunaX'): 'terra1qswfc7hmmsnwf7f2nyyx843sug60urnqgz75zu',
            ('LUNA', 'cLUNA'): 'terra102t6psqa45ahfd7wjskk3gcnfev32wdngkcjzd',
            ('PRISM', 'xPRISM'): 'terra1c868juk7lk9vuvetf0644qgxscsu4xwag6yaxs',
        },
        'TERRASWAP_PAIRS': {
            ('LUNA', 'bLUNA'): 'terra1jxazgm67et0ce260kvrpfv50acuushpjsz2y0p',
            ('LUNA', 'LunaX'): 'terra1zrzy688j8g6446jzd88vzjzqtywh6xavww92hy',
            ('LUNA', 'cLUNA'): 'terra1ejyqwcemr5kda5pxwz27t2ja784j3d0nj0v6lh',
            ('PRISM', 'xPRISM'): 'terra1urt608par6rkcancsjzm76472phptfwq397gpm',
        },
        'LOOP_PAIRS': {
            ('LUNA', 'bLUNA'): 'terra1v93ll6kqp33unukuwls3pslquehnazudu653au',
            ('LUNA', 'LunaX'): 'terra1ga8dcmurj8a3hd4vvdtqykjq9etnw5sjglw4rg',
            ('LUNA', 'cLUNA'): 'terra1ur6yyha884t5rhpf6was9xlr7xpcq40aw2r5jx',
        },
        'STADER_LIQUID_STAKING': 'terra1xacqx447msqp46qmv8k2sq6v5jh9fdj37az898',
    }
    TOKENS = {
        'bLUNA': 'terra1kc87mu460fwkqte29rquh4hc20m54fxwtsx7gp',
        'LunaX': 'terra17y9qkl8dfkeg4py7n0g5407emqnemc3yqk5rup',
        'cLUNA': 'terra13zaagrrrxj47qjwczsczujlvnnntde7fdt0mau',
        'pLUNA': 'terra1tlgelulz9pdkhls6uglfn5lmxarx7f2gxtdzh2',
        'yLUNA': 'terra17wkadg0tah554r35x6wvff0y5s7ve8npcjfuhz',
        'PRISM': 'terra1dh9478k2qvqhqeajhn75a2a7dsnf74y5ukregw',
        'xPRISM': 'terra1042wzrwg2uk6jqxjm34ysqquyr9esdgm5qyswz',
    }


class Testnet(TerraNetwork):
    chain_id = 'bombay-12'
    url = 'https://bombay-lcd.terra.dev'

    CONTRACTS = {
        'ANCHOR_BLUNA_HUB': 'terra1fflas6wv4snv8lsda9knvq2w0cyt493r8puh2e',
        'PRISM_LUNA_VAULT': 'terra1knak0taqkas4y07mupvxpr89kvtew5dx9jystw',
        'PRISM_SWAP_ROUTER': 'terra1hn2dlykp8k5uspy6np5ks27060wnav6stmpvm5',
        'PRISM_GOVERNANCE': 'terra1teddvnlz7jh00nvn67ezksheastm3saqec0um9',
        'ASTROPORT_PAIRS': {
            ('LUNA', 'bLUNA'): 'terra1esle9h9cjeavul53dqqws047fpwdhj6tynj5u4',
            ('LUNA', 'LunaX'): '',
        },
        'TERRASWAP_PAIRS': {
            ('LUNA', 'bLUNA'): 'terra13e4jmcjnwrauvl2fnjdwex0exuzd8zrh5xk29v',
            ('LUNA', 'LunaX'): '',
        },
        'LOOP_PAIRS': {
        },
        'STADER_LIQUID_STAKING': '',
    }
    TOKENS = {
        'bLUNA': 'terra1u0t35drzyy0mujj8rkdyzhe264uls4ug3wdp3x',
        'LunaX': '',
        'cLUNA': 'terra108kj35ef46tptcw69a0x5r9qkfu8h7vmjp6w39',
        'pLUNA': 'terra1sev4e0u23l75g5spzsquw6n7c8g5efl6hg0zl6',
        'yLUNA': 'terra1utwws3p0qzqrw7jslsuvt6drd7jsjhpu0rxauj',
        'PRISM': 'terra1cwle4remlf03mucutzhxfayvmdqsulx8xaahvy',
        'xPRISM': 'terra1tz4lxls6gp05m20tgx4t9ljhtvqnmcpujaadc2',
    }


network = {
    'mainnet': Mainnet,
    'testnet': Testnet,
}.get(config.NETWORK)()