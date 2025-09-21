import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from threading import Thread, Event
import time

class DAQControlGUI:
    def __init__(self, root, daq_interface, waveform_generator):
        self.root = root
        self.root.title("DAQ Control Interface")
        self.daq = daq_interface
        self.generator = waveform_generator
        
        # Configure the main window
        self.root.geometry("1200x800")
        
        # Create frames
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)
        
        self.plots_frame = ttk.Frame(self.root)
        self.plots_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create preview plot frame
        self.preview_frame = ttk.LabelFrame(self.plots_frame, text="Waveform Preview")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create monitoring plot frame
        self.plot_frame = ttk.LabelFrame(self.plots_frame, text="Input Monitor")
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create the preview plot
        self.preview_fig = Figure(figsize=(6, 3))
        self.preview_ax = self.preview_fig.add_subplot(111)
        self.preview_canvas = FigureCanvasTkAgg(self.preview_fig, master=self.preview_frame)
        self.preview_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Create the monitoring plot
        self.fig = Figure(figsize=(6, 3))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Create controls
        self.create_controls()
        
        # Initialize plotting
        self.plot_running = Event()
        self.plot_thread = None
        
    def create_controls(self):
        # Waveform selection
        ttk.Label(self.control_frame, text="Waveform Type:").pack(pady=5)
        self.waveform_var = tk.StringVar(value="sine")
        waveform_options = ["sine", "square", "triangle", "sawtooth"]
        for option in waveform_options:
            ttk.Radiobutton(self.control_frame, text=option.capitalize(),
                          variable=self.waveform_var, value=option,
                          command=self.update_preview).pack()
        
        # Parameters
        ttk.Label(self.control_frame, text="Frequency (Hz):").pack(pady=5)
        self.freq_var = tk.StringVar(value="1.0")
        ttk.Entry(self.control_frame, textvariable=self.freq_var).pack()
        self.freq_var.trace_add("write", self.update_preview)
        
        ttk.Label(self.control_frame, text="Amplitude (V):").pack(pady=5)
        self.amp_var = tk.StringVar(value="1.0")
        ttk.Entry(self.control_frame, textvariable=self.amp_var).pack()
        self.amp_var.trace_add("write", self.update_preview)
        
        ttk.Label(self.control_frame, text="Duration (s):").pack(pady=5)
        self.duration_var = tk.StringVar(value="1.0")
        ttk.Entry(self.control_frame, textvariable=self.duration_var).pack()
        self.duration_var.trace_add("write", self.update_preview)
        
        # Buttons
        ttk.Button(self.control_frame, text="Start Output",
                  command=self.start_output).pack(pady=20)
        ttk.Button(self.control_frame, text="Stop Output",
                  command=self.stop_output).pack(pady=5)
        ttk.Button(self.control_frame, text="Start Monitoring",
                  command=self.start_monitoring).pack(pady=20)
        ttk.Button(self.control_frame, text="Stop Monitoring",
                  command=self.stop_monitoring).pack(pady=5)
    
    def generate_waveform(self):
        try:
            waveform_type = self.waveform_var.get()
            frequency = float(self.freq_var.get())
            amplitude = float(self.amp_var.get())
            duration = float(self.duration_var.get())
            
            generator_method = getattr(self.generator, f"generate_{waveform_type}")
            return generator_method(frequency, amplitude, duration)
        except ValueError:
            return None, None
    
    def update_preview(self, *args):
        """Update the waveform preview plot when parameters change."""
        try:
            t, waveform = self.generate_waveform()
            if t is not None and waveform is not None:
                self.preview_ax.clear()
                self.preview_ax.plot(t, waveform)
                self.preview_ax.set_xlabel('Time (s)')
                self.preview_ax.set_ylabel('Voltage (V)')
                self.preview_ax.set_title(f'{self.waveform_var.get().capitalize()} Wave Preview')
                self.preview_ax.grid(True)
                self.preview_fig.tight_layout()
                self.preview_canvas.draw()
        except Exception as e:
            # Silently fail for preview - this happens during typing
            pass
    
    def start_output(self):
        try:
            self.daq.setup_analog_output()
            _, waveform = self.generate_waveform()
            if waveform is not None:
                self.daq.write_waveform(waveform)
            else:
                raise ValueError("Invalid waveform parameters")
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))
    
    def stop_output(self):
        if self.daq.task_ao:
            self.daq.task_ao.stop()
    
    def start_monitoring(self):
        self.daq.setup_analog_input()
        self.plot_running.set()
        self.plot_thread = Thread(target=self.update_plot)
        self.plot_thread.start()
    
    def stop_monitoring(self):
        self.plot_running.clear()
        if self.plot_thread:
            self.plot_thread.join()
    
    def update_plot(self):
        while self.plot_running.is_set():
            try:
                t, data = self.daq.read_analog()
                self.ax.clear()
                self.ax.plot(t, data)
                self.ax.set_xlabel('Time (s)')
                self.ax.set_ylabel('Voltage (V)')
                self.ax.grid(True)
                self.canvas.draw()
                time.sleep(0.1)  # Update rate
            except Exception as e:
                print(f"Error updating plot: {e}")
                break

def create_gui(daq_interface, waveform_generator):
    root = tk.Tk()
    app = DAQControlGUI(root, daq_interface, waveform_generator)
    return root, app