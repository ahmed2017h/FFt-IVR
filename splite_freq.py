import numpy as np
from scipy.io import wavfile

#دالة للتأكد من وجود التردد في المصفوفة
def isNumberInArray(array, number):
    offset = 5      #نسبة الخطأ
    for i in range(number - offset, number + offset):
        if i in array:
            return True
    return False
#dictionary تحتوي على ترددات المطلوب مرجعتها
DTMF_TABLE = {
    '1': [1209, 697],
    '2': [1336, 697],
    '3': [1477, 697],
    'A': [1633, 697],

    '4': [1209, 770],
    '5': [1336, 770],
    '6': [1477, 770],
    'B': [1633, 770],

    '7': [1209, 852],
    '8': [1336, 852],
    '9': [1477, 852],
    'C': [1633, 852],

    '*': [1209, 941],
    '0': [1336, 941],
    '#': [1477, 941],
    'D': [1633, 941],
} 
def main():
    # قراءة إشارة صوتية
    sample_rate, signal = wavfile.read('Ref_FREQ.wav')
    #sample_rate, signal = wavfile.read('target.wav')
    # إذا كانت الإشارة ثنائية القناة، تحويلها إلى أحادية القناة
    if signal.ndim > 1:
        signal = signal.mean(axis=1)

    # تطبيق تحويل فورييه السريع
    fft_spectrum = np.fft.fft(signal,20000)

    #تحويل المصفوفة من أرقام مركبة إلى أرقام صحيحة
    for i in range(len(fft_spectrum)):
            fft_spectrum[i] = int(np.absolute(fft_spectrum[i]))
    #حساب الحد الأدنى لتصفية أرقام تحويل فورييه       
    LowerBound = 20 * np.average(fft_spectrum)
    #avr = np.average(fft_spectrum)
    FilteredFrequencies = []
    #فلتر لتحديدالتردات الأكبر من الحد الأدنى
    for i in range(len(fft_spectrum)):
        if (fft_spectrum[i] > LowerBound):
            FilteredFrequencies.append(i)

    # طباعة  المفتاح المضغوط
    for char, frequency_pair in DTMF_TABLE.items():
        if (isNumberInArray(FilteredFrequencies, frequency_pair[0]) and
            isNumberInArray(FilteredFrequencies, frequency_pair[1])):
            print(FilteredFrequencies)
            #print(frequency_pair[0])
            #print(frequency_pair[1])
            print (f"Pressed key {char}")
if __name__ == "__main__":
    main()
# الترددات المهيمنة
#low_freq = frequencies[FilteredFrequencies[0]]
#high_freq = frequencies[FilteredFrequencies[1]]

# عرض النتائج
#print(f"Low Frequency: {FilteredFrequencies} Hz")
#print(f"High Frequency: {LowerBound} Hz")
