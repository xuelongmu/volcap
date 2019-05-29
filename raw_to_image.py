import numpy as np
import cv2
import glob, os
from pathlib import Path
# import PyCapture2 #not using this yet
imrows = 2048
imcols = 2448

imsize = imrows*imcols

infile = '/home/xuelong/Documents/Colmap_Projects/samsung_volcap/16375702/1.raw'

def read_uint12(data_chunk):
    data = np.frombuffer(data_chunk, dtype=np.uint8)
    fst_uint8, mid_uint8, lst_uint8 = np.reshape(data, (data.shape[0] // 3, 3)).astype(np.uint16).T
    fst_uint12 = ((mid_uint8 & 0x0F) << 8) | fst_uint8
    snd_uint12 = (lst_uint8 << 4) | ((mid_uint8 & 0xF0) >> 4)
    return np.reshape(np.concatenate((fst_uint12[:, None], snd_uint12[:, None]), axis=1), 2 * fst_uint12.shape[0])

# def read_uint12(data_chunk): #method to convert three 8-bit uints to two 12-bit uints.
#     data = np.frombuffer(data_chunk, dtype=np.uint8)
#     fst_uint8, mid_uint8, lst_uint8 = np.reshape(data, (data.shape[0] // 3, 3)).astype(np.uint16).T
#     fst_uint12 = (fst_uint8 << 4) + (mid_uint8 >> 4)
#     snd_uint12 = ((mid_uint8 % 16) << 8) + lst_uint8
#     return np.reshape(np.concatenate((fst_uint12[:, None], snd_uint12[:, None]), axis=1), 2 * fst_uint12.shape[0])

# def read_uint12(data_chunk):
#     data = np.frombuffer(data_chunk, dtype=np.uint8)
#     fst_uint8, mid_uint8, lst_uint8 = np.reshape(data, (data.shape[0] // 3, 3)).astype(np.uint16).T
#     fst_uint12 = (fst_uint8 << 4) + (mid_uint8 >> 4)
#     snd_uint12 = (lst_uint8 << 4) + (np.bitwise_and(15, mid_uint8))
#     return np.reshape (np.concatenate((fst_uint12[:, None], snd_uint12[:, None]), axis=1), 2 * fst_uint12.shape[0])

for file in Path('../mvrig3/').glob('**/*.raw'): # /media/xuelong/xue-intel-2/Colmap_Projects/samsung_volcap
    filepath = str(file)
    # print(str(filename))
    filepath_list = str(filepath).split('/') #[0:-1]
    print(filepath_list)
    filename = filepath_list[3].split('.')[0]
    print(filename)
    dirname = filepath_list[2]
    print(dirname)
    # file, path = splitPath(filename)
    # print('{} {}'.format(file, path))

# for x in range(1,60):
#     print(x)

#     infile = '/home/xuelong/Documents/Colmap_Projects/samsung_volcap/16375702/{}.raw'.format(str(x))

    with open(filepath, "rb") as rawimage:
        # print(rawimage.shape)
        f = np.fromfile(rawimage, np.dtype('uint8'), -1)
        print(f.shape)
        f12 = read_uint12(f)
        print(f12.shape)
        img16 = f12.reshape((imrows,imcols)) #np.array(f12.reshape((imrows,imcols)), dtype=np.uint16)

        scale_factor = 16.0
        img16 = np.int32(img16)     # convert to signed 32 bit integer to allow overflow
        img16 = scale_factor*img16  # apply scale factor
        img16 = np.clip(img16, 0, 65535) # force all values to be between 0 and 65535

        # after clip img2 is effectively unsigned 16 bit, but make it explicit:
        img16 = np.uint16(img16)
        # cv2.imshow('img16_gray', img16)

        # use the rg debayering algorithm
        color_rg = cv2.cvtColor(img16, cv2.COLOR_BAYER_RG2RGB)
        # cv2.imshow('color_rg',color_rg)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        cv2.imwrite('../converted_files/{}_{}.png'.format(filename,dirname),color_rg)



