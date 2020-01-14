import function 
import numpy as np 
from matplotlib import pyplot as plt 
import os

'''
    This method retrieves words before extension for given character.
'''
def RemoveCharactersBeforeExtension(char):
    chars = list(char)
    newChar = ''
    for char in chars:
        if char != '.':
            newChar = newChar + char
        else:
            break

    return newChar

'''
    Make list removed characters before extension for givne list.
'''
def MakeListRemovedBeforeExtension(fileList):
    newList = []
    for fileName in fileList:
        newList.append(RemoveCharactersBeforeExtension(fileName))

    return newList

def TransformToSpectrogram(filename):
    # ファイルパスの指定
    path = filename + '.wav'
    # wavファイルを読み込む
    data, samplerate = function.wavload(path)
    # 変形生成のための時間軸の作成
    x = np.arange(0, len(data)) / samplerate

    # Fsとoverlapでスペクトログラムの分解能を調整する。
    # フレームサイズ
    Fs = 4096
    # オーバーラップ率
    overlap = 90

    # オーバーラップ抽出された時間波形配列
    time_array, N_ave, final_time = function.ov(data, samplerate, Fs, overlap)

    # ハニング窓関数をかける
    time_array, acf = function.hanning(time_array, Fs, N_ave)

    # FFTをかける
    fft_array, fft_mean, fft_axis = function.fft_ave(time_array, samplerate, Fs, N_ave, acf)

    # スペクトログラムで縦軸を周波数、横軸を時間にするためにデータを転置
    fft_array = fft_array.T

    # ここからグラフ描写
    # グラフをオブジェクト指向で作成する。
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    # データをプロットする。
    im = ax1.imshow(fft_array, vmin = 0, vmax = 60, \
        extent = [0, final_time, 0, samplerate], aspect = 'auto', cmap = 'jet')

    """
    # カラーバーを設定する。
    cbar = fig.colorbar(im)
    cbar.set_label('SPL[dBA]')

    # 軸設定をする。
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Frequency [HZ]')
    """

    # スケールの設定をする。
    ax1.set_xticks(np.arange(0, 3, 1))
    ax1.set_yticks(np.arange(0, 10000, 10000))
    ax1.set_xlim(0, 3)
    ax1.set_ylim(0, 5000)

    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)

    # グラフを表示する。
    plt.close()

    fig.savefig('./../../spectrograms/bass/' + filename + '.png', bbox_inches='tight', pad_inches=0)

'''
    Main
'''
os.chdir('./../audio/bass')
originalFileNames = os.listdir()

fileNames = MakeListRemovedBeforeExtension(originalFileNames)
fileNames.sort()


for fileName in fileNames:
    TransformToSpectrogram(fileName)
