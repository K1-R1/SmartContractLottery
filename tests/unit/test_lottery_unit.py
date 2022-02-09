from brownie import exceptions
from scripts.deploy_lottery import deploy_lottery
from scripts.general_scripts import get_account
from web3 import Web3
from brownie import network, config
import pytest

def test_get_entrance_fee():
    #Arrange
    if not config['networks'][network.show_active()]['local'] is True:
        pytest.skip()
    lottery = deploy_lottery()
    #Act
    entrance_fee = lottery.getEntranceFee().return_value
    # Mock price feed ETHUSD value: 2000
    # USDEntryFee = 25
    # 25 / 2000 = 0.0125 ETH
    expected_entrance_fee = Web3.toWei(0.0125, 'ether')
    #Assert
    assert entrance_fee == expected_entrance_fee

def test_cant_enter_unless_started():
    #Arrage
    if not config['networks'][network.show_active()]['local'] is True:
        pytest.skip()
    lottery = deploy_lottery()
    #Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({'from': get_account(), 'value': lottery.getEntranceFee().return_value})
