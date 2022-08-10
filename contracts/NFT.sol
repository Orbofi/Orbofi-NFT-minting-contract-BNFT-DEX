//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "../interfaces/IERC20.sol";



contract OrbofiNFT is ERC721Enumerable, Ownable {

    using Strings for uint256;
    using Counters for Counters.Counter;

    string public baseURI;
    string public suffix;

    
    uint256 public LAUNCH_MAX_SUPPLY;    // max launch supply
    uint256 public LAUNCH_SUPPLY;        // current launch supply
    
    address public LAUNCHPAD;

    
    uint256 public MINT_PRICE = 0.3 ether; // ~100 USD per token
    Counters.Counter private currentTokenId;

    modifier onlyLaunchpad() {
        require(LAUNCHPAD != address(0), "launchpad address must set");
        require(msg.sender == LAUNCHPAD, "must call by launchpad");
        _;
    }

    

    constructor(string memory name_, string memory symbol_, string memory baseURI_, string memory suffix_, address launchpad, uint256 maxSupply) ERC721(name_, symbol_) {
        baseURI = baseURI_;
        suffix = suffix_;
        LAUNCHPAD = launchpad;
        LAUNCH_MAX_SUPPLY = maxSupply;
        
    }

    /**
	 * Mints some quantity of NFTs
	 * @param quantity of NFTs to mint
	 * @param receiver address that will receive NFT
	 * @notice Can not mint  more than 20 NFTs by account
	 */
    function mint( uint256 quantity, address receiver) payable public  {
        
        require(currentTokenId.current() <= LAUNCH_MAX_SUPPLY, "Max supply reached");
        require(balanceOf(receiver) + quantity <= 20, 'You are allowed to get only 20 NFTs');
        require(msg.value >= quantity * MINT_PRICE, "Not enough amount to mint");
        
        

        for (uint256 i = 0; i < quantity; i++) {

            _mint(receiver, currentTokenId.current());

            unchecked {
                 currentTokenId.increment();
            }

        }    

  }



    function setMintPrice(uint256 amount) external onlyOwner  {
        MINT_PRICE = amount;
    }

    
    function _baseURI() internal view virtual override returns (string memory){
        return baseURI;
    }

    function setBaseURI(string memory _newURI) external onlyOwner {
        baseURI = _newURI;
    }

    
    // called by the launchpad
    function mintTo(address to, uint size) external onlyLaunchpad {
        require(to != address(0), "can't mint to empty address");
        require(size > 0, "size must greater than zero");
        require(LAUNCH_SUPPLY + size <= LAUNCH_MAX_SUPPLY, "max supply reached");

        for (uint256 i=1; i <= size; i++) {
            _mint(to, ERC721Enumerable.totalSupply() + i);
            LAUNCH_SUPPLY++;
        }
    }


    /**
	 * Withdraw ERC20 from contract to owner address
	 * @param contractAddress addres of ERC20 contract
	 * @notice any ERC20 token can be withdrawed
	 * @notice only owner can withdraw 
	 */
	function withdrawERC20(address contractAddress) external onlyOwner {
		uint256 balance = IERC20(contractAddress).balanceOf(address(this));
		bool succeded = IERC20(contractAddress).transfer(msg.sender, balance);
		require(succeded, 'Withdrawable: Transfer did not happen');
	}

	/**
	 * Withdraw ETH from contract to owner address
	 * @notice only owner can withdraw
	 */
	function withdrawETH() external onlyOwner {
		(bool sent, ) = msg.sender.call{value: address(this).balance}('');
		require(sent, 'Failed to withdraw ETH');
	}


    function tokenURI(uint256 tokenId) public view virtual override returns (string memory) {
        require(_exists(tokenId), "ERC721Metadata: URI query for nonexistent token.");
        return string(abi.encodePacked(baseURI, tokenId.toString(), suffix));
    }
    

    function getMaxLaunchpadSupply() view public returns (uint256) {
        return LAUNCH_MAX_SUPPLY;
    }

    function getLaunchpadSupply() view public returns (uint256) {
        return LAUNCH_SUPPLY;
    }

    function getCurrentSupply() view external returns(uint256) {
        return  currentTokenId.current();
   }

}