#define X_END 9    //cong tac hành trình
#define Y_END 10
#define Z_END 11
#define EN 8
#define X_DIR 5    //chieu quay cua dong co
#define Y_DIR 6
#define Z_DIR 7
#define X_STP 2    //cap sung dong co
#define Y_STP 3
#define Z_STP 4
// chan tuoi nuoc tren shield
#define PUMP 13
//1 xung bánh răng lớn quay được 0.6 độ, bánh nhỏ quay 1.8 độ
#define ANGLE_PER_STEP 0.03

//import processing.serial.*
#include <SerialCommand.h>
SerialCommand sCmd;
int halfC = 500;
int n_stepX = 0;
int n_stepY = 0;
int n_stepZ = 0;

// Hàm điều khiển hướng và số bước của động cơ
void step(boolean dir, byte dirPin, byte stepperPin, int steps)
{
  digitalWrite(dirPin, dir);
  delay(halfC);
  for (int i = 0; i < steps; i++) {
    digitalWrite(stepperPin, HIGH);
    delayMicroseconds(halfC);  
    digitalWrite(stepperPin, LOW);
    delayMicroseconds(halfC);  
  }
}

void step2(int stepX, int stepY, int stepZ)
{
  if(stepX < 0)               
  {
    //neu step <0 thi xet huong cua set X nguoc chieu kim dong ho)
    digitalWrite(X_DIR, 0);
    stepX = -stepX;
  }else
  {
    digitalWrite(X_DIR, 1);
  }
  if(stepY < 0)               
  {
    //neu step <0 thi xet huong cua set Y nguoc chieu kim dong ho)
    digitalWrite(Y_DIR, 0);
    stepY = -stepY;
  }else
  {
    digitalWrite(Y_DIR, 1);
  }
  if(stepZ < 0)               
  {
    //neu step <0 thi xet huong cua set Z nguoc chieu kim dong ho)
    digitalWrite(Z_DIR, 0);
    stepZ = -stepZ;
  }else
  {
    digitalWrite(Z_DIR, 1);
  }
  delay(50);

  // tim gia tri step max
  int iteration = max(max(stepX, stepY),stepZ);
  for(int i = 0; i < iteration; i++)
  {
    digitalWrite(X_STP, (i<stepX));
    digitalWrite(Y_STP, (i<stepY));
    digitalWrite(Z_STP, (i<stepZ));
    delayMicroseconds(halfC);  
    digitalWrite(X_STP, LOW);
    digitalWrite(Y_STP, LOW);
    digitalWrite(Z_STP, LOW);
    delayMicroseconds(halfC);  
  }
}

void goHome2()
{
  //cho quay nguoc chieu kim dong ho
  digitalWrite(X_DIR, 0);
  digitalWrite(Y_DIR, 0);
  digitalWrite(Z_DIR, 0);
  delay(halfC);
  //doc trang thai cua cong tac hanh trinh
  int stopXStt = digitalRead(9);
  int stopYStt = digitalRead(10);
  int stopZStt = digitalRead(11);
  n_stepX = 0;
  n_stepY = 0;
  n_stepZ = 0;
  
  while(stopXStt == 1 || stopYStt == 1 || stopZStt == 1){
    //suat xung khi cong tac hanh trinh open
    digitalWrite(X_STP, stopXStt == 1);
    digitalWrite(Y_STP, stopYStt == 1);
    digitalWrite(Z_STP, stopZStt == 1);
    delayMicroseconds(halfC);  
    digitalWrite(X_STP, LOW);
    digitalWrite(Y_STP, LOW);
    digitalWrite(Z_STP, LOW);
    delayMicroseconds(halfC);  
    //update state cua cong tac hanh trinh
    stopXStt = digitalRead(X_END);
    stopYStt = digitalRead(Y_END);
    stopZStt = digitalRead(Z_END);   
  }
  
  //reset lai so sung cho 3 dong co
  //n_stepX = n_stepY = n_stepZ = 0;
  Serial.write(1);
} 


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  sCmd.addCommand("T", angle);
  sCmd.addCommand("H", goHome2);
  sCmd.addCommand("S", setSpeed);
  pinMode(PUMP, OUTPUT);
  
  pinMode(X_DIR, OUTPUT);
  pinMode(X_STP, OUTPUT);
  pinMode(Y_DIR, OUTPUT); 
  pinMode(Y_STP, OUTPUT);
  pinMode(Z_DIR, OUTPUT);
  pinMode(Z_STP, OUTPUT);
  pinMode(EN, OUTPUT);
  digitalWrite(EN, LOW);

  pinMode(X_END, INPUT_PULLUP);
  pinMode(Y_END, INPUT_PULLUP);
  pinMode(Z_END, INPUT_PULLUP);
  delayMicroseconds(halfC);
 
  goHome2();
  delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:
  sCmd.readSerial();
}

void setSpeed(){
  char *sp;
  sp = sCmd.next();
  int speed = atoi(sp); 
  halfC = speed;
  Serial.write(1);
}

void angle(){
  char *arg;
  //lay toa do tu cmd
  arg = sCmd.next();
  float theta1 = atof(arg);
  arg = sCmd.next();
  float theta2 = atof(arg);
  arg = sCmd.next();
  float theta3 = atof(arg);
  //chuyen goc(angle) to step
  int n_stepX_new = (int)(theta1 / ANGLE_PER_STEP);
  int n_stepY_new = (int)(theta2 / ANGLE_PER_STEP);
  int n_stepZ_new = (int)(theta3 / ANGLE_PER_STEP);
  //chenh lech xung so voi toa do cu
  step2(n_stepX_new - n_stepX, n_stepY_new - n_stepY, n_stepZ_new - n_stepZ);
  //save so buoc de chuan bi don so xung moi
  n_stepX = n_stepX_new;
  n_stepY = n_stepY_new;
  n_stepZ = n_stepZ_new;
  delay(500);
  // Watering
  digitalWrite(PUMP, HIGH);
  delay(500);
  digitalWrite(PUMP, LOW);
  
  Serial.write(1);
}
