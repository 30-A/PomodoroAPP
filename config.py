"""
Configurations.

This file acts as a central control panel for the App. Modifying values here will
change the app's look without needing to modify the core logic in 'app.py'.
"""

import os

# =============
# 1. FILE PATHS
# =============
# The file where user settings and session history are stored
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

# =================
# 2. TIMER DEFAULTS
# =================
# These settings are used when the app is run for the first time
TIMER_DEFAULTS = {
    "work_duration": 25,
    "short_break": 5,
    "long_break": 15,
    "sessions_per_long_break": 4,
    "auto_start": False,
}

# ====================
# 3. WINDOW DIMENSIONS
# ====================
MAIN_WINDOW_SIZE = "260x325"
SETTINGS_WINDOW_SIZE = "270x210"
STATS_WINDOW_SIZE = "320x280"

# ========
# 4. FONTS
# ========
FONT_MAIN_TIMER = ("Menlo", 50, "bold")
FONT_STATUS_LABEL = ("Ubuntu", 10, "normal")
FONT_BUTTON = ("Ubuntu", 11, "normal")
FONT_QUOTE = ("Ubuntu", 11, "italic")
FONT_FOOTER = ("Menlo", 10, "normal")
FONT_SETTINGS_TITLE = ("Ubuntu", 11, "bold")
FONT_SETTINGS_LABEL = ("Ubuntu", 11, "normal")
FONT_SETTINGS_ENTRY = ("Ubuntu", 11, "normal")
FONT_STATS_TITLE = ("Ubuntu", 14, "bold")
FONT_STATS_DAY_LABEL = ("Ubuntu", 12, "normal")
FONT_STATS_COUNT = ("Ubuntu", 12, "bold")
FONT_STATS_TOTAL = ("Ubuntu", 14, "bold")
FONT_STATS_NAV_BUTTON = ("Ubuntu", 12, "normal")

# ================
# 5. COLOR PALETTE
# ================
COLOR_TEXT_PRIMARY = "black"
COLOR_TEXT_SECONDARY = "#888888"
COLOR_STATS_WINDOW_BG = "#2d2d2d"
COLOR_STATS_TEXT = "white"
COLOR_STATS_ROW_BG = "#444444"
COLOR_STATS_TOTAL_BANNER_BG = "#1fa31f"
COLOR_STATS_NAV_BUTTON_BG = "white"
COLOR_STATS_NAV_BUTTON_FG = "black"

# ======================
# 6. UI STRINGS AND TEXT
# ======================
# All UI texts for easy modification
STRINGS = {
    'title_main': "Pomodoro Timer",
    'title_settings': "Settings",
    'title_stats': "Pomodoro Statistics",
    'status_ready': "Ready To Work.",
    'status_working': "Working...",
    'status_break': "Break...",
    'status_work_paused': "Work Paused",
    'status_break_paused': "Break Paused",
    'btn_start_work': "Start Work",
    'btn_pause_work': "Pause Work",
    'btn_start_break': "Start Break",
    'btn_pause_break': "Pause Break",
    'btn_settings': "Settings",
    'btn_stats': "Show Stats",
    'btn_reset_timer': "Reset Timer",
    'btn_reset_stats': "Reset Stats",
    'btn_pin': "PIN",
    'btn_unpin': "UNPIN",
    'btn_prev_week': "← Previous Week",
    'btn_next_week': "Next Week →",
    'settings_title': "Timer Durations",
    'settings_work_label': "Work Duration",
    'settings_short_break_label': "Short Break",
    'settings_long_break_label': "Long Break",
    'settings_sessions_label': "Sessions per Long Break",
    'settings_minutes_unit': "Minutes",
    'settings_sessions_unit': "Sessions",
    'settings_auto_start_format': "Auto Start: {}",
    'stats_date_range_format': "{start_date} - {end_date}",
    'stats_weekly_total_format': "Weekly Total: {} Pomodoros",
    'stats_weekdays': ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    'stats_session_icon': "🍅",
    'msg_work_complete': "Work session complete! Time for a break.",
    'msg_break_complete': "Break over! Back to work.",
    'msg_reset_confirm': "Are you sure you want to delete all your session data?",
    'title_work_complete': "Pomodoro",
    'title_break_complete': "Pomodoro",
    'title_reset_confirm': "Reset Stats",
    'title_file_error': "Data File Issue",
    'msg_file_created': f"Could not find '{os.path.basename(DATA_FILE)}'. A new one has been created.",
    'msg_file_corrupt': f"'{os.path.basename(DATA_FILE)}' was corrupted and has been reset.",
    'footer_text': "🍅 Pomodoro App\nMade by Mohamed Amine Aouini",
    'fallback_quote': "Stay focused and productive.",
}

# ================
# 7. WIDGET SIZING
# ================
QUOTE_WRAP_LENGTH = 230
SETTINGS_ENTRY_WIDTH = 5
SETTINGS_BUTTON_WIDTH = 10
MAIN_BUTTON_WIDTH = 10
STATS_NAV_BUTTON_WIDTH = 13
STATS_DAY_LABEL_WIDTH = 12
STATS_COUNT_LABEL_WIDTH = 3

# =========================
# 8. UI PADDING AND SPACING
# =========================
# Main Window
MAIN_FRAME_PADDING = {'pady': (10, 10)}
MAIN_STATUS_PADDING = {'pady': (0, 0)}
MAIN_BUTTON_FRAME_PADDING = {'pady': (0, 0)}
MAIN_BUTTON_PADDING = {'padx': 0, 'pady': 0}
MAIN_QUOTE_PADDING = {'padx': 0, 'pady': (15, 15)}
MAIN_FOOTER_PADDING = {'side': 'bottom', 'pady': 10}

# Settings Window
SETTINGS_MAIN_FRAME_PADDING = {'pady': 10, 'padx': 10}
SETTINGS_DURATIONS_FRAME_PADDING = {'pady': 0}
SETTINGS_DURATIONS_GRID_PADDING = {'padx': 0, 'pady': 0}
SETTINGS_CONTROLS_FRAME_PADDING = {'pady': 6}
SETTINGS_ACTIONS_FRAME_PADDING = {'pady': 0}
SETTINGS_BUTTON_INTERNAL_PADDING = {'padx': 0}

# Stats Window
STATS_NAV_FRAME_PADDING = {'pady': (0, 0), 'padx': 0}
STATS_NAV_BUTTON_PADDING = {'pady': (0, 0), 'padx': 0}
STATS_TITLE_PADDING = {'pady': (0, 0), 'padx': 0}
STATS_DAYS_FRAME_PADDING = {'pady': (0, 8), 'padx': 8}
STATS_DAY_ROW_PADDING = {'pady': (2, 2), 'padx': 2}
STATS_TOTAL_FRAME_PADDING = {'pady': (0, 0), 'padx': 0}
STATS_TOTAL_BANNER_PADDING = {'pady': (0, 8), 'padx': 8}
STATS_ROW_INTERNAL_PADDING_X = 10