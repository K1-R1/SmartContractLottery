// SPDX-License-Identifier: MIT

pragma solidity ^0.8;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

//All uint256 values will have 18 decimals

contract Lottery {
    address payable[] public players;
    uint256 public USDEntryFee;
    AggregatorV3Interface internal ETHUSDPriceFeed;

    constructor(address _priceFeedAddress) {
        USDEntryFee = 25 * (10**18);
        ETHUSDPriceFeed = AggregatorV3Interface(_priceFeedAddress);
    }

    function getEntranceFee() public returns (uint256) {
        (, int256 price, , , ) = ETHUSDPriceFeed.latestRoundData();
        //price has 8 decimals by default
        uint256 ETHUSDPrice = uint256(price) * 10**10;
        //multiply USDEntryFee by 10**18 to preserve 18 decimals in answer
        uint256 entryFee = (USDEntryFee * 10**18) / ETHUSDPrice;
        return entryFee;
    }

    function enter() public {
        //entry fee
        //store player
    }

    function startLottery() public {}

    function endLottery() public {}
}
