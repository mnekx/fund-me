
from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import deploy_mocks, get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS

# config for gar prices
from brownie.network import gas_price
from brownie.network.gas.strategies import LinearScalingStrategy
# from brownie.network.gas.strategies import GasNowStrategy
# gas_strategy = GasNowStrategy("fast")

def set_default_gas():
    gas_strategy = LinearScalingStrategy("10 gwei", "50 gwei", 1.1)
    gas_price(gas_strategy)

def deploy_fund_me():
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config['networks'][network.show_active()]['eth_usd_price_feed']
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(price_feed_address,{'from': account}, publish_source=config['networks'][network.show_active()].get('verify'))
    print(f'Contract deployed to {fund_me.address}')
    return fund_me

def main():
    set_default_gas()
    deploy_fund_me()
