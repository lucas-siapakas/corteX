import numpy as np

class WaveformGenerator:
    @staticmethod
    def generate_sine(frequency, amplitude, duration, sample_rate=1000):
        """
        Generate a sine wave.
        
        Args:
            frequency (float): Frequency of the wave in Hz
            amplitude (float): Peak amplitude of the wave in volts
            duration (float): Duration of the wave in seconds
            sample_rate (int): Number of samples per second
            
        Returns:
            tuple: (time_points, waveform)
        """
        t = np.linspace(0, duration, int(duration * sample_rate))
        wave = amplitude * np.sin(2 * np.pi * frequency * t)
        return t, wave

    @staticmethod
    def generate_square(frequency, amplitude, duration, sample_rate=1000):
        """
        Generate a square wave.
        
        Args:
            frequency (float): Frequency of the wave in Hz
            amplitude (float): Peak amplitude of the wave in volts
            duration (float): Duration of the wave in seconds
            sample_rate (int): Number of samples per second
            
        Returns:
            tuple: (time_points, waveform)
        """
        t = np.linspace(0, duration, int(duration * sample_rate))
        wave = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
        return t, wave

    @staticmethod
    def generate_triangle(frequency, amplitude, duration, sample_rate=1000):
        """
        Generate a triangle wave.
        
        Args:
            frequency (float): Frequency of the wave in Hz
            amplitude (float): Peak amplitude of the wave in volts
            duration (float): Duration of the wave in seconds
            sample_rate (int): Number of samples per second
            
        Returns:
            tuple: (time_points, waveform)
        """
        t = np.linspace(0, duration, int(duration * sample_rate))
        wave = amplitude * (2 * np.abs(2 * (frequency * t - np.floor(0.5 + frequency * t))) - 1)
        return t, wave
        
    @staticmethod
    def generate_sawtooth(frequency, amplitude, duration, sample_rate=1000):
        """
        Generate a sawtooth wave.
        
        Args:
            frequency (float): Frequency of the wave in Hz
            amplitude (float): Peak amplitude of the wave in volts
            duration (float): Duration of the wave in seconds
            sample_rate (int): Number of samples per second
            
        Returns:
            tuple: (time_points, waveform)
        """
        t = np.linspace(0, duration, int(duration * sample_rate))
        wave = amplitude * (2 * (frequency * t - np.floor(0.5 + frequency * t)))
        return t, wave