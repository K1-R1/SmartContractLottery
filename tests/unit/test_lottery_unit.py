from brownie import web3
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
from brownie import network, config
import pytest

def test_get_entrance_fee():
    if not config['networks'][network.show_active()]['local'] is True:
        pytest.skip()
    #Arrange
    lottery = deploy_lottery()
    #Act
    entrance_fee = lottery.getEntranceFee().return_value
    # Mock price feed ETHUSD value: 2000
    # USDEntryFee = 25
    # 25 / 2000 = 0.0125 ETH
    expected_entrance_fee = Web3.toWei(0.0125, 'ether')
    #Assert
    assert entrance_fee == expected_entrance_fee
