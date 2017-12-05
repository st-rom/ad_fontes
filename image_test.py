from PIL import Image


def ad_pontes(img, ps):
    broken = False
    pixels = img.load()# create the pixel map
    pa = ps
    conts = [pa]
    position = 0
    cont_col = pixels[pa[0], pa[-1]]
    pcn1, position1 = search_nearest(pixels, pa, position)
    if position1 is None:
        return conts
    pcn2, position2 = search_nearest(pixels, pa, position, False)
    if pcn1 == pcn2:
        pcn = pcn1
        if pixels[pa[0], pa[-1]][0] + 1 != 256:
            pixels[pa[0], pa[-1]] = (pixels[pa[0], pa[-1]][0] + 1, pixels[pa[0], pa[-1]][1], pixels[pa[0], pa[-1]][2])
        else:
            pixels[pa[0], pa[-1]] = (pixels[pa[0], pa[-1]][0] - 1, pixels[pa[0], pa[-1]][1], pixels[pa[0], pa[-1]][2])
        broken = True
    else:
        pe = pa
        position = position1
        pa = pcn1
        conts.append(pa)
        if len(conts) == 2:
            print('qwq', conts, position)
    while True:
        if broken is False:
            position = (position + 6) % 8
            pcn, position = search_nearest(pixels, pa, position)
        if pcn is not None and pcn != pe and pcn not in conts and broken is False:
            pa = pcn
            conts.append(pa)
            if len(conts) == 2:
                print('dodod',conts)
        elif pcn is not None and pcn != pe and pcn in conts:
            conts.remove(pa)
            if pixels[pa[0], pa[-1]][0] + 1 != 256:
                pixels[pa[0], pa[-1]] = (pixels[pa[0], pa[-1]][0] + 1, pixels[pa[0], pa[-1]][1],
                                         pixels[pa[0], pa[-1]][2])
            else:
                pixels[pa[0], pa[-1]] = (pixels[pa[0], pa[-1]][0] - 1, pixels[pa[0], pa[-1]][1],
                                         pixels[pa[0], pa[-1]][2])
            pa = conts[-1]
            broken = False
        elif pcn is None or pcn == pe:
            new_img = Image.new('RGB', [img.size[0], img.size[1]], 'white')
            new_pixels = new_img.load()
            for i in conts:
                new_pixels[i[0], i[-1]] = cont_col
            new_img.show()
            return conts


def search_nearest(pixels, ps, d, way=True):
    st = d
    i = 0
    for b in range(d, d + 8):
        b %= 8
        if way is False:
            b = st - i
            if b < 0:
                b += 8
        contour_pixel = pixels[ps[0], ps[-1]]
        try:
            if b == 0 and pixels[ps[0] - 1, ps[-1] - 1] == contour_pixel:
                return [ps[0] - 1, ps[-1] - 1], b
        except IndexError:
            pass
        try:
            if b == 1 and pixels[ps[0], ps[-1] - 1] == contour_pixel:
                return [ps[0], ps[-1] - 1], b
        except IndexError:
            pass
        try:
            if b == 2 and pixels[ps[0] + 1, ps[-1] - 1] == contour_pixel:
                return [ps[0] + 1, ps[-1] - 1], b
        except IndexError:
            pass
        try:
            if b == 3 and pixels[ps[0] + 1, ps[-1]] == contour_pixel:
                return [ps[0] + 1, ps[-1]], b
        except IndexError:
            pass
        try:
            if b == 4 and pixels[ps[0] + 1, ps[-1] + 1] == contour_pixel:
                return [ps[0] + 1, ps[-1] + 1], b
        except IndexError:
            pass
        try:
            if b == 5 and pixels[ps[0], ps[-1] + 1] == contour_pixel:
                return [ps[0], ps[-1] + 1], b
        except IndexError:
            pass
        try:
            if b == 6 and pixels[ps[0] - 1, ps[-1] + 1] == contour_pixel:
                return [ps[0] - 1, ps[-1] + 1], b
        except IndexError:
            pass
        try:
            if b == 7 and pixels[ps[0] - 1, ps[-1]] == contour_pixel:
                return [ps[0] - 1, ps[-1]], b
        except IndexError:
            pass
        i += 1
    return None, None


#img = Image.open("C:/Users/voyo/Pictures/Screenshots/test.png")
#print(ad_pontes(img, [335, 129]))
#img = Image.open("C:/Users/voyo/Pictures/Screenshots/star_test.png")
#print(ad_pontes(img, [197, 92]))
#print(ad_pontes(img, [222, 97]))
img = Image.open("C:/Users/voyo/Pictures/Screenshots/disfigured_test.png")
print(ad_pontes(img, [187, 172]))

