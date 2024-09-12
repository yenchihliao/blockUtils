'''
This file generates keys pairs from given(env var) mnemonics
'''
import os
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from eth_account import Account

# Read the mnemonic from the environment variable
mnemonic = os.getenv('MNEMONICS')

if not mnemonic:
    raise ValueError("MNEMONIC environment variable not set")

# Generate seed from mnemonic
seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

# Initialize BIP44 for Ethereum
bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)

# Number of addresses to derive
num_addresses = 10

# Lists to store addresses and private keys
addresses = []
private_keys = []

for i in range(num_addresses):
    bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(i)
    private_key = bip44_acc.PrivateKey().Raw().ToHex()
    account = Account.from_key(private_key)
    addresses.append(account.address)
    private_keys.append(private_key)

# Print the derived addresses and private keys
for i in range(num_addresses):
    print(f"Address {i+1}: {addresses[i]}")
    print(f"Private Key {i+1}: {private_keys[i]}")

