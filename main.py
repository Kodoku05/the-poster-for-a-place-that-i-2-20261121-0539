"""Draw the fictional floating isle of Caelora. Offline and deterministic."""
import math
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 3
W = 1024

def render():
    im = Image.new('RGB', (W*S, W*S))
    d = ImageDraw.Draw(im)
    stops = [(0, (30, 35, 76)), (270, (70, 60, 111)), (520, (185, 116, 129)), (735, (246, 184, 126)), (1024, (245, 209, 160))]
    for y in range(W*S):
        yy = y/S
        for (a, ca), (b, cb) in zip(stops, stops[1:]):
            if a <= yy <= b:
                t = (yy-a)/(b-a)
                c = tuple(round(x+(z-x)*t) for x,z in zip(ca,cb))
                d.line((0,y,W*S,y), fill=c)
                break
    def poly(points, fill):
        d.polygon([(round(x*S), round(y*S)) for x,y in points], fill=fill)
    def line(points, fill, width=1):
        d.line([(round(x*S), round(y*S)) for x,y in points], fill=fill, width=round(width*S), joint='curve')
    def ellipse(box, fill):
        d.ellipse(tuple(round(v*S) for v in box), fill=fill)
    def path(start, curves, fill):
        pts = [start]
        p = start
        for c in curves:
            if len(c)==2:
                pts.append(c); p=c
            else:
                x0,y0=p; x1,y1,x2,y2,x3,y3=c
                for j in range(1,33):
                    t=j/32; u=1-t
                    pts.append((u**3*x0+3*u*u*t*x1+3*u*t*t*x2+t**3*x3, u**3*y0+3*u*u*t*y1+3*u*t*t*y2+t**3*y3))
                p=(x3,y3)
        poly(pts,fill)
    # A restrained halo surrounds the low sun.
    glow=Image.new('RGBA', im.size)
    gd=ImageDraw.Draw(glow)
    for r in range(240,129,-3):
        gd.ellipse(((671-r)*S,(423-r)*S,(671+r)*S,(423+r)*S),fill=(255,205,137,2))
    glow=glow.filter(ImageFilter.GaussianBlur(18*S))
    im=Image.alpha_composite(im.convert('RGBA'),glow).convert('RGB'); d=ImageDraw.Draw(im)
    ellipse((537,289,805,557),'#ffdc9c')
    # Long, quiet wisps across the evening sky.
    path((72,399),[(175,382,209,388,277,396),(206,394,137,405,72,399)],'#b58b9d')
    path((780,329),[(838,314,910,323,955,316),(916,337,831,335,780,329)],'#ba929e')
    path((81,565),[(183,545,221,563,286,551),(238,578,144,574,81,565)],'#e6af9f')
    # Distant cloudbanks, giving the isle a high-altitude setting.
    path((0,704),[(72,672,100,699,154,684),(182,640,242,661,269,681),(346,648,371,687,424,692),(509,661,560,691,622,698),(680,663,740,680,777,685),(840,638,914,675,932,682),(971,668,1004,681,1024,686),(1024,1024),(0,1024)],'#d9b7b0')
    path((0,740),[(90,700,134,739,207,717),(260,682,324,722,348,733),(409,702,449,726,486,738),(593,701,632,722,686,738),(749,701,807,739,838,730),(915,688,967,707,1024,724),(1024,1024),(0,1024)],'#eac6b0')
    # The underside is a single suspended mountain, with broad lithic facets.
    poly([(284,509),(353,494),(471,490),(586,484),(740,482),(818,503),(792,550),(738,569),(720,624),(672,650),(624,706),(594,748),(563,709),(517,687),(489,638),(429,624),(391,586),(334,568)],'#65575d')
    poly([(284,509),(429,526),(465,586),(489,638),(391,586),(334,568)],'#9b7467')
    poly([(429,526),(547,539),(526,614),(563,709),(517,687),(489,638),(465,586)],'#7b6260')
    poly([(547,539),(657,531),(632,608),(624,706),(594,748),(563,709),(526,614)],'#554e5c')
    poly([(657,531),(818,503),(792,550),(738,569),(720,624),(672,650),(624,706),(632,608)],'#8b7065')
    poly([(745,532),(792,523),(777,551),(738,569),(713,601)],'#b18a6b')
    poly([(346,540),(420,554),(448,574),(368,559)],'#c39374')
    poly([(461,590),(503,600),(511,614),(479,605)],'#ac8370')
    poly([(644,620),(700,600),(687,619),(640,639)],'#aa826d')
    poly([(554,651),(574,665),(594,722),(572,695)],'#766266')
    # Thin ledges follow the faces rather than crossing the whole mountain.
    poly([(322,534),(383,547),(417,548),(426,554),(379,554),(332,543)],'#bd9275')
    poly([(548,565),(586,569),(640,552),(637,559),(586,578),(546,573)],'#70616a')
    poly([(723,570),(761,551),(758,558),(719,580)],'#d0a27c')
    poly([(534,625),(559,642),(591,647),(590,653),(555,648),(536,633)],'#8a7070')
    # Rounded turf rim and the gold meadows above it.
    path((284,509),[(320,477,383,470,445,466),(487,446,538,446,579,451),(644,438,699,448,742,460),(774,472,811,482,818,503),(771,531,715,536,657,531),(586,552,495,541,429,526),(365,531,313,522,284,509)],'#b5b46b')
    path((284,509),[(335,487,401,479,451,480),(518,463,566,470,608,461),(681,452,752,478,795,493),(721,482,674,491,615,504),(541,510,477,498,421,512),(358,519,318,514,284,509)],'#708a6c')
    path((385,489),[(463,451,536,464,577,463),(637,450,685,460,728,469),(647,460,610,481,557,485),(484,476,452,489,385,489)],'#d5c878')
    path((446,513),[(504,497,576,502,629,485),(671,472,708,474,747,482),(677,480,650,498,604,507),(548,524,504,522,446,513)],'#ece0a1')
    # A footpath curls toward the solitary lighthouse.
    path((505,482),[(563,474,567,492,628,483),(668,476,696,469,724,463),(703,478,666,486,628,490),(562,499,558,480,505,486)],'#f1dfa7')
    # A handful of small, sunlit houses, nestled into the meadow.
    for x,y,w,h in [(459,464,26,21),(491,457,23,23),(521,464,27,21)]:
        poly([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],'#f8e5c0')
        poly([(x+w,y),(x+w+8,y-6),(x+w+8,y+h-5),(x+w,y+h)],'#bcae95')
        poly([(x-3,y),(x+w/2,y-12),(x+w+10,y-6),(x+w,y+2)],'#805d61')
        poly([(x+11,y+h-10),(x+16,y+h-10),(x+16,y+h),(x+11,y+h)],'#666575')
    # Lighthouse on the bright outer rim.
    poly([(714,463),(744,463),(739,409),(719,409)],'#fff0cb')
    poly([(733,411),(739,409),(744,463),(735,463)],'#d9bc9a')
    poly([(717,430),(741,430),(742,439),(716,439)],'#b96559')
    poly([(716,409),(742,409),(742,399),(716,399)],'#514f61')
    poly([(720,401),(726,401),(726,408),(720,408)],'#fce8ac')
    poly([(730,401),(737,401),(737,408),(730,408)],'#ffdf95')
    poly([(711,399),(729,388),(747,399)],'#665363')
    line([(711,412),(747,412)],'#f9e3bb',2)
    line([(714,408),(714,413),(744,413),(744,408)],'#e4caa5',1)
    poly([(726,453),(732,453),(732,463),(726,463)],'#625d68')
    line([(729,388),(729,383)],'#504c5e',1)
    # Water crosses the lip and falls into the lower sea of clouds.
    path((396,506),[(408,505,424,507,435,511),(429,540,430,568,434,598),(433,646,420,681,429,744),(417,758,400,761,389,747),(406,687,398,649,406,597),(408,553,398,535,396,506)],'#91c8cf')
    path((405,508),[(414,507,421,510,425,511),(416,556,426,578,421,613),(414,663,418,699,409,748),(403,751,399,751,397,746),(412,692,404,650,413,610),(417,557,404,539,405,508)],'#eef0d7')
    line([(428,531),(425,562),(430,596),(426,631)],'#d3e5d6',2)
    line([(402,568),(400,615),(403,656),(398,702)],'#c4ddd6',2)
    # The torrent frays into ribbons, then dissolves into sunlit spray.
    path((399,691),[(399,723,389,744,376,761),(396,758,407,743,409,721),(405,708,405,700,399,691)],'#d8e6d5')
    path((421,690),[(421,721,432,738,451,749),(439,756,426,747,418,730),(415,717,417,699,421,690)],'#c4dbd1')
    mist=Image.new('RGBA',im.size)
    mistdraw=ImageDraw.Draw(mist)
    for box,alpha in [((365,720,453,772),100),((341,741,473,790),105),((376,702,430,758),65)]:
        mistdraw.ellipse(tuple(v*S for v in box),fill=(244,236,202,alpha))
    mist=mist.filter(ImageFilter.GaussianBlur(12*S))
    im=Image.alpha_composite(im.convert('RGBA'),mist).convert('RGB'); d=ImageDraw.Draw(im)
    path((349,770),[(356,751,381,749,391,756),(394,733,420,734,430,751),(452,741,469,756,476,770),(438,781,392,782,349,770)],'#f1d9b5')
    path((374,764),[(387,759,401,761,411,764),(422,754,441,758,448,765),(426,769,395,768,374,764)],'#fff0cc')
    # Foreground clouds are drawn as broad, flowing cut-paper shapes.
    path((0,794),[(40,759,93,768,123,789),(145,750,215,746,254,781),(294,765,338,777,354,802),(396,765,454,769,489,802),(545,787,587,803,612,819),(685,771,733,797,772,813),(831,761,887,778,914,801),(948,777,1000,775,1024,793),(1024,1024),(0,1024)],'#f7d7ad')
    path((0,852),[(61,826,105,851,140,859),(177,816,251,824,279,856),(344,826,394,845,418,869),(474,841,529,852,561,883),(611,853,673,851,714,873),(745,839,795,843,828,866),(900,832,975,840,1024,858),(1024,1024),(0,1024)],'#eabca0')
    path((0,901),[(54,859,117,876,145,902),(197,892,218,909,247,927),(293,875,368,884,396,914),(447,894,497,908,519,931),(573,895,623,902,653,923),(713,882,765,900,797,919),(850,876,909,891,936,911),(977,886,1004,888,1024,896),(1024,1024),(0,1024)],'#ffe5b8')
    path((0,970),[(75,940,114,956,150,971),(214,940,277,956,304,980),(366,954,420,971,446,986),(513,949,576,974,612,988),(684,953,741,975,781,984),(857,951,927,961,1024,973),(1024,1024),(0,1024)],'#c4c4ac')
    # Birds, in two small loose groups, kept clear of the typography.
    for x,y,z in [(236,345,11),(268,357,8),(294,336,6),(844,577,8),(868,566,6)]:
        pts=[]
        for j in range(25):
            t=j/24
            pts.append((x-z+2*z*t,y-4*math.sin(2*math.pi*t) if t<.5 else y+4*math.sin(2*math.pi*t)))
        line(pts,'#443e5b',2)
    # Name, deliberately spaced as one broad typographic crown.
    fontroot=Path('/usr/share/fonts/truetype/dejavu')
    fp=fontroot/'DejaVuSerif-Bold.ttf'
    if not fp.is_file(): fp=fontroot/'DejaVuSans-Bold.ttf'
    font=ImageFont.truetype(str(fp),111*S)
    title='CAELORA'; tracking=10*S
    widths=[d.textlength(ch,font=font) for ch in title]
    x=(W*S-sum(widths)-tracking*(len(title)-1))/2
    mask=Image.new('RGBA',im.size); md=ImageDraw.Draw(mask)
    tx=x
    for ch,width in zip(title,widths):
        md.text((tx,123*S),ch,font=font,fill=(15,22,51,125),stroke_width=1*S,anchor='lt'); tx+=width+tracking
    mask=mask.filter(ImageFilter.GaussianBlur(4*S))
    im=Image.alpha_composite(im.convert('RGBA'),mask).convert('RGB'); d=ImageDraw.Draw(im)
    for ch,width in zip(title,widths):
        d.text((x,119*S),ch,font=font,fill='#fff0ce',anchor='lt'); x+=width+tracking
    # Fine double rules finish the print.
    d.rectangle((27*S,27*S,997*S,997*S),outline='#f5deba',width=2*S)
    d.rectangle((35*S,35*S,989*S,989*S),outline='#e7cba8',width=S)
    im=im.resize((W,W),Image.Resampling.LANCZOS)
    out=Path(os.environ.get('MAKEFUN_OUTPUT_DIR','/output'))
    out.mkdir(parents=True,exist_ok=True)
    im.save(out/'entry.png',format='PNG',optimize=True)

if __name__=='__main__':
    try:
        render()
    except Exception as exc:
        print(f'Caelora rendering failed: {exc}',file=sys.stderr)
        sys.exit(1)
