import threading
import time

import streamlit as st
from pynput import keyboard
from pynput.mouse import Button, Controller

# Global state
trigger_key = "a"  # Default trigger key
clicking = False

mouse = Controller()

def clicker() -> None:
    """Continuously click the left mouse button at 15 clicks/s."""
    global clicking
    while True:
        if clicking:
            mouse.click(Button.left)
            time.sleep(1 / 15)
        else:
            time.sleep(0.1)

def on_press(key: keyboard.Key) -> None:
    """Toggle clicking when the trigger key is pressed."""
    global clicking, trigger_key
    try:
        if key.char and key.char.lower() == trigger_key:
            clicking = not clicking
    except AttributeError:
        # Ignore special keys
        pass

def start_listener() -> keyboard.Listener:
    """Start a background keyboard listener."""
    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()
    return listener

def main() -> None:
    global trigger_key
    st.title("Otomatik Tıklama Aracı")
    st.write(
        "Bir tuş seçin, AYARLA'ya basın. Başka bir uygulamaya geçip bu tuşa basarak "
        "tıklamayı başlatıp durdurabilirsiniz."
    )

    key_input = st.text_input("Tetikleyici tuş", value=trigger_key, max_chars=1)
    if st.button("AYARLA"):
        trigger_key = key_input.lower()
        st.success(f"Tetikleyici tuş '{trigger_key}' olarak ayarlandı.")

    if "listener" not in st.session_state:
        st.session_state.listener = start_listener()

    if "clicker_thread" not in st.session_state:
        t = threading.Thread(target=clicker, daemon=True)
        t.start()
        st.session_state.clicker_thread = t

if __name__ == "__main__":
    main()
