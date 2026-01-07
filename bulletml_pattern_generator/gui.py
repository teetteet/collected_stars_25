"""
BulletML Pattern Generator - GUI Module
Interactive Tkinter-based GUI for pattern creation
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from bulletml_core import BulletMLGenerator


class BulletMLGUI:
    """Main GUI class for BulletML Pattern Generator"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("BulletML Pattern Generator")
        self.root.geometry("1200x800")
        
        # Initialize generator
        self.generator = BulletMLGenerator()
        
        # Storage for parameter widgets
        self.param_widgets = {}
        
        # Setup GUI
        self.setup_gui()
        
        # Initial preview update
        self.update_preview()
    
    def setup_gui(self):
        """Setup the main GUI layout"""
        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Controls
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Right panel - Preview
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Setup left panel sections
        self.setup_toolbar(left_panel)
        self.setup_presets(left_panel)
        self.setup_parameters(left_panel)
        
        # Setup right panel
        self.setup_preview(right_panel)
        self.setup_keyboard_shortcuts()
    
    def setup_toolbar(self, parent):
        """Setup toolbar with file operations"""
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(toolbar, text="Load (Ctrl+O)", 
                  command=self.load_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Save (Ctrl+S)", 
                  command=self.save_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Reset (Ctrl+R)", 
                  command=self.reset_parameters).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Update Preview (Ctrl+U)", 
                  command=self.update_preview).pack(side=tk.LEFT, padx=2)
    
    def setup_presets(self, parent):
        """Setup preset buttons"""
        preset_frame = ttk.LabelFrame(parent, text="Presets", padding=10)
        preset_frame.pack(fill=tk.X, pady=(0, 10))
        
        presets = ['Spiral', 'Circle', 'Wave', 'Flower']
        for i, preset in enumerate(presets):
            ttk.Button(preset_frame, text=preset, 
                      command=lambda p=preset: self.load_preset(p)).grid(
                          row=0, column=i, padx=2, sticky=tk.EW)
            preset_frame.columnconfigure(i, weight=1)
    
    def setup_parameters(self, parent):
        """Setup parameter controls with sliders"""
        # Create scrollable frame for parameters
        canvas = tk.Canvas(parent, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Basic Parameters
        self.add_param_section(scrollable_frame, "Basic Parameters", [
            ('bullets_per_shoot', 'Bullets Per Shoot', 1, 100, 1),
            ('repeat_count', 'Repeat Count', 1, 50, 1),
            ('wait_time', 'Wait Time', 0.0, 2.0, 0.01)
        ])
        
        # Position Parameters
        self.add_param_section(scrollable_frame, "Position", [
            ('pos_x', 'Position X', -200.0, 200.0, 1.0),
            ('pos_y', 'Position Y', -200.0, 200.0, 1.0)
        ])
        
        # Movement Parameters
        self.add_param_section(scrollable_frame, "Movement", [
            ('speed', 'Speed', 0.1, 10.0, 0.1),
            ('acceleration', 'Acceleration', -1.0, 1.0, 0.01)
        ])
        
        # Angle Parameters
        self.add_param_section(scrollable_frame, "Angle", [
            ('angle_target', 'Target Angle', 0.0, 360.0, 1.0),
            ('angle_increment', 'Angle Increment', 0.0, 360.0, 0.5),
            ('rotation_speed', 'Rotation Speed', -20.0, 20.0, 0.1)
        ])
        
        # Sine Wave Parameters
        self.add_param_checkbox(scrollable_frame, "Sine Wave")
        self.add_param_section(scrollable_frame, "Sine Wave Parameters", [
            ('sine_amplitude', 'Amplitude', 0.0, 50.0, 0.1),
            ('sine_frequency', 'Frequency', 0.0, 10.0, 0.1),
            ('sine_phase', 'Phase', 0.0, 6.28, 0.01)
        ])
        
        # Polar Coordinates
        self.add_param_checkbox_polar(scrollable_frame, "Polar Coordinates")
        self.add_param_section(scrollable_frame, "Polar Parameters", [
            ('polar_radius', 'Radius', 0.0, 200.0, 1.0),
            ('polar_angle', 'Angle Offset', 0.0, 360.0, 1.0)
        ])
        
        # Iteration-based Modifications
        self.add_param_section(scrollable_frame, "Iteration Modifications", [
            ('iter_speed_mod', 'Speed Modifier', -0.5, 0.5, 0.01),
            ('iter_direction_mod', 'Direction Modifier', -10.0, 10.0, 0.1)
        ])
        
        # Sprite name (text entry)
        self.add_text_param(scrollable_frame, "Sprite Settings", 'sprite', 'Sprite Name')
    
    def add_param_section(self, parent, section_name, params):
        """Add a section of parameter sliders"""
        frame = ttk.LabelFrame(parent, text=section_name, padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        for param_name, label, min_val, max_val, resolution in params:
            self.add_slider(frame, param_name, label, min_val, max_val, resolution)
    
    def add_slider(self, parent, param_name, label, min_val, max_val, resolution):
        """Add a slider control for a parameter"""
        row_frame = ttk.Frame(parent)
        row_frame.pack(fill=tk.X, pady=2)
        
        # Label
        ttk.Label(row_frame, text=label, width=20).pack(side=tk.LEFT)
        
        # Value display
        value_var = tk.StringVar(value=str(self.generator.get_parameter(param_name)))
        value_label = ttk.Label(row_frame, textvariable=value_var, width=8, anchor=tk.E)
        value_label.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Slider
        slider = ttk.Scale(row_frame, from_=min_val, to=max_val,
                          orient=tk.HORIZONTAL,
                          command=lambda v, pn=param_name, vv=value_var: 
                              self.on_slider_change(pn, v, vv))
        slider.set(self.generator.get_parameter(param_name))
        slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.param_widgets[param_name] = {
            'slider': slider,
            'value_var': value_var,
            'resolution': resolution
        }
    
    def add_param_checkbox(self, parent, section_name):
        """Add checkbox for sine wave enable"""
        frame = ttk.LabelFrame(parent, text=section_name, padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        var = tk.BooleanVar(value=self.generator.get_parameter('sine_enabled'))
        check = ttk.Checkbutton(frame, text="Enable Sine Wave", variable=var,
                               command=lambda: self.on_checkbox_change('sine_enabled', var))
        check.pack(anchor=tk.W)
        
        self.param_widgets['sine_enabled'] = {'var': var}
    
    def add_param_checkbox_polar(self, parent, section_name):
        """Add checkbox for polar coordinates"""
        frame = ttk.LabelFrame(parent, text=section_name, padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        var = tk.BooleanVar(value=self.generator.get_parameter('polar_enabled'))
        check = ttk.Checkbutton(frame, text="Enable Polar Coordinates", variable=var,
                               command=lambda: self.on_checkbox_change('polar_enabled', var))
        check.pack(anchor=tk.W)
        
        self.param_widgets['polar_enabled'] = {'var': var}
    
    def add_text_param(self, parent, section_name, param_name, label):
        """Add text entry for sprite name"""
        frame = ttk.LabelFrame(parent, text=section_name, padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        row_frame = ttk.Frame(frame)
        row_frame.pack(fill=tk.X)
        
        ttk.Label(row_frame, text=label).pack(side=tk.LEFT, padx=(0, 5))
        
        entry_var = tk.StringVar(value=self.generator.get_parameter(param_name))
        entry = ttk.Entry(row_frame, textvariable=entry_var)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        entry.bind('<KeyRelease>', lambda e, pn=param_name, ev=entry_var: 
                  self.on_text_change(pn, ev))
        
        self.param_widgets[param_name] = {'var': entry_var}
    
    def setup_preview(self, parent):
        """Setup XML preview panel"""
        preview_frame = ttk.LabelFrame(parent, text="XML Preview", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create text widget with scrollbar
        self.preview_text = scrolledtext.ScrolledText(
            preview_frame,
            wrap=tk.WORD,
            width=60,
            height=40,
            font=('Courier', 9)
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-o>', lambda e: self.load_file())
        self.root.bind('<Control-r>', lambda e: self.reset_parameters())
        self.root.bind('<Control-u>', lambda e: self.update_preview())
        self.root.bind('<Control-1>', lambda e: self.load_preset('Spiral'))
        self.root.bind('<Control-2>', lambda e: self.load_preset('Circle'))
        self.root.bind('<Control-3>', lambda e: self.load_preset('Wave'))
        self.root.bind('<Control-4>', lambda e: self.load_preset('Flower'))
    
    def on_slider_change(self, param_name, value, value_var):
        """Handle slider value changes"""
        resolution = self.param_widgets[param_name]['resolution']
        
        # Round to resolution
        numeric_value = float(value)
        if resolution >= 1:
            numeric_value = int(round(numeric_value / resolution) * resolution)
        else:
            numeric_value = round(numeric_value / resolution) * resolution
        
        # Update generator
        self.generator.set_parameter(param_name, numeric_value)
        
        # Update display
        value_var.set(f"{numeric_value:.2f}" if resolution < 1 else str(numeric_value))
        
        # Auto-update preview
        self.update_preview()
    
    def on_checkbox_change(self, param_name, var):
        """Handle checkbox changes"""
        self.generator.set_parameter(param_name, var.get())
        self.update_preview()
    
    def on_text_change(self, param_name, var):
        """Handle text entry changes"""
        self.generator.set_parameter(param_name, var.get())
        self.update_preview()
    
    def update_preview(self):
        """Update the XML preview"""
        xml_content = self.generator.get_xml_preview()
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', xml_content)
    
    def load_preset(self, preset_name):
        """Load a preset pattern"""
        if self.generator.load_preset(preset_name):
            self.update_all_widgets()
            self.update_preview()
            messagebox.showinfo("Preset Loaded", f"{preset_name} preset loaded successfully!")
        else:
            messagebox.showerror("Error", f"Failed to load preset: {preset_name}")
    
    def reset_parameters(self):
        """Reset all parameters to defaults"""
        self.generator.reset_to_defaults()
        self.update_all_widgets()
        self.update_preview()
        messagebox.showinfo("Reset", "Parameters reset to defaults")
    
    def update_all_widgets(self):
        """Update all widget values from generator"""
        params = self.generator.get_all_parameters()
        
        for param_name, value in params.items():
            if param_name in self.param_widgets:
                widget_info = self.param_widgets[param_name]
                
                if 'slider' in widget_info:
                    # Update slider and value
                    widget_info['slider'].set(value)
                    resolution = widget_info['resolution']
                    display_value = f"{value:.2f}" if resolution < 1 else str(value)
                    widget_info['value_var'].set(display_value)
                
                elif 'var' in widget_info:
                    # Update checkbox or text entry
                    widget_info['var'].set(value)
    
    def save_file(self):
        """Save current pattern to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".xml",
            filetypes=[("BulletML files", "*.xml"), ("All files", "*.*")],
            initialdir=".",
            title="Save BulletML Pattern"
        )
        
        if filename:
            if self.generator.save_to_file(filename):
                messagebox.showinfo("Success", f"Pattern saved to {filename}")
            else:
                messagebox.showerror("Error", "Failed to save file")
    
    def load_file(self):
        """Load pattern from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("BulletML files", "*.xml"), ("All files", "*.*")],
            initialdir=".",
            title="Load BulletML Pattern"
        )
        
        if filename:
            if self.generator.load_from_file(filename):
                self.update_all_widgets()
                self.update_preview()
                messagebox.showinfo("Success", f"Pattern loaded from {filename}")
            else:
                messagebox.showerror("Error", "Failed to load file")
    
    def run(self):
        """Start the GUI main loop"""
        self.root.mainloop()


def create_gui():
    """Factory function to create and return the GUI"""
    root = tk.Tk()
    gui = BulletMLGUI(root)
    return gui
