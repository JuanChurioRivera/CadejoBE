import matplotlib.pyplot as plt
import numpy as np

def smooth_signal(signal: list[float], timestamps, n_coeffs: int = 10):
    """ Takes a single dimensional array of magnitude made of SleepEvent (x,y,z) """
    
    plt.plot(signal)
    plt.show()
    
    fft = np.fft.rfft(signal)
    
    fft_filtered = np.zeros_like(fft)
    fft_filtered[:n_coeffs] = fft[:n_coeffs]
    
    ifft = np.fft.irfft(fft_filtered, n=len(signal))
    
    plt.plot(timestamps, ifft)
    plt.show()
    
    return ifft
