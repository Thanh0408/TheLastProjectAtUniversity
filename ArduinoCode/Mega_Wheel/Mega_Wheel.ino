#define W1_A 2
#define W1_D 3
#define W2_A 4
#define W2_D 5
#define W3_A 6
#define W3_D 7
#define W4_A 8
#define W4_D 9

#include <SerialCommand.h>
SerialCommand sCmd;
//Xem lai dong co de tinh so xung can thiet

void setup() {
  Serial.begin(9600);
  sCmd.addCommand("E",nextToGo);
  pinMode(W1_A, OUTPUT);
  pinMode(W1_D, OUTPUT);
  pinMode(W2_A, OUTPUT);
  pinMode(W2_D, OUTPUT);
  pinMode(W3_A, OUTPUT);
  pinMode(W3_D, OUTPUT);
  pinMode(W4_A, OUTPUT);
  pinMode(W4_D, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  sCmd.readSerial();
}

void nextToGo(void){
    digitalWrite(W1_A, 0);
    digitalWrite(W1_D, 1);
    digitalWrite(W2_A, 0);
    digitalWrite(W2_D, 1);
    digitalWrite(W3_A, 0);
    digitalWrite(W3_D, 1);
    digitalWrite(W4_A, 0);
    digitalWrite(W4_D, 1);
    delay(5000);
    digitalWrite(W1_D, 0);
    digitalWrite(W2_D, 0);
    digitalWrite(W3_D, 0);
    digitalWrite(W4_D, 0);
    Serial.write("1");
  }
