from PIL import Image


def ad_pontes(img, ps):
    pixels = img.load()#  create the pixel map
    bgs = []
    pa = ps
    conts = [pa]
    position = 0
    cont_col = pixels[pa[0], pa[-1]]
    pcn1, position1 = search_nearest(pixels, pa, position, bgs)
    if position1 is None:
        return conts
    pcn2, position2 = search_nearest(pixels, pa, position, bgs, False)
    while pcn1 == pcn2:
        conts.remove(pa)
        bgs.append(pa)
        pa = pcn1
        conts.append(pa)
        pcn1, position1 = search_nearest(pixels, pa, position, bgs)
        if position1 is None:
            return conts
        pcn2, position2 = search_nearest(pixels, pa, position, bgs, False)
    #if pcn1 == pcn2:
    #    pcn = pcn1
    #    bgs.append(pa)
    #    broken = True
    pe = pa
    position = position1
    pa = pcn1
    conts.append(pa)
    #print('poo', )
    while True:
        #print(len(conts), conts)
        #print(pixels[conts[-1][0], conts[-1][-1]])
        #if len(conts) % 200 == 0:
        #    new_img = Image.new('RGB', [img.size[0], img.size[1]], 'white')
        #    new_pixels = new_img.load()
        #    for i in conts:
        #        new_pixels[i[0], i[-1]] = cont_col
        #    new_img.show()
        position = (position + 6) % 8
        pcn, position = search_nearest(pixels, pa, position, bgs)
        if pcn is not None and pcn != pe and pcn not in conts:
            pa = pcn
            conts.append(pa)
        elif pcn is not None and pcn != pe and pcn in conts:
            conts.remove(pa)
            bgs.append(pa)
            pa = conts[-1]
        elif pcn is None or pcn == pe:
            new_img = Image.new('RGB', [img.size[0], img.size[1]], 'white')
            new_pixels = new_img.load()
            for i in conts:
                new_pixels[i[0], i[-1]] = cont_col
            new_img.show()
            return conts


def search_nearest(pixels, ps, d, bgs, way=True):
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
            #if b == 0 and pixels[ps[0] - 1, ps[-1] - 1] == contour_pixel and [ps[0] - 1, ps[-1] - 1] not in bgs:
            if b == 0 and contour_pixel[0] - 10 <= pixels[ps[0] - 1, ps[-1] - 1][0] <= contour_pixel[0] + 10 and\
                                            contour_pixel[1] - 10 <= pixels[ps[0] - 1, ps[-1] - 1][1]\
                            <= contour_pixel[1] + 10 and contour_pixel[2] - 10 <= pixels[ps[0] - 1, ps[-1] - 1][2]\
                    <= contour_pixel[2] + 10 and [ps[0] - 1, ps[-1] - 1] not in bgs:
                return [ps[0] - 1, ps[-1] - 1], b
        except IndexError:
            pass
        try:
            if b == 1 and contour_pixel[0] - 10 <= pixels[ps[0], ps[-1] - 1][0] <= contour_pixel[0] + 10 and\
                                            contour_pixel[1] - 10 <= pixels[ps[0], ps[-1] - 1][1]\
                            <= contour_pixel[1] + 10 and contour_pixel[2] - 10 <= pixels[ps[0], ps[-1] - 1][2]\
                    <= contour_pixel[2] + 10 and [ps[0], ps[-1] - 1] not in bgs:
                return [ps[0], ps[-1] - 1], b
        except IndexError:
            pass
        try:
            if b == 2 and contour_pixel[0] - 10 <= pixels[ps[0] + 1, ps[-1] - 1][0] <= contour_pixel[0] + 10 and\
                                            contour_pixel[1] - 10 <= pixels[ps[0] + 1, ps[-1] - 1][1]\
                            <= contour_pixel[1] + 10 and contour_pixel[2] - 10 <= pixels[ps[0] + 1, ps[-1] - 1][2]\
                    <= contour_pixel[2] + 10 and [ps[0] + 1, ps[-1] - 1] not in bgs:
                return [ps[0] + 1, ps[-1] - 1], b
        except IndexError:
            pass
        try:
            if b == 3 and contour_pixel[0] - 10 <= pixels[ps[0] + 1, ps[-1]][0] <= contour_pixel[0] + 10 and\
                                            contour_pixel[1] - 10 <= pixels[ps[0] + 1, ps[-1]][1]\
                            <= contour_pixel[1] + 10 and contour_pixel[2] - 10 <= pixels[ps[0] + 1, ps[-1]][2]\
                    <= contour_pixel[2] + 10 and [ps[0] + 1, ps[-1]] not in bgs:
                return [ps[0] + 1, ps[-1]], b
        except IndexError:
            pass
        try:
            if b == 4 and contour_pixel[0] - 10 <= pixels[ps[0] + 1, ps[-1] + 1][0] <= contour_pixel[0] + 10 and\
                                            contour_pixel[1] - 10 <= pixels[ps[0] + 1, ps[-1] + 1][1]\
                            <= contour_pixel[1] + 10 and contour_pixel[2] - 10 <= pixels[ps[0] + 1, ps[-1] + 1][2]\
                    <= contour_pixel[2] + 10 and [ps[0] + 1, ps[-1] + 1] not in bgs:
                return [ps[0] + 1, ps[-1] + 1], b
        except IndexError:
            pass
        try:
            if b == 5 and contour_pixel[0] - 10 <= pixels[ps[0], ps[-1] + 1][0] <= contour_pixel[0] + 10 and\
                                            contour_pixel[1] - 10 <= pixels[ps[0], ps[-1] + 1][1]\
                            <= contour_pixel[1] + 10 and contour_pixel[2] - 10 <= pixels[ps[0], ps[-1] + 1][2]\
                    <= contour_pixel[2] + 10 and [ps[0], ps[-1] + 1] not in bgs:
                return [ps[0], ps[-1] + 1], b
        except IndexError:
            pass
        try:
            if b == 6 and contour_pixel[0] - 10 <= pixels[ps[0] - 1, ps[-1] + 1][0] <= contour_pixel[0] + 10 and\
                                            contour_pixel[1] - 10 <= pixels[ps[0] - 1, ps[-1] + 1][1]\
                            <= contour_pixel[1] + 10 and contour_pixel[2] - 10 <= pixels[ps[0] - 1, ps[-1] + 1][2]\
                    <= contour_pixel[2] + 10 and [ps[0] - 1, ps[-1] + 1] not in bgs:
                return [ps[0] - 1, ps[-1] + 1], b
        except IndexError:
            pass
        try:
            if b == 7 and contour_pixel[0] - 10 <= pixels[ps[0] - 1, ps[-1]][0] <= contour_pixel[0] + 10 and\
                                            contour_pixel[1] - 10 <= pixels[ps[0] - 1, ps[-1]][1]\
                            <= contour_pixel[1] + 10 and contour_pixel[2] - 10 <= pixels[ps[0] - 1, ps[-1]][2]\
                    <= contour_pixel[2] + 10 and [ps[0] - 1, ps[-1]] not in bgs:
                return [ps[0] - 1, ps[-1]], b
        except IndexError:
            pass
        i += 1
    return None, None


#img = Image.open("C:/Users/voyo/Pictures/Screenshots/test.png")
#print(ad_pontes(img, [335, 129]))
#print(ad_pontes(img, [327, 149]))
#img = Image.open("C:/Users/voyo/Pictures/Screenshots/star_test.png")
#print(ad_pontes(img, [197, 92]))
#print(ad_pontes(img, [430, 139]))
#img = Image.open("C:/Users/voyo/Pictures/Screenshots/disfigured_test.png")
#print(ad_pontes(img, [187, 172]))
#pixels = img.load()
#print(pixels[457, 110])
#img = Image.open("C:/Users/voyo/Downloads/infrared.jpg")
#print(ad_pontes(img, [60, 113]))
#print(ad_pontes(img, [293, 131]))
#img = Image.open("C:/Users/voyo/Downloads/test_algo.jpg")
#print(ad_pontes(img, [213, 307]))
img = Image.open("C:/Users/voyo/Pictures/Screenshots/hm.png")
print(ad_pontes(img, [260, 254]))

#pixels = img.load()
#print(pixels[198, 293])
#x = ad_pontes(img, [213, 307])
#for i in x:
#   print(pixels[i[0], i[1]])
