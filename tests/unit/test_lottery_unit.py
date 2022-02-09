from brownie import exceptions
from scripts.deploy_lottery import deploy_lottery
from scripts.general_scripts import get_account, get_contract, fund_with_link
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

def test_can_start_and_enter_lottery():
    #Arrange
    if not config['networks'][network.show_active()]['local'] is True:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    #Act
    lottery.startLottery({'from': account}).wait(1)
    lottery.enter({'from': account, 'value': lottery.getEntranceFee().return_value}).wait(1)
    #Assert
    assert lottery.lottery_state() == 0
    assert lottery.players(0) == account

def test_can_end_lottery():
    #Arrange
    if not config['networks'][network.show_active()]['local'] is True:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({'from': account}).wait(1)
    lottery.enter({'from': account, 'value': lottery.getEntranceFee().return_value}).wait(1)
    #Act
    fund_with_link(lottery.address)
    lottery.endLottery({'from': account}).wait(1)
    #Assert
    assert lottery.lottery_state() == 2

def test_can_pick_winner():
    #Arrange
    if not config['networks'][network.show_active()]['local'] is True:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({'from': account}).wait(1)
    lottery.enter({'from': account, 'value': lottery.getEntranceFee().return_value}).wait(1)
    lottery.enter({'from': get_account(index=1), 'value': lottery.getEntranceFee().return_value}).wait(1)
    lottery.enter({'from': get_account(index=2), 'value': lottery.getEntranceFee().return_value}).wait(1)
    #Act
    fund_with_link(lottery.address)
    end_tx = lottery.endLottery({'from': account})
    end_tx.wait(1)
    account_balance = account.balance()
    lottery_balance = lottery.balance()
    request_id = end_tx.events['RequestRandomness']['requestId']
    static_RNG = 3
    get_contract('vrf_coordinator').callBackWithRandomness(request_id, static_RNG, lottery.address, {'from': account}).wait(1)
    #Assert
    # uint256 winningIndex = _randomness % players.length;
    # 3 % 3 = 0
    assert lottery.lastWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == account_balance + lottery_balance
    