from brownie import accounts, web3, chain, MyToken, OrbofiNFT
import pytest



@pytest.fixture(scope="module", autouse=True)
def test_token():
    deployer = accounts[1]
    test_token = MyToken.deploy({"from": deployer})
    return test_token


@pytest.fixture(scope="module", autouse=True)
def orbofi_nft():
    """
    Deploys test ERC20 (BUSD) and NFT
    """

    deployer = accounts[0]
    base_uri = "https://jsonkeeper.com/b/J8J8"
    name = "Test NFT"
    symbol = "TEST"
    suffix = "XD"
    launchpad = "0xd73b53cBe6A5FE32Ae4aE475d4EA9307bD7aAAfA" #for testing only
    max_supply = 15_000
    

    contract = OrbofiNFT.deploy(name, symbol, base_uri, suffix, launchpad, max_supply, {"from": deployer})

    return contract
 

    