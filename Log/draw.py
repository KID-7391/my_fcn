import cv2
from matplotlib import pyplot as plt
import numpy as np


file_train = open('caffe.log.train', 'r')
file_test = open('caffe.log.test', 'r')

train = np.zeros(1010)
test = np.zeros((50, 2))

line = file_train.readline()
i = 0
x_train = []
while True:
    line = file_train.readline()
    if line:
        line = line.split()
        if len(line) < 4:
            break
        it = line[0]
        x_train.append(int(it))
        train[i] = float(line[2])
    else:
        break
    i += 1

train = train[0:i]
x_train = np.array(x_train, dtype=np.int32)

line = file_test.readline()
i = 0
x_test = []
while True:
    line = file_test.readline()
    if line:
        line = line.split()
        if len(line) < 4:
            break
        it = line[0]
        x_test.append(int(it))
        test[i, 0] = float(line[3])
        test[i, 1] = float(line[2])
    else:
        break
    i += 1

test = test[0:i]
x_test = np.array(x_test, dtype=np.int32)


plt.subplot(2, 2, 1)
plt.title('train loss')
plt.plot(x_train, train)
plt.subplot(2, 2, 3)
plt.title('test loss')
plt.plot(x_test, test[:, 0])
plt.subplot(2, 2, 4)
plt.title('test acc')
plt.plot(x_test, test[:, 1])
plt.show()
