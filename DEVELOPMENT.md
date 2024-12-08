First you need to setup a venv with python (Python 3.12 is recommended)


### Steps to Install Dev Venv

1. **Virtual Environment creation and activation:**
   It’s a common practice to use a virtual environment to isolate your project dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   .\venv\Scripts\activate   # On Windows
   ```

2. **Ensure `pip` is Installed:**
   Verify that `pip` is installed and up to date:
   ```bash
   python -m pip install --upgrade pip
   ```

3. **Use `pip install` with `-r`:**
   Run the following command, replacing `requirements.txt` with the path to your requirements file:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation:**
   After the installation completes, you can check if all packages are installed using:
   ```bash
   pip list
   ```
