import caffe
from caffe import layers as L, params as P, to_proto
from caffe.coord_map import crop
import tools

def conv_relu(bottom, nout, ks=3, stride=1, pad=1):
    conv = L.Convolution(bottom,
                         kernel_size=ks,
                         stride=stride,
                         num_output=nout,
                         pad=pad,
                         bias_term=True,
                         weight_filler=dict(type='xavier'),
                         bias_filler=dict(type='constant'),
                         param=[dict(lr_mult=1, decay_mult=1),
                                dict(lr_mult=2, decay_mult=0)]
                         )

    return conv, L.ReLU(conv, in_place=True)

def max_pool(bottom, ks=2, stride=2):
    return L.Pooling(bottom, pool=P.Pooling.MAX, kernel_size=ks, stride=stride)

def fcn(split):
    n = caffe.NetSpec()
    pydata_params = dict(split=split, mean=(104.00699, 116.66877, 122.67892), seed=1337)

    if split == 'train':
        pydata_params['sbdd_dir'] = '/home/wen/caffe-master/semantic/fcn/data/sbdd/benchmark/benchmark_RELEASE/dataset'
        pylayer = 'SBDDSegDataLayer'
    else:
        pydata_params['voc_dir'] = '/home/wen/caffe-master/semantic/fcn/data/pascal/VOC2012'
        pylayer = 'VOCSegDataLayer'
    n.data, n.label = L.Python(module='voc_layers',
                               layer=pylayer,
                               ntop=2,
                               param_str=str(pydata_params)
                               )

    n.conv1_1, n.relu1_1 = conv_relu(n.data, 16*4, pad=10)
    n.conv1_2, n.relu1_2 = conv_relu(n.relu1_1, 16*4)
    n.pool1 = max_pool(n.relu1_2)

    n.conv2_1, n.relu2_1 = conv_relu(n.pool1, 32*4)
    n.conv2_2, n.relu2_2 = conv_relu(n.relu2_1, 32*4)
    n.pool2 = max_pool(n.relu2_2)

    n.conv3_1, n.relu3_1 = conv_relu(n.pool2, 64*4)
    n.conv3_2, n.relu3_2 = conv_relu(n.relu3_1, 64*4)
    n.conv3_3, n.relu3_3 = conv_relu(n.relu3_2, 64*4)
    n.pool3 = max_pool(n.relu3_3)

    n.conv4_1, n.relu4_1 = conv_relu(n.pool3, 128*4)
    n.conv4_2, n.relu4_2 = conv_relu(n.relu4_1, 128*4)
    n.conv4_3, n.relu4_3 = conv_relu(n.relu4_2, 128*4)
    n.pool4 = max_pool(n.relu4_3)

    n.conv5_1, n.relu5_1 = conv_relu(n.pool4, 128*4)
    n.conv5_2, n.relu5_2 = conv_relu(n.relu5_1, 128*4)
    n.conv5_3, n.relu5_3 = conv_relu(n.relu5_2, 128*4)
    n.pool5 = max_pool(n.relu5_3)


    n.fc6_new, n.relu6 = conv_relu(n.pool5, 1024, ks=3, pad=0)
    n.drop6 = L.Dropout(n.relu6, dropout_ratio=0.5, in_place=True)
    n.fc7_new, n.relu7 = conv_relu(n.drop6, 1024, ks=1, pad=0)
    n.drop7 = L.Dropout(n.relu7, dropout_ratio=0.5, in_place=True)

    n.score_fr_new = L.Convolution(n.drop7,
                               num_output=21,
                               kernel_size=1,
                               pad=0,
                               weight_filler=dict(type='xavier'),
                               bias_filler=dict(type='constant'),
                               param=[dict(lr_mult=1, decay_mult=1),
                                      dict(lr_mult=2, decay_mult=0)
                                      ]
                               )

    n.upscore_new = L.Deconvolution(n.score_fr_new,
                               convolution_param=dict(num_output=21,
                                                      kernel_size=128,
                                                      stride=8,
                                                      bias_term=False,
                                                      ),
                               param=[dict(lr_mult=0)]
                               )

    n.score = L.Crop(n.upscore_new, n.data)
    n.loss = L.SoftmaxWithLoss(n.score,
                               n.label,
                               loss_param=dict(normalize=False, ignore_label=255)
                               )

    return n.to_proto()



def make_net():
    with open('train.prototxt', 'w') as f:
        f.write(str(fcn('train')))

    with open('val.prototxt', 'w') as f:
        f.write(str(fcn('seg11valid')))

if __name__ == '__main__':
    make_net()
    solver_path = '/home/wen/caffe-master/semantic/fcn/my_fcn32s/solver.prototxt'
    solver_prototxt = tools.CaffeSolver()
    solver_prototxt.write(solver_path)
