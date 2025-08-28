import threading
import time

import streamlit as st
from pynput import keyboard
from pynput.mouse import Button, Controller

# Global state
left_trigger_key = "a"  # Default left-click trigger key
right_trigger_key = "b"  # Default right-click trigger key
stop_key = "q"  # Default key to stop the app
left_clicking = False
right_clicking = False

mouse = Controller()


def clicker() -> None:
    """Continuously click the mouse at 15 clicks/s."""
    global left_clicking, right_clicking
    while True:
        did_click = False
        if left_clicking:
            mouse.click(Button.left)
            did_click = True
        if right_clicking:
            mouse.click(Button.right)
            did_click = True
        if did_click:
            time.sleep(1 / 15)
        else:
            time.sleep(0.1)


def on_press(key: keyboard.Key) -> None:
    """Toggle clicking or stop based on the pressed key."""
    global left_clicking, right_clicking, left_trigger_key, right_trigger_key, stop_key
    try:
        if key.char:
            k = key.char.lower()
            if k == left_trigger_key:
                left_clicking = not left_clicking
            elif k == right_trigger_key:
                right_clicking = not right_clicking
            elif k == stop_key:
                left_clicking = False
                right_clicking = False
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
    global left_trigger_key, right_trigger_key, stop_key
    st.title("Otomatik Tıklama Aracı")
    st.write(
        "Sol ve sağ tıklamalar için tuşları seçip AYARLA'ya basın. Uygulama açıkken "
        "seçilen tuşlara basarak tıklamayı başlatıp durdurabilirsiniz. Durdurma tuşu "
        "tıklamaları sonlandırır."
    )

    left_key_input = st.text_input(
        "Sol tıklama tetikleyici tuş", value=left_trigger_key, max_chars=1
    )
    right_key_input = st.text_input(
        "Sağ tıklama tetikleyici tuş", value=right_trigger_key, max_chars=1
    )
    stop_key_input = st.text_input("Durdurma tuşu", value=stop_key, max_chars=1)
    if st.button("AYARLA"):
        left_trigger_key = left_key_input.lower()
        right_trigger_key = right_key_input.lower()
        stop_key = stop_key_input.lower()
        st.success(
            f"Sol '{left_trigger_key}', sağ '{right_trigger_key}', durdurma '{stop_key}' olarak ayarlandı."
        )

    if "listener" not in st.session_state:
        st.session_state.listener = start_listener()

    if "clicker_thread" not in st.session_state:
        t = threading.Thread(target=clicker, daemon=True)
        t.start()
        st.session_state.clicker_thread = t

if __name__ == "__main__":
    main()
