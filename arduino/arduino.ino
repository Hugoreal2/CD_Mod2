
constexpr int BAUD_RATE = 9600;
constexpr bool INTRODUCE_ERROR = true;

//////////////////////////////
//        MAIN FUNCTIONS
//////////////////////////////
void setup() {
  Serial.begin(BAUD_RATE);
  while (!Serial) continue;
}

void loop() {
  if (Serial.available() == 0) return;

  int target_number = Serial.read();
  bool send_checksum = Serial.read() != 0;

  unsigned long checksum = 0lu;

  for (int i = 0; i < target_number; i++) {
    if (isPrime(i)) {
      const byte low = lowByte(i);
      const byte high = highByte(i);

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

  // Termination Message
  Serial.write(0xFF);
  Serial.write(0xFF);

  // Serial.write(lowByte(checksum));
  // Serial.write(highByte(checksum));

  delay(1000); // Don't spam the serial port
}

//////////////////////////////
//        MAIN FUNCTIONS
//////////////////////////////
bool isPrime(int n) {
  if (n <= 1) return false;
  if (n <= 3) return true;
  if (n % 2 == 0 || n % 3 == 0) return false;

  for (int i = 5; i * i <= n; i += 6) {
    if (n % i == 0 || n % (i + 2) == 0) return false;
  }

  return true;
}

