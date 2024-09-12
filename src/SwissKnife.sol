// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin-upgradeable/proxy/utils/Initializable.sol";

contract SwissKnife is Initializable, UUPSUpgradeable, OwnableUpgradeable {
    function initialize() public initializer {
        __Ownable_init(msg.sender); // Initialize ownership
    }

    function delegateForward(address _addr, bytes calldata _calldata) external {
        (bool success,) = _addr.call(_calldata);
        if(!success) {
            revert();
        }
    }

    function _authorizeUpgrade(address newImplementation) internal override onlyOwner {}
}

