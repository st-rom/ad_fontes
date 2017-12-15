import tkinter.filedialog
from PIL import Image, ImageTk
from sys import argv
import numpy as np
import cv2
import os
import time


def ad_fontes(img, ps, ran=35, steps=False, bg_search=False):
    if bg_search is False:
        ran = int(argv[1]) if len(argv) >= 2 and argv[1] != 'test' and argv[1] != 'save' and argv[1] != 'steps' else ran
    steps = True if len(argv) >= 2 and 'steps' in argv else steps
    pixels = img.load()     # create the pixel map
    bgs = []        # list of contour color pixels which are background og object
    pa = ps
    conts = [pa]        # list of contour pixels
    position = 0  # position of nearest contour pixel(out of 8)
    pcn1, position1 = search_nearest(pixels, pa, position, bgs, ran)
    if position1 is None:
        return conts
    pcn2, position2 = search_nearest(pixels, pa, position, bgs, ran, False)
    while pcn1 == pcn2:
        conts.remove(pa)
        bgs.append(pa)
        pa = pcn1
        conts.append(pa)
        pcn1, position1 = search_nearest(pixels, pa, position, bgs, ran)
        if position1 is None:
            return conts
        pcn2, position2 = search_nearest(pixels, pa, position, bgs, ran, False)
    pe = pa
    if bg_search is True:
        return pixels[pe[0] - 1, pe[1] - 1]
    position = position1
    pa = pcn1
    conts.append(pa)
    while True:
        if len(conts) % 200 == 0 and steps is True:
            new_img = Image.new('RGB', [img.size[0], img.size[1]], 'white')
            new_pixels = new_img.load()
            for i in conts:
                new_pixels[i[0], i[-1]] = (0, 0, 0)
            new_img.show()
        position = (position + 6) % 8
        old_pos = position
        pcn, position = search_nearest(pixels, pa, position, bgs, ran)
        if pcn is not None and pcn != pe and pcn not in conts:
            pa = pcn
            conts.append(pa)
        elif pcn is not None and pcn != pe and pcn in conts:
            bgs.append(pcn)
            position = old_pos
        elif pcn == pe or len(conts) == 0:
            new_img = Image.new('RGB', [img.size[0], img.size[1]], 'white')
            new_pixels = new_img.load()
            for i in conts:
                new_pixels[i[0], i[-1]] = (0, 0, 0)
            new_img.show()
            if len(argv) >= 2 and 'save' in argv:
                new_img.save("ad_fontes_contour.jpg")
            return conts
        elif pcn is None:
            conts.remove(pa)
            bgs.append(pa)
            pa = conts[-1]
            position = old_pos


def search_nearest(pixels, ps, d, bgs, ran=10, way=True):
    st = d  # saving position in case way is false(loop goes the other way around)
    i = 0
    coords = {0: [-1, -1], 1: [0, -1], 2: [1, -1], 3: [1, 0], 4: [1, 1], 5: [0, 1], 6: [-1, 1], 7: [-1, 0]}
    for b in range(d, d + 8):
        b %= 8
        if way is False:
            b = st - i
            if b < 0:
                b += 8
        e = exc(coords[b][0], coords[b][-1], pixels, ps, bgs, ran)      # next contour pixel
        if e is not None:
            return e, b
        i += 1
    return None, None


def exc(n, m, pixels, ps, bgs, ran=10):
    contour_pixel = pixels[ps[0], ps[-1]]
    try:
        if contour_pixel[0] - ran <= pixels[ps[0] + n,
                                            ps[-1] + m][0] <= contour_pixel[0] + ran and \
                                        contour_pixel[1] - ran <= pixels[ps[0] + n,
                                                                         ps[-1] + m][1] <= contour_pixel[1] + ran and\
                                        contour_pixel[2] - ran <= pixels[ps[0] + n,
                                                                         ps[-1] + m][2] <= contour_pixel[2] + ran and\
                        [ps[0] + n, ps[-1] + m] not in bgs:
            return [ps[0] + n, ps[-1] + m]
    except IndexError:
        return None


def callback(event):
    global ps
    print("Starting pixel of object is: ", event.x, event.y)
    ps[0] = event.x
    ps[1] = event.y
    root.title('Choose starting pixel -- ' + str(ps))


def watershed(im2r, bg_color):
    global root
    img = cv2.imread(im2r)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    ret, markers = cv2.connectedComponents(sure_fg)
    markers += 1
    markers[unknown == 255] = 0
    markers = cv2.watershed(img, markers)
    this_color = [0, 0, 0]
    for i in range(3):
        if bg_color[i] < 128:
            this_color[i] = 255
        else:
            this_color[i] = 0
    this_color.reverse()
    img[markers == -1] = this_color
    name = im2r[:-4] + '_temp' + im2r[-4:]
    cv2.imwrite(name, img)
    return name


def test():
    images = ["hm.png", "test_algo.jpg", "planet.png", "glasses.jpg"]
    ps_pixels = [[215, 119], [223, 230], [188, 165], [436, 238]]
    for i in range(len(images)):
        starting_time = time.time()
        image = images[i]
        img = Image.open(image)
        cont_col = ad_fontes(img, ps_pixels[i], bg_search=True)
        temp_im = watershed(image, cont_col)
        img = Image.open(temp_im)
        print('Number of contour pixels: ', len(ad_fontes(img, ps_pixels[i])))
        os.remove(temp_im)
        print('Time of execution: ', round(time.time() - starting_time, 2), )


if __name__ == '__main__':
    if len(argv) >= 2 and 'test' in argv:
        test()
    else:
        starting_time = time.time()
        root = tkinter.Tk()
        width, height = root.winfo_screenwidth(), root.winfo_screenheight()
        root.withdraw()
        image = tkinter.filedialog.askopenfilename()
        ps = [0, 0]
        img = Image.open(image)
        img = img.resize((img.size[0] // 2, img.size[1] // 2) if img.size[0] > width or img.size[1] > height else
                         (img.size[0], img.size[1]), Image.ANTIALIAS)
        pixels = img.load()
        image_tk = ImageTk.PhotoImage(img)
        root.deiconify()
        canvas = tkinter.Canvas(root, width=img.size[0], height=img.size[1])
        canvas.pack()
        canvas.create_image(img.size[0] // 2, img.size[1] // 2, image=image_tk)
        canvas.bind("<Button-1>", callback)
        tkinter.mainloop()
        cont_col = ad_fontes(img, ps, 60, bg_search=True)
        temp_im = watershed(image, cont_col)
        img = Image.open(temp_im)
        img.show()
        print('Number of contour pixels: ', len(ad_fontes(img, ps)))
        os.remove(temp_im)
        print('Time of execution: ', round(time.time() - starting_time, 2))
