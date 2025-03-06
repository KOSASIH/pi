// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract GovernanceToken is ERC20, Ownable {
    // Mapping from proposal ID to votes
    mapping(uint256 => mapping(address => uint256)) public votes;
    mapping(uint256 => uint256) public totalVotes;

    // Event for proposal voting
    event Voted(address indexed voter, uint256 proposalId, uint256 amount);

    constructor(uint256 initialSupply) ERC20("Governance Token", "GOV") {
        _mint(msg.sender, initialSupply * (10 ** decimals()));
    }

    // Function to vote on a proposal
    function vote(uint256 proposalId, uint256 amount) external {
        require(amount > 0, "Amount must be greater than 0");
        require(balanceOf(msg.sender) >= amount, "Insufficient token balance");

        // Transfer tokens from the voter to the contract
        _transfer(msg.sender, address(this), amount);

        // Update votes
        votes[proposalId][msg.sender] += amount;
        totalVotes[proposalId] += amount;

        emit Voted(msg.sender, proposalId, amount);
    }

    // Function to withdraw tokens after voting
    function withdrawVotes(uint256 proposalId) external {
        uint256 amount = votes[proposalId][msg.sender];
        require(amount > 0, "No votes to withdraw");

        // Reset the votes
        votes[proposalId][msg.sender] = 0;
        totalVotes[proposalId] -= amount;

        // Transfer tokens back to the voter
        _transfer(address(this), msg.sender, amount);
    }

    // Function to check the voting power of an address for a specific proposal
    function getVotingPower(uint256 proposalId, address voter) external view returns (uint256) {
        return votes[proposalId][voter];
    }
}
