from src.daq.interface import DAQInterface
from src.waveforms.generator import WaveformGenerator
from src.gui.app import create_gui

def main():
    # Initialize the DAQ interface
    daq = DAQInterface()
    
    # Initialize the waveform generator
    generator = WaveformGenerator()
    
    # Create and start the GUI
    root, _ = create_gui(daq, generator)
    try:
        root.mainloop()
    finally:
        # Ensure cleanup when the application closes
        daq.stop()

if __name__ == "__main__":
    main()