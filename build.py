import PyInstaller.__main__

if __name__ == "__main__":
    PyInstaller.__main__.run([
        "app.py",
        "--name=sol_klik",
        "--onefile",
        "--copy-metadata=streamlit",
    ])
