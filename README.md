# WhatsApp Broadcast Tool

A simple Python-based automation tool to send messages to multiple WhatsApp contacts using Selenium and WhatsApp Web.

## 📝 Overview

This script reads a list of phone numbers from a text file and sends a predefined message to each number through WhatsApp Web. It uses Selenium to automate the browser, requiring a one-time QR code scan for authentication.

## 🛠️ Stack

- **Language:** Python 3.x
- **Automation Framework:** Selenium
- **Browser Driver:** `webdriver-manager` (automatically handles ChromeDriver)
- **Target Platform:** WhatsApp Web (`web.whatsapp.com`)

## 📋 Requirements

- **Python 3.7+**
- **Google Chrome** installed on your machine.
- Stable internet connection.

## 🚀 Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd wa-broadcast
   ```

2. **(Optional) Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. **Contact List:**
   Prepare your contacts in `nomor_kontak.txt`. Each number should be on a new line.
   Supported formats:
   - `08123456789` (automatically converted to international format `628...`)
   - `+628123456789`
   - `628123456789`

2. **Message Content:**
   Currently, the message is hardcoded in `main.py` under the `pesan_asli` variable. Update this variable with your desired message.
   - **TODO:** Move the message to an external file (e.g., `pesan.txt`) or environment variable for easier configuration.

## 📂 Project Structure

- `main.py`: The entry point and main automation script.
- `requirements.txt`: Python package dependencies.
- `nomor_kontak.txt`: Input file for phone numbers.
- `PyWhatKit_DB.txt`: Internal database/log (if applicable).
- `README.md`: This file.

## ▶️ Usage

1. **Run the script:**
   ```bash
   python main.py
   ```

2. **Authentication:**
   A Chrome window will open. **Scan the QR code** using your phone's WhatsApp.

3. **Confirmation:**
   Once the WhatsApp Web chat list appears, go back to your terminal/IDE and **press Enter** to start the broadcast.

4. **Execution:**
   The script will navigate to each contact's chat and send the message with a built-in delay (approx. 6 seconds) to prevent account flagging.

## ⚠️ Important Notes (Anti-Ban)

- **Do not send too many messages too quickly.** The script has a built-in 6-second delay between messages.
- Sending spam or unsolicited messages can lead to your WhatsApp account being **banned**. Use this tool responsibly for your own contacts.
- **Manual Step:** The script requires you to manually press Enter in the terminal after scanning the QR code to ensure the session is ready.

## 📜 License

This project is for educational purposes.
- **TODO:** Specify a license (e.g., MIT, GPL).

---
*Disclaimer: This project is not affiliated with WhatsApp Inc.*
