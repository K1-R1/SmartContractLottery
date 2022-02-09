import time

from .general_scripts import get_account, fund_with_link

from brownie import Lottery


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    fund_with_link(lottery.address)
    lottery.endLottery({'from': account}).wait(1)
    print('Awaiting respone from VRFCoordinator...')
    time.sleep(180)
    print(f"{lottery.lastWinner()} is the new winner ...")

def main():
    end_lottery()

