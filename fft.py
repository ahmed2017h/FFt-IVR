import cmath  # للدوال المعقدة (مثل exp و pi)

def fft(x):
    N = len(x)
    if N <= 1:
        return x

    # قسّم الإشارة إلى زوجي وفردي
    even = fft(x[0::2])
    odd = fft(x[1::2])

    # جذور الوحدة
    T = [cmath.exp(-2j * cmath.pi * k / N) * odd[k] for k in range(N // 2)]

    # دمج النتائج
    return [even[k] + T[k] for k in range(N // 2)] + \
           [even[k] - T[k] for k in range(N // 2)]
# سلسلة بسيطة
x = [0, 1, 2, 3]

# تحويل FFT يدوي
X_manual = fft(x)

# تحويل باستخدام numpy للمقارنة
import numpy as np
X_numpy = np.fft.fft(x)

# طباعة النتائج
print("النتيجة اليدوية:")
for val in X_manual:
    print(val)

print("\nالنتيجة باستخدام numpy:")
for val in X_numpy:
    print(val)
