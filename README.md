# 🍅 PomodoroAPP

A simple, customizable Pomodoro timer built with Python and tkinter. Features motivational quotes, session statistics and a clean, minimal interface. Based on the time management method: [Pomodoro Technique](https://en.wikipedia.org/wiki/Pomodoro_Technique).

#### Features

- **Customizable Timer Durations**: Set work periods, short breaks and long breaks
- **Automatic Break Scheduling**: Long breaks after a set number of work sessions
- **Session Statistics**: Weekly view of completed Pomodoro sessions
- **Motivational Quotes**: Fetches inspiring quotes from [ZenQuotes API](https://zenquotes.io/)
- **Auto-start Option**: Automatically start the next session
- **Always on Top**: Pin the timer window above other apps
- **Data Persistence**: The settings and session history are saved automatically

#### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/30-A/PomodoroAPP.git
   cd PomodoroAPP
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

#### How to Use

1. **Start a work session**: Click "Start Work" to begin a work session
2. **Take breaks**: Click "Start Break" for short or long breaks
3. **Customize settings**: Click "Settings" to adjust durations and preferences
4. **View progress**: Click "Show Stats" to see the weekly Pomodoro count
5. **Get motivated**: Click the quote area to fetch a new inspirational quote
6. **Reset stats or timer**: Use "Reset Timer" to restart current session or "Reset Stats" to clear all history

#### Default Settings

- Work Duration: 25 minutes
- Short Break: 5 minutes
- Long Break: 15 minutes
- Sessions per Long Break: 4

#### Files Overview

- [`app.py`](app.py) - Main application with timer logic and UI
- [`config.py`](config.py) - All settings, colors, fonts and text strings
- [`quotes.py`](quotes.py) - Quote fetching from ZenQuotes API
- [`data.json`](data.json) - User settings and session history storage

---

Made by Mohamed Amine Aouini
