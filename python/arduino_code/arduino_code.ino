void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() >= 2) {
    // Read the incoming 2 bytes
    int number = Serial.read() | (Serial.read() << 8);
    unsigned long checksum = 0;

    // Collect all prime numbers up to the given number
    for (int i = 2; i <= number; i++) {
      if (isPrime(i)) {
        byte low = lowByte(i);
        byte high = highByte(i);

        // Send each prime number as 2 bytes
        Serial.write(low);
        Serial.write(high);

        // Add to checksum
        checksum += (high << 8) | low;

        // Handle carry around
        while (checksum >> 16) {
          checksum = (checksum & 0xFFFF) + (checksum >> 16);
        }
      }
    }

    // Final checksum calculation: one's complement
    checksum = ~checksum & 0xFFFF;

    // Send checksum as 2 bytes
    Serial.write(lowByte(checksum));
    Serial.write(highByte(checksum));
  }
}

bool isPrime(int num) {
  if (num <= 1) return false;
  for (int i = 2; i <= sqrt(num); i++) {
    if (num % i == 0) return false;
  }
  return true;
}
