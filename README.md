# optophone

1. Set Up the Button on the Raspberry Pi
Connect a push button to one of the GPIO pins on your Raspberry Pi. For example, connect one side of the button to GPIO 17 and the other side to GND.

2. Install Required Libraries
Ensure you have the necessary Python libraries installed:

sudo apt-get update
sudo apt-get install python3-picamera python3-pil tesseract-ocr
pip3 install pytesseract mido pygame RPi.GPIO


4. Running the Script
Save the script on your Raspberry Pi.
Run the script using Python 3:

python3 your_script_name.py

Press the button connected to GPIO 17 to capture an image, process the text, convert it to MIDI, and display the letters as the notes play.

Key Features:
Button-Triggered Workflow: The entire process begins with a button press.
Automated Image Processing: Captures an image, extracts text, converts it to MIDI, and displays the corresponding characters.
Real-Time Display: Displays each letter as its MIDI notes are played.
