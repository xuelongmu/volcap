import numpy as np
import cv2
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
#     return np.reshape(np.concatenate((fst_uint12[:, None], snd_uint12[:, None]), axis=1), 2 * fst_uint12.shape[0])


for x in range(1,60):
    print(x)
    infile = '/home/xuelong/Documents/Colmap_Projects/samsung_volcap/16375702/{}.raw'.format(str(x))

    with open(infile, "rb") as rawimage:
        # print(rawimage.shape)
        f = np.fromfile(rawimage, np.dtype('uint8'), -1)
        print(f.shape)
        f12 = read_uint12(f)
        print(f12.shape)
        img16 = f12.reshape((imrows,imcols)) #np.array(f12.reshape((imrows,imcols)), dtype=np.uint16)

        # img8 = np.array(img12, dtype=np.uint8) #coerce and display in 8 bit, sanity check
        # cv2.imshow('img8_gray', img8)

        # #try each debayering algorithm in 8bit
        # color_bg_8bit = cv2.cvtColor(img8, cv2.COLOR_BAYER_BG2RGB) 
        # cv2.imshow('color_bg_8bit',color_bg_8bit)
        # color_gb_8bit = cv2.cvtColor(img8, cv2.COLOR_BAYER_GB2RGB) 
        # cv2.imshow('color_gb_8bit',color_gb_8bit)
        # color_rg_8bit = cv2.cvtColor(img8, cv2.COLOR_BAYER_RG2RGB) 
        # cv2.imshow('color_rg_8bit',color_rg_8bit)
        # color_gr_8bit = cv2.cvtColor(img8, cv2.COLOR_BAYER_GR2RGB) 
        # cv2.imshow('color_gr_8bit',color_gr_8bit)

        scale_factor = 16.0
        img16 = np.int32(img16)     # convert to signed 32 bit integer to allow overflow
        img16 = scale_factor*img16  # apply scale factor
        img16 = np.clip(img16, 0, 65535) # force all values to be between 0 and 65535

        # after clip img2 is effectively unsigned 16 bit, but make it explicit:
        img16 = np.uint16(img16)
        cv2.imshow('img16_gray', img16)

        # try each debayering algorithm in 16 bit
        color_bg = cv2.cvtColor(img16, cv2.COLOR_BAYER_BG2RGB)
        cv2.imshow('color_bg',color_bg) #np.array(color, dtype=np.uint8)
        color_gb = cv2.cvtColor(img16, cv2.COLOR_BAYER_GB2RGB)
        cv2.imshow('color_gb',color_gb)
        color_rg = cv2.cvtColor(img16, cv2.COLOR_BAYER_RG2RGB)
        cv2.imshow('color_rg',color_rg)
        color_gr = cv2.cvtColor(img16, cv2.COLOR_BAYER_GR2RGB)
        cv2.imshow('color_gr',color_gr)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        #save all to disk in working folder
        # cv2.imwrite('img8_gray.bmp', img8)
        # cv2.imwrite('color_bg_8bit.bmp', color_bg_8bit)
        # cv2.imwrite('color_gb_8bit.bmp', color_gb_8bit)
        # cv2.imwrite('color_rg_8bit.bmp', color_rg_8bit)
        # cv2.imwrite('color_gr_8bit.bmp', color_gr_8bit)

        cv2.imwrite('img16_gray.png', img16)
        cv2.imwrite('color_bg.png',color_bg)
        cv2.imwrite('color_gb.png',color_gb)
        cv2.imwrite('color_rg.png',color_rg)
        cv2.imwrite('color_gr.png',color_gr)




