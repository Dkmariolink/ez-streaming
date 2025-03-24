"""
EZ Streaming - A simple launcher for streaming applications
Main application module containing the core UI and functionality
"""

import tkinter as tk
from tkinter import ttk, filedialog
import os
import subprocess
import sys
from config_manager import ConfigManager

class StreamerApp:
    """Main application class for EZ Streaming"""
    
    def __init__(self):
        """Initialize the application"""
        self.root = None
        self.programs = []
        self.config_manager = ConfigManager()
        self.current_profile = "Default"
        self.profiles = {"Default": []}
        self.changes_made = False
        self.is_initial_loading = True  # Flag to prevent marking changes during initial load

    def run(self):
        """Start the application UI and main loop"""
        self.root = tk.Tk()
        self.root.title("EZ Streaming")
        self.root.geometry("700x550")  # Increased window size
        self.root.minsize(700, 550)    # Increased minimum size

        # Set up close window handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Set window icon
        icon_path = None
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            if hasattr(sys, '_MEIPASS'):
                # Running from PyInstaller bundle
                base_dir = sys._MEIPASS
            else:
                # Fallback to executable directory
                base_dir = os.path.dirname(sys.executable)
            icon_path = os.path.join(base_dir, "assets", "icon.ico")
        else:
            # Running as script
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            icon_path = os.path.join(current_dir, "assets", "icon.ico")

        # Add debug prints to track icon loading
        print(f"Looking for icon at: {icon_path}")
        print(f"Icon exists: {os.path.exists(icon_path)}")

        if icon_path and os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

        # Set app styling
        self.setup_styling()

        # Build the UI
        self.create_widgets()

        # Load saved configuration
        self.load_config()

        # Start main event loop
        self.root.mainloop()
        
    def on_close(self):
        """Handle window close event"""
        if self.changes_made:
            # This is the only popup in the app - for unsaved changes on exit
            from tkinter import messagebox
            result = messagebox.askyesno(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to close without saving?",
                icon="warning"
            )
            if not result:  # User clicked "No"
                return  # Don't close the window
                
        # Close the window
        self.root.destroy()

    def setup_styling(self):
        """Configure the application styling and theme"""
        # Define colors
        self.bg_color = "#1E1E1E"
        self.fg_color = "#FFFFFF"
        self.accent_color = "#9146FF"  # Twitch purple
        self.button_color = "#772CE8"  # Lighter Twitch purple
        
        # Configure ttk styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure frame style
        self.style.configure('TFrame', background=self.bg_color)
        
        # Configure button style
        self.style.configure('TButton', 
                             background=self.button_color, 
                             foreground=self.fg_color, 
                             font=('Arial', 10, 'bold'),
                             borderwidth=1)
        self.style.map('TButton', 
                      background=[('active', self.accent_color)])
        
        # Configure label style
        self.style.configure('TLabel', 
                             background=self.bg_color, 
                             foreground=self.fg_color, 
                             font=('Arial', 10))
        
        # Configure entry style
        self.style.configure('TEntry', 
                             fieldbackground="#2E2E2E",
                             foreground=self.fg_color)
        
        # Configure combobox style
        self.style.configure('TCombobox', 
                            fieldbackground="#2E2E2E",
                            foreground=self.fg_color,
                            background=self.bg_color)
        
        # Apply background color to root window
        self.root.configure(bg=self.bg_color)

        # Add status colors
        self.ready_color = "#FFFFFF"     # White (same as regular text)
        self.launching_color = "#9146FF" # Purple (same as accent_color)
        self.launched_color = "#00C853"  # Green
        self.error_color = "#FF5252"     # Red
        self.warning_color = "#FFC107"   # Amber - for warnings/notifications

    def create_widgets(self):
        """Create and arrange all UI widgets"""
        # Main container frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Application header with title
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(header_frame, 
                               text="EZ Streaming", 
                               font=('Arial', 18, 'bold'), 
                               foreground=self.accent_color)
        title_label.pack(side=tk.LEFT)
        
        # Profile selection area
        profile_frame = ttk.Frame(main_frame)
        profile_frame.pack(fill=tk.X, pady=(0, 10))
        
        profile_label = ttk.Label(profile_frame, text="Current Profile:")
        profile_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Create a custom style for the purple combobox
        self.style.configure('Purple.TCombobox', 
                             fieldbackground="#2E2E2E",
                             background=self.accent_color,
                             foreground=self.fg_color,
                             arrowcolor=self.fg_color)
        
        self.profile_var = tk.StringVar(value=self.current_profile)
        self.profile_combobox = ttk.Combobox(profile_frame, 
                                            textvariable=self.profile_var,
                                            state="readonly",
                                            style='Purple.TCombobox')
        self.profile_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.profile_combobox.bind("<<ComboboxSelected>>", self.change_profile)
        
        # Ensure combobox styling - explicitly set dropdown foreground color
        self.style.map('Purple.TCombobox', 
                       fieldbackground=[('readonly', "#2E2E2E")],
                       selectbackground=[('readonly', "#2E2E2E")],
                       selectforeground=[('readonly', "#FFFFFF")],
                       background=[('readonly', self.accent_color)])  # Purple background for the button
        
        # Profile creation section with proper label
        new_profile_label = ttk.Label(profile_frame, text="New Profile:")
        new_profile_label.pack(side=tk.LEFT, padx=(15, 5))
        
        self.new_profile_var = tk.StringVar()
        new_profile_entry = ttk.Entry(profile_frame, textvariable=self.new_profile_var, width=15)
        new_profile_entry.pack(side=tk.LEFT, padx=(0, 0))
        new_profile_entry.bind("<Return>", lambda e: self.new_profile_from_entry())
        
        add_profile_btn = ttk.Button(profile_frame, 
                                   text="+", 
                                   width=2,
                                   command=self.new_profile_from_entry)
        add_profile_btn.pack(side=tk.LEFT, padx=(2, 0))
        
        # Program list header
        list_header_frame = ttk.Frame(main_frame)
        list_header_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(list_header_frame, text="App Name", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        ttk.Label(list_header_frame, text="Path", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        ttk.Label(list_header_frame, text="Actions", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(5, 95))
        
        # Scrollable program list area
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        # Create canvas with scrollbar for program entries
        self.canvas = tk.Canvas(list_frame, 
                               bg=self.bg_color, 
                               highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, 
                                 orient=tk.VERTICAL, 
                                 command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame to contain program entries
        self.program_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window(
            (0, 0), 
            window=self.program_frame, 
            anchor=tk.NW,
            width=self.canvas.winfo_width()
        )
        
        # Configure canvas and scrolling behavior
        self.program_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Status bar area
        self.status_frame = ttk.Frame(main_frame)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(5, 5))
        
        self.status_var = tk.StringVar(value="")
        self.status_label = ttk.Label(self.status_frame, 
                                     textvariable=self.status_var,
                                     font=('Arial', 9),
                                     foreground=self.fg_color)
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Action buttons at bottom
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 5))
        
        add_btn = ttk.Button(button_frame, 
                            text="Add Program", 
                            command=self.add_program)
        add_btn.pack(side=tk.LEFT)

        save_btn = ttk.Button(button_frame, 
                             text="Save Profile", 
                             command=lambda: self.save_config(True))
        save_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
        launch_all_btn = ttk.Button(button_frame, 
                                   text="Launch All", 
                                   command=self.launch_all)
        launch_all_btn.pack(side=tk.RIGHT)
        
        # Footer with credits
        credit_label = ttk.Label(main_frame, 
                                text="Created by Dkmariolink - Free Software", 
                                font=('Arial', 8),
                                foreground="#AAAAAA")
        credit_label.pack(side=tk.BOTTOM, pady=(0, 5))

    def show_status(self, message, color=None, duration=5000, blink=False):
        """
        Show a message in the status bar that auto-clears after duration
        
        Args:
            message (str): The message to display
            color (str, optional): The text color. Defaults to self.fg_color.
            duration (int, optional): How long to show message in ms. Defaults to 5000.
            blink (bool, optional): Whether to make the message blink for attention. Defaults to False.
        """
        if color is None:
            color = self.fg_color
        
        self.status_var.set(message)
        self.status_label.configure(foreground=color)
        
        # If it's an error message, make it blink for attention
        if color == self.error_color or blink:
            self._blink_status(color, 5)  # Blink 5 times
        
        # Auto-clear after duration
        self.root.after(duration, self.clear_status)
        
    def _blink_status(self, color, times=7, interval=200):
        """
        Make the status message blink to get attention
        
        Args:
            color (str): The color to blink between
            times (int, optional): Number of blinks. Defaults to 7.
            interval (int, optional): Time between blinks in ms. Defaults to 200.
        """
        if times <= 0:
            # Ensure we end with the proper color visible
            self.status_label.configure(foreground=color)
            return
            
        # Toggle visibility - blink between color and invisible
        current_color = self.status_label.cget("foreground")
        
        # Create very high contrast by alternating between color and invisible
        if current_color == color:
            # Make text color match the background color (effectively invisible)
            self.status_label.configure(foreground=self.bg_color)
        else:
            # Make text visible again
            self.status_label.configure(foreground=color)
            
        # Schedule next blink with faster interval for more attention
        self.root.after(interval, lambda: self._blink_status(color, times-1, interval))

    def clear_status(self):
        """Clear the status message"""
        self.status_var.set("")

    def mark_unsaved_changes(self):
        """Mark that unsaved changes have been made"""
        self.changes_made = True
        self.show_status("Changes made. Remember to save your profile.", self.warning_color)

    def on_frame_configure(self, event=None):
        """Update the scrollregion of the canvas when the frame size changes"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event=None):
        """Update the width of the frame inside canvas when canvas size changes"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def add_program(self, name="", path=""):
        """Add a new program entry to the UI"""
        idx = len(self.programs)
        program_entry = ttk.Frame(self.program_frame)
        program_entry.pack(fill=tk.X, pady=5, padx=2)
        
        # Program name entry
        name_var = tk.StringVar(value=name)
        name_entry = ttk.Entry(program_entry, textvariable=name_var)
        name_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        # Program path entry
        path_var = tk.StringVar(value=path)
        path_entry = ttk.Entry(program_entry, textvariable=path_var)
        path_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)

        # Mark unsaved changes when entries are modified
        name_var.trace_add("write", lambda *args: self.mark_unsaved_changes())
        path_var.trace_add("write", lambda *args: self.mark_unsaved_changes())
        
        # Browse button
        browse_btn = ttk.Button(program_entry, 
                               text="Browse", 
                               command=lambda: self.browse_file(path_var))
        browse_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Launch button
        launch_btn = ttk.Button(program_entry, 
                               text="Launch",
                               command=lambda: self.launch_program(path_var.get()))
        launch_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Remove button
        remove_btn = ttk.Button(program_entry, 
                               text="✕",
                               command=lambda i=idx: self.remove_program(i))
        remove_btn.pack(side=tk.LEFT)

        # Status indicator
        status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(program_entry, textvariable=status_var, width=10)
        status_label.configure(foreground=self.ready_color)  # Set initial color
        status_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Store program data
        program_data = {
            "frame": program_entry,
            "name_var": name_var,
            "path_var": path_var,
            "status_var": status_var,
            "process": None 
        }
        self.programs.append(program_data)
        
        # Only mark changes if this isn't during initial loading
        if not self.is_initial_loading and not (name == "" and path == ""):
            self.mark_unsaved_changes()
        
        return program_data

    def browse_file(self, path_var):
        """Open file browser to select program executable"""
        file_path = filedialog.askopenfilename(
            title="Select Program",
            filetypes=[("Executable", "*.exe"), ("All Files", "*.*")]
        )
        if file_path:
            path_var.set(file_path)
            self.mark_unsaved_changes()

    def launch_program(self, path):
        """Launch a single program"""
        if not path:
            self.show_status("Please select a program file", self.warning_color, blink=True)
            return
    
        try:
            # Find the program entry that matches this path
            for program in self.programs:
                if program["path_var"].get() == path:
                    # Update status to "Launching..."
                    program["status_var"].set("Launching...")
                    # Get the status label (last child in the frame)
                    status_label = [child for child in program["frame"].winfo_children() 
                                 if isinstance(child, ttk.Label)][-1]
                    status_label.configure(foreground=self.launching_color)
                    self.root.update()
            
                    # Extract the directory from the path
                    program_dir = os.path.dirname(path)
                    # Launch the program with its directory as working directory
                    process = subprocess.Popen([path], cwd=program_dir)
            
                    # Store the process object for status checking
                    program["process"] = process
            
                    # Update status to "Launched"
                    program["status_var"].set("Launched")
                    status_label.configure(foreground=self.launched_color)
                    self.root.update()
                    
                    # Show status message
                    app_name = program["name_var"].get() or os.path.basename(path)
                    self.show_status(f"Launched {app_name}", self.launched_color)
            
                    # Start monitoring the process
                    self.monitor_process(program)
                    break
        except Exception as e:
            # Find the program entry that matches this path (for error case)
            for program in self.programs:
                if program["path_var"].get() == path:
                    # Update status to "Error"
                    program["status_var"].set("Error")
                    status_label = [child for child in program["frame"].winfo_children() 
                                  if isinstance(child, ttk.Label)][-1]
                    status_label.configure(foreground=self.error_color)
                    self.root.update()
            
            # Show status message with error
            self.show_status(f"Error launching program: {str(e)}", self.error_color, 5000, blink=True)

    def monitor_process(self, program):
        """Monitor a launched process and update status when it exits"""
        if "process" in program and program["process"] is not None:
            process = program["process"]
        
            # Check if process is still running
            if process.poll() is None:
                # Process is still running, check again in 2 seconds
                self.root.after(2000, lambda p=program: self.monitor_process(p))
            else:
                # Process has exited, update status
                program["status_var"].set("Ready")
                status_label = [child for child in program["frame"].winfo_children() 
                               if isinstance(child, ttk.Label)][-1]
                status_label.configure(foreground=self.ready_color)
                program["process"] = None  # Reset the process reference
                
                # Show status message when program closes
                app_name = program["name_var"].get() or os.path.basename(program["path_var"].get())
                self.show_status(f"{app_name} has closed", self.warning_color)       

    def launch_all(self):
        """Launch all configured programs with a short delay between each"""
        if not self.programs:
            self.show_status("No programs configured to launch", self.warning_color, blink=True)
            return
            
        launched = 0
    
        for program in self.programs:
            path = program["path_var"].get()
            name = program["name_var"].get() or "Unknown"
        
            if path: 
                # Update status to "Launching..."
                program["status_var"].set("Launching...")
                status_label = [child for child in program["frame"].winfo_children() 
                            if isinstance(child, ttk.Label)][-1]
                status_label.configure(foreground=self.launching_color)
                self.root.update()

                try:
                    program_dir = os.path.dirname(path)
                    process = subprocess.Popen([path], cwd=program_dir)
                
                    # Store the process object for status checking
                    program["process"] = process
                
                    launched += 1

                    # Update status to "Launched"
                    program["status_var"].set("Launched")
                    status_label.configure(foreground=self.launched_color)
                    self.root.update()
                
                    # Start monitoring the process
                    self.monitor_process(program)

                    # Small delay to prevent system overload
                    self.root.after(1500)
                except Exception as e:
                    # Update status to "Error"
                    program["status_var"].set("Error")
                    status_label.configure(foreground=self.error_color)
                    self.show_status(f"Error launching {name}: {str(e)}", self.error_color, 5000, blink=True)
        
        # Show launch summary in status bar
        if launched > 0:
            self.show_status(f"Successfully launched {launched} programs", self.launched_color)
        else:
            self.show_status("No programs were launched", self.warning_color, blink=True)

    def reset_launch_statuses(self):
        """Reset all launch status indicators to Ready"""
        for program in self.programs:
            if "status_var" in program:
                program["status_var"].set("Ready")
                status_label = [child for child in program["frame"].winfo_children() 
                              if isinstance(child, ttk.Label)][-1]
                status_label.configure(foreground=self.ready_color)

    def remove_program(self, idx):
        """Remove a program from the list"""
        if 0 <= idx < len(self.programs):
            self.programs[idx]["frame"].destroy()
            self.programs.pop(idx)
            
            # Mark that changes have been made
            self.mark_unsaved_changes()
            
            # Refresh UI
            self.refresh_program_list()
            
            # Show status message
            self.show_status("Program removed", self.warning_color)

    def refresh_program_list(self):
        """Refresh the program list UI from data"""
        # Destroy all program frames
        for program in self.programs:
            program["frame"].destroy()
        
        # Recreate program entries from stored data
        temp_programs = self.programs.copy()
        self.programs = []
        
        for program in temp_programs:
            name = program["name_var"].get()
            path = program["path_var"].get()
            self.add_program(name, path)

    def new_profile_from_entry(self):
        """Create a new profile from the entry field"""
        profile_name = self.new_profile_var.get().strip()
        
        if not profile_name:
            self.show_status("Please enter a profile name", self.warning_color, blink=True)
            return
            
        if profile_name in self.profiles:
            self.show_status(f"Profile '{profile_name}' already exists", self.warning_color, blink=True)
            return
            
        # Create new profile
        self.profiles[profile_name] = []
        self.update_profile_combobox()
        self.profile_var.set(profile_name)
        self.change_profile()
        
        # Clear the entry field
        self.new_profile_var.set("")
        
        # Show status message
        self.show_status(f"Created new profile: {profile_name}", self.launched_color)

    def change_profile(self, event=None):
        """Change to a different profile"""
        selected_profile = self.profile_var.get()
        if selected_profile != self.current_profile:
            # Check for unsaved changes
            if self.changes_made:
                self.show_status("Warning: Changes not saved! Click Save Profile to save them.", 
                              self.error_color, 5000, blink=True)
            
            # Load new profile
            self.current_profile = selected_profile
            self.load_profile(selected_profile)
            
            # Reset changes flag
            self.changes_made = False
            
            # Show status message
            self.show_status(f"Switched to profile: {selected_profile}", self.launched_color)

    def save_config(self, show_confirmation=False):
        """
        Save the current configuration
        
        Args:
            show_confirmation (bool): Whether to show a confirmation
        """
        # Build the configuration to save
        profile_data = []
        for program in self.programs:
            profile_data.append({
                "name": program["name_var"].get(),
                "path": program["path_var"].get()
            })
        self.profiles[self.current_profile] = profile_data
        
        config = {
            "profiles": self.profiles,
            "current_profile": self.current_profile
        }
        
        success = self.config_manager.save_config(config)
        
        # Reset the changes flag
        self.changes_made = False
        
        # Show confirmation with status bar message
        if success:
            if show_confirmation:
                self.show_status(f"Profile '{self.current_profile}' saved successfully.", self.launched_color)
        else:
            self.show_status("Failed to save profile.", self.error_color)

    def load_profile(self, profile_name):
        """Load a profile by name"""
        # Clear current program list
        for program in self.programs:
            program["frame"].destroy()
        self.programs = []
        
        # Load profile programs
        if profile_name in self.profiles:
            for program_data in self.profiles[profile_name]:
                self.add_program(
                    program_data.get("name", ""), 
                    program_data.get("path", "")
                )
        
        # Update UI
        self.update_profile_combobox()

    def update_profile_combobox(self):
        """Update the profile selection dropdown"""
        self.profile_combobox["values"] = list(self.profiles.keys())

    def load_config(self):
        """Load the saved configuration"""
        config = self.config_manager.load_config()
        
        if config:
            self.profiles = config.get("profiles", {"Default": []})
            self.current_profile = config.get("current_profile", "Default")
        else:
            # Initialize with default streaming apps
            default_apps = [
                {"name": "", "path": ""},
                {"name": "", "path": ""},
                {"name": "", "path": ""},
                {"name": "", "path": ""},
                {"name": "", "path": ""}
            ]
            self.profiles = {"Default": default_apps}
            
        # Ensure Default profile exists
        if "Default" not in self.profiles:
            self.profiles["Default"] = []
            
        # Mark that we're doing initial loading (don't mark changes)
        self.is_initial_loading = True
        
        # Update UI
        self.update_profile_combobox()
        self.profile_var.set(self.current_profile)
        self.load_profile(self.current_profile)
        
        # Reset changes flag since we just loaded
        self.changes_made = False
        
        # Initial loading is complete
        self.is_initial_loading = False