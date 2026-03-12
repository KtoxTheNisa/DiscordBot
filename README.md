# 🤖 Discord Bot & Web Dashboard PRO

> **Advanced Programming Course Term Project**
>
> This project is a comprehensive Discord bot with multi-server support and a web dashboard, developed using modern asynchronous programming techniques.

## 🚀 Tech Stack

The project is built with industry-standard technologies and a **100% Asynchronous** architecture.

### Backend & Bot
* **Python 3.10+**: Core development language.
* **Quart Framework**: An **Asynchronous (Async)** version of Flask used for the web dashboard. This ensures the bot stays responsive while the website handles high concurrency.
* **Discord.py (2.0+)**: Modern library for interacting with the Discord API.
* **AsyncIO**: For concurrent process management.

### Database
* **SQLite3**: Data storage.
* **Aiosqlite**: Asynchronous driver used to prevent database queries from blocking the bot (non-blocking).

### Frontend (Dashboard)
* **HTML5 & CSS3**: Modern, responsive design.
* **Glassmorphism UI**: A premium interface design with modern effects (backdrop-filter).
* **Jinja2**: HTML Template Engine.

---

## 🔥 Key Features

### 1. Economy System
* **Global Economy**: Coin earning through daily rewards and chatting.
* **Stock Market**: A system where stock prices change every 5 minutes with randomized algorithms.
* **Marketplace**: Users can buy/sell items and manage their inventory.

### 2. Management & Moderation
* **Advanced Log System**: All actions (deleted messages, joining/leaving) are logged to specific channels.
* **Authority Control**: Server-specific settings (auto-role, welcome messages).

### 3. Statistics & Leveling
* **Voice/Chat Levels**: Earn XP and level up based on activity.
* **Profile Cards**: Advanced dynamic profile cards (`!profile`).
* **Leaderboards**: Weekly and overall rankings for voice and text activity (`!stat`, `!top_voice`).

### 4. Entertainment & Social
* **Marriage System**: Roleplay marriage features (`!marry`, `!divorce`).
* **Reputation**: Rep points system (`!rep`).
* **Games**: Word games, duels, coinflip, and more.

---

## 🛠️ Setup

### 1. Requirements
```bash
pip install -r requirements.txt
2. Environment Variables (.env)
Create a .env file in the root directory:

Kod snippet'i
TOKEN=YOUR_DISCORD_BOT_TOKEN
OWNER_ID=YOUR_USER_ID
CLIENT_SECRET=OAUTH2_SECRET
CLIENT_ID=BOT_ID
REDIRECT_URI=http://localhost:5000/callback
SECRET_KEY=random_security_key
3. Launch
Bash
python main.py
This command starts both the Bot and the Web Server asynchronously within a single Event Loop.

📂 Project Structure
discord-bot/
├── main.py              # Entry Point (Bot + Web Server integration)
├── database.py          # Asynchronous Data Access Layer (DAL)
├── cogs/                # Modular Command Categories (Economy, Stats, etc.)
├── dashboard/           # Quart Web Server & Frontend Files
├── logs/                # System and Error Logs
└── tests/               # Unit and Integration Tests
