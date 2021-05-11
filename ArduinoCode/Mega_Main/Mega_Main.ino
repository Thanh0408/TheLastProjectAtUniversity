#include <avr/io.h>
#include <avr/interrupt.h>
#define F_CPU 16000000
#define USART_BAUDRATE 9600
#define UBRR_VALUE (((F_CPU / (USART_BAUDRATE * 16UL))) - 1)

#include <SerialCommand.h>
SerialCommand sCmd;

//bien trang thai cua delta: 1 la dang hoat dong ,0 la k hoat dong
int deltaStatus;

void USART2Init(void);
void angle(void);
void goHome(void);
void USART2_send_char(char);
void USART2_send_string(char*);

void setup ()
{
  Serial.begin(9600);
  deltaStatus = 1;
  sCmd.addCommand("T", angle);
  sCmd.addCommand("H", goHome);
  sCmd.addCommand("DSTT", getDeltaStt);
  //send speed
  sCmd.addCommand("S",speed)

  noInterrupts();     
  pinMode(19,INPUT);
  pinMode(18,OUTPUT);
  
  USART2Init();
  //sei();
  interrupts();       
   //delay(100);
}
void loop()
{
   sCmd.readSerial();
}
void getDeltaStt(void){
  Serial.println(deltaStatus);
}

void speed(void){
  deltaStatus = 1;
  String cmd = "S\n";
  for(int i = 0; i < cmd.length(); i++){
    USART2_send_char(cmd[i]);
  }
}

void goHome(void){
  deltaStatus = 1;
  String cmd = "H\n";
  for(int i = 0; i < cmd.length(); i++){
    USART2_send_char(cmd[i]);
  }
}

void angle(void){
  deltaStatus = 1;
  char *arg;
  //lay toa do tu cmd
  arg = sCmd.next();
  String theta1 = (arg);
  arg = sCmd.next();
  String theta2 = (arg);
  arg = sCmd.next();
  String theta3 = (arg);
  String cmd = "T " + theta1 + " " + theta2 + " " + theta3 + "\n";
  //USART2_send_string(strdup(cmd.c_str()));
  
  //Serial.println(cmd.c_str);
  for(int i = 0; i < cmd.length(); i++){
    USART2_send_char(cmd[i]);
  }
}


void USART2_send_char(char c){
  while (!(UCSR2A & ( 1 << UDRE2))) {};
  UDR2 = c;
}

void USART2_send_string(char* s){
  while (*s){
    USART2_send_char(*s);
    s++;
  };
}

//interrupt 2: Delta
void USART2Init(void){
  // Set baud rate
  UCSR2A = 0x00; //Clear send and receive flags
  UBRR2H = (uint8_t)(UBRR_VALUE >> 8);
  UBRR2L = (uint8_t)UBRR_VALUE;
  // Set frame format to 8 data bits, no parity, 1 stop bit
  UCSR2C |= (1 << UCSZ20) | (1 << UCSZ21);
  UCSR2B |= (1<<RXEN2)|(1<<TXEN2)|(1<<RXCIE2);
}

ISR(USART2_RX_vect){
  while (!(UCSR2A & (1 << RXC2))) {};
  
  char ReceivedByte;
  ReceivedByte = UDR2; // Fetch the received byte value into the variable "ByteReceived"
  if(ReceivedByte == 1){
    deltaStatus = 0;
  }
}
