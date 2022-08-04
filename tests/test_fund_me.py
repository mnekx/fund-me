
from logging import exception
import pytest
from scripts.deploy import deploy_fund_me, set_default_gas
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from brownie import accounts, network, exceptions
from brownie.network import gas_price
from brownie.network.gas.strategies import LinearScalingStrategy

def test_can_fund_and_withdraw():
    account = get_account()
    set_default_gas()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee()
    tx1 = fund_me.fund({'from': account, 'value': entrance_fee})
    tx1.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    tx2 = fund_me.withdraw({'from': account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0

def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip('Only for local testing!')
    gas_strategy = LinearScalingStrategy("1 gwei", "5000000 gwei", 1.1)
    gas_price(gas_strategy)
    fund_me = deploy_fund_me()
    bad_actor = accounts[1]
    print(f'BAD ACTOR {bad_actor}')
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({'from': bad_actor, 'gas_price': gas_strategy})


