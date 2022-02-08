from brownie import accounts, Lottery, config, network
from web3 import Web3


def test_get_entrance_fee():
    account = accounts[0]
    print(account)
    lottery = Lottery.deploy(config['networks'][network.show_active()]['eth_usd_price_feed'], {'from': account})
    print(lottery.getEntranceFee().return_value)
    assert lottery.getEntranceFee().return_value > Web3.toWei(0.005, 'ether')
