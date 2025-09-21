"""
Pomodoro App - Main Script.

This script contains the application's core logic and UI. All visual
styles and text are imported from 'config.py'. While the 'quotes.py'
contains the API quote fetching logic.
"""
# Import necessary libraries
import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

from quotes import get_quote
import config as cfg

# ================
# UTILITY FUNCTION
# ================
def format_time(seconds):
    """Converts a total number of seconds into a MM:SS string."""
    return f"{seconds//60:02d}:{seconds%60:02d}"

# ============
# CORE CLASSES
# ============
class PomodoroTimer:
    """Manages all timing logic and state for the timer."""
    def __init__(self, settings):
        # Store the timer settings passed from the main app
        self.settings = settings
        # Set the timer to its default starting state
        self.reset()

    def reset(self):
        """Resets the timer to its initial, idle state."""
        # What the timer is doing: idle, running or paused
        self.state = 'idle'
        # The session type tracks whether we are in a work period or a break
        self.session_type = 'work'
        # Calculate the starting time in seconds from user's settings
        self.time_left = self.settings["work_duration"] * 60
        # Reset the count of completed work sessions
        self.completed_sessions = 0

    def start(self):
        """Changes the timer's state to 'running' if it is not already."""
        if self.state != 'running':
            self.state = 'running'

    def pause(self):
        """Changes the timer's state to 'paused' if it is currently running."""
        if self.state == 'running':
            self.state = 'paused'

    def set_session(self, session_type):
        """Sets up the timer for a new session type and makes it idle."""
        # When switching, always return to the 'idle' state
        self.state = 'idle'
        # Set the new session type
        self.session_type = session_type
        # Load the duration for this new session type
        self.time_left = self._get_duration_for_session()

    def tick(self):
        """Decrements the timer by one second if it is running."""
        # It exits early if there's nothing to do
        if self.state != 'running' or self.time_left <= 0:
            return None

        # Count down by one
        self.time_left -= 1

        # If the timer is still ticking skip
        if self.time_left > 0:
            return None

        # If we reach here, the timer just hit zero
        self.state = 'idle'   # The timer is now finished
        if self.session_type == 'work':
            # Increment the counter after a work session is completed
            self.completed_sessions += 1
            # Return a string indicating what just finished
            return "work_complete"
        else:
            return "break_complete"

    def get_next_break_type(self):
        """Determines if the next break should be a long break or a short break."""
        # Get the user's setting for how many work sessions are required
        sessions_for_long_break = self.settings["sessions_per_long_break"]

        # Rule 1: You don't get a long break if no sessions are completed
        if self.completed_sessions == 0:
            return 'short_break'

        # Rule 2: Check if the number of completed sessions is an exact multiple of `sessions_for_long_break`
        if self.completed_sessions % sessions_for_long_break == 0:
            # If it's an exact multiple, it's time for a long break
            return 'long_break'
        else:
            # Otherwise, it's a short break
            return 'short_break'

    def _get_duration_for_session(self):
        """Returns the duration in seconds for the current session type."""
        # This dictionary translates the simple session type names into the keys
        # used in the settings file, making the code cleaner
        key_map = {'work': 'work_duration',
                   'short_break': 'short_break',
                   'long_break': 'long_break'}
        
        duration_key = key_map[self.session_type]
        # Get the duration in minutes from settings and convert it to seconds
        return self.settings[duration_key] * 60


class SettingsWindow(tk.Toplevel):
    """The popup window for configuring application settings."""
    def __init__(self, parent, main_app):
        # Initialize this window as a Toplevel window (a popup)
        super().__init__(parent)
        self.title(cfg.STRINGS['title_settings'])  # Window title from our config file
        self.geometry(cfg.SETTINGS_WINDOW_SIZE)    # Window size from config file
        self.main_app = main_app   # Store a reference to the main application to call its methods
        self.app_data = main_app.app_data  # Get a direct reference to the app's data for easy access
        self._create_interface()  # Build the UI for this window.

    def _create_interface(self):
        """Builds all the visual elements (widgets) for the settings window."""
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, **cfg.SETTINGS_MAIN_FRAME_PADDING)

        durations_frame = tk.LabelFrame(frame, text=cfg.STRINGS['settings_title'], font=cfg.FONT_SETTINGS_TITLE)
        durations_frame.pack(fill=tk.X, **cfg.SETTINGS_DURATIONS_FRAME_PADDING)

        # This list defines the UI for each setting
        settings_config = [
            {'label': cfg.STRINGS['settings_work_label'],'key': "work_duration", 'unit': cfg.STRINGS['settings_minutes_unit']},
            {'label': cfg.STRINGS['settings_short_break_label'], 'key': "short_break", 'unit': cfg.STRINGS['settings_minutes_unit']},
            {'label': cfg.STRINGS['settings_long_break_label'], 'key': "long_break", 'unit': cfg.STRINGS['settings_minutes_unit']},
            {'label': cfg.STRINGS['settings_sessions_label'], 'key': "sessions_per_long_break", 'unit': cfg.STRINGS['settings_sessions_unit']}
        ]
        self.setting_vars = {}
        # Loop through our configuration list to build the UI grid
        for i, config in enumerate(settings_config):
            # Create the text label
            tk.Label(durations_frame, text=config['label'], font=cfg.FONT_SETTINGS_LABEL).grid(row=i, column=0, sticky="w", **cfg.SETTINGS_DURATIONS_GRID_PADDING)
            var = tk.StringVar(value=str(self.app_data["settings"][config['key']]))
            # Create the entry box where the user types a number
            entry = tk.Entry(durations_frame, width=cfg.SETTINGS_ENTRY_WIDTH, textvariable=var, font=cfg.FONT_SETTINGS_ENTRY, justify="center")
            entry.grid(row=i, column=1, **cfg.SETTINGS_DURATIONS_GRID_PADDING)
            # The bind method tells the entry box to call our function whenever the user types
            entry.bind("<KeyRelease>", self._on_settings_change)
            self.setting_vars[config['key']] = var
            tk.Label(durations_frame, text=config['unit'], font=cfg.FONT_SETTINGS_LABEL, fg=cfg.COLOR_TEXT_SECONDARY).grid(row=i, column=2, sticky="w", **cfg.SETTINGS_DURATIONS_GRID_PADDING)

        # This section creates the control buttons like PIN and Auto-Start
        controls_frame = tk.Frame(frame)
        controls_frame.pack(fill=tk.X, **cfg.SETTINGS_CONTROLS_FRAME_PADDING)
        pin_text = cfg.STRINGS['btn_unpin'] if self.main_app.window_pinned else cfg.STRINGS['btn_pin']
        self.pin_button = tk.Button(controls_frame, text=pin_text, command=self._toggle_pin, width=cfg.SETTINGS_BUTTON_WIDTH, font=cfg.FONT_BUTTON)
        self.pin_button.pack(side=tk.LEFT, **cfg.SETTINGS_BUTTON_INTERNAL_PADDING)
        auto_text = cfg.STRINGS['settings_auto_start_format'].format("ON" if self.app_data['settings']['auto_start'] else "OFF")
        self.auto_button = tk.Button(controls_frame, text=auto_text, command=self._toggle_auto_start, width=cfg.SETTINGS_BUTTON_WIDTH, font=cfg.FONT_BUTTON)
        self.auto_button.pack(side=tk.RIGHT, **cfg.SETTINGS_BUTTON_INTERNAL_PADDING)

        # This section creates the action buttons like Reset Timer and Reset Stats
        actions_frame = tk.Frame(frame)
        actions_frame.pack(fill=tk.X, **cfg.SETTINGS_ACTIONS_FRAME_PADDING)
        tk.Button(actions_frame, text=cfg.STRINGS['btn_reset_timer'], command=self.main_app.reset_timer, width=cfg.SETTINGS_BUTTON_WIDTH, font=cfg.FONT_BUTTON).pack(side=tk.LEFT, **cfg.SETTINGS_BUTTON_INTERNAL_PADDING)
        tk.Button(actions_frame, text=cfg.STRINGS['btn_reset_stats'], command=self.main_app.reset_stats, width=cfg.SETTINGS_BUTTON_WIDTH, font=cfg.FONT_BUTTON).pack(side=tk.RIGHT, **cfg.SETTINGS_BUTTON_INTERNAL_PADDING)

    def _toggle_pin(self):
        """Toggles the main window's 'always on top' state."""
        # Flip the boolean value (True becomes False, and vice-versa)
        self.main_app.window_pinned = not self.main_app.window_pinned
        # Apply the setting to the main window (the 'master' of this popup)
        self.master.attributes("-topmost", self.main_app.window_pinned)
        # Update the button's text to reflect the new state
        self.pin_button.config(text=cfg.STRINGS['btn_unpin'] if self.main_app.window_pinned else cfg.STRINGS['btn_pin'])

    def _toggle_auto_start(self):
        """Toggles the auto-start setting."""
        # Get the current state of the auto_start setting
        is_on = self.app_data["settings"]["auto_start"]
        # Set the setting to the opposite of its current state
        self.app_data["settings"]["auto_start"] = not is_on
        # Save the change to the data.json file
        self.main_app._save_data()
        # Update the button's text to show the new state
        self.auto_button.config(text=cfg.STRINGS['settings_auto_start_format'].format("ON" if not is_on else "OFF"))

    def _on_settings_change(self, event=None):
        """Validates and saves settings as the user types."""
        for key, var in self.setting_vars.items():
            try:
                # Step 1: Attempt to convert the input text to a number.
                # Automatically fail and jump to 'except' if the text is not a number
                value = int(var.get())

                # Step 2: Check if the number is a valid number (must be positive)
                if value <= 0:
                    # If not positive, we treat it as an error. We can force a jump to the 'except'
                    raise ValueError()

                # If both checks pass, we update the app's data with the new number
                self.app_data["settings"][key] = value

            except ValueError:
                # We revert the entry box to its last known good value if no valid input
                var.set(str(self.app_data["settings"][key]))
        
        # After checking all fields, save any changes that were made
        self.main_app._save_data()


class StatsWindow(tk.Toplevel):
    """The popup window for displaying session statistics."""
    def __init__(self, parent, sessions):
        super().__init__(parent)
        self.title(cfg.STRINGS['title_stats'])
        self.geometry(cfg.STATS_WINDOW_SIZE)
        self.configure(bg=cfg.COLOR_STATS_WINDOW_BG)
        self.resizable(False, False)
        self.sessions = sessions
        self.week_offset = 0
        self._create_interface()
        self._update_display()

    def _create_interface(self):
        """Builds the widgets for the stats window."""
        # Create a frame for the navigation buttons and title
        nav_frame = tk.Frame(self, bg=cfg.COLOR_STATS_WINDOW_BG)
        nav_frame.pack(**cfg.STATS_NAV_FRAME_PADDING)
        tk.Button(nav_frame, text=cfg.STRINGS['btn_prev_week'], command=lambda: self._change_week(-1), font=cfg.FONT_STATS_NAV_BUTTON, width=cfg.STATS_NAV_BUTTON_WIDTH, bg=cfg.COLOR_STATS_NAV_BUTTON_BG, fg=cfg.COLOR_STATS_NAV_BUTTON_FG).grid(row=0, column=0, **cfg.STATS_NAV_BUTTON_PADDING)
        tk.Button(nav_frame, text=cfg.STRINGS['btn_next_week'], command=lambda: self._change_week(1), font=cfg.FONT_STATS_NAV_BUTTON, width=cfg.STATS_NAV_BUTTON_WIDTH, bg=cfg.COLOR_STATS_NAV_BUTTON_BG, fg=cfg.COLOR_STATS_NAV_BUTTON_FG).grid(row=0, column=1, **cfg.STATS_NAV_BUTTON_PADDING)
        self.week_label = tk.Label(nav_frame, font=cfg.FONT_STATS_TITLE, fg=cfg.COLOR_STATS_TEXT, bg=cfg.COLOR_STATS_WINDOW_BG)
        self.week_label.grid(row=1, column=0, columnspan=2, **cfg.STATS_TITLE_PADDING)

        # Create a frame to hold the rows of daily stats
        stats_frame = tk.Frame(self, bg=cfg.COLOR_STATS_WINDOW_BG)
        stats_frame.pack(fill=tk.BOTH, expand=True, **cfg.STATS_DAYS_FRAME_PADDING)
        self.count_labels = []
        for day in cfg.STRINGS['stats_weekdays']:
            row = tk.Frame(stats_frame, bg=cfg.COLOR_STATS_ROW_BG)
            row.pack(fill=tk.X, **cfg.STATS_DAY_ROW_PADDING)
            tk.Label(row, text=day, font=cfg.FONT_STATS_DAY_LABEL, fg=cfg.COLOR_STATS_TEXT, bg=cfg.COLOR_STATS_ROW_BG, anchor="w", width=cfg.STATS_DAY_LABEL_WIDTH).pack(side=tk.LEFT, padx=cfg.STATS_ROW_INTERNAL_PADDING_X)
            lbl = tk.Label(row, text="0", font=cfg.FONT_STATS_COUNT, fg=cfg.COLOR_STATS_TEXT, bg=cfg.COLOR_STATS_ROW_BG, width=cfg.STATS_COUNT_LABEL_WIDTH, anchor="e")
            lbl.pack(side=tk.LEFT, padx=cfg.STATS_ROW_INTERNAL_PADDING_X)
            self.count_labels.append(lbl)
            tk.Label(row, text=cfg.STRINGS['stats_session_icon'], font=cfg.FONT_STATS_COUNT, bg=cfg.COLOR_STATS_ROW_BG).pack(side=tk.RIGHT, padx=cfg.STATS_ROW_INTERNAL_PADDING_X)

        # Create the weekly total banner at the bottom
        total_frame = tk.Frame(self, bg=cfg.COLOR_STATS_WINDOW_BG)
        total_frame.pack(fill=tk.X, **cfg.STATS_TOTAL_FRAME_PADDING)
        self.total_label = tk.Label(total_frame, font=cfg.FONT_STATS_TOTAL, fg=cfg.COLOR_STATS_TEXT, bg=cfg.COLOR_STATS_TOTAL_BANNER_BG)
        self.total_label.pack(fill=tk.X, **cfg.STATS_TOTAL_BANNER_PADDING)

    def _change_week(self, direction):
        """Navigates the week view forward or backward."""
        self.week_offset += direction
        self._update_display()

    def _update_display(self):
        """Refreshes the stats display for the current week in three simple steps."""
        # Determine the week's date range
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=self.week_offset)
        end_of_week = start_of_week + timedelta(days=6)

        # Count the sessions that fall within this range
        counts_per_day = [0] * 7   # Create a list of 7 zeros (Monday to Sunday)
        for session in self.sessions:
            session_date = datetime.fromisoformat(session["timestamp"]).date()
            # Check if the session is inside our target week
            if start_of_week <= session_date <= end_of_week:
                day_index = session_date.weekday() # Returns 0 for Monday, 1 for Tuesday, etc
                counts_per_day[day_index] += 1     # Add 1 to the correct day's count

        # Update the UI labels with the results
        self.week_label.config(text=cfg.STRINGS['stats_date_range_format'].format(
            start_date=start_of_week.strftime('%B %d'),
            end_date=end_of_week.strftime('%B %d, %Y')
        ))

        # Update each of the 7 daily count labels on the screen
        for i, count in enumerate(counts_per_day):
            self.count_labels[i].config(text=str(count))

        # Update the total at the bottom by summing the daily counts
        total = sum(counts_per_day)
        self.total_label.config(text=cfg.STRINGS['stats_weekly_total_format'].format(total))


class MainWindow:
    """The main application class that orchestrates all components."""
    def __init__(self, root):
        self.root = root
        self.root.title(cfg.STRINGS['title_main'])
        self.root.geometry(cfg.MAIN_WINDOW_SIZE)
        self.root.resizable(False, False)

        self.app_data = self._load_data()
        self.timer = PomodoroTimer(self.app_data["settings"])

        self.window_pinned = False
        self.settings_window = None

        # Build the UI, get the first quote and start the main timer loop
        self._create_interface()
        self.refresh_quote()
        self._update_loop()

    def _load_data(self):
        """
        Loads data from the file. If the file is missing, corrupt, or invalid,
        it shows a notification and creates a new default file.
        """
        try:
            # Attempt to open and read the data file
            # This will fail if the file doesn't exist (FileNotFoundError)
            with open(cfg.DATA_FILE, 'r') as f:
                # Attempt to parse the file as JSON.
                # This will fail if the file is empty or has broken syntax (JSONDecodeError)
                data = json.load(f)

            # Check if the data has the structure we expect
            # Accessing the keys will fail if they don't exist (KeyError)
            _ = data['settings']
            _ = data['sessions']

            # If all three steps succeed, the data is valid
            return data

        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            # Catches ANY error that occurs during loading
            messagebox.showwarning(
                cfg.STRINGS['title_file_error'],
                "Could not load user data. The application will start with default settings.",
                parent=self.root
            )  # Show a single, clear message to the user

            # Create a clean, default data structure
            default_data = {"settings": cfg.TIMER_DEFAULTS.copy(), "sessions": []}
            # Save this default structure to a new data.json file
            self._save_data(default_data)
            # Return the default data for use in the app
            return default_data

    def _save_data(self, data=None):
        """Saves the current app data to file and syncs the timer."""
        # If specific data is passed, save that. Otherwise, save the app's current data.
        data_to_save = data if data is not None else self.app_data
        try:
            with open(cfg.DATA_FILE, 'w') as f:
                json.dump(data_to_save, f, indent=2)
        except IOError as e:
            messagebox.showinfo("Error", f"Could not save data file:\n{e}", parent=self.root)

        # If we saved the app's current data, make sure the timer object is updated.
        if data is None:
            self.timer.settings = self.app_data["settings"]

    def _create_interface(self):
        """Builds the main user interface."""
        # Create and place the main timer
        self.timer_display = tk.Label(self.root, font=cfg.FONT_MAIN_TIMER)
        self.timer_display.pack(**cfg.MAIN_FRAME_PADDING)

        # Create and place the status label (e.g., "Working...")
        self.status_label = tk.Label(self.root, font=cfg.FONT_STATUS_LABEL)
        self.status_label.pack(**cfg.MAIN_STATUS_PADDING)

        # Create a frame to hold the four main buttons
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(**cfg.MAIN_BUTTON_FRAME_PADDING)
        
        # This list defines the layout for the main buttons
        button_configs = [
            {'command': self.toggle_work, 'row': 0, 'col': 0, 'ref_name': 'work_button'},
            {'command': self.toggle_break, 'row': 0, 'col': 1, 'ref_name': 'break_button'},
            {'text': cfg.STRINGS['btn_stats'], 'command': self.show_stats, 'row': 1, 'col': 0},
            {'text': cfg.STRINGS['btn_settings'], 'command': self.show_settings, 'row': 1, 'col': 1}
        ]
        # Loop through the configuration to create each button
        for config in button_configs:
            btn = tk.Button(buttons_frame, text=config.get('text', ''), command=config['command'], width=cfg.MAIN_BUTTON_WIDTH, font=cfg.FONT_BUTTON)
            btn.grid(row=config['row'], column=config['col'], **cfg.MAIN_BUTTON_PADDING)
            # If a ref_name is provided, store the button as an instance variable (e.g., self.work_button).
            if config.get('ref_name'):
                setattr(self, config['ref_name'], btn)

        # Create and place the quote label
        self.quote_label = tk.Label(self.root, font=cfg.FONT_QUOTE, wraplength=cfg.QUOTE_WRAP_LENGTH, justify=tk.CENTER, height=7, cursor="hand2")
        self.quote_label.pack(**cfg.MAIN_QUOTE_PADDING)
        self.quote_label.bind("<Button-1>", self.refresh_quote) # Make the quote clickable to refresh

        # Create and place the footer text
        tk.Label(self.root, text=cfg.STRINGS['footer_text'], font=cfg.FONT_FOOTER, fg=cfg.COLOR_TEXT_SECONDARY).pack(**cfg.MAIN_FOOTER_PADDING)

    def toggle_work(self):
        """Handles clicks on the 'Start/Pause Work' button."""
        # If the timer is currently on a break, switch it back to a work session first
        if self.timer.session_type != 'work':
            self.timer.set_session('work')
        # Now, either start or pause the timer
        if self.timer.state == 'running':
            self.timer.pause()
        else: # This handles both 'idle' and 'paused' states
            self.timer.start()

    def toggle_break(self):
        """Handles clicks on the 'Start/Pause Break' button."""
        # If the timer is currently in a work session, figure out the correct break type
        if self.timer.session_type == 'work':
            self.timer.set_session(self.timer.get_next_break_type())
        # Now, either start or pause the timer
        if self.timer.state == 'running':
            self.timer.pause()
        else: # This handles both 'idle' and 'paused' states
            self.timer.start()

    def reset_timer(self):
        """Resets the timer to its initial state."""
        self.timer.reset()

    def show_settings(self):
        """Opens the settings window, ensuring only one instance can exist."""
        # If the settings window already exists, just bring it to the front
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.lift()
        else:
            # Otherwise, create a new one
            self.settings_window = SettingsWindow(self.root, self)

    def show_stats(self):
        """Opens the statistics window."""
        StatsWindow(self.root, self.app_data["sessions"])

    def reset_stats(self):
        """Clears all session data after user confirmation."""
        # Ask the user for confirmation before deleting data
        if messagebox.askyesno(cfg.STRINGS['title_reset_confirm'], cfg.STRINGS['msg_reset_confirm'], parent=self.root):
            # If they click "Yes", clear the list of sessions and save the change
            self.app_data["sessions"].clear()
            self._save_data()

    def refresh_quote(self, event=None):
        """Fetches and displays a new motivational quote."""
        self.quote_label.config(text=get_quote())

    def _update_loop(self):
        """The main application loop, which runs every second."""
        # Ask the timer to count down by one second
        result = self.timer.tick()

        # 'result' will be None unless a session has just finished.
        if result:
            # Play a simple notification sound
            self.root.bell()
            # This dictionary defines what to do for each type of completion.
            completion_details = {
                "work_complete": {"title": cfg.STRINGS['title_work_complete'], "message": cfg.STRINGS['msg_work_complete'], "next": self.timer.get_next_break_type()},
                "break_complete": {"title": cfg.STRINGS['title_break_complete'], "message": cfg.STRINGS['msg_break_complete'], "next": 'work'}
            }
            details = completion_details.get(result)

            # If the result was valid, proceed with notifications and state changes
            if details:
                messagebox.showinfo(details["title"], details["message"], parent=self.root)
                if result == "work_complete":
                    self.app_data["sessions"].append({"timestamp": datetime.now().isoformat()})
                    self._save_data()
                if self.app_data["settings"]["auto_start"]:
                    self.timer.set_session(details["next"])
                    self.timer.start()

        # After handling any logic, refresh the UI
        self._update_ui()
        # Tell tkinter to run this method again after 1000 milliseconds (1 second)
        self.root.after(1000, self._update_loop)

    def _update_ui(self):
        """Refreshes the UI to reflect the current timer state."""
        # Update the main timer display with the correctly formatted time
        self.timer_display.config(text=format_time(self.timer.time_left))

        # This dictionary maps the timer's state directly to the text needed for the labels and buttons
        ui_map = {
            'work_idle':    (cfg.STRINGS['status_ready'], cfg.STRINGS['btn_start_work'], cfg.STRINGS['btn_start_break']),
            'work_running': (cfg.STRINGS['status_working'], cfg.STRINGS['btn_pause_work'], cfg.STRINGS['btn_start_break']),
            'work_paused':  (cfg.STRINGS['status_work_paused'], cfg.STRINGS['btn_start_work'], cfg.STRINGS['btn_start_break']),
            'break_idle':   (cfg.STRINGS['status_ready'], cfg.STRINGS['btn_start_work'], cfg.STRINGS['btn_start_break']),
            'break_running':(cfg.STRINGS['status_break'], cfg.STRINGS['btn_start_work'], cfg.STRINGS['btn_pause_break']),
            'break_paused': (cfg.STRINGS['status_break_paused'], cfg.STRINGS['btn_start_work'], cfg.STRINGS['btn_start_break']),
        }

        # Determine the correct key to look up in our map
        session_category = 'work' if self.timer.session_type == 'work' else 'break'
        state_key = f"{session_category}_{self.timer.state}"

        # Get the tuple of texts for the current state
        status_text, work_button_text, break_button_text = ui_map[state_key]

        # Apply the new text to the UI widgets
        self.status_label.config(text=status_text)
        self.work_button.config(text=work_button_text)
        self.break_button.config(text=break_button_text)

# =================
# APPLICATION USAGE
# =================
if __name__ == "__main__":
    root = tk.Tk()         # Create the main application window
    app = MainWindow(root) # Create an instance of our main application class, which builds the UI
    root.mainloop()        # Start the tkinter event loop to show the window and run the app