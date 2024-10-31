import sys

encoded = sys.argv[1]
print("#####")

# Define thresholds
UPPER_THRESHOLD = 2**160
LOWER_THRESHOLD = 2**150

for i in range(len(encoded) // 64):
    chunk = encoded[i*64:i*64+64]
    # print(f"Chunk {i+1}: {chunk}")

    try:
        # Convert the chunk to a uint256 value
        uint_value = int(chunk, 16)
    except ValueError:
        print(f"Invalid chunk (not hex): {chunk}")
        continue  # Skip to the next chunk

    if uint_value > UPPER_THRESHOLD:
        # More like a string, keep it as is
        print(f"As is: {chunk}")
    elif LOWER_THRESHOLD < uint_value <= UPPER_THRESHOLD:
        # More likely to be an address
        # Extract the last 40 hex characters (20 bytes)
        address = chunk[-40:]
        print(f"address: 0x{address}")
    else:
        # More like a number, print in scientific notation
        print(f"Number: {chunk} {uint_value}")

