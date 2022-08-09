// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MyToken is ERC20 {
    constructor() ERC20("TestBUSD", "BUSD") {
        _mint(msg.sender, 1000000 * 10 ** 18);
    }
}