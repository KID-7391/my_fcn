import sys
sys.path.append('/home/wen/caffe-master/python')
import caffe
import surgery, score

import numpy as np
import os

caffe_root = '/home/wen/caffe-master'  # caffe的根目录

try:
    import setproctitle
    setproctitle.setproctitle(os.path.basename(os.getcwd()))
except:
    pass

weights = '/home/wen/caffe-master/semantic/fcn/my_fcn32s/fcn32s-heavy-pascal.caffemodel'

# ini
# caffe.set_device(int(sys.argv[1]))
caffe.set_mode_gpu()

solver = caffe.SGDSolver('/home/wen/caffe-master/semantic/fcn/my_fcn32s/solver.prototxt')
solver.net.copy_from(weights)

# surgeries
interp_layers = [k for k in solver.net.params.keys() if 'up' in k]
surgery.interp(solver.net, interp_layers)

# scoring
val = np.loadtxt('/home/wen/caffe-master/semantic/fcn/data/pascal/segvalid11.txt', dtype=str)

for _ in range(20):
    solver.step(500)
    score.seg_tests(solver, False, val, layer='score')
