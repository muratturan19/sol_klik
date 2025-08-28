import threading
import time
import os

import streamlit as st
from pynput import keyboard
from pynput.mouse import Button, Controller

# Global state
left_combo_text = "a"  # Default left-click trigger
right_combo_text = "b"  # Default right-click trigger
stop_combo_text = "q"  # Default stop trigger
pause_combo_text = "p"  # Default pause trigger

left_combo = {"a"}
right_combo = {"b"}
stop_combo = {"q"}
pause_combo = {"p"}

left_clicking = False
right_clicking = False
paused = False

pressed_keys: set[str] = set()
combo_active = {"left": False, "right": False, "stop": False, "pause": False}

mouse = Controller()


def parse_key_combo(text: str) -> set[str]:
    """Parse a user supplied key combination string."""
    return {p.strip().lower() for p in text.split("+") if p.strip()}


def normalize_key(key: keyboard.Key) -> str:
    """Normalize key objects to comparable strings."""
    try:
        if key.char:
            return key.char.lower()
    except AttributeError:
        pass
    name = str(key).split(".")[-1].lower()
    return name.replace("_l", "").replace("_r", "")


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
    """Handle key press events for configured combinations."""
    global left_clicking, right_clicking, paused
    k = normalize_key(key)
    if not k:
        return
    pressed_keys.add(k)

    if (
        not paused
        and left_combo <= pressed_keys
        and not combo_active["left"]
    ):
        left_clicking = not left_clicking
        combo_active["left"] = True
    if (
        not paused
        and right_combo <= pressed_keys
        and not combo_active["right"]
    ):
        right_clicking = not right_clicking
        combo_active["right"] = True
    if stop_combo <= pressed_keys and not combo_active["stop"]:
        combo_active["stop"] = True
        os._exit(0)
    if pause_combo <= pressed_keys and not combo_active["pause"]:
        paused = not paused
        left_clicking = False
        right_clicking = False
        combo_active["pause"] = True


def on_release(key: keyboard.Key) -> None:
    """Track released keys to reset combination state."""
    k = normalize_key(key)
    if not k:
        return
    pressed_keys.discard(k)
    if k in left_combo:
        combo_active["left"] = False
    if k in right_combo:
        combo_active["right"] = False
    if k in stop_combo:
        combo_active["stop"] = False
    if k in pause_combo:
        combo_active["pause"] = False

def start_listener() -> keyboard.Listener:
    """Start a background keyboard listener."""
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.daemon = True
    listener.start()
    return listener


def main() -> None:
    global left_combo_text, right_combo_text, stop_combo_text, pause_combo_text
    global left_combo, right_combo, stop_combo, pause_combo

    st.title("Otomatik Tıklama Aracı")
    st.write(
        "Sol ve sağ tıklamalar için tuşları seçip AYARLA'ya basın. Uygulama açıkken "
        "seçilen tuşlara basarak tıklamayı başlatıp durdurabilirsiniz. Durdurma tuşu "
        "tıklamaları sonlandırır. Duraklatma tuşu tetikleyicileri geçici olarak etkisiz kılar."
    )

    left_key_input = st.text_input(
        "Sol tıklama tetikleyici tuş (ör. a veya ctrl+a)", value=left_combo_text
    )
    right_key_input = st.text_input(
        "Sağ tıklama tetikleyici tuş (ör. b veya ctrl+b)", value=right_combo_text
    )
    stop_key_input = st.text_input(
        "Durdurma tuşu (ör. q veya ctrl+q)", value=stop_combo_text
    )
    pause_key_input = st.text_input(
        "Duraklatma tuşu (ör. p veya ctrl+p)", value=pause_combo_text
    )
    if st.button("AYARLA"):
        left_combo_text = left_key_input.lower()
        right_combo_text = right_key_input.lower()
        stop_combo_text = stop_key_input.lower()
        pause_combo_text = pause_key_input.lower()

        left_combo = parse_key_combo(left_combo_text)
        right_combo = parse_key_combo(right_combo_text)
        stop_combo = parse_key_combo(stop_combo_text)
        pause_combo = parse_key_combo(pause_combo_text)

        st.success(
            "Ayarlar güncellendi: "
            f"sol '{left_combo_text}', sağ '{right_combo_text}', durdurma '{stop_combo_text}', "
            f"duraklatma '{pause_combo_text}'."
        )

    if "listener" not in st.session_state:
        st.session_state.listener = start_listener()

    if "clicker_thread" not in st.session_state:
        t = threading.Thread(target=clicker, daemon=True)
        t.start()
        st.session_state.clicker_thread = t
    
if __name__ == "__main__":
    import sys
    import streamlit as st
    from streamlit.web import cli as stcli

    if getattr(st, "_is_running_with_streamlit", False):
        main()
    else:
        sys.argv = ["streamlit", "run", __file__]
        sys.exit(stcli.main())
