from brownie import network, accounts, config, Contract, MockV3Aggregator, LinkToken, VRFCoordinatorMock


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    elif id:
        return accounts.load(id)
    elif not config['networks'][network.show_active()]['local'] is False:
        return accounts[0]
    else:
        return accounts.add(config['wallets']['dev_account_1']['private_key'])


contracts_to_mock = {'eth_usd_price_feed': MockV3Aggregator,
                     'vrf_coordinator': VRFCoordinatorMock,
                     'link_token': LinkToken}

def get_contract(contract_name):
    contract_type = contracts_to_mock[contract_name]
    if config['networks'][network.show_active()]['local'] is True:
        deploy_mocks(contract_type)
        contract = contract_type[-1]
    
    else:
        contract_address = config['networks'][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)

    return contract

DECIMALS = 8
STARTING_VALUE = 2000

def deploy_mocks(contract_type, decimals=DECIMALS, starting_value=STARTING_VALUE):
    if contract_type == MockV3Aggregator:
        if len(contract_type) == 0:
            MockV3Aggregator.deploy(decimals, starting_value * (10**8), {'from': get_account()})
            print('MockV3Aggregator deployed')
    
    elif contract_type == VRFCoordinatorMock:
        if len(contract_type) == 0:
            if len(LinkToken) == 0:
                LinkToken.deploy({'from': get_account()})
            VRFCoordinatorMock.deploy(LinkToken[-1].address, {'from': get_account()})
            print('VRFCoordinatorMock deployed')

    elif contract_type == LinkToken:
        if len(contract_type) == 0:
            LinkToken.deploy({'from': get_account()})
            print('LinkToken (mock) deployed')
    