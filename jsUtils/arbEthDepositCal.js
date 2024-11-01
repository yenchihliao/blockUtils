const { ethers, BigNumber } = require('ethers');

// Example inputs
const childChainId = 42161;
const messageNumber = 1738248;
const fromAddress = "0xbe029E0cb91017E74C5b788110e0B2037362470f";
const toAddress = "0xbe029E0cb91017E74C5b788110e0B2037362470f";
const value = 7526694164;

// Function to format BigNumber and remove leading zeros
const formatNumber = (numberVal) => {
  return ethers.utils.arrayify(ethers.utils.stripZeros(numberVal.toHexString()));
};

// Function to pad a value to 32 bytes
const zeroPad = (value, length) => {
  return ethers.utils.zeroPad(value, length);
};

// Convert numbers to BigNumber format
const chainId = BigNumber.from(childChainId);
const msgNum = BigNumber.from(messageNumber);
const val = BigNumber.from(value);

// Constructing the fields array
const fields = [
  formatNumber(chainId),
  zeroPad(formatNumber(msgNum), 32),
  ethers.utils.getAddress(fromAddress),
  ethers.utils.getAddress(toAddress),
  formatNumber(val),
];

// Arbitrum ETH deposit transactions have type 0x64
const rlpEnc = ethers.utils.hexConcat([
  '0x64',
  ethers.utils.RLP.encode(fields),
]);

// Calculate and log the keccak256 hash
const retryableId = ethers.utils.keccak256(rlpEnc);
console.log('Retryable ID:', retryableId);
