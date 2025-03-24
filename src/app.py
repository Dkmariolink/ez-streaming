"""
EZ Streaming - A simple launcher for streaming applications
Main application module containing the core UI and functionality
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
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

    def run(self):
        """Start the application UI and main loop"""
        self.root = tk.Tk()
        self.root.title("EZ Streaming")
        self.root.geometry("620x500")
        self.root.minsize(500, 400)

        # Set window icon
        icon_path = None
        if getattr(sys, 'frozen', False):
        # Running as compiled executable
            app_dir = os.path.dirname(sys.executable)
            icon_path = os.path.join(app_dir, "assets", "icon.ico")
        else:
            # Running as script
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            icon_path = os.path.join(current_dir, "assets", "icon.ico")
    
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
        
        profile_label = ttk.Label(profile_frame, text="Profile:")
        profile_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.profile_var = tk.StringVar(value=self.current_profile)
        self.profile_combobox = ttk.Combobox(profile_frame, 
                                            textvariable=self.profile_var,
                                            state="readonly")
        self.profile_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.profile_combobox.bind("<<ComboboxSelected>>", self.change_profile)
        
        new_profile_btn = ttk.Button(profile_frame, 
                                    text="New Profile", 
                                    command=self.new_profile)
        new_profile_btn.pack(side=tk.LEFT, padx=(5, 0))
        
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
        
        # Action buttons at bottom
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 5))
        
        add_btn = ttk.Button(button_frame, 
                            text="Add Program", 
                            command=self.add_program)
        add_btn.pack(side=tk.LEFT)
        
        launch_all_btn = ttk.Button(button_frame, 
                                   text="Launch All", 
                                   command=self.launch_all)
        launch_all_btn.pack(side=tk.RIGHT)
        
        # Footer with credits
        credit_label = ttk.Label(main_frame, 
                                text="Created by Dkmariolink - Free Software", 
                                font=('Arial', 8),
                                foreground="#AAAAAA")
        credit_label.pack(side=tk.BOTTOM, pady=(10, 0))

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
        
        # Store program data
        program_data = {
            "frame": program_entry,
            "name_var": name_var,
            "path_var": path_var
        }
        self.programs.append(program_data)
        
        # Update configuration
        self.save_config()
        
        return program_data

    def browse_file(self, path_var):
        """Open file browser to select program executable"""
        file_path = filedialog.askopenfilename(
            title="Select Program",
            filetypes=[("Executable", "*.exe"), ("All Files", "*.*")]
        )
        if file_path:
            path_var.set(file_path)
            self.save_config()

    def launch_program(self, path):
         """Launch a single program"""
         if not path:
            messagebox.showerror("Error", "Please select a program file.")
            return
            
         try:
            # Extract the directory from the path
            program_dir = os.path.dirname(path)
            # Launch the program with its directory as working directory
            subprocess.Popen([path], cwd=program_dir)
         except Exception as e:
            messagebox.showerror("Launch Error", str(e))

    def launch_all(self):
        """Launch all configured programs with a short delay between each"""
        if not self.programs:
            messagebox.showinfo("No Programs", "No programs configured to launch.")
            return
            
        launched = 0
        
        for program in self.programs:
            path = program["path_var"].get()
            name = program["name_var"].get() or "Unknown"
            
            if path:
                try:
                    program_dir = os.path.dirname(path)
                    subprocess.Popen([path], cwd=program_dir)
                    launched += 1
                    # Update UI to give feedback
                    self.root.update()
                    # Small delay to prevent system overload
                    self.root.after(1500)
                except Exception as e:
                    messagebox.showerror("Launch Error", 
                                       f"Error launching {name}: {str(e)}")
        
        if launched > 0:
            messagebox.showinfo("Launch Complete", 
                             f"Successfully launched {launched} programs.")
        else:
            messagebox.showwarning("Launch Failed", 
                                "No programs were launched. Please check your configuration.")

    def remove_program(self, idx):
        """Remove a program from the list"""
        if 0 <= idx < len(self.programs):
            self.programs[idx]["frame"].destroy()
            self.programs.pop(idx)
            self.save_config()
            
            # Refresh UI
            self.refresh_program_list()

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

    def new_profile(self):
        """Create a new profile"""
        import tkinter.simpledialog as simpledialog
        
        profile_name = simpledialog.askstring("New Profile", 
                                            "Enter profile name:")
        if profile_name and profile_name not in self.profiles:
            # Save current profile first
            self.save_current_profile()
            
            # Create new profile
            self.profiles[profile_name] = []
            self.update_profile_combobox()
            self.profile_var.set(profile_name)
            self.change_profile()
        elif profile_name in self.profiles:
            messagebox.showwarning("Profile Exists", 
                                "A profile with that name already exists.")

    def change_profile(self, event=None):
        """Change to a different profile"""
        selected_profile = self.profile_var.get()
        if selected_profile != self.current_profile:
            # Save current profile
            self.save_current_profile()
            
            # Load new profile
            self.current_profile = selected_profile
            self.load_profile(selected_profile)

    def save_current_profile(self):
        """Save the current profile data"""
        profile_data = []
        for program in self.programs:
            profile_data.append({
                "name": program["name_var"].get(),
                "path": program["path_var"].get()
            })
        self.profiles[self.current_profile] = profile_data

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
        
        # Update config with new current profile
        self.config_manager.save_config({
            "profiles": self.profiles,
            "current_profile": self.current_profile
        })

    def update_profile_combobox(self):
        """Update the profile selection dropdown"""
        self.profile_combobox["values"] = list(self.profiles.keys())

    def save_config(self):
        """Save the current configuration"""
        self.save_current_profile()
        
        config = {
            "profiles": self.profiles,
            "current_profile": self.current_profile
        }
        
        self.config_manager.save_config(config)

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
            
        # Update UI
        self.update_profile_combobox()
        self.profile_var.set(self.current_profile)
        self.load_profile(self.current_profile)