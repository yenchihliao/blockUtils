// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin-upgradeable/proxy/utils/Initializable.sol";

contract SwissKnife is Initializable, UUPSUpgradeable, OwnableUpgradeable {
    function initialize(address _owner) public initializer {
        __Ownable_init(_owner); // Initialize ownership
        __UUPSUpgradeable_init(); // Initialize UUPS upgradeability
    }

    function delegateForward(address _addr, bytes calldata _calldata) payable external onlyOwner {
        (bool success,) = _addr.call{value:msg.value}(_calldata);
        if(!success) {
            revert();
        }
    }

    function _authorizeUpgrade(address newImplementation) internal override onlyOwner {}
}

