#include <SPI.h>                //Include the libraries for the display
#include <Wire.h>

#define NUM_LEDS 1
#define CPU_TEMP_PIN 11
#define CPU_LOAD_PIN 9
#define RAM_LOAD_PIN 5
#define GPU_LOAD_PIN 3


const byte numChars = 17;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

// variables to hold the parsed data
char messageFromPC[numChars] = {0};
int integerFromPC = 0;
float floatFromPC = 0.0;


boolean newData = false;

int cpuTempValue = 0;  //Variable for the CPU temp
int cpuLoadValue = 0;  //Variable for the CPU load
int ramLoadValue = 0;  //Variable for the RAM load
int gpuLoadValue = 0;  //Variable for the GPU load


void setup() { 
  Serial.begin(9600);        
}

void loop() 
{ 

  int a = 255 * 3.14 / 5;
  analogWrite(CPU_TEMP_PIN, a * cpuTempValue / 50);        

  int b = 255 * 3.1 / 5;
  analogWrite(CPU_LOAD_PIN, b * cpuLoadValue / 100);      

  int c = 255 * 3.05 / 5;
  analogWrite(RAM_LOAD_PIN, c * ramLoadValue / 100);      

  int d = 255 * 3.06 / 5;
  analogWrite(GPU_LOAD_PIN, d * gpuLoadValue / 100);  

    int cpuTempOffset = 1;
    int cpuLoadOffset = 5;
    int ramLoadOffset = 9;
    int gpuLoadOffset = 13;
     

  recvWithStartEndMarkers();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
            // this temporary copy is necessary to protect the original data
            //   because strtok() used in parseData() replaces the commas with \0
        parseData();
        newData = false;
    }
}

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            } else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        } else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}


void parseData() {      // split the data into its parts
    
    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(tempChars,",");      // get the first part - the string
    cpuTempValue = atoi(strtokIndx);     // convert this part to an integer
    cpuTempValue = constrain(cpuTempValue, 40, 95) - 40; 
 
    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    cpuLoadValue = atoi(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, ",");
    ramLoadValue = atof(strtokIndx);     // convert this part to a float
    
    strtokIndx = strtok(NULL, ",");
    gpuLoadValue = atof(strtokIndx);     // convert this part to a float
}

