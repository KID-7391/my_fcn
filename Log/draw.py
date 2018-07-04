import cv2
from matplotlib import pyplot as plt
import numpy as np
import re

test_it = []
test_mean_iu = []
test_fwavacc = []
test_loss = []
train_loss = []
train_it = []

p_test_it = re.compile('Iteration \d* loss .*')
p_test_mean_iu = re.compile('Iteration \d* mean IU .*')
p_test_fwavacc = re.compile('Iteration \d* fwavacc .*')
p_train_it = re.compile('Iteration \d*, lr ')
p_train_loss = re.compile('Train net output #0: loss = .* \(')

file = open('caffe.log', 'r')
log = file.read()
file.close()

test_it_list = p_test_it.findall(log)
test_mean_iu_list = p_test_mean_iu.findall(log)
test_fwavacc_list = p_test_fwavacc.findall(log)
train_it_list = p_train_it.findall(log)
train_loss_list = p_train_loss.findall(log)

# print(test_fwavacc_list)
for i in range(len(train_it_list)):
    train_it.append(int(str.replace(train_it_list[i].split(' ')[1], ',', '')))
    train_loss.append(float(train_loss_list[i].split(' ')[6]))

for i in range(len(test_it_list)):
    test_it.append(int(test_it_list[i].split(' ')[1]))
    test_loss.append(float(test_it_list[i].split(' ')[3]))
    test_mean_iu.append(float(test_mean_iu_list[i].split(' ')[4]))
    test_fwavacc.append(float(test_fwavacc_list[i].split(' ')[3]))

# print(train_it)
# print(train_loss)

plt.subplot(2, 2, 1)
plt.title('train loss')
plt.plot(train_it, train_loss)
plt.subplot(2, 2, 2)
plt.title('test loss')
plt.plot(test_it, test_loss)
plt.subplot(2, 2, 3)
plt.title('test mean IU')
plt.plot(test_it, test_mean_iu)
plt.subplot(2, 2, 4)
plt.title('test fwavacc')
plt.plot(test_it, test_fwavacc)
plt.show()


# file_train = open('caffe.log.train', 'r')
# file_test = open('caffe.log.test', 'r')
#
# train = np.zeros(1010)
# test = np.zeros((50, 2))
#
# line = file_train.readline()
# i = 0
# x_train = []
# while True:
#     line = file_train.readline()
#     if line:
#         line = line.split()
#         if len(line) < 4:
#             break
#         it = line[0]
#         x_train.append(int(it))
#         train[i] = float(line[2])
#     else:
#         break
#     i += 1
#
# train = train[0:i]
# x_train = np.array(x_train, dtype=np.int32)
#
# line = file_test.readline()
# i = 0
# x_test = []
# while True:
#     line = file_test.readline()
#     if line:
#         line = line.split()
#         if len(line) < 4:
#             break
#         it = line[0]
#         x_test.append(int(it))
#         test[i, 0] = float(line[3])
#         test[i, 1] = float(line[2])
#     else:
#         break
#     i += 1
#
# test = test[0:i]
# x_test = np.array(x_test, dtype=np.int32)
#
#
# plt.subplot(2, 2, 1)
# plt.title('train loss')
# plt.plot(x_train, train)
# plt.subplot(2, 2, 3)
# plt.title('test loss')
# plt.plot(x_test, test[:, 0])
# plt.subplot(2, 2, 4)
# plt.title('test acc')
# plt.plot(x_test, test[:, 1])
# plt.show()
