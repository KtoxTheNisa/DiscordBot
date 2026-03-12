# 🤖 Discord Bot & Web Dashboard PRO

> **Advanced Programming Course – Term Project**

This project is a comprehensive Discord bot that supports **multiple servers** and includes a **web-based management dashboard**.  
It is built using modern **asynchronous programming techniques** to ensure high performance, scalability, and responsiveness.

---

# 🚀 Tech Stack

The project is developed using **industry-standard technologies** and a **100% asynchronous architecture**.

## Backend & Bot
- **Python 3.10+** – Main programming language used for development.
- **Quart Framework** – An asynchronous version of Flask used for the web dashboard. This ensures the website remains responsive while the bot processes Discord events.
- **Discord.py (2.0+)** – A modern library used to communicate with the Discord API.
- **AsyncIO** – Used for concurrent task management.

## Database
- **SQLite3** – Used for data storage.
- **aiosqlite** – Asynchronous SQLite driver that prevents database queries from blocking the bot.

## Frontend (Dashboard)
- **HTML5 & CSS3** – Used to build a modern and responsive interface.
- **Glassmorphism UI** – A modern UI design style with blurred backgrounds and transparent components.
- **Jinja2** – Template engine for dynamic HTML rendering.

---

# 🔥 Features

## 1. Web Management Dashboard
- **Discord Login (OAuth2)**
- **Server-specific configuration** (command prefix, log channel, etc.)
- **Live leaderboards** for XP, messages, and voice activity
- Modern **Glassmorphism interface design**

## 2. Advanced Global Economy System
- `!buy_coin`, `!sell_coin` – Dynamic virtual trading system
- `!daily` – Daily reward system
- `!steal` – Risk-based stealing mechanic
- `!market` – Marketplace for buying badges and items

## 3. Level & Statistics System
- Users gain **XP from messages and voice activity**
- Advanced **profile card** (`!profile`)
- **Weekly and global rankings** (`!stat`, `!top_voice`)

## 4. Fun & Social Systems
- **Marriage system** (`!marry`, `!divorce`)
- **Reputation points** (`!rep`)
- Mini games such as **Word Game, Duel, and Coin Flip**

---

# 🛠️ Installation

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Environment Variables (.env)

Create a `.env` file in the root directory of the project:

```env
TOKEN=DISCORD_BOT_TOKEN
OWNER_ID=YOUR_ID
CLIENT_SECRET=OAUTH2_SECRET
CLIENT_ID=BOT_ID
REDIRECT_URI=http://localhost:5000/callback
SECRET_KEY=random_security_key
```

## 3. Run the Project

```bash
python main.py
```

This command starts **both the Discord bot and the web dashboard asynchronously in the same event loop**.

---

# 📂 Project Structure

```
discord-bot/
│
├── main.py              # Entry point (Bot + Web Server integration)
├── database.py          # Asynchronous Database Layer
│
├── cogs/                # Modular Bot Components
│   ├── ekonomi.py       # Economy Commands
│   ├── oyun.py          # Game Mechanics
│   ├── sosyal.py        # Social Interactions
│   ├── stats.py         # Statistics & Level System
│   └── yonetim.py       # Moderation Tools
│
├── dashboard/           # Web Application (Quart)
│   ├── app.py           # Web Server Logic
│   ├── templates/       # HTML Templates
│   └── static/          # CSS & Assets
│
└── requirements.txt     # Project Dependencies
```

---
