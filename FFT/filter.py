import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack

'''
TODO:
http://stackoverflow.com/questions/19122157/fft-bandpass-filter-in-python
http://stackoverflow.com/questions/20618804/how-to-smooth-a-curve-in-the-right-way
'''



x = np.arange(0,2*np.pi,0.05)
signal_theory = np.sin(2*x)
noise = np.random.normal(0, 0.1, len(signal_theory))
signal_noisy = signal_theory + noise


W = fftpack.fftfreq(signal_noisy.size, d=x[1]-x[0])
f_signal = fftpack.rfft(signal_noisy)

# If our original signal time was in seconds, this is now in Hz
cut_f_signal = f_signal.copy()
cut_f_signal[(W<6)] = 0
cut_signal = fftpack.irfft(cut_f_signal)


plt.subplot(221)
plt.plot(x,signal_theory)
plt.plot(x,signal_noisy)

plt.subplot(222)

plt.subplot(223)
plt.plot(W,cut_f_signal)
plt.xlim(0,10)
plt.subplot(224)
plt.plot(x,cut_signal)

plt.show()
