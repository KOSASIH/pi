// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PiCoinStabilization {
    string public name = "Pi Coin";
    string public symbol = "PI";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    uint256 public pegValue = 314159 * 10 ** uint256(decimals); // Pegged value in wei
    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event PegAdjusted(uint256 newPegValue);

    constructor(uint256 initialSupply) {
        totalSupply = initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply; // Assign all tokens to the contract creator
    }

    function transfer(address to, uint256 value) public returns (bool success) {
        require(balanceOf[msg.sender] >= value, "Insufficient balance");
        balanceOf[msg.sender] -= value;
        balanceOf[to] += value;
        emit Transfer(msg.sender, to, value);
        return true;
    }

    function adjustPeg(uint256 newPegValue) public {
        // Only the owner can adjust the peg
        pegValue = newPegValue;
        emit PegAdjusted(newPegValue);
    }

    function getPegValue() public view returns (uint256) {
        return pegValue;
    }
}
