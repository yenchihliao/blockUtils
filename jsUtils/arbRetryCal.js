const { BigNumber, ethers } = require('ethers');

/* This is the goal
[
  Uint8Array(2) [ 164, 177 ],
  Uint8Array(32) [
    0, 0,  0,   0,  0, 0, 0, 0, 0,
    0, 0,  0,   0,  0, 0, 0, 0, 0,
    0, 0,  0,   0,  0, 0, 0, 0, 0,
    0, 0, 26, 129, 58
  ],
  '0x89156053e5b02ca2056d7007cf55747244224f6C',
  Uint8Array(5) [ 1, 239, 191, 41, 195 ],
  Uint8Array(6) [ 25, 18, 255, 240, 26, 97 ],
  Uint8Array(4) [ 1, 49, 45, 0 ],
  Uint8Array(2) [ 82, 8 ],
  '0x51c289a2C7aE30BC39D60F0d210cC17FA15C8950',
  Uint8Array(1) [ 1 ],
  '0x9C9F55ebc51D0D606227790d14Afcb706178dE98',
  Uint8Array(6) [ 24, 177, 53, 252, 178, 96 ],
  '0x856c363e043Ac34B19D584D3930bfa615947994E',
  '0x'
]
0x69f89682a4b1a000000000000000000000000000000000000000000000000000000000001a813a9489156053e5b02ca2056d7007cf55747244224f6c8501efbf29c3861912fff01a618401312d008252089451c289a2c7ae30bc39d60f0d210cc17fa15c895001949c9f55ebc51d0d606227790d14afcb706178de988618b135fcb26094856c363e043ac34b19d584d3930bfa615947994e80
*/
// Example usage data
const l2ChainId = 42161; // Example L2 Chain ID (Arbitrum One)
const fromAddress = '0x78046053E5B02Ca2056D7007cf55747244223E5B';
const fromAddress_aliased = '0x89156053e5b02ca2056d7007cf55747244224f6C';
const messageNumber = BigNumber.from(1737018);
const l1BaseFee = BigNumber.from(8317249987);
const destAddress = '0x51c289a2C7aE30BC39D60F0d210cC17FA15C8950';
const l2CallValue = BigNumber.from(1);
const l1Value = BigNumber.from(27569394031201);
const maxSubmissionFee = BigNumber.from(27149394031200);
const excessFeeRefundAddress = '0x856C363E043AC34B19D584D3930BFA615947994E';
const callValueRefundAddress = '0x9C9F55EBC51D0D606227790D14AFCB706178DE98';
const gasLimit = BigNumber.from(21000);
const maxFeePerGas = BigNumber.from(20000000);
const data = '0x';

// Function to format numbers by removing leading zeros
const formatNumber = (value) => {
  return ethers.utils.arrayify(ethers.utils.stripZeros(value.toHexString()));
};

// Helper function to pad a value to 32 bytes
const zeroPad = (value, length) => {
  return ethers.utils.zeroPad(value, length);
};

// Constructing the fields array
const fields = [
  formatNumber(BigNumber.from(l2ChainId)),
  zeroPad(formatNumber(BigNumber.from(messageNumber)), 32),
  fromAddress_aliased,
  formatNumber(l1BaseFee),
  formatNumber(l1Value),
  formatNumber(maxFeePerGas),
  formatNumber(gasLimit),
  // when destAddress is 0x0, arbos treat that as nil
  destAddress === ethers.constants.AddressZero ? '0x' : destAddress,
  formatNumber(l2CallValue),
  callValueRefundAddress,
  formatNumber(maxSubmissionFee),
  excessFeeRefundAddress,
  data
];


console.log('Fields:', fields);
// Arbitrum submit retry transactions have type 0x69
const rlpEnc = ethers.utils.hexConcat([
  '0x69',
  ethers.utils.RLP.encode(fields),
]);
console.log('encode:', rlpEnc);

// Calculate the keccak256 hash
const retryableId = ethers.utils.keccak256(rlpEnc);

console.log('Retryable ID:', retryableId);