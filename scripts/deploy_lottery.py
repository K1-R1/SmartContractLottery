from .general_scripts import get_account, get_contract
from .start_lottery import start_lottery
from .enter_lottery import enter_lottery
from .end_lottery import end_lottery

from brownie import Lottery, network, config

def deploy_lottery():
    account = get_account()
    Lottery.deploy(
        get_contract('eth_usd_price_feed').address,
        get_contract('vrf_coordinator').address,
        get_contract('link_token').address,
        config['networks'][network.show_active()]['vrf_fee'],
        config['networks'][network.show_active()]['vrf_keyhash'],
        {'from': account},
        publish_source = config['networks'][network.show_active()]['verify']
        )

def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()