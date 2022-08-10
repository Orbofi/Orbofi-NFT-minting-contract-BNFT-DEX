from brownie import  accounts, web3, Wei, chain, reverts
import pytest
from web3 import Web3



@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_nft_config( orbofi_nft):
    nft_contract = orbofi_nft
   

    assert nft_contract.name() == "Test NFT"
    assert nft_contract.symbol() == "TEST"
    assert nft_contract.suffix() == "XD"
    assert nft_contract.LAUNCHPAD() =="0xd73b53cBe6A5FE32Ae4aE475d4EA9307bD7aAAfA"
    assert nft_contract.LAUNCH_MAX_SUPPLY() == 15000
    assert nft_contract.MINT_PRICE() == Web3.toWei(0.3, "ether")
    assert nft_contract.baseURI() == "https://jsonkeeper.com/b/J8J8"
    assert nft_contract.getCurrentSupply() == 0
    


def minting( orbofi_nft):

    deployer = accounts[0]
    alice = accounts[2]
   
    mint_price = orbofi_nft.MINT_PRICE()
    quantity = 20
    amount = mint_price * quantity
    print(f"Minting price for {quantity} NFTs: {amount/10**18} BNB")
    
    #deployer  balance before mint
    balance_before = deployer.balance()
   
    with reverts("Not enough amount to mint"):
        orbofi_nft.mint(quantity, alice, {"from": deployer, "value": amount - 1})

    orbofi_nft.mint(quantity, alice, {"from": deployer, "value": amount})

    assert orbofi_nft.balanceOf(alice) == quantity
    assert orbofi_nft.balance() == amount
    assert deployer.balance() == balance_before - amount

    return  orbofi_nft

def test_can_mint_only_20( orbofi_nft):
    deployer = accounts[0]
    alice = accounts[2]
    nft_contract = minting( orbofi_nft)
    
    mint_price = nft_contract.MINT_PRICE()
    quantity = 1
    amount = mint_price * quantity
    
    
    with reverts("You are allowed to get only 20 NFTs"):
        nft_contract.mint(quantity, alice, {"from": deployer, "value": amount})


def test_withdraw_bnb(orbofi_nft):
    deployer = accounts[0]
    alice = accounts[2]
    nft_contract = minting( orbofi_nft)

    balance_before = deployer.balance()
    
    with reverts("Ownable: caller is not the owner"):
        nft_contract.withdrawBNB( {"from": alice})

    nft_contract.withdrawBNB({"from": deployer})
    assert nft_contract.balance() == 0
    assert deployer.balance() >= balance_before 


def test_withdraw_erc_20(orbofi_nft, test_token):
    deployer = accounts[1]
    admin = accounts[0]
    

    amount = Web3.toWei(300, "ether")
    test_token.transfer(orbofi_nft, amount, {"from": deployer})

    assert test_token.balanceOf(orbofi_nft) == amount
    assert test_token.balanceOf(admin) == 0

    with reverts("Ownable: caller is not the owner"):
        orbofi_nft.withdrawERC20(test_token, {"from": accounts[3]})

    orbofi_nft.withdrawERC20(test_token,  {"from": admin})

    assert test_token.balanceOf(orbofi_nft) == 0
    assert test_token.balanceOf(admin) == amount
    
    
    

    



    
