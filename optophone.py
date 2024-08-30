import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
from PIL import Image
import pytesseract
import mido
import pygame as pg
import time

# Set up GPIO for the button
button_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Path to Tesseract-OCR executable (modify this for your system if necessary)
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Function to capture image from Raspberry Pi camera
def capture_image_from_camera():
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    sleep(2)  # Camera warm-up time
    image_path = 'captured_image.jpg'
    camera.capture(image_path)
    camera.stop_preview()
    return image_path

# Function to convert image to text
def image_to_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

# Define a mapping of letters to sequences of MIDI notes
note_map = {
    'a': [60, 64, 67],
    'b': [62, 65, 69],
    # Add more mappings as needed
}

# Function to convert text to MIDI notes and display each letter
def text_to_midi_and_display(text, output_midi_file):
    pg.init()
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("MIDI Text Display")
    
    font = pg.font.SysFont('Arial', 200)
    
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(120)))

    for char in text:
        if char in note_map:
            screen.fill((0, 0, 0))
            text_surface = font.render(char, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(400, 300))
            screen.blit(text_surface, text_rect)
            pg.display.flip()
            
            midi_notes = note_map[char]
            for note in midi_notes:
                track.append(mido.Message('note_on', note=note, velocity=64, time=240))
                track.append(mido.Message('note_off', note=note, velocity=64, time=240))
                pg.mixer.music.load(mido.MidiFile(output_midi_file))
                pg.mixer.music.play()
                while pg.mixer.music.get_busy():
                    pg.time.Clock().tick(10)

            time.sleep(0.5)

    mid.save(output_midi_file)
    pg.quit()

# Function to play the MIDI file
def play_midi(midi_file):
    pg.mixer.music.load(midi_file)
    pg.mixer.music.play()

    while pg.mixer.music.get_busy():
        pg.time.Clock().tick(10)

    pg.quit()

# Main function
def main():
    while True:
        # Wait for button press
        input_state = GPIO.input(button_pin)
        if input_state == False:
            print("Button Pressed. Capturing Image...")
            
            # Step 1: Capture image from Raspberry Pi camera
            image_path = capture_image_from_camera()
            
            # Step 2: Convert image to text
            text = image_to_text(image_path)
            print(f"Extracted Text: {text}")

            # Step 3: Convert text to MIDI and display characters
            output_midi_file = 'output.mid'
            text_to_midi_and_display(text, output_midi_file)

            # Step 4: Play the generated MIDI
            play_midi(output_midi_file)
            
            # Debounce delay to avoid multiple triggers
            sleep(0.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
