from brownie import  accounts, web3, Wei, chain, reverts
import pytest



@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_nft_config(test_token, orbofi_nft):
    nft_contract = orbofi_nft
    test_erc_20 = test_token

    assert nft_contract.name() == "Test NFT"
    assert nft_contract.symbol() == "TEST"
    assert nft_contract.suffix() == "XD"
    assert nft_contract.LAUNCHPAD() =="0xd73b53cBe6A5FE32Ae4aE475d4EA9307bD7aAAfA"
    assert nft_contract.LAUNCH_MAX_SUPPLY() == 15000
    assert nft_contract.MINT_PRICE() == 100 * 10**18
    assert nft_contract.baseURI() == "https://jsonkeeper.com/b/J8J8"
    assert nft_contract.getCurrentSupply() == 0
    assert nft_contract.underlying() == test_erc_20


def test_minting(test_token, orbofi_nft):

    deployer = accounts[0]
    alice = accounts[2]
    nft_contract = orbofi_nft
    test_erc_20 = test_token
    mint_price = nft_contract.MINT_PRICE()
    quantity = 20
    amount = mint_price * quantity
    print(f"Minting price for {quantity} NFTs: ${amount/10**18}")
    
    #deployer erc20 balance before mint
    balance_before = test_erc_20.balanceOf(deployer)
    test_erc_20.approve(nft_contract, amount, {"from": deployer})
   
    with reverts("Not enough amount to mint"):
        nft_contract.mint(quantity, alice, amount-1, {"from": deployer})

    nft_contract.mint(quantity, alice, amount, {"from": deployer})

    assert nft_contract.balanceOf(alice) == quantity
    assert test_erc_20.balanceOf(deployer) == balance_before - amount

    return  nft_contract

def test_can_mint_only_20(test_token, orbofi_nft):
    deployer = accounts[0]
    alice = accounts[2]
    nft_contract = test_minting(test_token, orbofi_nft)
    test_erc_20 = test_token
    mint_price = nft_contract.MINT_PRICE()
    quantity = 1
    amount = mint_price * quantity
    
    
    #deployer erc20 balance before mint
    
    test_erc_20.approve(nft_contract, amount, {"from": deployer})

    with reverts("You are allowed to get only 20 NFTs"):
        nft_contract.mint(quantity, alice, amount, {"from": deployer})

    

    



    
