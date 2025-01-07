// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Script.sol";
import {Create2} from "@openzeppelin/contracts/utils/Create2.sol";

import {SwissKnife} from "../src/SwissKnife.sol";
import {UUPSProxy} from "../src/UUPSProxy.sol";

contract DeploySwissKnife is Script {
    modifier broadcastAll() {
        vm.startBroadcast();
        _;
        vm.stopBroadcast();
    }

    function run() external broadcastAll {
        // Deploy SwissKnife implementation contract
        bytes32 _salt = keccak256(abi.encodePacked("SwissKnifeDeploymentSalt"));
        address _impl = Create2.deploy(0, _salt, type(SwissKnife).creationCode);

        // Deploy the SwissKnife proxy contract using create2
        // // Calculate a salt for deterministic deployment
        _salt = keccak256(abi.encodePacked("SwissKnifeProxySalt"));
        bytes memory _bytecode = abi.encodePacked(
            type(UUPSProxy).creationCode,
            abi.encode(_impl, abi.encodeWithSelector(SwissKnife.initialize.selector, msg.sender))
        );
        address _proxy = Create2.deploy(0, _salt, _bytecode);

        // Confirm deployment
        console.log("SwissKnife logic deployed at:", _impl); // 0x017F8cBFbabf7bA7c38078f7FBF8275D78D9f374
        console.log("SwissKnife proxy deployed at:", _proxy); // 0x2b223c44C2Ad3f1cFf0022e91c87ad7DbfA05026
    }
}
