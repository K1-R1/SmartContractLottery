from brownie import network, accounts, config

DECIMALS = 8
STARTING_VALUE = 2500

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    elif id:
        return accounts.load(id)
    elif not config['networks'][network.show_active()]['local'] is False:
        return accounts[0]
    else:
        return accounts.add(config['wallets']['dev_account_1']['private_key'])



# def deploy_mocks():
#     if not len(MockV3Aggregator):
#         MockV3Aggregator.deploy(DECIMALS, STARTING_VALUE * 10 ** 8, {'from': get_account()})
#     print('Mocks deployed\n')
    