void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() >= 2) {
    // Read the incoming 2 bytes
    int number = Serial.read() | (Serial.read() << 8);
    for (int i = 2; i <= number; i++) {
      if (isPrime(i)) {
        // Send each prime number as 2 bytes
        // Serial.write(i);
        Serial.write(lowByte(i));
        Serial.write(highByte(i));
      }
    }
  }
}

bool isPrime(int num) {
  if (num <= 1) return false;
  for (int i = 2; i <= sqrt(num); i++) {
    if (num % i == 0) return false;
  }
  return true;
}
