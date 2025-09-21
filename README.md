# Analog PC Stats Set Up/ReadMe

## To RetrieveData About CPU Temperature:  
- Install Core Temp: https://www.alcpu.com/CoreTemp/
- Plugin Core Temp Remote Server: https://www.alcpu.com/CoreTemp/addons.html 

### Add the Plugin to the Core Temp: 
1. Install .Net 3.5. Go to 'Turn Windows features on or off' (under Settings in the Start screen), tick .NET Framework 3.5 and click OK.
2. Open the folder where Core Temp is installed, create a 'plugins' folder if it doesn't exist and extract the zip file into a 'CoreTempRemoteServer' folder.
3. Restart Core Temp, go to Tools, Plug-in manager and enable plug-ins.
4. Select the plug-in and click Start, the status should change to 'Started'. You should be prompted to unblock Core Temp in Windows' Firewall, you must do it, or else it will block the server and you won't be able to connect.
 *If you wish to see the connection status of the server, or change the default listening port you can click 'Configure' now. 
5. NOTE: Double check if the port is 5200. 
6. Close the manager.

Reference: https://www.alcpu.com/forums/viewtopic.php?t=1945 

## To Retrieve Data About CPU, RAM, and GPU Usage: 
1. Install Open Hardware Monitor: https://openhardwaremonitor.org/ 
2. Open the software, and go to ‘Options’, ‘Remote Web Server’, and ‘Run’. 
3. Note: Check the port is 8085 under ‘Port’

## Install Python, if Needed: 
1. Install Python 3+ (tested with 3.4-3.7), making sure to check the "Add Python 3.X to PATH" checkbox so you can run it from the Command Prompt. screenshot
2. Install the pyserial package by running  `pip install pyserial` in a Command Prompt.
3. Download the pcStats.py file and edit the following constant values to match the names in the Open Hardware Monitor, and your IP address. 
```
RAM_NAME = 'Generic Memory'
CPU_NAME = 'ABC 123'
GPU_NAME = 'DFC 456'

HOST = 'xxx.xxx.xxx.xxx'  # (localhost)
CORE_TEMP_PORT = 5200  # Core temp port 
OHW_PORT = 8085 # Open Hardware Monitor Port 
ARDUINO_PORT = 'COM3' # Arduino port
``` 

## Making Everything Run on Startup: 
### Set these options in Open Hardware Monitor: 
- Start Minimized
- Minimize To Tray 
- Run On Windows Startup 

### In Core Temp: 
1. Go to ‘Options’, ‘Settings’, ‘General’. 
- Select ‘Start Core Temp with Windows’.
- Select ‘Logging on Startup’.
2. Go to ‘Display’.
- Select ‘Start Core Temp Minimized’

## Start the Python script silently
1. Setup a task in Windows' Task Scheduler (find it by searching in the start menu)
2. Set the task to "Start a program"
3. Set the program to pythonw.exe (so it doesn't create a command prompt window)
4. I found mine at: C:\Users\<NAME>\AppData\Local\Programs\Python\Python313\pythonw.exe
5. Add the path to pcStats.py as an argument (enclose in quotes if it has any spaces).
6. Set the task to run at log on of any user and on workstation unlock. 
7. Finally, in the Settings tab of the task, select to Stop the existing instance if the task is already running.
   
Reference: https://github.com/leots/Arduino-PC-Monitor 

## Some Observations: 
- Task Manager requires about 40 - 74.1 MB of memory, and 0 - 0.8% of CPU 
Running the Analog Meter: 
- Python Script: 10 - 11.1MB
- CPU Core: 4.2 MB 
- Open Hardware Monitor: 13 - 14.7MB 
- Total: around 30 MB of memory :D 
