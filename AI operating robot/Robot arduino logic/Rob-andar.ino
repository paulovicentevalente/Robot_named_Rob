//Include the Falcon Robot library
#include <FalconRobot.h>
FalconRobotMotors motors(5, 7, 6, 8);

//Include the SoftwareSerial library
#include <SoftwareSerial.h>

//Create a new software  serial
SoftwareSerial bluetooth(11, 12); // TX, RX (Bluetooth)

// initializes 4 Object Distance Sensors on pins 2 and 3, 4 and 9, A0 and A1, A4 and A5
FalconRobotDistanceSensor dist_Sens_F(2, 3);  // (echo, trig)
FalconRobotDistanceSensor dist_Sens_T(4, 9);
FalconRobotDistanceSensor dist_Sens_E(A0, A1);
FalconRobotDistanceSensor dist_Sens_D(A4, A5);

int incomingByte;      // a variable to read incoming serial data: f - forward, d - right, e - left, t - backward, p - stop

int dist_f, dist_t, dist_e, dist_d, dist_f1, dist_t1, dist_e1, dist_d1;  // variable to store the distance value

void setup() {

  //Inicializa - Initialize - bluetooth serial
  bluetooth.begin(9600);

// envia conjunto de dados de inicialização - send initialization data

//  delay(100);

//  if (bluetooth.available() >0 ) {

//      read sensor distace in cm and store.
     delay(60);
     dist_f = dist_Sens_F.read();
     delay(60);
     dist_t = dist_Sens_T.read();
     delay(60);
     dist_e = dist_Sens_E.read();
     delay(60);
     dist_d = dist_Sens_D.read();

     dist_f1 = dist_f;
     dist_t1 = dist_t;
     dist_e1 = dist_e;
     dist_d1 = dist_d;

     bluetooth.print(dist_f);
     bluetooth.print(",");
     bluetooth.print(dist_t);
     bluetooth.print(",");
     bluetooth.print(dist_d);
     bluetooth.print(",");
     bluetooth.print(dist_e);
     bluetooth.print(",");
     bluetooth.print(dist_f1);
     bluetooth.print(",");
     bluetooth.print(dist_t1);
     bluetooth.print(",");
     bluetooth.print(dist_d1);
     bluetooth.print(",");
     bluetooth.println(dist_e1);

//  }

}

void loop() {

// see if there's incoming serial data: 
if (bluetooth.available() >0 ) {  

  incomingByte = bluetooth.read();
  

    // read the oldest byte in the serial buffer:

    if (incomingByte=='f'||incomingByte=='t'||incomingByte=='d'||incomingByte=='e'||incomingByte=='p' ) {   
    // read sensor distace in cm and store.
    delay(60);
    dist_f = dist_Sens_F.read();
    delay(60);
    dist_t = dist_Sens_T.read();
    delay(60);
    dist_e = dist_Sens_E.read();
    delay(60);
    dist_d = dist_Sens_D.read();

     
    // if it's a f (ASCII 72), go forward:

    if (incomingByte == 'f') {
     
      incomingByte='s';
     // go forward if protected against impact
      if (dist_f >20 && dist_e >10 && dist_d >10) {
      
        motors.drive(50, FORWARD);
        delay(250);
        motors.stop();
        delay(500);
     
     }
 
  
      delay(60);
      dist_f1 = dist_Sens_F.read();
      delay(60);
      dist_t1 = dist_Sens_T.read();
      delay(60);
      dist_e1 = dist_Sens_E.read();
      delay(60);
      dist_d1 = dist_Sens_D.read();
      
      // print starting ending point sensor values to serial port

      bluetooth.print(dist_f);
      bluetooth.print(",");
      bluetooth.print(dist_t);
      bluetooth.print(",");
      bluetooth.print(dist_d);
      bluetooth.print(",");
      bluetooth.print(dist_e);
      bluetooth.print(",");
      bluetooth.print(dist_f1);
      bluetooth.print(",");
      bluetooth.print(dist_t1);
      bluetooth.print(",");
      bluetooth.print(dist_d1);
      bluetooth.print(",");
      bluetooth.println(dist_e1);
   
    
    }
    
    if (incomingByte == 't') {
      incomingByte='s';
      
     // mover para trás
      if (dist_t > 20) {

        motors.drive(50, BACKWARD);
        delay(250);
        motors.stop();
        delay(500);      
      
      }

      delay(60);
      dist_f1 = dist_Sens_F.read();
      delay(60);
      dist_t1 = dist_Sens_T.read();
      delay(60);
      dist_e1 = dist_Sens_E.read();
      delay(60);
      dist_d1 = dist_Sens_D.read();

      // print starting ending point sensor values to serial port

      bluetooth.print(dist_f);
      bluetooth.print(",");
      bluetooth.print(dist_t);
      bluetooth.print(",");
      bluetooth.print(dist_d);
      bluetooth.print(",");
      bluetooth.print(dist_e);
      bluetooth.print(",");
      bluetooth.print(dist_f1);
      bluetooth.print(",");
      bluetooth.print(dist_t1);
      bluetooth.print(",");
      bluetooth.print(dist_d1);
      bluetooth.print(",");
      bluetooth.println(dist_e1);
    
    }

    if (incomingByte == 'e') {
      incomingByte='s';
      
          
     // mover para esquerda
      if (dist_e > 5 && dist_f > 5) {

        motors.leftDrive(50, BACKWARD);  // spin CCW
        motors.rightDrive(50, FORWARD); // spin CCW
        delay(250);
        motors.stop();
        delay(500);
      
      }

      delay(60);
      dist_f1 = dist_Sens_F.read();
      delay(60);
      dist_t1 = dist_Sens_T.read();
      delay(60);
      dist_e1 = dist_Sens_E.read();
      delay(60);
      dist_d1 = dist_Sens_D.read();

      // print starting ending point sensor values to serial port

      bluetooth.print(dist_f);
      bluetooth.print(",");
      bluetooth.print(dist_t);
      bluetooth.print(",");
      bluetooth.print(dist_d);
      bluetooth.print(",");
      bluetooth.print(dist_e);
      bluetooth.print(",");
      bluetooth.print(dist_f1);
      bluetooth.print(",");
      bluetooth.print(dist_t1);
      bluetooth.print(",");
      bluetooth.print(dist_d1);
      bluetooth.print(",");
      bluetooth.println(dist_e1);

    }
    
    if (incomingByte == 'd') {
      incomingByte='s';

         
     // mover para direita
      if (dist_d > 5 && dist_f > 5) {

        motors.leftDrive(50, FORWARD);  // spin CCW
        motors.rightDrive(50, BACKWARD); // spin CCW
        delay(250);
        motors.stop();
        delay(500);
      
      }
      delay(60);
      dist_f1 = dist_Sens_F.read();
      delay(60);
      dist_t1 = dist_Sens_T.read();
      delay(60);
      dist_e1 = dist_Sens_E.read();
      delay(60);
      dist_d1 = dist_Sens_D.read();

      // print starting ending point sensor values to serial port

      bluetooth.print(dist_f);
      bluetooth.print(",");
      bluetooth.print(dist_t);
      bluetooth.print(",");
      bluetooth.print(dist_d);
      bluetooth.print(",");
      bluetooth.print(dist_e);
      bluetooth.print(",");
      bluetooth.print(dist_f1);
      bluetooth.print(",");
      bluetooth.print(dist_t1);
      bluetooth.print(",");
      bluetooth.print(dist_d1);
      bluetooth.print(",");
      bluetooth.println(dist_e1);

       
    }

    if (incomingByte == 'p') {
      incomingByte='s';

            
     // parar
        motors.stop();
        delay(1000);
    
    }


      delay(60);
      dist_f1 = dist_Sens_F.read();
      delay(60);
      dist_t1 = dist_Sens_T.read();
      delay(60);
      dist_e1 = dist_Sens_E.read();
      delay(60);
      dist_d1 = dist_Sens_D.read();

      // print starting ending point sensor values to serial port

      bluetooth.print(dist_f);
      bluetooth.print(",");
      bluetooth.print(dist_t);
      bluetooth.print(",");
      bluetooth.print(dist_d);
      bluetooth.print(",");
      bluetooth.print(dist_e);
      bluetooth.print(",");
      bluetooth.print(dist_f1);
      bluetooth.print(",");
      bluetooth.print(dist_t1);
      bluetooth.print(",");
      bluetooth.print(dist_d1);
      bluetooth.print(",");
      bluetooth.println(dist_e1);
    }

}  
}
