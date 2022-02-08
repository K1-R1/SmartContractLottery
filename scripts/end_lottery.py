import time

from .general_scripts import get_account, fund_with_link

from brownie import Lottery


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    fund_with_link(lottery.address)
    lottery.endLottery({'from': account}).wait(1)
    time.sleep(10)
    print(f"{lottery.lastWinner()} is the new winner ...")

def main():
    end_lottery()

