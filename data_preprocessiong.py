import cv2
import numpy as np
import os

# path = '/home/wen/caffe-master/semantic/fcn/data/sbdd/benchmark/benchmark_RELEASE/dataset/'
input_path = ['/home/wen/caffe-master/semantic/fcn/data/pascal/VOC2012/SegmentationClass0/',
              '/home/wen/caffe-master/semantic/fcn/data/pascal/VOC2012/JPEGImages0/',
              '/home/wen/caffe-master/semantic/fcn/data/sbdd/benchmark/benchmark_RELEASE/dataset/cls0',
              '/home/wen/caffe-master/semantic/fcn/data/sbdd/benchmark/benchmark_RELEASE/dataset/img0'
              ]
output_path = ['/home/wen/caffe-master/semantic/fcn/data/pascal/VOC2012/SegmentationClass/',
               '/home/wen/caffe-master/semantic/fcn/data/pascal/VOC2012/JPEGImages/',
               '/home/wen/caffe-master/semantic/fcn/data/sbdd/benchmark/benchmark_RELEASE/dataset/cls',
               '/home/wen/caffe-master/semantic/fcn/data/sbdd/benchmark/benchmark_RELEASE/dataset/img'
               ]

file_list = ['/home/wen/caffe-master/semantic/fcn/data/pascal/segvalid11.txt',
             '/home/wen/caffe-master/semantic/fcn/data/sbdd/benchmark/benchmark_RELEASE/dataset/train.txt'
             ]
f = open('/home/wen/caffe-master/semantic/fcn/data/pascal/segvalid11.txt', 'r')
file = f.read().split('\n')

for i in range(4):
    ip = input_path[i]
    op = output_path[i]
    f = open(file_list[int(i/2)], 'r')
    file = f.read().split('\n')

    if i %2 == 1:
        for j in file:
            img = cv2.imread(ip + i + '.jpg')
            img = cv2.resize(img, (256, 256), interpolation=cv2.INTER_NEAREST)
            cv2.imwrite(op + i + '.jpg', img)
    else:
        for j in file:
            img = cv2.imread(ip + i + '.png')
            img = cv2.resize(img, (256, 256), interpolation=cv2.INTER_NEAREST)
            cv2.imwrite(op + i + '.png', img)
# for i in file:
#     print(i)
#     img = cv2.imread(input_path + i + '.png')
#     img = cv2.resize(img, (128, 128), interpolation=cv2.INTER_NEAREST)
#     cv2.imwrite(output_path + i + '.png', img)
