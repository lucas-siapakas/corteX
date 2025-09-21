def validate_parameters(frequency, amplitude, duration, sample_rate):
    """
    Validate waveform parameters.
    
    Args:
        frequency (float): Frequency in Hz
        amplitude (float): Amplitude in volts
        duration (float): Duration in seconds
        sample_rate (int): Samples per second
        
    Raises:
        ValueError: If any parameter is invalid
    """
    if frequency <= 0:
        raise ValueError("Frequency must be positive")
    if amplitude <= 0:
        raise ValueError("Amplitude must be positive")
    if duration <= 0:
        raise ValueError("Duration must be positive")
    if sample_rate <= 0:
        raise ValueError("Sample rate must be positive")
    if frequency * 2 > sample_rate:
        raise ValueError("Sample rate must be at least twice the frequency (Nyquist criterion)")

def calculate_buffer_size(duration, sample_rate):
    """
    Calculate the buffer size needed for a waveform.
    
    Args:
        duration (float): Duration in seconds
        sample_rate (int): Samples per second
        
    Returns:
        int: Buffer size in samples
    """
    return int(duration * sample_rate)