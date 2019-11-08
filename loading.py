import numpy as np
import struct
import matplotlib.pyplot as plt

# ѵ�����ļ�
train_images_idx3_ubyte_file = 'MNIST_data/train-images.idx3-ubyte'
# ѵ������ǩ�ļ�
train_labels_idx1_ubyte_file = 'MNIST_data/train-labels.idx1-ubyte'

# ���Լ��ļ�
test_images_idx3_ubyte_file = 'MNIST_data/t10k-images.idx3-ubyte'
# ���Լ���ǩ�ļ�
test_labels_idx1_ubyte_file = 'MNIST_data/t10k-labels.idx1-ubyte'


def decode_idx3_ubyte(idx3_ubyte_file):
    """
    ����idx3�ļ���ͨ�ú���
    :param idx3_ubyte_file: idx3�ļ�·��
    :return: ���ݼ�
    """
    # ��ȡ����������
    bin_data = open(idx3_ubyte_file, 'rb').read()

    # �����ļ�ͷ��Ϣ������Ϊħ����ͼƬ������ÿ��ͼƬ�ߡ�ÿ��ͼƬ��
    offset = 0
    fmt_header = '>iiii' #��Ϊ���ݽṹ��ǰ4�е��������Ͷ���32λ���ͣ����Բ���i��ʽ����������Ҫ��ȡǰ4�����ݣ�������Ҫ4��i�����Ǻ���ῴ����ǩ���У�ֻʹ��2��ii��
    magic_number, num_images, num_rows, num_cols = struct.unpack_from(fmt_header, bin_data, offset)
    print('ħ��:%d, ͼƬ����: %d��, ͼƬ��С: %d*%d' % (magic_number, num_images, num_rows, num_cols))

    # �������ݼ�
    image_size = num_rows * num_cols
    offset += struct.calcsize(fmt_header)  #��������ڻ����е�ָ��λ�ã���ǰ����ܵ����ݽṹ���Կ�������ȡ��ǰ4��֮��ָ��λ�ã���ƫ��λ��offset��ָ��0016��
    print(offset)
    fmt_image = '>' + str(image_size) + 'B'  #ͼ����������ֵ������Ϊunsigned char�ͣ���Ӧ��format��ʽΪB�����ﻹ�м���ͼ���С784����Ϊ�˶�ȡ784��B��ʽ���ݣ����û����ֻ���ȡһ��ֵ����һ��ͼ���е�һ������ֵ��
    print(fmt_image,offset,struct.calcsize(fmt_image))
    images = np.empty((num_images, num_rows, num_cols))
    #plt.figure()
    for i in range(num_images):
        if (i + 1) % 10000 == 0:
            print('�ѽ��� %d' % (i + 1) + '��')
            print(offset)
        images[i] = np.array(struct.unpack_from(fmt_image, bin_data, offset)).reshape((num_rows, num_cols))
        #print(images[i])
        offset += struct.calcsize(fmt_image)
#        plt.imshow(images[i],'gray')
#        plt.pause(0.00001)
#        plt.show()
    #plt.show()

    return images


def decode_idx1_ubyte(idx1_ubyte_file):
    """
    ����idx1�ļ���ͨ�ú���
    :param idx1_ubyte_file: idx1�ļ�·��
    :return: ���ݼ�
    """
    # ��ȡ����������
    bin_data = open(idx1_ubyte_file, 'rb').read()

    # �����ļ�ͷ��Ϣ������Ϊħ���ͱ�ǩ��
    offset = 0
    fmt_header = '>ii'
    magic_number, num_images = struct.unpack_from(fmt_header, bin_data, offset)
    print('ħ��:%d, ͼƬ����: %d��' % (magic_number, num_images))

    # �������ݼ�
    offset += struct.calcsize(fmt_header)
    fmt_image = '>B'
    labels = np.empty(num_images)
    for i in range(num_images):
        if (i + 1) % 10000 == 0:
            print ('�ѽ��� %d' % (i + 1) + '��')
        labels[i] = struct.unpack_from(fmt_image, bin_data, offset)[0]
        offset += struct.calcsize(fmt_image)
    return labels


def load_train_images(idx_ubyte_file=train_images_idx3_ubyte_file):
    """
    TRAINING SET IMAGE FILE (train-images-idx3-ubyte):
    [offset] [type]          [value]          [description]
    0000     32 bit integer  0x00000803(2051) magic number
    0004     32 bit integer  60000            number of images
    0008     32 bit integer  28               number of rows
    0012     32 bit integer  28               number of columns
    0016     unsigned byte   ??               pixel
    0017     unsigned byte   ??               pixel
    ........
    xxxx     unsigned byte   ??               pixel
    Pixels are organized row-wise. Pixel values are 0 to 255. 0 means background (white), 255 means foreground (black).

    :param idx_ubyte_file: idx�ļ�·��
    :return: n*row*colάnp.array����nΪͼƬ����
    """
    return decode_idx3_ubyte(idx_ubyte_file)


def load_train_labels(idx_ubyte_file=train_labels_idx1_ubyte_file):
    """
    TRAINING SET LABEL FILE (train-labels-idx1-ubyte):
    [offset] [type]          [value]          [description]
    0000     32 bit integer  0x00000801(2049) magic number (MSB first)
    0004     32 bit integer  60000            number of items
    0008     unsigned byte   ??               label
    0009     unsigned byte   ??               label
    ........
    xxxx     unsigned byte   ??               label
    The labels values are 0 to 9.

    :param idx_ubyte_file: idx�ļ�·��
    :return: n*1άnp.array����nΪͼƬ����
    """
    return decode_idx1_ubyte(idx_ubyte_file)


def load_test_images(idx_ubyte_file=test_images_idx3_ubyte_file):
    """
    TEST SET IMAGE FILE (t10k-images-idx3-ubyte):
    [offset] [type]          [value]          [description]
    0000     32 bit integer  0x00000803(2051) magic number
    0004     32 bit integer  10000            number of images
    0008     32 bit integer  28               number of rows
    0012     32 bit integer  28               number of columns
    0016     unsigned byte   ??               pixel
    0017     unsigned byte   ??               pixel
    ........
    xxxx     unsigned byte   ??               pixel
    Pixels are organized row-wise. Pixel values are 0 to 255. 0 means background (white), 255 means foreground (black).

    :param idx_ubyte_file: idx�ļ�·��
    :return: n*row*colάnp.array����nΪͼƬ����
    """
    return decode_idx3_ubyte(idx_ubyte_file)


def load_test_labels(idx_ubyte_file=test_labels_idx1_ubyte_file):
    """
    TEST SET LABEL FILE (t10k-labels-idx1-ubyte):
    [offset] [type]          [value]          [description]
    0000     32 bit integer  0x00000801(2049) magic number (MSB first)
    0004     32 bit integer  10000            number of items
    0008     unsigned byte   ??               label
    0009     unsigned byte   ??               label
    ........
    xxxx     unsigned byte   ??               label
    The labels values are 0 to 9.

    :param idx_ubyte_file: idx�ļ�·��
    :return: n*1άnp.array����nΪͼƬ����
    """
    return decode_idx1_ubyte(idx_ubyte_file)



if __name__ == '__main__':
    train_images = load_train_images()

    train_labels = load_train_labels()
    # test_images = load_test_images()
    # test_labels = load_test_labels()

    # �鿴ǰʮ�����ݼ����ǩ�Զ�ȡ�Ƿ���ȷ
    for i in range(10):
        print(train_labels[i])
        plt.imshow(train_images[i], cmap='gray')
        plt.pause(0.000001)
        plt.show()
