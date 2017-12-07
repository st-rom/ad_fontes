from PIL import Image


def ad_pontes(img, ps, ran=10):
    pixels = img.load()#  create the pixel map
    bgs = []#list of contour color pixels which are background og object
    pa = ps
    conts = [pa]#list of contour pixels
    position = 0#position of nearest contour pixel(out of 8)
    cont_col = pixels[pa[0], pa[-1]]#color of starting pixel
    pcn1, position1 = search_nearest(pixels, pa, position, bgs, ran)
    if position1 is None:
        #print('pp')
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
    position = position1
    print('ss', position1, pcn1, position2, pcn2, pa)
    pa = pcn1
    conts.append(pa)
    #print('poo')
    while True:
        #print(len(conts), conts)
        #print(pixels[conts[-1][0], conts[-1][-1]])
        '''
        if len(conts) % 200 == 0:
            new_img = Image.new('RGB', [img.size[0], img.size[1]], 'white')
            new_pixels = new_img.load()
            for i in conts:
                new_pixels[i[0], i[-1]] = cont_col
            new_img.show()
        '''
        #print(position, pa)
        position = (position + 6) % 8
        pcn, position = search_nearest(pixels, pa, position, bgs, ran)
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


def search_nearest(pixels, ps, d, bgs, ran=10, way=True):
    st = d#saving position in case way is false(loop goes the other way around)
    i = 0
    coords = {0: [-1, -1], 1: [0, -1], 2: [1, -1], 3: [1, 0], 4: [1, 1], 5: [0, 1], 6: [-1, 1], 7: [-1, 0]}#coordinats
    for b in range(d, d + 8):
        b %= 8
        if way is False:
            b = st - i
            if b < 0:
                b += 8
        e = exc(coords[b][0], coords[b][-1], pixels, ps, bgs, ran)#next contour pixel
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






#img = Image.open("C:/Users/voyo/Pictures/ad_fontes/test.png")
#print(ad_pontes(img, [335, 129]))
#print(ad_pontes(img, [327, 149]))
#img = Image.open("C:/Users/voyo/Pictures/ad_fontes/star_test.png")
#print(ad_pontes(img, [430, 139]))
#img = Image.open("C:/Users/voyo/Pictures/ad_fontes/disfigured_test.png")
#print(ad_pontes(img, [187, 172]))
#img = Image.open("C:/Users/voyo/Pictures/ad_fontes/infrared.jpg")
#print(ad_pontes(img, [60, 113]))
#print(ad_pontes(img, [293, 131]))
#img = Image.open("C:/Users/voyo/Pictures/ad_fontes/test_algo.jpg")
#print(ad_pontes(img, [213, 307]))
#img = Image.open("C:/Users/voyo/Pictures/ad_fontes/hm.png")
#print(ad_pontes(img, [260, 254]))
#img = Image.open("C:/Users/voyo/Pictures/ad_fontes/tree.png")
#print(ad_pontes(img, [950, 350]))
img = Image.open("C:/Users/voyo/Pictures/ad_fontes/test_algo2.jpg") #30
print(ad_pontes(img, [113, 130], 30))
#img = Image.open("C:/Users/voyo/Pictures/ad_fontes/planet.png") #20
#print(ad_pontes(img, [215, 350], 20))
#print(ad_pontes(img, [191, 191]))
#img = Image.open("C:/Users/voyo/Pictures/ad_fontes/glasses.jpg") #10    #12
#print(ad_pontes(img, [424, 260], 13))

#pixels = img.load()
#print(pixels[214, 350])
#x = ad_pontes(img, [213, 307])
#for i in x:
#   print(pixels[i[0], i[1]])
#16 27 54
