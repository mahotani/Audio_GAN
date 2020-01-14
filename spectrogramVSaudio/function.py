import numpy as np 
from scipy import signal
from scipy import fftpack
import soundfile as sf 

def wavload(path):
    data, samplerate = sf.read(path)
    return data, samplerate 

# オーバーラップ処理
def ov(data, samplerate, Fs, overlap):
    Ts = len(data) / samplerate
    Fc = Fs / samplerate
    x_ol = Fs * (1 - (overlap / 100))
    N_ave = int((Ts - (Fc * (overlap / 100))) / (Fc * (1 - (overlap / 100))))
    
    array = []

    for i in range(N_ave):
        ps = int(x_ol * i)
        array.append(data[ps:ps + Fs:1])
        final_time = (ps + Fs) / samplerate
    
    return array, N_ave, final_time

# 窓関数処理（ハニング窓）
def hanning(data_array, Fs, N_ave):
    han = signal.hann(Fs)
    acf = 1 / (sum(han) / Fs)

    # オーバーラップされた複数時間波形全てに窓関数をかける
    for i in range(N_ave):
        data_array[i] = data_array[i] * han
    
    return data_array, acf

# FFT処理
def fft_ave(data_array, samplerate, Fs, N_ave, acf):
    fft_array = []
    fft_axis = np.linspace(0, samplerate, Fs)
    a_scale = aweightings(fft_axis)

    # FFTをして配列にdBで追加、窓関数補正値をかけ、(Fs / 2)の正規化を実施。
    for i in range(N_ave):
        fft_array.append(db(acf * np.abs(fftpack.fft(data_array[i]) / (Fs / 2)), 2e-5))
    
    fft_array = np.array(fft_array) + a_scale
    fft_mean = np.mean(fft_array, axis=0)

    return fft_array, fft_mean, fft_axis

# リニア値からdBへ変換
def db(x, dBref):
    y = 20 * np.log10(x / dBref)
    return y

# dB値からリニア値へ変換
def idb(x, dBref):
    y = dBref * np.power(10, x / 20)
    return y

# 聴感補正（A特性カーブ)
def aweightings(f):
    if f[0] == 0:
        f[0] = 1
    else:
        pass

    ra = (np.power(12194, 2) * np.power(f, 4)) / \
         ((np.power(f, 2) + np.power(20.6, 2)) * \
          np.sqrt((np.power(f, 2) + np.power(107.7, 2)) * \
                  (np.power(f, 2) + np.power(737.9, 2))) * \
          (np.power(f, 2) + np.power(12194, 2)))
    a = 20 * np.log10(ra) + 2.00

    return a
