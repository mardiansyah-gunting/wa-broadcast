# WhatsApp Broadcast Tool

A Python automation tool to send messages to multiple contacts via the web client. Uses Selenium and a browser; one-time QR scan for authentication.

## Stack

- **Language:** Python 3.7+
- **Automation:** Selenium
- **Driver:** `webdriver-manager` (ChromeDriver)
- **Target:** Web client (configure via environment)

## Requirements

- Python 3.7+
- Google Chrome
- Stable internet connection

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo>
   cd wa-broadcast
   ```

2. **(Optional) Virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**
   - Copy `.env.example` to `.env`.
   - Set the required variable in `.env` (see that file). Do not commit `.env` or any tokens/keys.

## Configuration

1. **Contact list**  
   Use `nomor_kontak.txt`. One number per line. Formats supported:
   - `08123456789` (converted to international)
   - `+628123456789`
   - `628123456789`

2. **Message**  
   Put the broadcast text in `pesan.txt`. The script reads this file.

## Project layout

- `main.py` — Entry point and automation script
- `requirements.txt` — Python dependencies
- `nomor_kontak.txt` — Contact numbers (create locally, gitignored)
- `pesan.txt` — Message body (create locally, gitignored)
- `README.md` — This file

## Usage

1. **Run**
   ```bash
   python main.py
   ```

2. **Auth**  
   When the browser opens, complete the one-time QR step in the client.

3. **Start**  
   When the chat list is visible, go back to the terminal and press Enter to begin sending.

4. **Sending**  
   The script opens each contact and sends the message with a delay between sends to reduce risk of restrictions.

## Important (anti-ban)

- Do not send too many messages too quickly. The script uses a delay between messages.
- Sending spam or unsolicited messages can get an account restricted. Use only for your own contacts and lawful purposes.
- You must complete the QR step and press Enter in the terminal before broadcasting starts.

## Security

- Never commit `.env`, tokens, API keys, or credentials.
- Keep `nomor_kontak.txt` and `pesan.txt` local; they are gitignored.
- All sensitive configuration (e.g. base URL) is read from environment variables.

## License

This project is for educational use. Choose and add a license (e.g. MIT, GPL) as needed.

---

*This project is not affiliated with WhatsApp Inc.*
