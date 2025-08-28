import os
import PyInstaller.__main__


if __name__ == "__main__":
    sep = ";" if os.name == "nt" else ":"
    PyInstaller.__main__.run([
        "app.py",
        "--name=sol_klik",
        "--onefile",
        f"--add-data=app.py{sep}.",
        "--hidden-import=streamlit.web.cli",
        "--hidden-import=streamlit.cli",
        "--copy-metadata=streamlit",
    ])
