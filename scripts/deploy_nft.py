from brownie import Contract, accounts, OrbofiNFT, MyToken, config, network
from scripts.helpful_scripts import get_account


def deploy_erc_token():
    deployer = get_account()

    if len(MyToken) > 0:
        return MyToken[-1]
    
    else:
        contract = MyToken.deploy({"from": deployer})
        return contract



def deploy_nft():
    deployer = get_account()
    base_uri = "https://jsonkeeper.com/b/J8J8"
    name = "Test NFT"
    symbol = "TEST"
    suffix = "XD"
    launchpad = config["networks"][network.show_active()]["launchpad"]
    max_supply = 15_000
    # underlying = deploy_erc_token()


    # Deploy the NFT contract
    contract = OrbofiNFT.deploy(name, symbol, base_uri, suffix, launchpad, max_supply, {"from": deployer}, publish_source=config["networks"][network.show_active()]["verify"])
 


    return contract

def main():
    deploy_nft()
