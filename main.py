import mido
import ctypes

PREV_NOTE = 13
PLAY_PAUSE_NOTE = 14
NEXT_NOTE = 15
VOL_CC = 8

def main():
    # List all available MIDI input ports
    print("Available MIDI input ports:")
    for port in mido.get_input_names():
        print(port)

    # Open the first available MIDI input port
    with mido.open_input(mido.get_input_names()[0]) as inport:
        print("Listening for MIDI signals...")
        last_volume_value = None
        for msg in inport:
            print(msg)
        
            if msg.type == 'note_on':
                if msg.note == PLAY_PAUSE_NOTE:
                    # Pause the currently playing media
                    ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)  # VK_MEDIA_PLAY_PAUSE
                    ctypes.windll.user32.keybd_event(0xB3, 0, 2, 0)  # KEYEVENTF_KEYUP
                elif msg.note == PREV_NOTE:
                    # Previous track
                    ctypes.windll.user32.keybd_event(0xB1, 0, 0, 0)  # VK_MEDIA_PREV_TRACK
                    ctypes.windll.user32.keybd_event(0xB1, 0, 2, 0)  # KEYEVENTF_KEYUP
                elif msg.note == NEXT_NOTE:
                    # Next track
                    ctypes.windll.user32.keybd_event(0xB0, 0, 0, 0)  # VK_MEDIA_NEXT_TRACK
                    ctypes.windll.user32.keybd_event(0xB0, 0, 2, 0)  # KEYEVENTF_KEYUP
            elif msg.type == 'control_change' and msg.control == VOL_CC:
                if last_volume_value is not None:
                    if msg.value > last_volume_value:
                        # Volume up
                        ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)  # VK_VOLUME_UP
                        ctypes.windll.user32.keybd_event(0xAF, 0, 2, 0)  # KEYEVENTF_KEYUP
                    elif msg.value < last_volume_value:
                        # Volume down
                        ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0)  # VK_VOLUME_DOWN
                        ctypes.windll.user32.keybd_event(0xAE, 0, 2, 0)  # KEYEVENTF_KEYUP
                last_volume_value = msg.value

if __name__ == "__main__":
    main()