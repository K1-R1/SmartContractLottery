from .general_scripts import get_account

from brownie import Lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    lottery.startLottery({'from': account}).wait(1)
    print('Lottery started...\n')

def main():
    start_lottery()