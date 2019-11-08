import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
#��׼��Ϊ0.1����̬�ֲ�
def weight_variable(shape):
    initial = tf.truncated_normal(shape,stddev=0.1)
    return tf.Variable(initial)

#0.1��ƫ�����Ϊ�˱��������ڵ�
def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

#��ά�������
#strides������ģ���ƶ��Ĳ�����ȫ��1�����߹����е�ֵ
#padding��ΪSAME��˼�Ǳ�����������Ĵ�Сһ����ʹ��ȫ0����
def conv2d(x,W):
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')

#ksize [1, height, width, 1] ��һ�������һ�������batches��channel���ػ���1�����ػ�
#strides [1, stride,stride, 1]��˼�ǲ���Ϊ2������ʹ�õ����ػ�
def max_pool_2x2(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1], strides=[1,2,2,1],padding='SAME')