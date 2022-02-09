from brownie import exceptions
from scripts.deploy_lottery import deploy_lottery
from scripts.general_scripts import get_account, get_contract, fund_with_link
from web3 import Web3
from brownie import network, config
import pytest

def test_can_pick_winner():
    #Arrange
    if not config['networks'][network.show_active()]['local'] is False:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({'from': account}).wait(1)
    lottery.enter({'from': account, 'value': lottery.getEntranceFee().return_value}).wait(1)
    lottery.enter({'from': account, 'value': lottery.getEntranceFee().return_value}).wait(1)
    #Act
    account_balance = account.balance()
    lottery_balance = lottery.balance()
    
    fund_with_link(lottery.address)
    lottery.endLottery({'from': account}).wait(1)
    
    #Assert
    assert lottery.lastWinner() == account
    assert lottery.balance() == 0