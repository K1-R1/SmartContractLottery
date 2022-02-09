# SmartContractLottery

A contract to:
- Initiate a lottery
- Allow anyone to enter with a sufficient deposit
- Allow the deployer of the contract to choose when to end the lottery, and use chainlink's VRF to randomly select a winner. Before resseting the contrcat ready for another lottery

The contract is designed to be deployed and tested on multiple networks, currently those networks are:
- Local developmemt networks
- Rinkeby test networks

The contract has been unit tested locally, with intergration testing performed on Rinkeby.

### Made with
- solidity
- python
- brownie 

### Deployed to
- local ganache network
- rinkeby test network
