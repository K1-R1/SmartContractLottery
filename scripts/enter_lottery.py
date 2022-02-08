from multiprocessing.connection import wait
from os import access

from eth_account import Account
from .general_scripts import get_account

from brownie import Lottery

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    entrance_fee = lottery.getEntranceFee().return_value
    lottery.enter({'from': account, 'value': entrance_fee}).wait(1)
    print('Lottery entered...')

def main():
    enter_lottery()