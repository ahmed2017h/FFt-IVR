import pyaudio
import wave
import numpy as np
import os
from scipy.io import wavfile
#pip install pyaudio
#pip install numpy
# إعدادات التسجيل
FORMAT = pyaudio.paInt16
CHANNELS = 1  # قناة واحدة (مونو)
RATE = 20000
CHUNK = 1024
RECORD_SECONDS = 2  # مدة التسجيل بالثواني
#TARGET_FREQ = 1000  # التردد المطلوب بالكيلوهرتز
def recorde(OUTPUT_FILENAME):
    # إنشاء كائن PyAudio
    audio = pyaudio.PyAudio()

    # بدء التسجيل
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")
    input()
    # إيقاف التسجيل
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # حفظ الصوت إلى ملف WAV
    wf = wave.open(OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# تحليل الترددات في الصوت المسجل
def analyze_frequency(data, rate):
    numpy_data = np.frombuffer(data, dtype=np.int16)
    
    # تطبيق FFT على البيانات الصوتية
    fft_result = np.fft.fft(numpy_data)
    fft_freq = np.fft.fftfreq(len(fft_result), 1.0 / rate)
    #print(f"fft_freq= {fft_freq[np.argsort(np.abs(fft_result))]}")
    #print(f"fft_result= {int(np.abs(fft_result[1]))}")
    # البحث عن التردد الأعظم في الطيف
    peak_freq = np.abs(fft_freq[np.argmax(np.abs(fft_result))])
    
    return peak_freq
def detect(OUTPUT_FILENAME,TARGET_FREQ):
    # فتح ملف الصوت وتحليل التردد
    with wave.open(OUTPUT_FILENAME, 'rb') as wf:
        frames = wf.readframes(wf.getnframes())
        peak_frequency = analyze_frequency(frames, RATE)

    print(f"Peak frequency detected: {peak_frequency} Hz")

    if abs(peak_frequency - TARGET_FREQ) < 1:  # سماحية ±5 هرتز
        print(f"Target frequency {TARGET_FREQ} Hz detected!")
        #os.startfile(r'c:/')
    else:
        print(f"Target frequency {TARGET_FREQ} Hz not detected.")


if __name__ == "__main__":
    sel =int(input("Choose [1]Refrance record [2] detect ? [1,2]"))
    ref_file="Ref_FREQ.wav"
    if sel == 1:
        recorde(ref_file)
        with wave.open("Ref_FREQ.wav", 'rb') as wf:
            frames = wf.readframes(wf.getnframes())
            TARGET_FREQ = analyze_frequency(frames, RATE)
        print(f"Target frequency {TARGET_FREQ} HZ")
    elif sel == 2:
        OUTPUT_FILENAME="target.wav"
        recorde(OUTPUT_FILENAME)
        with wave.open("Ref_FREQ.wav", 'rb') as wf:
            frames = wf.readframes(wf.getnframes())
            TARGET_FREQ = analyze_frequency(frames, RATE)
        
        detect("target.wav",TARGET_FREQ)
    else:
        print("Your answer 1 or 2")