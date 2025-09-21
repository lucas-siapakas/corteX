import nidaqmx
import numpy as np
from nidaqmx.constants import AcquisitionType

class DAQInterface:
    def __init__(self):
        self.task_ao = None
        self.task_ai = None
        
    def setup_analog_output(self, channel="Dev1/ao0"):
        """
        Set up an analog output task.
        
        Args:
            channel (str): The name of the analog output channel
        """
        if self.task_ao is not None:
            self.task_ao.close()
        
        self.task_ao = nidaqmx.Task()
        self.task_ao.ao_channels.add_ao_voltage_chan(channel)
    
    def setup_analog_input(self, channel="Dev1/ai0"):
        """
        Set up an analog input task.
        
        Args:
            channel (str): The name of the analog input channel
        """
        if self.task_ai is not None:
            self.task_ai.close()
            
        self.task_ai = nidaqmx.Task()
        self.task_ai.ai_channels.add_ai_voltage_chan(channel)
    
    def write_waveform(self, waveform, sample_rate=1000):
        """
        Write a waveform to the analog output.
        
        Args:
            waveform (numpy.ndarray): The waveform data to output
            sample_rate (int): Number of samples per second
        """
        if self.task_ao is None:
            raise RuntimeError("Analog output task not initialized")
            
        self.task_ao.timing.cfg_samp_clk_timing(
            rate=sample_rate,
            sample_mode=AcquisitionType.CONTINUOUS,
            samps_per_chan=len(waveform)
        )
        self.task_ao.write(waveform, auto_start=True)
    
    def read_analog(self, num_samples=1000, sample_rate=1000):
        """
        Read from the analog input.
        
        Args:
            num_samples (int): Number of samples to read
            sample_rate (int): Number of samples per second
            
        Returns:
            tuple: (time_points, voltage_data)
        """
        if self.task_ai is None:
            raise RuntimeError("Analog input task not initialized")
            
        self.task_ai.timing.cfg_samp_clk_timing(
            rate=sample_rate,
            sample_mode=AcquisitionType.FINITE,
            samps_per_chan=num_samples
        )
        
        data = self.task_ai.read(number_of_samples_per_channel=num_samples)
        t = np.linspace(0, num_samples/sample_rate, num_samples)
        return t, np.array(data)
    
    def stop(self):
        """Stop and clean up all tasks."""
        if self.task_ao is not None:
            self.task_ao.stop()
            self.task_ao.close()
            self.task_ao = None
            
        if self.task_ai is not None:
            self.task_ai.stop()
            self.task_ai.close()
            self.task_ai = None
            
    def __del__(self):
        """Destructor to ensure tasks are properly closed."""
        self.stop()