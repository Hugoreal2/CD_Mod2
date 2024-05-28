
def ip_checksum(data: bytes) -> int:
  """
  Calculates the IP checksum for a given byte array.

  Args:
      data: A byte array representing the IP header or data.

  Returns:
      An integer representing the 16-bit checksum.
  """
  if len(data) % 2 != 0:
    raise ValueError("data length must be a multiple of 2")

  words = [data[i] << 8 | data[i + 1] for i in range(0, len(data), 2)]

  checksum = sum(words)

  while checksum > 0xffff:
    checksum = (checksum & 0xffff) + (checksum >> 16)

  return (~checksum) & 0xffff

# Example usage
data = bytes([0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111])
checksum = ip_checksum(data)
print(f"Checksum: {checksum:04X}")
