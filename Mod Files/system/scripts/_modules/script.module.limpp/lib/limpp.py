'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from struct import unpack, pack, calcsize
import array
import zlib
from os.path import getsize as ospath_getsize, splitext as ospath_splitext

imageop = None
try:
    import imageop
except ImportError:
    pass

'''
TODO:
    Process the tRNS chunk
    Improve (make correct?) the adaptive filtering
    Replace file vars with non reserved name
'''

class PseudoFile:
    def __init__(self,fileobj_or_path):
        self.obj = None
        self.path = None
        if isinstance(fileobj_or_path, basestring):
            self.path = fileobj_or_path
        else:
            self.obj = fileobj_or_path

    def __getattr__(self,name):
        return getattr(self.obj, name)

    def open(self,mode='r'):
        if self.path:
            self.obj = open(self.path,mode)
        return self

    def close(self):
        if self.path: self.obj.close()

def openfile(fileobj_or_path,mode='r'):
    return PseudoFile(fileobj_or_path).open(mode)

################################################################################
''' Class: Image_Error '''
################################################################################
class Image_Error(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class Color8888:
    def __init__(self):
        self.r = 0
        self.g = 0
        self.b = 0
        self.a = 0xFF

class Color565:
    def __init__(self):
        self.nRed = 0
        self.nGreen = 0
        self.nBlue = 0
        self.nAlpha = 0xFF
        self.val = 0
        
    def Assign_bits(self,d):
        self.val = d
        self.nRed   = (d & 63488) >> 8
        self.nGreen = (d & 2016) >> 3
        self.nBlue  = (d & 31) << 3

class Color1555:
    def __init__(self,alpha=True):
        self.alpha = alpha
        self.nRed = 0
        self.nGreen = 0
        self.nBlue = 0
        self.nAlpha = 0xFF
        self.val = 0
        
    def Assign_bits(self,d):
        self.val = d
        if self.alpha:
            if (d >> 15):
                self.nAlpha = 255
            else:
                self.nAlpha = 0
        self.nRed   = (d & 31744) >> 7
        self.nGreen = (d & 992) >> 2
        self.nBlue  = (d & 31) << 3

    def RGBA_value(self):
        return unpack('L',chr(self.nRed) + chr(self.nGreen) +  chr(self.nBlue) + chr(self.nAlpha))

class DXTAlphaBlockExplicit:
    def __init__(self,data):
        self.row = []
        self.row.append(data[0])
        self.row.append(data[1])
        self.row.append(data[2])
        self.row.append(data[3])

def GetBitsFromMask(Mask):
    if Mask == 0: return 0,0 

    Temp = Mask
    i=0
    while i < 32:
        if (Temp & 1):
            break
        i+=1
        Temp = Temp >> 1
    ShiftRight = i

    # Temp is preserved, so use it again:
    i=0
    while i < 8:
        if not (Temp & 1):
            break
        i+=1
        Temp = Temp >> 1
    ShiftLeft = 8 - i

    return ShiftLeft,ShiftRight

################################################################################
''' Class: RGBA_data '''
################################################################################
class RGBA_data:
    Bpp = 4
    format = 'RGBA'
    is_image = True

    def __init__(self,width,height,data=None,mode='CHANNEL',fill=chr(0)):
        self.Update_dimensions(width,height)
        self.has_alpha = False
        self.grey = False
        self.mono = False
        self.indexed = False
        if not data:
            if len(fill) == 1:
                data = fill * (self.size_of_plane * 4)
            else:
                data = fill * self.size_of_plane
        if isinstance(data,array.array):
            self.data = data
            if self.data.typecode == 'L':
                self.mode = 'PIXEL'
            else:
                self.mode = 'CHANNEL'
        else:
            if mode.upper() == 'PIXEL':
                self.data = array.array('L',data)
                self.mode = 'PIXEL'
            else:
                self.data = array.array('B',data)
                self.mode = 'CHANNEL'
    
    def Pixel_mode(self):
        if self.data.typecode == 'L': return
        self.mode = 'PIXEL'
        self.data = array.array('L',self.data.tostring())

    def Channel_mode(self):
        if self.data.typecode == 'B': return
        self.mode = 'CHANNEL'
        self.data = array.array('B',self.data.tostring())

    def Data_length(self):
        return len(self.data)

    def Data_size(self):
        return self.data.itemsize * len(self.data)

    def Update_dimensions(self,width,height):
        self.width = width
        self.height = height
        self.Bps = width * self.Bpp
        self.size_of_plane = width * height

################################################################################
''' Class: Manipulator '''
################################################################################
class Manipulator:
    def __init__(self,image=None):
        if image: self.Set_image(image)
            
    def Set_image(self,image):
        if not image.is_image: image = image.RGBA
        self.RGBA = image
        self.width = self.RGBA.width
        self.height = self.RGBA.height
        self.Bpp = self.RGBA.Bpp
    
    def Flip(self):
        self.RGBA.Pixel_mode()
        temp = self.RGBA.data[:]
        y = self.height - 1
        pos = 0
        while y >= 0:
            ls = y*self.width
            ds = pos*self.width
            self.RGBA.data[ds:ds+self.width] = temp[ls:ls+self.width]
            pos +=1
            y-=1

    def FlipLR(self):
        self.RGBA.Pixel_mode()
        y = 0
        while y < self.height:
            ls = y*self.width
            le = ls + self.width
            line = self.RGBA.data[ls:le]
            line.reverse()
            self.RGBA.data[ls:le] = line
            y+=1
        return
        
    def Rotate_90(self):
        self.RGBA.Pixel_mode()
        temp = self.RGBA.data[:]
        
        width = self.height
        height = self.width
        pos = 0
        x=0
        while x < self.width:
            y=self.height-1
            while y > -1:
                self.RGBA.data[pos] = temp[y*self.width+x]
                pos+=1
                y-=1
            x+=1
        self.width = width
        self.height = height
        self.Bps = self.width * self.Bpp
        self.RGBA.Update_dimensions(width,height)
        
    def Rotate_right(self): self.Rotate_90()
    
    def Rotate_180(self):
        self.RGBA.Pixel_mode()
        self.RGBA.data.reverse()
            
    def Rotate_270(self):
        self.RGBA.Pixel_mode()
        temp = self.RGBA.data[:]
        width = self.height
        height = self.width
        pos = 0
        x=self.width-1
        while x > -1:
            y=0
            while y < self.height:
                self.RGBA.data[pos] = temp[y*self.width+x]
                pos+=1
                y+=1
            x-=1
        self.width = width
        self.height = height
        self.Bps = self.width * self.Bpp
        self.RGBA.Update_dimensions(width,height)
        
    def Rotate_left(self): self.Rotate_270()

    def Crop(self,top_x,top_y,bottom_x,bottom_y):
        width  = bottom_x - top_x
        height = bottom_y - top_y
        self.Bps = self.width * self.Bpp
        self.RGBA.Pixel_mode()
        temp = self.RGBA.data[:]
        self.RGBA.data = array.array('L',chr(0)*(width*height*4))
        self.RGBA.Update_dimensions(width,height)
        pos = 0
        y = top_y
        while y < bottom_y:
            new_row = pos*width
            old_row = y*self.width
            self.RGBA.data[new_row:new_row+width] = temp[old_row+top_x:old_row+bottom_x]
            pos+=1
            y+=1
        self.width = width
        self.height = height
        self.Bps = self.width * self.Bpp

    def Half(self,multiple=1):
        while multiple > 0:
            width = int(self.width/2)
            height = int(self.height/2)
            self.RGBA.Channel_mode()
            t = self.RGBA.data[:]
            self.RGBA.data = array.array('B',chr(0)*(width*height*4))
            self.RGBA.Update_dimensions(width,height)
            width_mult = self.width * 4
            pos = 0
            y=0
            while y < height*2:
                x=0
                while x < width*8:
                    r1 = y*width_mult+x
                    r2 = (y+1)*width_mult+x
                    self.RGBA.data[pos]   = (t[r1]   + t[r1+4] + t[r2]   + t[r2+4])/4
                    self.RGBA.data[pos+1] = (t[r1+1] + t[r1+5] + t[r2+1] + t[r2+5])/4
                    self.RGBA.data[pos+2] = (t[r1+2] + t[r1+6] + t[r2+2] + t[r2+6])/4
                    self.RGBA.data[pos+3] = (t[r1+3] + t[r1+7] + t[r2+3] + t[r2+7])/4
                    pos+=4
                    x+=8
                y+=2
            self.width = width
            self.height = height
            self.size_of_plane = self.width * self.height
            self.Bps = self.width * self.Bpp
            self.final_size = self.size_of_plane * self.Bpp
            multiple-=1
            
    def Double(self,multiple=1):
        while multiple > 0:
            width  = self.width * 2
            height = self.height * 2
            self.RGBA.Channel_mode()
            temp = self.RGBA.data[:]
            t = array.array('B',chr(0)*(width*height*4))
            self.RGBA.width = width
            self.RGBA.height = height
            pos = 0
            y=0
            while y < height:
                x=0
                while x < width*4:
                    r1 = y*width*4+x
                    r2 = (y+1)*width*4+x
                    t[r1]   = t[r1+4] = t[r2]   = t[r2+4] = temp[pos]
                    t[r1+1] = t[r1+5] = t[r2+1] = t[r2+5] = temp[pos+1]
                    t[r1+2] = t[r1+6] = t[r2+2] = t[r2+6] = temp[pos+2]
                    t[r1+3] = t[r1+7] = t[r2+3] = t[r2+7] = temp[pos+3]
                    pos+=4
                    x+=8
                y+=2
            self.RGBA.data = t
            self.width = width
            self.height = height
            self.size_of_plane = self.width * self.height
            self.Bps = self.width * self.Bpp
            self.final_size = self.size_of_plane * self.Bpp
            multiple-=1

    def Scale(self,width,height):
        if not imageop: #imageop is deprecated
            ct = 0
            cw = self.width
            ch = self.height
            while width < cw or height < ch:
                cw/=2
                ch/=2
                ct+=1
            if ct: return self.Half(ct)
            while width > cw and height > ch:
                cw/=2
                ch/=2
                ct+=1
            if ct:
                ct-=1
                if ct: return self.Double(ct)
            return

        self.RGBA.data = array.array('L',imageop.scale(self.RGBA.data.tostring(),self.Bpp,self.width,self.height,width,height))
        self.RGBA.mode = 'PIXEL'
        self.RGBA.Update_dimensions(width,height)
        self.width = width
        self.height = height
        self.size_of_plane = self.width * self.height
        self.Bps = self.width * self.Bpp
        self.final_size = self.size_of_plane * self.Bpp

    def Invert(self):
        self.RGBA.Channel_mode()
        x=0
        l = len(self.RGBA.data)
        while x < l:
            self.RGBA.data[x]   = 255 - self.RGBA.data[x]
            self.RGBA.data[x+1] = 255 - self.RGBA.data[x+1]
            self.RGBA.data[x+2] = 255 - self.RGBA.data[x+2]
            x+=4

    def Grey_image(self):
        self.RGBA.grey = True
        self.RGBA.Channel_mode()
        x=0
        l = len(self.RGBA.data)
        while x < l:
            avg = (self.RGBA.data[x] + self.RGBA.data[x+1] + self.RGBA.data[x+2])/3
            self.RGBA.data[x] = avg
            self.RGBA.data[x+1] = avg
            self.RGBA.data[x+2] = avg
            x+=4

    def Alpha_to_color(self,color=(0,0,0)):
        if not self.RGBA.has_alpha: return
        self.RGBA.has_alpha = False
        r=color[0]
        g=color[1]
        b=color[2]
        self.RGBA.Channel_mode()
        x=0
        l = len(self.RGBA.data)
        while x < l:
            alpha = self.RGBA.data[x+3]
            self.RGBA.data[x]   = self.RGBA.data[x]   + int((r - self.RGBA.data[x]  )*((255-alpha)/255.0))
            self.RGBA.data[x+1] = self.RGBA.data[x+1] + int((g - self.RGBA.data[x+1])*((255-alpha)/255.0))
            self.RGBA.data[x+2] = self.RGBA.data[x+2] + int((b - self.RGBA.data[x+2])*((255-alpha)/255.0))
            self.RGBA.data[x+3] = 255
            x+=4
            
################################################################################
''' Class: Base_image '''
################################################################################
class Base_image:
    def init(self):
        self.grey = False
        self.mono = False
        self.flipped = False
        self.has_alpha = False
        self.is_image = False
        self.pad = False
        
    def Write_PNG(self,outfilename,type='RGBA8',filter=0,compression=6):
        RGBA_to_PNG(self.RGBA,outfilename,type=type,filter=filter,compression=compression)
        return 0
    
    def Write_TGA(self,outfilename,type='BGR24',flip=False):
        RGBA_to_TGA(self.RGBA,outfilename,type=type,flip=flip)
        
    def Write_GIF(self,outfilename,colors=2,fg=(255,255,255),bg=(0,0,0),trans=False,invert=False):
        if not self.RGBA.grey:
            m = Manipulator()
            m.Set_image(self.RGBA)
            m.Grey_image()
            del m
            
        temp = array.array('B',self.RGBA.data.tostring())
        out = array.array('B',chr(0)*(len(self.RGBA.data)/4))
        l = len(self.RGBA.data)
        pos=0
        x=0
        while x < l:
            if invert:
                out[pos] = 255 - temp[x]
            else:
                out[pos] = temp[x]
            pos+=1
            x+=4
        mono = imageop.dither2mono(out.tostring(),self.width,self.height)
        from gif_image import make_gif
        open(outfilename,'wb').write(make_gif(mono,self.width,self.height,fg,bg,trans))
        
    def Write_BMP(self,outfilename,type='24'):
        BGR_to_BMP(self.RGBA,outfilename,type)

    def Write_XPM(self,outfilename):
        RGBA_to_XPM(self.RGBA,outfilename)

    def Write_XBM(self,outfilename):
        RGBA_to_XBM(self.RGBA,outfilename)
            
    def Read_image_data(self,element_size):
        f = open(self.file,'rb')
        f.seek(self.addr + self.data_offset)
        self.unprocessed = array.array(element_size,f.read(self.data_size))
        f.close()
        
    ################################################################################
    ### Function: Create_blank
    ################################################################################    
    def Create_blank(self):
        self.file = None
        self.mipmap = 0
        self.addr = 0
        self.height = 128
        self.width = 128
        self.size_of_plane = self.width * self.height
        self.Bps = self.width * 4
        self.Bpp = 4
        self.final_size = self.size_of_plane * self.Bpp
        self.RGBA = RGBA_data(self.width,self.height)

################################################################################
''' Class: Base_Indexed_image '''
################################################################################
class Base_indexed_image:
    def Read_palette(self,size,pixBytes=4):
        f = open(self.file,'rb')
        f.seek(self.palette_offset)
        p_temp = array.array('B',f.read(size))
        pix = array.array('B',chr(0)*4)
        self.palette = array.array('L',chr(0)*((size/pixBytes)*4))
        f.close()
        i=0
        p=0
        pix[3] = 255
        l = size/pixBytes
        while i < l:
            pix[0] = p_temp[p+2]
            pix[1] = p_temp[p+1]
            pix[2] = p_temp[p]
            self.palette[i] = unpack('L',pix.tostring())[0]
            p += pixBytes
            i+=1
            
    def Read_16bit_palette(self,size):
        f = open(self.file,'rb')
        f.seek(self.palette_offset)
        p_temp = array.array('H',f.read(size))
        self.palette = array.array('L',chr(0)*((size/2)*4))
        f.close()
        color = Color1555()
        i=0
        l = size/2
        while i < l:
            color.assign_bits(p_temp[i])
            self.palette[i] = color.RGBA_value()
            i+=1

################################################################################
''' Class: Indexed_image '''
################################################################################
class Indexed_image(Base_image,Base_indexed_image):
    def Process1bit(self):
        self.Read_image_data('B')
        back = self.palette[1:].tostring()
        self.RGBA = RGBA_data(self.width,self.height,fill=back,mode='PIXEL')
        color = self.palette[0]
        padsize = 0
        if self.pad: padsize = ((32 - (self.width % 32)) / 8) % 4
        pos = 0           
        if self.flipped:
            compare = self.height
            j = 0
            it = 1
        else:
            compare = -1
            j=self.height-1
            it = -1
        while j != compare:
            i=0
            while i < self.width:
                c=0
                k=128
                while c < 8:
                    if not (self.unprocessed[pos] & k): self.RGBA.data[j * self.width + i] = color
                    k >>= 1
                    i+=1
                    if i >= self.width: break
                    c+=1
                pos +=1
            pos +=padsize
            j+=it
            
    def Process2bit(self):
        self.Read_image_data('B')
        back = self.palette[1:].tostring()
        self.RGBA = RGBA_data(self.width,self.height,fill=back,mode='PIXEL')
        padsize = 0
        if self.pad: padsize = ((32 - (self.width % 32)) / 8) % 4
        pos = 0           
        if self.flipped:
            compare = self.height
            j = 0
            it = 1
        else:
            compare = -1
            j=self.height-1
            it = -1
        while j != compare:
            i=0
            while i < self.width:
                c=6
                k=192
                while c > -2:
                    color = (self.unprocessed[pos] & k) >> c
                    self.RGBA.data[j * self.width + i] = self.palette[color]
                    k >>= 2
                    i+=1
                    if i >= self.width: break
                    c-=2
                pos +=1
            pos +=padsize
            j+=it
            
    def Process4bit(self):
        self.Read_image_data('B')
        back = self.palette[0:1].tostring()
        self.RGBA = RGBA_data(self.width,self.height,fill=back,mode='PIXEL')
        padsize = 0
        if self.pad: padsize = ((8 - (self.width % 8)) / 2) % 4
        pos=0
        j=0
        if self.flipped:
            compare = self.height
            j = 0
            it = 1
        else:
            compare = -1
            j=self.height-1
            it = -1
        while j != compare:
            i=0
            while i < self.width:
                bytedata = self.unprocessed[pos]
                self.RGBA.data[j * self.width + i] = self.palette[bytedata >> 4]
                i+=1
                if i == self.width: break
                self.RGBA.data[j * self.width + i] = self.palette[bytedata & 0x0F]
                i+=1
                pos+=1
            pos+=padsize
            j+=it

    def Process8bit(self,read=True):
        if read: self.Read_image_data('B')
        back = self.palette[0:1].tostring()
        self.RGBA = RGBA_data(self.width,self.height,fill=back,mode='PIXEL')
        #padsize = 0
        #if self.pad: padsize = (4 - (self.Bps % 4)) % 4
        pos=0
        j=0
        if self.flipped:
            compare = self.height
            j = 0
            it = 1
        else:
            compare = -1
            j=self.height-1
            it = -1
        while j != compare:
            i=0
            while i < self.width:
                bytedata = self.unprocessed[pos]
                self.RGBA.data[j * self.width + i] = self.palette[bytedata]
                i+=1
                pos+=1
            j+=it
            
################################################################################
''' Class: Indexed_RLE_image '''
################################################################################
class RLE_image(Base_image,Base_indexed_image):
    def Process_RLE8(self):
        self.Read_image_data('B')
        self.RGBA = RGBA_data(self.width,self.height,fill=self.palette[0:1].tostring(),mode='PIXEL')
        pos = 0
        bytes = array.array('B',chr(0)*2)
        y=0
        while y < self.height:
            x=0
            while True:
                bytes[0] = self.unprocessed[pos]
                bytes[1] = self.unprocessed[pos+1]
                pos+=2
                if bytes[0] == 0: #Escape
                    if bytes[1] == 0: break #EOL
                    elif bytes[1] == 1: #Bitmap End
                        y = self.height
                        break
                    elif bytes[1] == 2:
                        bytes[0] = self.unprocessed[pos]
                        bytes[1] = self.unprocessed[pos+1]
                        pos+=2
                        x += bytes[0]
                        y += bytes[1]
                        if y >= self.height: break
                    
                    else:  # Run of pixels
                        if self.width - x < bytes[1]: return False
                        r=0
                        while r < bytes[1]:
                            self.RGBA.data[y*self.width+x+r] = self.palette[self.unprocessed[pos+r]]
                            r+=1
                        pos+=r
                        x+=r
                        if bytes[1] % 2: pos +=1
                else:
                    dc_loc = y * self.width + x
                    r=0
                    while r < bytes[0]:
                        self.RGBA.data[dc_loc+r] = self.palette[bytes[1]]
                        r+=1
                    x += bytes[0]
            y+=1
        if not self.flipped: Manipulator(image=self.RGBA).Flip()
        
    def Process_RLE4(self):
        self.Read_image_data('B')
        self.RGBA = RGBA_data(self.width,self.height,fill=self.palette[0:1].tostring(),mode='PIXEL')
        pos = 0
        bytes = array.array('B',chr(0)*2)
        y=0
        while y < self.height:
            x=0
            while True:
                bytes[0] = self.unprocessed[pos]
                bytes[1] = self.unprocessed[pos+1]
                pos+=2
                if bytes[0] == 0:
                    if bytes[1] == 0: break
                    elif bytes[1] == 1:
                        y = self.height
                        break
                    elif bytes[1] == 2:
                        bytes[0] = self.unprocessed[pos]
                        bytes[1] = self.unprocessed[pos+1]
                        pos+=2
                        x += bytes[0]
                        y += bytes[1]
                        if y >= self.height: break
                    
                    else:  # Run of pixels
                        r=0
                        while r < bytes[1] and x < self.width:
                            twopix = self.unprocessed[pos]
                            pos+=1
                            upper = twopix >> 4
                            lower = twopix & 15
                            x+=1
                            self.RGBA.data[y * self.width + x] = self.palette[upper]
                            x+=1
                            self.RGBA.data[y * self.width + x] = self.palette[lower]
                            r+=2

                        align = bytes[1] % 4

                        if align == 1 or align == 2: pos+=1
                else:
                    dc_loc = y * self.width
                    upper = bytes[1] >> 4
                    lower = bytes[1] & 15
                    r=0
                    while r < bytes[0] and x < self.width-1:
                        x+=1
                        if r & 1:
                            self.RGBA.data[dc_loc+x] = self.palette[lower]
                        else:
                            self.RGBA.data[dc_loc+x] = self.palette[upper]
                        r+=1
            y+=1
        if not self.flipped: Manipulator(image=self.RGBA).Flip()
        
    def Process_PacketRLE8(self):
        self.Read_image_data('B')
        self.RGBA = RGBA_data(self.width,self.height,fill=self.palette[0:1].tostring(),mode='PIXEL')
        pos = 0
        x = 0
        l = self.RGBA.Data_length()
        #dl = len(self.unprocessed)
        while x < l:
            head = self.unprocessed[pos]
            pos+=1
            #if not pos < dl: return
            if head & 128:
                rep = (head & 127) + x
                #if not pos < dl: return
                index = self.unprocessed[pos]
                pos+=1
                while x <= rep:
                    self.RGBA.data[x] = self.palette[index]
                    x+=1
            else:
                run = (head & 127) + x
                while x <= run:
                    self.RGBA.data[x] = self.palette[self.unprocessed[pos]]
                    pos+=1
                    x+=1
                    #if not pos < dl: return
        if not self.flipped: Manipulator(image=self.RGBA).Flip()

    def Process_PacketRLE_BGR(self):
        if self.sourceBpp == 2:
            self.Process_PacketRLE_BGR16()
            return
        self.Read_image_data('B')
        self.RGBA = RGBA_data(self.width,self.height,mode='CHANNEL')
        pos = 0
        x = 0
        l = self.RGBA.Data_length()
        #dl = len(self.unprocessed)
        Bpp = self.sourceBpp
        a = 255
        while x < l:
            head = self.unprocessed[pos]
            pos+=1
            if head & 128:
                rep = (head & 127)*4 + x
                r = self.unprocessed[pos+2]
                g = self.unprocessed[pos+1]
                b = self.unprocessed[pos]
                if Bpp == 4: a = self.unprocessed[pos+3]
                pos+=Bpp
                while x <= rep:
                    self.RGBA.data[x]   = r
                    self.RGBA.data[x+1] = g
                    self.RGBA.data[x+2] = b
                    self.RGBA.data[x+3] = a
                    x+=4
                    #if not x < l: break
            else:
                run = (head & 127)*4 + x
                while x <= run:
                    self.RGBA.data[x]   = self.unprocessed[pos+2]
                    self.RGBA.data[x+1] = self.unprocessed[pos+1]
                    self.RGBA.data[x+2] = self.unprocessed[pos]
                    if Bpp == 4: a = self.unprocessed[pos+3]
                    self.RGBA.data[x+3] = a
                    pos+=Bpp
                    x+=4
                    #if not x < l: break
        if not self.flipped: Manipulator(image=self.RGBA).Flip()
        
    def Process_PacketRLE_BGR16(self):
        self.Read_image_data('B')
        self.RGBA = RGBA_data(self.width,self.height,mode='CHANNEL')
       
        l = self.RGBA.Data_length()
        if self.alpha_bits: alpha=False #WHY???????????? -------------------------------------------------------FIX???
        color = Color1555(alpha=alpha)
        
        pos = 0
        x = 0
        while x < l:
            head = self.unprocessed[pos]
            pos+=1
            if head & 128:
                rep = (head & 127)*4 + x
                bytes = (self.unprocessed[pos+1]<<8) | self.unprocessed[pos]
                color.Assign_bits(bytes)
                pos+=2
                while x <= rep:
                    self.RGBA.data[x]   = color.nRed
                    self.RGBA.data[x+1] = color.nGreen
                    self.RGBA.data[x+2] = color.nBlue
                    self.RGBA.data[x+3] = color.nAlpha
                    x+=4
                    #if not x < l: break
            else:
                run = (head & 127)*4 + x
                while x <= run:
                    bytes = (self.unprocessed[pos+1]<<8) | self.unprocessed[pos]
                    color.Assign_bits(bytes)
                    self.RGBA.data[x]   = color.nRed
                    self.RGBA.data[x+1] = color.nGreen
                    self.RGBA.data[x+2] = color.nBlue
                    self.RGBA.data[x+3] = color.nAlpha
                    pos+=2
                    x+=4
                    #if not x < l: break
        if not self.flipped: Manipulator(image=self.RGBA).Flip()
    
################################################################################
''' Class: BGR_image '''
################################################################################
class BGR_image(Base_image):
    def Process16bit(self,pad=True,alpha=False):
        self.Read_image_data('H')
        self.RGBA = RGBA_data(self.width,self.height,mode='CHANNEL')
        color = Color1555(alpha=alpha)
        padsize = 0
        if pad: padsize = (4 - (self.width*2 % 4)) % 4
        pos = 0            
        outbytewidth = self.width*4
        offset = 0
        if self.flipped:
            offsetmult = self.width
            origin = pos
            offset -= offsetmult
        else:
            offsetmult = self.width * -1
            origin = offsetmult * self.height * -1
        i=0
        while i < self.final_size:
            offset += offsetmult
            pos = origin + offset
            j=0
            while j < outbytewidth:
                color.Assign_bits(self.unprocessed[pos])
                self.RGBA.data[i]   = color.nRed
                self.RGBA.data[i+1] = color.nGreen
                self.RGBA.data[i+2] = color.nBlue
                self.RGBA.data[i+3] = color.nAlpha
                j+=4
                i+=4
                pos +=1
            pos+=padsize
                
    def Process24bit(self,pad=True):
        self.Read_image_data('B')
        self.RGBA = RGBA_data(self.width,self.height,mode='CHANNEL')
        pos = 0
        padsize = 0
        if pad:
            padsize = (4 - (self.Bps % 4)) % 4
            if padsize != 0:
                padsize = (4 - (self.Bps % 4))
        offset = 0
        if self.flipped:
            offsetmult = self.width * 3 + padsize
            origin = pos
            offset -= offsetmult
        else:
            offsetmult = self.width * -3 - padsize
            origin = offsetmult * self.height * -1
        self.Process_BGR_data(offset,offsetmult,origin)
                
    def Process32bit(self,alpha=False):
        self.Read_image_data('B')
        self.RGBA = RGBA_data(self.width,self.height,mode='CHANNEL')
        pos = 0
        offset = 0
        if self.flipped:
            offsetmult = self.width * 4
            origin = pos
            offset -= offsetmult
        else:
            origin = pos + self.final_size
            offsetmult = self.width * -4
        if alpha:
            self.Process_BGRA_data(offset,offsetmult,origin)
        else:
            self.Process_BGR_data(offset,offsetmult,origin)
                
    def Process_BGR_data(self,offset,offsetmult,origin):
        outbytewidth = self.width*4
        i=0
        while i < self.final_size:
            offset += offsetmult
            pos = origin + offset
            j=0
            while j < outbytewidth:
                self.RGBA.data[i] = self.unprocessed[pos+2]
                self.RGBA.data[i+1] = self.unprocessed[pos+1]
                self.RGBA.data[i+2] = self.unprocessed[pos]
                self.RGBA.data[i+3] = 0xFF
                j+=4
                i+=4
                pos +=self.sourceBpp

    def Process_BGRA_data(self,offset,offsetmult,origin):
        outbytewidth = self.width*4
        i=0
        while i < self.final_size:
            offset += offsetmult
            pos = origin + offset
            j=0
            while j < outbytewidth:
                self.RGBA.data[i] = self.unprocessed[pos+2]
                self.RGBA.data[i+1] = self.unprocessed[pos+1]
                self.RGBA.data[i+2] = self.unprocessed[pos]
                self.RGBA.data[i+3] = self.unprocessed[pos+3]
                j+=4
                i+=4
                pos +=self.sourceBpp
                
################################################################################
''' Class: Greyscale_image '''
################################################################################
class Greyscale_image:
    def Process_greyA_16bit(self):
        self.sourceBpp = 2
        self.Bps = self.width * self.sourceBpp
        self.Read_image_data('B')
        l=len(self.unprocessed)
        self.RGBA = RGBA_data(self.width,self.height,mode='PIXEL')
        x=0
        y=0
        l=len(self.unprocessed)
        while x < l:
            self.RGBA.data[y] = self.unprocessed[x] * 65793 + self.unprocessed[x+1]*16777216
            y+=1
            x+=2
            
    def Process_greyA_32bit(self):
        self.sourceBpp = 4
        self.Bps = self.width * self.sourceBpp
        self.Read_image_data('B')
        l=len(self.unprocessed)
        self.RGBA = RGBA_data(self.width,self.height)
        x=0
        y=0
        l=len(self.unprocessed)
        while x < l:
            self.RGBA.data[y] = self.unprocessed[x] * 65793 + self.unprocessed[x+2]*16777216
            y+=1
            x+=4
            
    def Process_grey_16bit(self):
        self.Create_grey_palette(256)
        self.sourceBpp = 2
        self.Bps = self.width * 2
        x=0
        y=0
        self.Read_image_data('B')
        l=len(self.unprocessed)
        temp = array.array('B',chr(0)*(l/2))
        while y < l:
            temp[x] = self.unprocessed[y]
            x+=1
            y+=2
        self.unprocessed = temp
        self.Process8bit(read=False)
        
    def Process_grey_8bit(self):
        self.Create_grey_palette(256)
        self.sourceBpp = 1
        self.Bps = self.width
        self.Process8bit()
        
    def Process_grey_4bit(self):
        self.sourceBpp = 0.5
        self.Bps = (self.width + (2-self.width % 2)%2)/2
        if self.interlaced:
            self.Create_grey_palette(256)
            self.Process8bit()
        else:
            self.Create_grey_palette(16)
            self.Process4bit()
        
    def Process_grey_2bit(self):
        self.sourceBpp = 0.25
        self.Bps = (self.width + (4-self.width % 4)%4)/4
        if self.interlaced:
            self.Create_grey_palette(256)
            self.Process8bit()
        else:
            self.Create_grey_palette(4)
            self.Process2bit()
        
    def Process_grey_1bit(self):
        self.sourceBpp = 0.125
        self.Bps = (self.width + (8-self.width % 8)%8)/8
        if self.interlaced:
            self.Create_grey_palette(256)
            self.Process8bit()
        else:
            self.Create_grey_palette(2) #Look at using imageop/mono2grey for this---------------------------------------------------------------------OPTIMIZE
            self.Process1bit()
            
    def Process_grey_PacketRLE8(self): #Needs RLE_image to work
        self.Create_grey_palette(256)
        self.sourceBpp = 1
        self.Bps = self.width
        self.Process_PacketRLE8()

    def Process_grey_PacketRLE16(self):
        self.Read_image_data('B')
        self.RGBA = RGBA_data(self.width,self.height,mode='PIXEL')
        pos = 0
        x = 0
        l = self.RGBA.Data_length()
        #dl = len(self.unprocessed)
        while x < l:
            head = self.unprocessed[pos]
            pos+=1
            #if not pos < dl: return
            if head & 128:
                rep = (head & 127) + x
                #if not pos < dl: return
                pixel = self.unprocessed[pos] * 65793 + self.unprocessed[pos+1]*16777216
                pos+=2
                while x <= rep:
                    self.RGBA.data[x] = pixel
                    x+=1
            else:
                run = (head & 127) + x
                while x <= run:
                    pixel = self.unprocessed[pos] * 65793 + self.unprocessed[pos+1]*16777216
                    self.RGBA.data[x] = pixel
                    pos+=2
                    x+=1
                    #if not pos < dl: return
        if not self.flipped: Manipulator(image=self.RGBA).Flip()
        
    def Create_grey_palette(self,num):
        self.palette = array.array('L',chr(0)*(num*4))
        step = 255/(num-1)
        p=0
        for x in range(0,256,step):
            self.palette[p] = long(long(65793 * x) + 4278190080)
            p+=1
            
################################################################################
''' Class: Texture_image '''
################################################################################
class Texture_image(Base_image):
    ################################################################################
    ### Function: DecompressDXT1
    ################################################################################    
    def DecompressDXT1(self):
        self.Read_image_data('H')
        self.RGBA = RGBA_data(self.width,self.height,mode='CHANNEL')
        #RGB Red 5 Green 6 Blue 5
        color_0 = Color565()
        color_1 = Color565()
        
        # 32 bit RGBA
        colors  = []
        colors.append(Color8888())
        colors.append(Color8888())
        colors.append(Color8888())
        colors.append(Color8888())
        
        three = long(3)

        pos = 0
        zoff = self.mipmap * self.size_of_plane
        y=0
        while y < self.height:
            x=0
            while x < self.width:
                color_0.Assign_bits(self.unprocessed[pos])
                color_1.Assign_bits(self.unprocessed[pos+1])
                
                bitmask = (long(self.unprocessed[pos+2]) << 16) + self.unprocessed[pos+3]
                
                pos += 4

                colors[0].r = color_0.nRed
                colors[0].g = color_0.nGreen
                colors[0].b = color_0.nBlue

                colors[1].r = color_1.nRed
                colors[1].g = color_1.nGreen
                colors[1].b = color_1.nBlue


                if color_0.val > color_1.val:
                    colors[2].b = (2 * colors[0].b + colors[1].b + 1) / 3
                    colors[2].g = (2 * colors[0].g + colors[1].g + 1) / 3
                    colors[2].r = (2 * colors[0].r + colors[1].r + 1) / 3

                    colors[3].b = (colors[0].b + 2 * colors[1].b + 1) / 3
                    colors[3].g = (colors[0].g + 2 * colors[1].g + 1) / 3
                    colors[3].r = (colors[0].r + 2 * colors[1].r + 1) / 3
                    colors[3].a = 0xFF
                else:
                    colors[2].b = (colors[0].b + colors[1].b) >> 1
                    colors[2].g = (colors[0].g + colors[1].g) >> 1
                    colors[2].r = (colors[0].r + colors[1].r) >> 1

                    colors[3].b = (colors[0].b + 2 * colors[1].b + 1) / 3
                    colors[3].g = (colors[0].g + 2 * colors[1].g + 1) / 3
                    colors[3].r = (colors[0].r + 2 * colors[1].r + 1) / 3
                    colors[3].a = 0x00
                    
                j=0
                k=0
                for j in (2,3,0,1):
                    i=0
                    yval = y + j
                    yoff = yval * self.Bps
                    while i < 4:
                        shift = k*2
                        select = (bitmask & (three << shift)) >> shift
                        col = colors[select]
                        xval = x + i
                        if xval < self.width and yval < self.height:
                            offset = zoff + yoff + (xval * self.Bpp)
                            self.RGBA.data[offset]   = col.r
                            self.RGBA.data[offset+1] = col.g
                            self.RGBA.data[offset+2] = col.b
                            self.RGBA.data[offset+3] = col.a
                        i+=1
                        k+=1
                x+=4
            y+=4
        del self.unprocessed
        
    ################################################################################
    ### Function: DecompressDXT2 - untested and unused - so far...
    ################################################################################
    def DecompressDXT2(self):
        self.DecompressDXT3()
        self.CorrectPreMult()
	
    def CorrectPreMult(self):
        i=0
        while i < self.final_size:
            if not self.RGBA.data[i+3] == 0:
                self.RGBA.data[i]   = (int(self.RGBA.data[i])   << 8) / self.RGBA.data[i+3]
                self.RGBA.data[i+1] = (int(self.RGBA.data[i+1]) << 8) / self.RGBA.data[i+3]
                self.RGBA.data[i+2] = (int(self.RGBA.data[i+2]) << 8) / self.RGBA.data[i+3]
            i+=4
                                          
    ################################################################################
    ### Function: DecompressDXT3
    ################################################################################    
    def DecompressDXT3(self):
        self.Read_image_data('H')
        self.RGBA = RGBA_data(self.width,self.height,mode='CHANNEL')
        #RGB Red 5 Green 6 Blue 5
        color_0 = Color565()
        color_1 = Color565()
        
        # 32 bit RGBA
        colors  = []
        colors.append(Color8888())
        colors.append(Color8888())
        colors.append(Color8888())
        colors.append(Color8888())
        
        three = long(3)

        pos = 0
        zoff = self.mipmap * self.size_of_plane
        y=0
        while y < self.height:
            x=0
            while x < self.width:
                alpha = DXTAlphaBlockExplicit(self.unprocessed[pos:pos+4])
                pos += 4
                color_0.Assign_bits(self.unprocessed[pos])
                color_1.Assign_bits(self.unprocessed[pos+1])
                bitmask = (long(self.unprocessed[pos+2]) << 16) + self.unprocessed[pos+3]
                pos += 4

                colors[0].r = color_0.nRed
                colors[0].g = color_0.nGreen
                colors[0].b = color_0.nBlue

                colors[1].r = color_1.nRed
                colors[1].g = color_1.nGreen
                colors[1].b = color_1.nBlue
               
                colors[2].b = (2 * colors[0].b + colors[1].b + 1) / 3
                colors[2].g = (2 * colors[0].g + colors[1].g + 1) / 3
                colors[2].r = (2 * colors[0].r + colors[1].r + 1) / 3

                colors[3].b = (colors[0].b + 2 * colors[1].b + 1) / 3
                colors[3].g = (colors[0].g + 2 * colors[1].g + 1) / 3
                colors[3].r = (colors[0].r + 2 * colors[1].r + 1) / 3

                k=0
                j=0
                for j in (2,3,0,1):
                    i=0
                    yval = y + j
                    yoff = yval * self.Bps
                    while i < 4:
                        shift = k*2
                        select = (bitmask & (three << shift)) >> shift
                        col = colors[select]
                        xval = x + i
                        if xval < self.width and yval < self.height:
                            offset = zoff + yoff + (xval * self.Bpp)
                            self.RGBA.data[offset]   = col.r
                            self.RGBA.data[offset+1] = col.g
                            self.RGBA.data[offset+2] = col.b
                        i+=1
                        k+=1

                j=0
                while j < 4:
                    yval = y + j
                    yoff = yval * self.Bps
                    word = alpha.row[j]
                    i=0
                    while i < 4:
                        xval = x + i
                        if xval < self.width and yval < self.height:
                            offset = zoff + yval * self.Bps + (xval * self.Bpp) + 3
                            self.RGBA.data[offset] = word & 0x0F
                            self.RGBA.data[offset] = self.RGBA.data[offset] | (self.RGBA.data[offset] << 4)
                        word = word >> 4
                        i+=1
                    j+=1
                x+=4
            y+=4
        del self.unprocessed
    
    ################################################################################
    ### Function: DecompressDXT4 - untested and unused - so far...
    ################################################################################
    def DecompressDXT4(self):
        self.DecompressDXT5()
        self.CorrectPreMult()
        
    ################################################################################
    ### Function: DecompressDXT5
    ################################################################################    
    def DecompressDXT5(self):
        self.Read_image_data('H')
        self.RGBA = RGBA_data(self.width,self.height,mode='CHANNEL')
        #RGB Red 5 Green 6 Blue 5
        color_0 = Color565()
        color_1 = Color565()
        
        # 32 bit RGBA
        colors  = []
        colors.append(Color8888())
        colors.append(Color8888())
        colors.append(Color8888())
        colors.append(Color8888())
        alphas = [0,0,0,0,0,0,0,0]
        three = long(3)
        z=0
        pos = 0
        zoff = self.mipmap * self.size_of_plane
        y=0
        while y < self.height:
            x=0
            while x < self.width:
                if y >= self.height or x >= self.width: break
                alphas[0] = self.unprocessed[pos] >> 8
                alphas[1] = self.unprocessed[pos] % (alphas[0] << 8)
                alphamask = self.unprocessed[pos+1]
                alphamask2 = self.unprocessed[pos+2]
                
                pos += 4
                color_0.Assign_bits(self.unprocessed[pos])
                color_1.Assign_bits(self.unprocessed[pos+1])
                bitmask = (long(self.unprocessed[pos+2]) << 16) + self.unprocessed[pos+3]
                pos += 4

                colors[0].r = color_0.nRed
                colors[0].g = color_0.nGreen
                colors[0].b = color_0.nBlue

                colors[1].r = color_1.nRed
                colors[1].g = color_1.nGreen
                colors[1].b = color_1.nBlue
               
                colors[2].b = (2 * colors[0].b + colors[1].b + 1) / 3
                colors[2].g = (2 * colors[0].g + colors[1].g + 1) / 3
                colors[2].r = (2 * colors[0].r + colors[1].r + 1) / 3

                colors[3].b = (colors[0].b + 2 * colors[1].b + 1) / 3
                colors[3].g = (colors[0].g + 2 * colors[1].g + 1) / 3
                colors[3].r = (colors[0].r + 2 * colors[1].r + 1) / 3

                k=0
                j=0
                for j in (2,3,0,1):
                    i=0
                    yval = y + j
                    yoff = yval * self.Bps
                    while i < 4:
                        shift = k*2
                        select = (bitmask & (three << shift)) >> shift
                        col = colors[select]
                        xval = x + i
                        if xval < self.width and yval < self.height:
                            offset = zoff + yoff + (xval * self.Bpp)
                            self.RGBA.data[offset]   = col.r
                            self.RGBA.data[offset+1] = col.g
                            self.RGBA.data[offset+2] = col.b
                        i+=1
                        k+=1

                j=0
                if (alphas[0] > alphas[1]):    
                    alphas[2] = (6 * alphas[0] + 1 * alphas[1] + 3) / 7
                    alphas[3] = (5 * alphas[0] + 2 * alphas[1] + 3) / 7
                    alphas[4] = (4 * alphas[0] + 3 * alphas[1] + 3) / 7
                    alphas[5] = (3 * alphas[0] + 4 * alphas[1] + 3) / 7
                    alphas[6] = (2 * alphas[0] + 5 * alphas[1] + 3) / 7
                    alphas[7] = (1 * alphas[0] + 6 * alphas[1] + 3) / 7
                else :
                    alphas[2] = (4 * alphas[0] + 1 * alphas[1] + 2) / 5
                    alphas[3] = (3 * alphas[0] + 2 * alphas[1] + 2) / 5
                    alphas[4] = (2 * alphas[0] + 3 * alphas[1] + 2) / 5
                    alphas[5] = (1 * alphas[0] + 4 * alphas[1] + 2) / 5
                    alphas[6] = 0x00
                    alphas[7] = 0xFF
                bits = alphamask
                j=0
                while j < 2:
                    i=0
                    while i < 4:
                        if (((x + i) < self.width) and ((y + j) < self.height)):
                            offset = z * self.size_of_plane + (y + j) * self.Bps + (x + i) * self.Bpp + 3
                            self.RGBA.data[offset] = alphas[bits & 0x07]
                        bits >>= 3
                        i+=1
                    j+=1
                bits = alphamask2
                j=2
                while j < 4:
                    i=0
                    while i < 4:
                        if (((x + i) < self.width) and ((y + j) < self.height)):
                            offset = z * self.size_of_plane + (y + j) * self.Bps + (x + i) * self.Bpp + 3
                            self.RGBA.data[offset] = alphas[bits & 0x07]
                        bits >>= 3
                        i+=1
                    j+=1
                x+=4
            y+=4
        del self.unprocessed
    
    ################################################################################
    ### Function: DecompressARGB32bit
    ################################################################################
    def DecompressARGB32bit(self,alpha=True,rgb=True,swizzled=False):
        self.Read_image_data('B')
        self.RGBA = RGBA_data(self.width,self.height,mode='CHANNEL')
        i=0
        size = self.final_size
        #account for BGR
        r=2 ; b=0
        if not rgb: r=0 ; b=2
            
        while i < size:
            self.RGBA.data[i]   = self.unprocessed[i+r]
            self.RGBA.data[i+1] = self.unprocessed[i+1]
            self.RGBA.data[i+2] = self.unprocessed[i+b]
            if alpha:
                self.RGBA.data[i+3] = self.unprocessed[i+3]
            else:
                self.RGBA.data[i+3] = 0xFF
            i+= 4
                
        if swizzled:
            self.RGBA.data = array.array('L',self.RGBA.data.tostring())
            self.unswiz = array.array('L',chr(0)*self.final_size)
            self.offset = 0
            self.Unswizzle(0,0,self.width,self.height,self.width)
            self.RGBA.data = array.array('B',self.unswiz.tostring())
            
    ##############################################################################
    ### Function: DecompressRGB16bit
    ############################################################################        
    def DecompressRGB16bit(self,a1555=False,alpha=False,swizzled=False):
        self.Read_image_data('H')
        self.RGBA = RGBA_data(self.width,self.height,mode='CHANNEL')
        if a1555:
            color = Color1555(alpha=alpha)
        else:
            color = Color565()
            
        pos = 0            
        size = self.final_size
        i=0
        while i < size:
            color.Assign_bits(self.unprocessed[pos])
            pos+=1
            self.RGBA.data[i]   = color.nRed
            self.RGBA.data[i+1] = color.nGreen
            self.RGBA.data[i+2] = color.nBlue
            self.RGBA.data[i+3] = color.nAlpha
           
            i+=4
            
        if swizzled:
            self.RGBA.data = array.array('L',self.RGBA.data.tostring())
            self.unswiz = array.array('L',chr(0)*self.final_size)
            self.offset = 0
            self.Unswizzle(0,0,self.width,self.height,self.width)
            self.RGBA.data = array.array('B',self.unswiz.tostring())
            
    ############################################################################
    ### Function: DecompressRGB24bit
    ############################################################################        
    def DecompressRGB24bit(self,swizzled=False):
        self.Read_image_data('B')
        self.RGBA = RGBA_data(self.width,self.height,mode='CHANNEL')
        i=0
        pos = 0
        size = self.final_size
        while i < size:
            self.RGBA.data[i]   = self.unprocessed[pos+2]
            self.RGBA.data[i+1] = self.unprocessed[pos+1]
            self.RGBA.data[i+2] = self.unprocessed[pos]
            self.RGBA.data[i+3] = 0xFF
            pos+=3
            i+=4
            
        if swizzled:
            self.RGBA.data = array.array('L',self.RGBA.data.tostring())
            self.unswiz = array.array('L',chr(0)*self.final_size)
            self.offset = 0
            self.Unswizzle(0,0,self.width,self.height,self.width)
            self.RGBA.data = array.array('B',self.unswiz.tostring())
            
    ############################################################################
    ### Function: Unswizzle
    ############################################################################    
    def Unswizzle(self,offset,offsetout,width,height,stride):
        if width < 2 or height < 2:
            length = width * height
            self.unswiz[offsetout:offsetout+length] = self.RGBA.data[self.offset:self.offset+length]
            offsetout = offsetout + (length)
        elif width == 2 and height == 2:
            self.unswiz[offsetout] = self.RGBA.data[self.offset]
            self.unswiz[offsetout + 1] = self.RGBA.data[self.offset + 1]
            self.unswiz[offsetout + stride] = self.RGBA.data[self.offset + 2]
            self.unswiz[offsetout + stride + 1] = self.RGBA.data[self.offset + 3]
            self.offset = self.offset + 4
        else:
            self.Unswizzle(self.offset, offsetout, width / 2, height / 2, stride)
            self.Unswizzle(self.offset, offsetout + (width / 2), width / 2, height / 2, stride)
            self.Unswizzle(self.offset, offsetout + (stride * (height / 2)), width / 2, height / 2, stride)
            self.Unswizzle(self.offset, offsetout + (stride * (height / 2)) + (width / 2), width / 2, height / 2, stride)
        
################################################################################
''' Class: XPR0_image '''
################################################################################    
class XPR0_image(Texture_image):
    def __init__(self,mipmap=0,addr=0,size=None,file=None,process=True):
        self.init()
        self.type = 'XPR0'
        if not file:
            self.Create_blank()
            return
        if not size:
            size = ospath_getsize(file)
        self.file = file
        self.mipmap = mipmap
        self.addr = addr
        self.size = size
        self.Read_header()
        self.Get_image_dimensions()
        self.data_size = self.size - self.data_offset
        self.size_of_plane = self.width * self.height
        self.Bps = self.width * 4
        self.Bpp = 4
        self.final_size = self.size_of_plane * self.Bpp
        self.RGBA = None
        if not process: return
        if self.header['TextureFormat'] == 12:
            self.DecompressDXT1()
        elif self.header['TextureFormat'] == 14:
            self.DecompressDXT3()
        elif self.header['TextureFormat'] == 6:
            self.DecompressARGB32bit(swizzled=True)
        elif self.header['TextureFormat'] == 7:
            self.DecompressARGB32bit(alpha=False,swizzled=True)
        elif self.header['TextureFormat'] == 15:
            self.DecompressDXT5()
        else:
            pass
        #6  RGBA8   0x06
        #12 DXT1    0x0C
        #14 DXT3    0x0E
	#15 DXT5    0x0F
	#11 P8      0x0B

    def Read_header(self):
        format = '4s5L4B2L'
        f = open(self.file,'rb')
        f.seek(self.addr)
        
        self.header = {}
        self.header['XPRMagic'],\
        self.header['TotalSize'],\
        self.header['HeaderSize'],\
        self.header['TextureCommon'],\
        self.header['TextureData'],\
        self.header['TextureLock'],\
        self.header['TextureMisc1'],\
        self.header['TextureFormat'],\
        l_w,\
        h_m,\
        self.header['TextureSize'],\
        self.header['EndOfHeader'] = unpack(format,f.read(calcsize(format)))
        f.close()
        # Get 4 bit values
        l = l_w >> 4
        self.header['TextureLevel'] = l
        if l:
            self.header['TextureWidth'] = l_w % (l << 4)
        else:
            self.header['TextureWidth'] = l_w
        h = h_m >> 4
        self.header['TextureHeight'] = h
        if h:
            self.header['TextureMisc2'] = h_m % (h << 4)
        else:
            self.header['TextureMisc2'] = h_m
        
    def Get_image_dimensions(self):
        levels = {8:(256,256),
                  7:(128,128),
                  6:(64,64),
                  5:(32,32),
                  4:(16,16),
                  3:(8,8),
                  2:(4,4),
                  1:(2,2),
                  0:(1,1)}
        if levels.has_key(self.header['TextureLevel']):
            self.width, self.height = levels[self.header['TextureLevel']]
        else:
            self.width, self.height = 128 , 128
        self.data_offset = self.header['HeaderSize']
        
################################################################################
''' Class: DDS_image ''' 
################################################################################    
class DDS_image(Texture_image):
    def __init__(self,mipmap=0,addr=0,size=None,file=None,process=True):
        self.init()
        self.type = 'DDS'
        if not file:
            self.Create_blank()
            return
        if not size:
            size = ospath_getsize(file)
        self.file = file
        self.mipmap = mipmap
        self.addr = addr
        self.size = size
        self.Read_header(addr)
        self.Get_image_dimensions()
        self.data_size = self.size - self.data_offset
        self.size_of_plane = self.width * self.height
        self.Bps = self.width * 4
        self.Bpp = 4
        self.final_size = self.size_of_plane * self.Bpp
        self.RGBA = None
        if not process: return
        alpha = True
        if self.header['pfFourCC'] == 'DXT1':
            self.DecompressDXT1()
        elif self.header['pfFourCC'] == 'DXT2':
            self.DecompressDXT2()
        elif self.header['pfFourCC'] == 'DXT3':
            self.DecompressDXT3()
        elif self.header['pfFourCC'] == 'DXT4':
            self.DecompressDXT4()
        elif self.header['pfFourCC'] == 'DXT5':
            self.DecompressDXT5()
        elif self.header['pfFourCC'] == '\x00\x00\x00\x00':
            #Need to find out if image is swizzled?
            if self.header['pfBpp'] == 32:
                rgb = True
                alpha = True
                if not self.header['pfBlueMask'] == 0xFF: rgb=False
                if not self.header['pfAlphaMask']: alpha = False
                self.DecompressARGB32bit(alpha=alpha,rgb=rgb)
            elif self.header['pfBpp'] == 16:
                a1555 = False
                alpha = False
                if self.header['pfGreenMask'] == 992:
                    a1555 = True
                    if self.header['pfAlphaMask']: alpha = True     
                self.DecompressRGB16bit(a1555=a1555,alpha=alpha)
            elif self.header['pfBpp'] == 24:
                self.DecompressRGB24bit()
            else:
                pass
        else:
            pass
        self.RGBA.has_alpha = alpha
        
    def Read_header(self,addr):
        format = '4s8L40s2L4s10L'
        f = open(self.file,'rb')
        f.seek(self.addr)

        self.header = {}
        self.header['magic'],\
        self.header['size'],\
        self.header['flags'],\
        self.header['height'],\
        self.header['width'],\
        self.header['pitch'],\
        self.header['depth'],\
        self.header['mipMapLevels'],\
        self.header['alphaBitDepth'],\
        reserved,\
        self.header['pfSize'],\
        self.header['pfFlags'],\
        self.header['pfFourCC'],\
        self.header['pfBpp'],\
        self.header['pfRedMask'],\
        self.header['pfGreenMask'],\
        self.header['pfBlueMask'],\
        self.header['pfAlphaMask'],\
        self.header['caps1'],\
        self.header['caps2'],\
        self.header['caps3'],\
        self.header['caps4'],\
        self.header['textureStage'] = unpack(format,f.read(calcsize(format)))
        f.close()
    
    def Get_image_dimensions(self):
        self.width = self.header['width']
        self.height = self.header['height']
        self.data_offset = self.header['size'] + 4

################################################################################
''' Class: TGA_image ''' 
################################################################################    
class TGA_image(Indexed_image,BGR_image,RLE_image,Greyscale_image):
    def __init__(self,addr=0,size=None,file=None,process=True):
        self.init()
        if not size:
            size = ospath_getsize(file)
        self.file_size = size
        self.file = file
        self.addr = addr
        self.size = size
        self.type = 'TGA'
        self.pallete = None
        self.Read_header()
        self.flipped = False
        if self.header['ImageDescriptor'] & 32:
            self.flipped = True
        self.alpha_bits = self.header['ImageDescriptor'] & 15
        self.Get_image_dimensions()
        self.size_of_plane = self.width * self.height
        self.sourceBpp = self.header['BitsPerPixel']/8
        self.data_size = self.width * self.height * self.sourceBpp
        self.Bps = self.width * self.sourceBpp
        self.Bpp = 4
        self.final_size = self.size_of_plane * self.Bpp
        self.RGBA = None
        if not process: return
        self.Process()

    def Process(self):
        typecode = self.header['DataTypeCode']
        bpp = self.header['BitsPerPixel']
        index_pixel = self.header['ColorMapDepth'] / 8
        if typecode == 2: #BGR
            if   bpp == 32:
                self.Process32bit(alpha=True)
            elif bpp == 24:
                self.Process24bit(pad=False)
            elif bpp == 16:
                self.Process16bit(pad=False)
        elif typecode == 1: #Indexed
            psize = self.header['ColorMapLength'] * index_pixel
            self.pad = False
            if index_pixel == 32:
                self.Read_palette(psize,4)
                if bpp == 8: self.Process8bit()
            elif index_pixel == 24:
                self.Read_palette(psize,3)
                if bpp == 8: self.Process8bit()
            elif index_pixel == 16:
                self.Read_16bit_palette(psize)
                if bpp == 8: self.Process8bit()
        elif typecode == 9: #RLE Indexed
            self.data_size = self.size - self.data_offset
            psize = self.header['ColorMapLength'] * index_pixel
            self.pad = False
            if index_pixel == 4:
                self.Read_palette(psize,4)
                if bpp == 8: self.Process_PacketRLE8()
            elif index_pixel == 3:
                self.Read_palette(psize,3)
                if bpp == 8: self.Process_PacketRLE8()
            elif index_pixel == 2:
                self.Read_16bit_palette(psize)
                if bpp == 8: self.Process_PacketRLE8()
        elif typecode == 10: #RLE
            self.data_size = self.size - self.data_offset
            self.Process_PacketRLE_BGR()
        elif typecode == 3: # Grey
            if bpp == 16:
                self.Process_greyA_16bit()
                if not self.flipped: Manipulator(image=self.RGBA).Flip()
            elif bpp == 8:
                self.Process_grey_8bit()
        elif typecode == 11: #Grey RLE
            self.data_size = self.size - self.data_offset
            if bpp == 16:
                self.Process_grey_PacketRLE16()
            elif bpp == 8:
                self.Process_grey_PacketRLE8()
                
        if self.alpha_bits: self.RGBA.has_alpha = True
            
    def Read_header(self):
        format = '<3B2HB4H2B'
        f = open(self.file,'rb')
        f.seek(self.addr)

        self.header = {}
        self.header['IdLength'],\
        self.header['ColorMapType'],\
        self.header['DataTypeCode'],\
        self.header['ColorMapOrigin'],\
        self.header['ColorMapLength'],\
        self.header['ColorMapDepth'],\
        self.header['xOrigin'],\
        self.header['yOrigin'],\
        self.header['Width'],\
        self.header['Height'],\
        self.header['BitsPerPixel'],\
        self.header['ImageDescriptor'] = unpack(format,f.read(calcsize(format)))
        self.head_size = calcsize(format)
        
        format = '<2L16sH'
        f.seek(-26,2)

        self.footer = {}
        self.footer['ExtOffset'],\
        self.footer['DevOffset'],\
        self.footer['Signature'],\
        self.footer['Unimportant'] = unpack(format,f.read(calcsize(format)))
        f.close()
        if self.footer['Signature'] == 'TRUEVISION-XFILE':
            if self.footer['ExtOffset']:
                self.size = self.footer['ExtOffset'] - 1
            else:
                self.size -= 26
        else:
            del self.footer
            self.footer = None
        return True
        
    def Get_image_dimensions(self):
        self.width = self.header['Width']
        self.height = self.header['Height']
        self.data_offset = 18 + self.header['IdLength'] + (self.header['ColorMapLength'] * (self.header['ColorMapDepth']/8))
        self.palette_offset = 18 + self.header['IdLength']

################################################################################
''' Class: ICO_image ''' 
################################################################################    
class ICO_image(Indexed_image,BGR_image,RLE_image):
    def __init__(self,addr=0,size=None,file=None,process=True,options=None):
        self.default_icon = None
        if options:
            if options.has_key('icon'):
                self.default_icon = options['icon']
        self.init()
        if not size:
            size = ospath_getsize(file)
        self.file_size = size
        self.file = file
        self.addr = addr
        self.size = size
        self.type = 'ICO'
        self.Read_header()
        self.final_size = self.width * self.height * 4
        if process: self.Process()

    def Process(self):
        bitcount = self.icon_heads[self.default_icon]['Bitcount']
        if bitcount == 32:
            self.Process32bit()
        elif bitcount == 24:
            self.Process24bit()
        elif bitcount == 16:
            self.Process16bit()
        elif bitcount == 8:
            self.Read_palette(self.palette_size)
            self.Process8bit()
        elif bitcount == 4:
            self.Read_palette(self.palette_size)
            self.Process4bit()
        elif bitcount == 1:
            self.Read_palette(self.palette_size)
            self.Process1bit()
            self.RGBA.mono = True

        self.Process_Mask()
        self.RGBA.has_alpha = True

    def Process_Mask(self):
        f = open(self.file,'rb')
        f.seek(self.mask_offset)
        mask = array.array('B',f.read(self.mask_size))
        f.close
        self.RGBA.Channel_mode()
        
        padsize = ((32 - (self.width % 32)) / 8) % 4
        pos = 0
        row_l = self.width * 4
        j = (self.height-1)*row_l
        while j >= 0:
            i=0
            while i < row_l:
                c=0
                k=128
                while c < 8:
                    if (mask[pos] & k): self.RGBA.data[j+i+3] = 0
                    k >>= 1
                    i+=4
                    if i >= row_l: break
                    c+=1
                pos +=1
            pos +=padsize
            j-=row_l
        
    def Read_header(self):
        format = '<3H'
        f = open(self.file,'rb')
        f.seek(self.addr)

        self.header = {}
        self.header['Reserved'],\
        self.header['Type'],\
        self.header['Count'] = unpack(format,f.read(calcsize(format)))

        format = '<BBBBHHLL'
        format2 = '<3i2h6i'
        self.icon_heads = []
        x = 0
        last = 0
        choice = 0
        while x < self.header['Count']:
            header = {}
            header['Width'],\
            header['Height'],\
            header['ColorCount'],\
            header['Reserved'],\
            header['Planes'],\
            header['Bitcount'],\
            header['BytesInRes'],\
            header['ImageOffset'] = unpack(format,f.read(calcsize(format)))
            
            self.icon_heads.append(header)
            #choose largest icon as default
            test = header['Width'] * header['Height'] * header['Bitcount']
            if test > last:
                last = test
                choice = x
            x+=1
        for h in range(0,len(self.icon_heads)):
            f.seek(self.icon_heads[h]['ImageOffset'])
            
            self.icon_heads[h]['HeaderSize'],\
            width,\
            height,\
            self.icon_heads[h]['Planes'],\
            self.icon_heads[h]['Bitcount'],\
            self.icon_heads[h]['Compression'],\
            self.icon_heads[h]['SizeImage'],\
            self.icon_heads[h]['XPelsPerMeter'],\
            self.icon_heads[h]['YPelsPerMeter'],\
            self.icon_heads[h]['ClrUsed'],\
            self.icon_heads[h]['ClrImportant'] = unpack(format2,f.read(calcsize(format2)))
            #print self.icon_heads[h]
        f.close()
        if not self.default_icon == None:
            if self.default_icon < len(self.icon_heads):
                choice = self.default_icon
            else:
                self.default_icon = choice
        else:
            self.default_icon = choice
        self.width = self.icon_heads[choice]['Width']
        self.height = self.icon_heads[choice]['Height']
        self.data_offset = self.icon_heads[choice]['ImageOffset'] + 40
        self.sourceBpp = self.icon_heads[choice]['Bitcount'] / 8.0
        if self.sourceBpp >= 1: self.sourceBpp = int(self.sourceBpp)
        colors = self.icon_heads[choice]['ClrUsed']
        if self.sourceBpp <= 1:
            self.palette_size = colors * 4
            if not self.palette_size:
                if self.sourceBpp == 1:
                    self.palette_size = 1024
                elif self.sourceBpp == 0.5:
                    self.palette_size = 64
                elif self.sourceBpp == 0.125:
                    self.palette_size = 2
            self.palette_offset = self.data_offset
            self.data_offset = self.palette_offset + self.palette_size
        self.Bps = self.width * self.sourceBpp
        #Do I need to pad this? --------------------------------------------------------------------------------------------_FIX
        self.data_size = int(self.width * self.height * self.sourceBpp)
        #print self.data_size
        #self.data_size =
        #print self.icon_heads[choice]['SizeImage']        
        self.mask_offset = self.data_offset + self.data_size
        self.mask_size = self.icon_heads[choice]['BytesInRes'] + self.icon_heads[choice]['ImageOffset'] - self.mask_offset

def GetShiftFromMask(mask): #TODO: Test if this works
	if not mask: return 0

	shift = 0;
	while mask & 1 == 0:
		mask >>= 1
		shift+=1
  
	return shift

################################################################################
''' Class: BMP_image ''' 
################################################################################    
class BMP_image(Indexed_image,BGR_image,RLE_image):
    def __init__(self,addr=0,size=None,file=None,process=True):
        self.init()
        if not size:
            size = ospath_getsize(file)
        self.file_size = size
        self.file = file
        self.addr = addr
        self.size = size
        self.type = 'BMP'
        self.pallete = None
        self.pad = True
        if not self.Read_header():
            self.Process_OS2(process)
            return
        self.flipped = False
        if self.header['Height'] < 0:
            self.flipped = True
            self.header['Height'] = self.header['Height'] * -1
        self.palette_offset = self.addr + self.head_size
        self.Get_image_dimensions()
        self.size_of_plane = self.width * self.height
        self.sourceBpp = self.header['BitCount']/8
        self.data_size = self.header['SizeImage']
        self.Bps = self.width * self.sourceBpp
        self.Bpp = 4
        self.final_size = self.size_of_plane * self.Bpp
        self.RGBA = None
        if not process: return
        if not self.header['Compression'] or self.header['Compression'] == 3:
            if self.header['BitCount'] == 24:
                self.Process24bit()
            elif self.header['BitCount'] == 16:
                self.Process16bit()
            elif self.header['BitCount'] == 32:
                if self.header['Compression'] == 3:
                    self.Process32bitCompressed()
                else:
                    self.Process32bit()
            elif self.header['BitCount'] == 1:
                self.Read_palette(8)
                self.Process1bit()
                self.RGBA.indexed = True
                self.RGBA.mono = True
            elif self.header['BitCount'] == 4:
                self.Read_palette(64)
                self.Process4bit()
                self.RGBA.indexed = True
            elif self.header['BitCount'] == 8:
                self.Read_palette(1024)
                self.Process8bit()
                self.RGBA.indexed = True
            else:
                pass
        else:
            size = self.header['ClrUsed'] * 4
            if self.header['Compression'] == 2:
                if not size: size = 64
                self.Read_palette(size)
                self.Process_RLE4()
            elif self.header['Compression'] == 1:
                if not size: size = 1024
                self.Read_palette(size)
                self.Process_RLE8()
            else:
                pass
            self.RGBA.indexed = True

    def Process_OS2(self,process):
        self.Read_OS2_header()
        self.Get_image_dimensions()
        self.size_of_plane = self.width * self.height
        self.sourceBpp = self.header['BitCount']/8
        self.size = self.header['FileSize']
        self.Bps = self.width * self.sourceBpp
        self.Bpp = 4
        self.final_size = self.size_of_plane * self.Bpp
        self.flipped = False
        self.RGBA = None
        if not process: return
        if self.header['BitCount'] == 1:
            self.Read_palette(6,pixBytes=3)
            self.Process1bit()
            self.RGBA.indexed = True
            self.RGBA.mono = True
        elif self.header['BitCount'] == 4:
            self.Read_palette(48,pixBytes=3)
            self.Process4bit()
            self.RGBA.indexed = True
        elif self.header['BitCount'] == 8:
            self.Read_palette(768,pixBytes=3)
            self.Process8bit()
            self.RGBA.indexed = True
        else:
            self.Process24bit()
            
    def Read_palette(self,size,pixBytes=4):
        f = open(self.file,'rb')
        f.seek(self.addr + self.head_size)
        p_temp = array.array('B',f.read(size))
        pix = array.array('B',chr(0)*4)
        self.palette = array.array('L',chr(0)*((size/pixBytes)*4))
        f.close()
        i=0
        p=0
        pix[3] = 255
        while i < size/pixBytes:
            pix[0] = p_temp[p+2]
            pix[1] = p_temp[p+1]
            pix[2] = p_temp[p]
            self.palette[i] = unpack('L',pix.tostring())[0]
            p += pixBytes
            i+=1
        
    def Read_header(self):
        format = '<2siI4i2h6i'
        f = open(self.file,'rb')
        f.seek(self.addr)

        self.header = {}
        self.header['Magic'],\
        self.header['FileSize'],\
        self.header['Reserved'],\
        self.header['DataOff'],\
        self.header['HeaderSize'],\
        self.header['Width'],\
        self.header['Height'],\
        self.header['Planes'],\
        self.header['BitCount'],\
        self.header['Compression'],\
        self.header['SizeImage'],\
        self.header['XPelsPerMeter'],\
        self.header['YPelsPerMeter'],\
        self.header['ClrUsed'],\
        self.header['ClrImportant'] = unpack(format,f.read(calcsize(format)))
        self.head_size = calcsize(format)
        f.close()
        if not self.header['HeaderSize'] == 40: return False
        return True

    def Read_OS2_header(self):
        format = '<2sIhhII4H'
        f = open(self.file,'rb')
        f.seek(self.addr)

        self.header = {}
        self.header['Magic'],\
        self.header['FileSize'],\
        self.header['XHotSpot'],\
        self.header['YHotspot'],\
        self.header['DataOff'],\
        self.header['Fix'],\
        self.header['Width'],\
        self.header['Height'],\
        self.header['Planes'],\
        self.header['BitCount'] = unpack(format,f.read(calcsize(format)))
        self.head_size = calcsize(format)
        f.close()
        return True
        
    def Get_image_dimensions(self):
        self.width = self.header['Width']
        self.height = self.header['Height']
        self.data_offset = self.header['DataOff']

    def Process32bitCompressed(self):
        self.Read_image_data('B')
        self.RGBA = RGBA_data(self.width,self.height,mode='CHANNEL')
        pos = 0
        #Neet to test......                                                      FIX----
        pos = self.header['DataOff'] - 12
        rMask = unpack('L',self.unprocessed[pos:pos+4].tostring())
        pos += 4
        gMask = unpack('L',self.unprocessed[pos:pos+4].tostring())
        pos += 4
        bMask = unpack('L',self.unprocessed[pos:pos+4].tostring())
        pos += 4
        rShiftL, rShiftR = GetShiftFromMask(rMask) 
        gShiftL, gShiftR = GetShiftFromMask(gMask)
        bShiftL, bShiftR = GetShiftFromMask(bMask)     
        i=0
        while i < self.final_size:
            Read = unpack('L',self.unprocessed[pos:pos+4].tostring())
            pos+=4
            if Read != 1: return False            
            self.RGBA.data[i] = ((Read & bMask) >> bShiftR) << bShiftL
            self.RGBA.data[i + 1] = ((Read & gMask) >> gShiftR) << gShiftL
            self.RGBA.data[i + 2] = ((Read & rMask) >> rShiftR) << rShiftL
            self.RGBA.data[i + 3] = 0xFF
            i+=4
        
################################################################################
''' Class: JPEG_image NOT FINISHED - WIP =]''' 
################################################################################    
class JPEG_image(Base_image):
    def __init__(self,addr=0,size=None,file=None,process=True):
        self.init()
        import TonyJpegDecoder
        if not size:
            size = ospath_getsize(file)
        self.file_size = size
        self.file = file
        self.addr = addr
        self.size = size
        self.type = 'JPG'
        self.header = {}
        self.decoder = TonyJpegDecoder.TonyJpegDecoder()
        self.data = self.decoder.DecompressImage(openfile(file,'rb').read())
        self.width = self.decoder.Width
        self.height = self.decoder.Height
        self.size_of_plane = self.width * self.height
        self.sourceBpp = 3
        self.size = size
        self.Bps = self.width * self.sourceBpp
        self.Bpp = 4
        self.final_size = self.size_of_plane * self.Bpp
        self.RGBA = None
        if not process: return
        self.Process_data()

    def Process_data(self):
        self.RGBA = RGBA_data(self.width,self.height,fill=chr(255),mode='CHANNEL')
        pos=0
        x=0
        y=self.height-1
        padding = (self.width % 2)*3
        while y > 0:
            x=0
            while x < self.width*4:
                row = y*self.width*4
                self.RGBA.data[row+x]   = self.data[pos+2]
                self.RGBA.data[row+x+1] = self.data[pos+1]
                self.RGBA.data[row+x+2] = self.data[pos]
                self.RGBA.data[row+x+3] = 255
                pos+=3
                x+=4
            pos+=padding
            y-=1

################################################################################
''' Class: PNG_image '''
################################################################################    
class PNG_image(Indexed_image,Greyscale_image):
    
    def Filter_0(self,row,data): #None
        self.over = data
        return data
    
    def Filter_1(self,row,data): #Left
        l=len(data);x=0
        #l=self.Bps;x=0
        while x < l:
            left = x - self.filterBpp
            if left < 0:
                left = 0
            else:
                left = data[left]
            data[x] = (data[x] + left) % 256
            x+=1
        self.over = data
        return data
    
    def Filter_2(self,row,data): #Up
        row_l = len(data)#self.Bps
        x=0
        while x < row_l:
            data[x] = (data[x] + self.over[x]) % 256
            x+=1
        self.over = data
        return data

    def Filter_3(self,row,data): #Average
        row_l = len(data)#self.Bps
        x=0
        while x < row_l:
            left = x - self.filterBpp
            if left < 0:
                left = 0
            else:
                left = data[left]
            above = self.over[x]
            data[x] = (data[x] + ((left + above)/2)) % 256
            x+=1
        self.over = data
        return data
    
    def Filter_4(self,row,data): #Paeth
        row_l = len(data)#self.Bps
        x=0
        while x < row_l:
            left = x - self.filterBpp
            if left < 0:
                left = 0
                above_left = 0
            else:
                left = data[left]
                above_left = self.over[x - self.filterBpp]
            above = self.over[x]
            data[x] = (data[x] + self.PaethPredictor(left,above,above_left)) % 256
            x+=1
        self.over = data
        return data
        
    def PaethPredictor(self,l,a,ul):
        p = l + a - ul        # initial estimate
        pa = abs(p - l)     # distances to a, b, c
        pb = abs(p - a)
        pc = abs(p - ul)
        # return nearest of a,b,c,
        # breaking ties in order a,b,c.
        if pa <= pb and pa <= pc:
            return l
        elif pb <= pc:
            return a
        else:
            return ul

    def Init_filter(self):
        self.filterBpp = self.sourceBpp
        if self.filterBpp < 1: self.filterBpp = 1
        self.over = array.array('B',chr(0)*self.Bps)

    def De_filter_rows(self):
        row_l = self.Bps
        x=0
        l = self.height*row_l
        self.Init_filter()
        while x < l:
            flt = self.unprocessed.pop(x)
            if flt < 5: self.unprocessed[x:x+row_l] = self.filter[flt](self,x,self.unprocessed[x:x+row_l])
            x+=row_l
                
    filter = {}
    filter[0] = Filter_0
    filter[1] = Filter_1
    filter[2] = Filter_2
    filter[3] = Filter_3
    filter[4] = Filter_4
    
    def __init__(self,addr=0,size=None,file=None,process=True):
        self.init()
        if not size:
            size = ospath_getsize(file)
        self.file_size = size
        self.file = file
        self.addr = addr
        self.size = size
        self.type = 'PNG'
        self.pad = False
        self.data_offsets = {}
        self.Read_header()
        self.Get_image_dimensions()

        self.interlaced = self.header['InterlaceType']
        self.size_of_plane = self.width * self.height
        self.Bpp = 4
        self.final_size = self.size_of_plane * self.Bpp
        self.RGBA = None
        if not process: return
        self.Process()

    def Process(self):
        colortype = self.header['ColorType']
        bitdepth = self.header['Bitdepth']
        if colortype == 6:
            if bitdepth == 8: #RGB with alpha
                self.Process_RGBA_32bit()
            else:
                self.Process_RGBA_64bit()
            self.RGBA.has_alpha = True
        elif colortype == 4: #Greyscale with alpha
            if bitdepth == 8:
                self.Process_greyA_16bit()
            else:
                self.Process_greyA_32bit()
            self.RGBA.has_alpha = True
            self.RGBA.grey = True
        elif colortype == 3: #Indexed (Palette)
            self.flipped = True            
            if bitdepth == 8:
                self.Process_indexed_8bit()
            elif bitdepth == 4:
                self.Process_indexed_4bit()
            elif bitdepth == 2:
                self.Process_indexed_2bit()
            else:
                self.Process_indexed_1bit()
                self.RGBA.mono = True
            self.RGBA.indexed = True
        elif colortype == 2: #RGB 
            if bitdepth == 8:
                self.Process_RGB_24bit()
            else:
                self.Process_RGB_48bit()
        elif colortype == 0: #Greyscale
            self.flipped = True
            if bitdepth == 16:
                self.Process_grey_16bit()
            elif bitdepth == 8:
                self.Process_grey_8bit()
            elif bitdepth == 4:
                self.Process_grey_4bit()
            elif bitdepth == 2:
                self.Process_grey_2bit()
            else:
                self.Process_grey_1bit()
                self.RGBA.mono = True
            self.RGBA.grey = True
        if self.interlaced: self.DeInterlace()
                
    def Process_palette(self,data):
        l=len(data)
        self.palette = array.array('L',chr(0)*((l/3)*4))
        i=0
        p=0
        while p < l:
            self.palette[i] = unpack('L',data[p:p+3] + chr(255))[0]
            p+=3
            i+=1
            
    def DeInterlace(self):
        # 1 6 4 6 2 6 4 6
        # 7 7 7 7 7 7 7 7
        # 5 6 5 6 5 6 5 6
        # 7 7 7 7 7 7 7 7
        # 3 6 4 6 3 6 4 6
        # 7 7 7 7 7 7 7 7
        # 5 6 5 6 5 6 5 6
        # 7 7 7 7 7 7 7 7
        # Good for testimg the De-Filtered data
        self.RGBA.Pixel_mode()
        data = self.RGBA.data[:]
        pos = 0
        
        for xi,y,xjump,yjump in ((0,0,8,8),
                                 (4,0,8,8),
                                 (0,4,4,8),
                                 (2,0,4,4),
                                 (0,2,2,4),
                                 (1,0,2,2),
                                 (0,1,1,2)):
            while y < self.height:
                x=xi
                while x < self.width:
                    if pos >= len(data): break
                    self.RGBA.data[(y*self.width)+x] = data[pos]
                    x+=xjump
                    pos+=1
                if pos >= len(data): break
                y+=yjump
                
    def DeFilter_interlaced_rows(self,data,width,height,row_l):
        x=0
        l = row_l*height
        self.Init_filter()
        while x < l:
            flt = data.pop(x)
            if flt < 5: data[x:x+row_l] = self.filter[flt](self,x,data[x:x+row_l])
            x+=row_l
        return data

    def Read_interlaced_image_data(self):
        f = openfile(self.file,'rb')
        data = ''
        s = self.data_offsets.keys()
        s.sort()
        for k in s:
            f.seek(k,0)
            data += f.read(self.data_offsets[k])
        self.unprocessed = array.array('B',chr(0)*int(self.width*self.height*self.sourceBpp))
        step = []
        step.append( ( ((self.width+((8-self.width%8)%8))/8) , ((self.height+((8-self.height%8)%8))/8) ) )
        step.append( ( ((self.width+((4-self.width%4)%4))/8) , ((self.height+((8-self.height%8)%8))/8) ) )
        step.append( ( ((self.width+((4-self.width%4)%4))/4) , ((self.height+((4-self.height%4)%4))/8) ) )
        step.append( ( ((self.width+((2-self.width%2)%2))/4) , ((self.height+((4-self.height%4)%4))/4) ) )
        step.append( ( ((self.width+self.width%2)/2) , ((self.height+((2-self.height%2)%2))/4) ) )
        step.append( ( (self.width/2) , ((self.height+self.height%2)/2) ) )
        step.append( ( (self.width),(self.height/2) ) )
        start = 0
        d = array.array('B')
        data = zlib.decompress(data)
        sb=0
        for width,height in step:
            size = int(width*self.sourceBpp+1) * height
            row_l = int(width*self.sourceBpp)
            if self.sourceBpp == 0.125:
                row_l = int((width + (8-width % 8)%8)/8)
                size = (row_l+1) * height
            elif self.sourceBpp == 0.250:
                row_l = int((width + (4-width % 4)%4)/4)
                size = (row_l+1) * height
            elif self.sourceBpp == 0.5:
                row_l = int((width + (2-width % 2)%2)/2)
                size = (row_l+1) * height
            tmp = array.array('B',data[start:start+size])
            tmp =  self.DeFilter_interlaced_rows(tmp,width,height,row_l)
            if self.sourceBpp < 1:
                d+= self.Byte_convert(tmp,width)
            else:
                d += tmp
            start+=size
            sb+=1
        f.close()
        self.unprocessed = d

    def Byte_convert(self,data,wid):
        byted = array.array('B')
        l=len(data)
        x=0
        z=1
        if self.sourceBpp == 0.125:
            m = 256;ss=1
        elif self.sourceBpp == 0.250:
            m = 64;ss=2
        elif self.sourceBpp == 0.5:
            m = 16;ss=4
        while x < l:
            c=7
            s=128
            byte = data[x]
            while c >= 0:
                if z > wid and wid%8:
                    z=1
                    break
                val = ((byte & s)>>c) * m
                if val: val-=1
                byted += array.array('B',chr(val))
                s>>=ss
                c-=ss
                z+=1
            x+=1
        return byted
    
    def Process_RGBA_32bit(self):
        self.sourceBpp = 4
        self.Bps = self.width * self.sourceBpp
        self.Read_image_data('B')
        self.RGBA = RGBA_data(self.width,self.height,data=self.unprocessed)
        del self.unprocessed
        
    def Process_RGBA_64bit(self):
        self.sourceBpp = 8
        self.Bps = self.width * self.sourceBpp
        self.Read_image_data('B')
        x=0
        y=0
        l=len(self.unprocessed)
        self.RGBA = RGBA_data(self.width,self.height,mode='CHANNEL')
        while y < l:
            self.RGBA.data[x] = self.unprocessed[y]
            x+=1
            y+=2
        del self.unprocessed
    
    def Process_indexed_8bit(self):
        self.sourceBpp = 1
        self.Bps = self.width
        self.Process8bit()
        
    def Process_indexed_4bit(self):
        self.sourceBpp = 0.5
        self.Bps = (self.width + (2-self.width % 2)%2)/2
        self.Process4bit()
        
    def Process_indexed_2bit(self):
        self.sourceBpp = 0.25
        self.Bps = (self.width + (4-self.width % 4)%4)/4
        self.Process2bit()
        
    def Process_indexed_1bit(self):
        self.sourceBpp = 0.125
        self.Bps = (self.width + (8-self.width % 8)%8)/8
        self.Process1bit()
        
    def Process_RGB_24bit(self):
        self.sourceBpp = 3
        self.Bps = self.width * self.sourceBpp
        self.Read_image_data('B')
        x=0
        y=0
        l=len(self.unprocessed)
        self.RGBA = RGBA_data(self.width,self.height,mode='CHANNEL')
        while y < l:
            self.RGBA.data[x]   = self.unprocessed[y]
            self.RGBA.data[x+1] = self.unprocessed[y+1]
            self.RGBA.data[x+2] = self.unprocessed[y+2]
            x+=4
            y+=3
        del self.unprocessed
        
    def Process_RGB_48bit(self):
        self.sourceBpp = 6
        self.Bps = self.width * self.sourceBpp
        self.Read_image_data('B')
        x=0
        y=0
        l=len(self.unprocessed)
        self.RGBA = RGBA_data(self.width,self.height,mode='CHANNEL')
        while y < l:
            self.RGBA.data[x]   = self.unprocessed[y]
            self.RGBA.data[x+1] = self.unprocessed[y+2]
            self.RGBA.data[x+2] = self.unprocessed[y+4]
            x+=4
            y+=6
        del self.unprocessed
                
    def Get_image_dimensions(self):
        self.width = self.header['Width']
        self.height = self.header['Height']

    def Read_header(self):
        format = '>8sL4s2L5BL'
        f = openfile(self.file,'rb')
        f.seek(self.addr)

        self.header = {}
        self.header['Magic'],\
        self.header['HeadSize'],\
        self.header['HeaderType'],\
        self.header['Width'],\
        self.header['Height'],\
        self.header['Bitdepth'],\
        self.header['ColorType'],\
        self.header['FilterMethod'],\
        self.header['CompressionType'],\
        self.header['InterlaceType'],\
        self.header['HeadCRC'] = unpack(format,f.read(calcsize(format)))
        self.head_size = calcsize(format)
        type = None
        size = 0
        while not type == 'IEND':
            if size: f.seek(size+4,1)
            size,type = unpack('>L4s',f.read(8))
            if type =='IDAT':
                self.data_offsets[f.tell()] = size
            elif type =='PLTE':
                self.Process_palette(f.read(size))
                f.seek(4,1)
                size = 0
        self.size = size
        
        f.close()
        return True

    def Read_image_data(self,element_size):
        if self.interlaced:
            self.Read_interlaced_image_data()
            return
        f = openfile(self.file,'rb')
        data = ''
        s = self.data_offsets.keys()
        s.sort()
        for k in s:
            f.seek(k,0)
            data += f.read(self.data_offsets[k])
        data = zlib.decompress(data)
        self.unprocessed = array.array(element_size,data)
        f.close()
        self.De_filter_rows()

################################################################################
''' Class: XPM_image ''' 
################################################################################    
class XPM_image(Base_image):
    def __init__(self,addr=0,size=None,file=None,process=True):
        self.init()
        if not size:
            size = ospath_getsize(file)
        self.file_size = size
        self.file = file
        self.addr = addr
        self.size = size
        self.type = 'XPM'
        self.Read_header()
        self.size_of_plane = self.width * self.height
        self.Bps = self.width * self.sourceBpp
        self.Bpp = 4
        self.final_size = self.size_of_plane * self.Bpp
        self.RGBA = None
        if not process: return
        self.Process()

    def Process(self):
        self.RGBA = RGBA_data(self.width,self.height,fill=chr(255),mode='PIXEL')
        from namedrgb import NAMEDCOLOR
        self.named_color = NAMEDCOLOR
        import binascii
        f = openfile(self.file,'rb')
        for x in range(1,self.header['StartLine']):
            f.readline()
            
        self.palette = {}
        x=0
        cl = self.color_length
        while x < int(self.header['NumberOfColors']):
            data = f.readline()
            if not data.startswith('/'): 
                data = data.split('\"')[1]
                cc = data[0:cl]
                data = data[cl:].strip()
                if data[0] == 'c':
                    if 'c #' in data:
                        val = data.split('c #')[1] + 'FF'
                    else:
                        data.split(' ')[1]
                        val = self.Get_named_color(data.split(' ')[1])
                elif data[0] == 'm':
                    if 'm #' in data:
                        val = data.split('c #')[1] + 'FF'
                    else:
                        data.split(' ')[1]
                        val = self.Get_named_color(data.split(' ')[1])
                else:
                    val = '000000FF'
                self.palette[cc] = unpack('L',binascii.unhexlify(val))[0]
                x+=1
        pos=0
        y=0
        for line in f:
            if y > self.height-1: break
            if not line.startswith('/'): 
                data = line.split('\"')[1]
                if data == ',\n': break
                x=0
                l=len(data)
                while x < l:
                    self.RGBA.data[pos] = self.palette[data[x:x+cl]]
                    x+=cl
                    pos+=1
                y+=1
        f.close()
        del binascii
        del self.named_color
        del NAMEDCOLOR

    def Get_named_color(self,name):
        if name == 'None':
            return '00000000'
            self.RGBA.has_alpha = True
        else:
            return self.named_color[name.upper().replace(' ','')] + 'FF'
    
    def Read_header(self):
        f = openfile(self.file,'rb')
        f.seek(self.addr)
        x=0
        while 1:
            x+=1
            line = f.readline()
            if '\"' in line: break
        line = line.replace('\"','')
        line = line.replace(',\n','')
        line += ' '
        self.header = {}
        self.header['StartLine'] = x + 1
        
        self.header['Width'],\
        self.header['Height'],\
        self.header['NumberOfColors'],\
        self.header['ColorLength'],\
        nothing = line.split(' ',4)
        self.width = int(self.header['Width'])
        self.height = int(self.header['Height'])
        self.color_length = int(self.header['ColorLength'])
        self.sourceBpp = 3
        f.close()

################################################################################
''' Class: XBM_image ''' 
################################################################################    
class XBM_image(Base_image,Indexed_image):
    def __init__(self,addr=0,size=None,file=None,process=True):
        self.init()
        if not size:
            size = ospath_getsize(file)
        self.file_size = size
        self.file = file
        self.addr = addr
        self.size = size
        self.type = 'XBM'
        self.Read_header()
        self.size_of_plane = self.width * self.height
        self.Bps = self.width * self.sourceBpp
        self.Bpp = 4
        self.final_size = self.size_of_plane * self.Bpp
        self.RGBA = None
        if not process: return
        self.Process()
        self.RGBA.mono = True

    def Process(self):
        self.RGBA = RGBA_data(self.width,self.height,fill=chr(255),mode='PIXEL')
        import binascii
        f = openfile(self.file,'rb')
        for x in range(1,self.header['StartLine']):
            f.readline()
        
        self.unprocessed = ''
        for line in f:
            line = line.replace(';','').replace('}','').replace('\n','').replace(' ','').replace('0x','')
            vals = line.split(',')
            for v in vals:
                v = v[2:4] + v[0:2]
                if v: self.unprocessed += binascii.unhexlify(v)
        f.close()
        del binascii
        self.unprocessed = array.array('B',self.unprocessed)

        self.RGBA = RGBA_data(self.width,self.height,fill=chr(255),mode='PIXEL')
        pos=0
        y=0
        while y < self.height:
            x=0
            while x < self.width:
                byte = self.unprocessed[pos]
                k = 1
                while k < 256:
                    if x >= self.width: break
                    if (byte & k): self.RGBA.data[y*self.width+x] = 4278190080
                    k<<=1
                    x+=1
                pos+=1
            y+=1
        
    def Read_header(self):
        f = openfile(self.file,'rb')
        f.seek(self.addr)
        self.header = {}
        x=0
        while 1:
            x+=1
            line = f.readline()
            if 'width' in line:
                self.header['Width'] = line.split('width')[-1].split(' ')[-1].replace('\n','')
            elif 'height' in line:
                self.header['Height'] = line.split('height')[-1].split(' ')[-1].replace('\n','')
            elif '{' in line:
                break
        if '0x' in line:
            self.header['StartLine'] = x
        else:
            self.header['StartLine'] = x+1
            
        self.width = int(self.header['Width'])
        self.height = int(self.header['Height'])
        self.sourceBpp = 0.125
        f.close()
        
################################################################################
''' Class: SaveImage_base '''
################################################################################
class SaveImage_base:
    def RGBA_to_BGR_string(self,pad=0):
        if self.RGBA.has_alpha: Manipulator(image=self.RGBA).Alpha_to_color()
        temp = array.array('B',self.RGBA.data.tostring())
        out = array.array('B',chr(0)*((self.width+pad)*self.height*3))
        x=0
        y=self.height-1
        pos=0
        Bpp = self.RGBA.Bpp
        row_l = self.width * Bpp
        while y > -1:
            x=0
            while x < row_l:
                loc = y * row_l + x
                out[pos]   = temp[loc+2]
                out[pos+1] = temp[loc+1]
                out[pos+2] = temp[loc]
                pos+=3
                x+=Bpp
            pos+=pad
            y-=1
        return out.tostring()

    def Create_palette_quick(self):
        pal = array.array('B',chr(255)*1012)
        x = 0
        for r in range(5,256,50):
            for g in range(3,256,42):
                for b in range(5,256,50):
                    pal[x] = r
                    pal[x+1] = g
                    pal[x+2] = b
                    x+=4
        pal.append(0)
        pal.append(0)
        pal.append(0)
        pal.append(0)
        return pal

    def Create_palette(self):
        if self.RGBA.has_alpha: Manipulator(image=self.RGBA).Alpha_to_color()
        self.RGBA.Pixel_mode()
        pixels = {}
        l = len(self.RGBA.data)
        x=0
        div=1
        if l > 2047:
            div = int(l/1024)
            div = div + (div%4)
        while x < l:
            pix = self.RGBA.data[x]
            if not pixels.has_key(pix):
                pixels[pix] = 1
            x+=div
        return array.array('B',array.array('L',pixels.keys()[0:256]).tostring())
        
    def Create_indexed_image(self,pad=0,flip=False):
        palette = self.Create_palette()
        if flip: Manipulator(image=self.RGBA).Flip() #Do something smarter here please :) -----------------FIX
        temp = array.array('B',self.RGBA.data.tostring())
        if flip: Manipulator(image=self.RGBA).Flip()
        image = array.array('B',chr(0)*((self.width+pad)*self.height))
        o=0
        i=0
        w=0
        l=len(image)
        lp=len(palette)
        while i < l:
            if w >= self.width:
                w=0
                i+=pad
            r = temp[o]
            g = temp[o+1]
            b = temp[o+2]
            p=0
            lastdiff=65536
            pal=0
            pn=0
            while p < lp:
                rdif = r - palette[p]
                gdif = g - palette[p+1]
                bdif = b - palette[p+2]
                if rdif < 0: rdif *= -1
                if gdif < 0: gdif *= -1
                if bdif < 0: bdif *= -1
                diff = rdif+gdif+bdif
                if diff < lastdiff:
                    lastdiff = diff
                    pal = pn
                pn+=1
                p+=4
            image[i]=pal
            i+=1
            o+=4
            w+=1
        x=0
        l = len(palette)
        if self.order == 'BGR':
            while x < lp:
                t=palette[x]
                palette[x] = palette[x+2]
                palette[x+2] = t
                x+=4
        return palette[0:lp].tostring(),image.tostring()
    
################################################################################
''' Class: BGR_to_BMP '''
################################################################################
class BGR_to_BMP(SaveImage_base):
    headerSize=40
    planes=1
    headerFormat = '<2siI4i2h6i'
    order = 'BGR'
    def __init__(self,image,filename,type):
        self.RGBA = image
        self.height = image.height
        self.width = image.width
        self.file = filename
        self.dataOffset = 54
        self.compress=0
        self.clrUsed=0
        self.clrImportant=0
        if type   == '16':
            ps = (4-((self.width*2)%4))%4
            self.data = self.RGBA_to_BGR_string(pad=ps)
            self.Write_16bit()
        elif type == '24':
            ps = (4-((self.width*3)%4))%4
            self.data = self.RGBA_to_BGR_string(pad=ps)
            self.Write_24bit()
        elif type == '32':
            self.data = self.RGBA_to_BGR_string()
            self.Write_32bit()
        elif type == '8':
            ps = (4-((self.width)%4))%4
            self.data = self.Create_indexed_image(pad=ps,flip=True)
            self.Write_8bit()
        else:
            ps = (4-((self.width*3)%4))%4
            self.data = self.RGBA_to_BGR_string(pad=ps)
            self.Write_24bit()
            
    def Write_8bit(self):
        palette,self.data = self.data
        self.bitcount = 8
        self.dataOffset = 54 + len(palette)
        self.clrUsed=len(palette)/4
        self.clrImportant=len(palette)/4
        f = openfile(self.file,'wb')
        f.write(self.Create_header())
        f.write(palette)
        f.write(self.data)
        f.close()
        
    def Write_16bit(self):
        temp = array.array('B',self.data)
        out = array.array('H',chr(0)*((len(temp)/3)*2))
        x=0
        pos=0
        l=len(temp)
        while x < l:
            out[pos] = ((temp[x+2] & 240) << 7) |\
                       ((temp[x+1] & 248) << 2) |\
                       (temp[x] >> 3)
            pos +=1
            x+=3
        self.data = out.tostring()
        self.bitcount = 16
        f = openfile(self.file,'wb')
        f.write(self.Create_header())
        f.write(self.data)
        f.close()

    def Write_24bit(self):
        self.bitcount = 24
        f = openfile(self.file,'wb')
        f.write(self.Create_header())
        f.write(self.data)
        f.close()

    def Write_32bit(self):
        temp = array.array('B',self.data)
        out = array.array('B',chr(0)*((len(temp)/3)*4))
        x=0
        pos=0
        l=len(temp)
        while x < l:
            out[pos]   = temp[x]
            out[pos+1] = temp[x+1]
            out[pos+2] = temp[x+2]
            out[pos+3] = 0
            pos+=4
            x+=3
        self.data = out.tostring()
        self.bitcount = 32
        f = openfile(self.file,'wb')
        f.write(self.Create_header())
        f.write(self.data)
        f.close()
        
    def Create_header(self):
        XPPM=2834
        YPPM=2834
        fSize=self.dataOffset + len(self.data)
        imgSize=len(self.data)
        header = pack(self.headerFormat,'BM',
                             fSize,
                             0,
                             self.dataOffset,
                             self.headerSize,
                             self.width,
                             self.height,
                             self.planes,
                             self.bitcount,
                             self.compress,
                             imgSize,
                             XPPM,
                             YPPM,
                             self.clrUsed,
                             self.clrImportant)
        return header
    
################################################################################
''' Class: RGBA_to_PNG '''
################################################################################
class RGBA_to_PNG(SaveImage_base):
    order = 'RGB'
    
    def __init__(self,rgba_data,file,type='RGBA8',filter=0,compression=6):
        self.RGBA = rgba_data
        height = self.height = self.RGBA.height
        width = self.width = self.RGBA.width
        rgba_data = self.RGBA.data.tostring()
        palette = False
        filtered = ''
        if type == 'RGBA8':
            self.Bpp = 4
            self.bitdepth = 8
            self.type = 6
        elif type == 'RGB8':
            self.Bpp = 3
            self.bitdepth = 8
            self.type = 2
            data = rgba_data
            rgba_data = ''
            x=0
            while x < len(data):
                rgba_data += data[x]
                rgba_data += data[x+1]
                rgba_data += data[x+2]
                x+=4
        elif type == 'GREY8':
            self.Bpp = 1
            self.bitdepth = 8
            self.type = 0
            data = rgba_data
            rgba_data = ''
            x=0
            while x < len(data):
                rgba_data += chr(int((ord(data[x]) + ord(data[x+1]) + ord(data[x+2]))/3))
                x+=4
        elif type == 'GREYA8':
            self.Bpp = 2
            self.bitdepth = 8
            self.type = 4
            data = rgba_data
            rgba_data = ''
            x=0
            while x < len(data):
                rgba_data += chr(int((ord(data[x]) + ord(data[x+1]) + ord(data[x+2]))/3)) + data[x+3]
                x+=4
        elif type == 'INDEX8':
            self.Bpp = 1
            self.bitdepth = 8
            self.type = 3
            filter = 0
            pal, rgba_data = self.Create_indexed_image()
            x=0
            palette = ''
            while x < len(pal):
                palette += pal[x:x+3]
                x+=4
            del pal
        row_l = width * self.Bpp
        
        # Separate these so non-filtering is as fast as possible
        if filter:
            self.over = array.array('B',chr(0) * row_l)
            self.filterBpp = self.Bpp
            rgba_data = array.array('B',rgba_data)
            if filter == 6:
                for x in range(0,height): filtered += self.Filter_adaptive(rgba_data[x*row_l:x*row_l+row_l],x)
            elif filter == 5:
                for x in range(0,height): filtered += self.Filter_smart(rgba_data[x*row_l:x*row_l+row_l])
            elif filter == 4:
                for x in range(0,height): filtered += self.Filter_4(rgba_data[x*row_l:x*row_l+row_l])
            elif filter == 3:
                for x in range(0,height): filtered += self.Filter_3(rgba_data[x*row_l:x*row_l+row_l])
            elif filter == 2:
                for x in range(0,height): filtered += self.Filter_2(rgba_data[x*row_l:x*row_l+row_l])
            else:
                for x in range(0,height): filtered += self.Filter_1(rgba_data[x*row_l:x*row_l+row_l])
        else:
            zero = chr(0)
            for x in range(0,height): filtered += zero + rgba_data[x*row_l:x*row_l+row_l]
        del rgba_data
        signature = chr(0x89) + 'PNG' + chr(0x0d) + chr(0x0a) + chr(0x1a) + chr(0x0a)
        header = pack('>LL5B',width,height,self.bitdepth,self.type,0,0,0)
        header_chunk = self.Create_chunk('IHDR',header)
        data_chunk = self.Create_chunk('IDAT',zlib.compress(filtered,compression))
        end_chunk = self.Create_chunk('IEND','')
        f=openfile(file,'wb')
        f.write(signature)
        f.write(header_chunk)
        if palette: f.write(self.Create_chunk('PLTE',palette))
        f.write(data_chunk)
        f.write(end_chunk)
        f.close()
        
    def Filter_0(self,data): #None
        self.over = data
        return data
    
    def Filter_1(self,data): #Left
        raw = data[:]
        l=len(data);x=0
        while x < l:
            left = x - self.filterBpp
            if left < 0:
                left = 0
            else:
                left = raw[left]
            data[x] = (raw[x] - left) % 256
            x+=1
        self.over = raw
        data.insert(0,1)
        return data.tostring()
    
    def Filter_2(self,data): #Up
        raw = data[:]
        row_l = len(data)
        x=0
        while x < row_l:
            data[x] = (raw[x] - self.over[x]) % 256
            x+=1
        self.over = raw
        data.insert(0,2)
        return data.tostring()

    def Filter_3(self,data): #Average
        raw = data[:]
        row_l = len(data)
        x=0
        while x < row_l:
            left = x - self.filterBpp
            if left < 0:
                left = 0
            else:
                left = raw[left]
            above = self.over[x]
            data[x] = (raw[x] - ((left + above)/2)) % 256
            x+=1
        self.over = raw
        data.insert(0,3)
        return data.tostring()
    
    def Filter_4(self,data): #Paeth
        row_l = len(data)
        raw = data[:]
        x=0
        while x < row_l:
            left = x - self.filterBpp
            if left < 0:
                left = 0
                above_left = 0
            else:
                left = raw[left]   
                above_left = self.over[x - self.filterBpp]
            above = self.over[x]
            data[x] = (raw[x] - self.PaethPredictor(left,above,above_left)) % 256
            x+=1
        self.over = raw
        data.insert(0,4)
        return data.tostring()
        
    def PaethPredictor(self,l,a,ul):
        p = l + a - ul        # initial estimate
        pa = abs(p - l)     # distances to a, b, c
        pb = abs(p - a)
        pc = abs(p - ul)
        # return nearest of a,b,c,
        # breaking ties in order a,b,c.
        if pa <= pb and pa <= pc:
            return l
        elif pb <= pc:
            return a
        else:
            return ul
        
    def Filter_test(self,data,type):
        row_l = len(data)
        x=0
        val = 0
        test = {}
        while x < row_l:
            left = x - self.filterBpp
            if left < 0:
                left = 0
                above_left = 0
            else:
                left = data[left]   
                above_left = self.over[x - self.filterBpp]
            above = self.over[x]
            mod = 0
            if type == 0:
                mod = data[x]
            elif type == 1:
                mod = (data[x] - left)%256
            elif type == 2:
                mod = (data[x] - above)%256
            elif type == 3:
                mod = (data[x] - ((left + above)/2))%256
            elif type == 4:
                mod = (data[x] - self.PaethPredictor(left,above,above_left))%256
            if mod > 127: mod = 256 - mod
            val += mod
            test[mod] = 1
            x+=1
        self.temp = test
        test.update(self.last)
        return len(test.keys()) * val
    
    def Filter_adaptive(self,row_data,pos):
        #row_l = len(row_data)
        type = 0
        last = None
        self.last = {}
        for x in (0,1,2,3,4):
            #y = 1
            val = self.Filter_test(row_data,x)
            if val <= last or last == None:
                lt = self.temp
                last = val
                type = x
        self.last = lt
        if type == 0:
            return chr(0) + row_data.tostring()
        elif type == 1:
            return self.Filter_1(row_data)
        elif type == 2:
            return self.Filter_2(row_data)
        elif type == 3:
            return self.Filter_3(row_data)
        elif type == 4:
            return self.Filter_4(row_data)
                
    def Filter_smart(self,row_data):
        return self.Filter_4(row_data)
    
    def Create_chunk(self,type,data):
        format = '>L4s' + str(len(data)) + 'sL'
        return pack(format,len(data),type,data,self.CRC(type + data) & 0xffffffff)
    
    def CRC(self,buf):
        return zlib.crc32(buf)

################################################################################
''' Class: RGBA_to_TGA '''
################################################################################
class RGBA_to_TGA(SaveImage_base):
    order = 'BGR'
    
    def __init__(self,rgba,file,type='BGR24',flip=False):
        self.RGBA = rgba
        self.file = file
        self.flip = flip
        
        self.height = self.RGBA.height
        self.width = self.RGBA.width
        
        self.ColorMapDepth = 0
        self.ColorMapLength = 0
        self.ColorMapOrigin = 0
        self.ColorMapType = 0
        self.ImageDescriptor = 0
        if self.flip:
            self.ImageDescriptor = 32
        
        if type == 'BGR32':
            self.BitsPerPixel = 32
            self.DataTypeCode = 2
            self.ImageDescriptor |= 8
            self.Write_32bit()
        elif type == 'BGR24':
            self.BitsPerPixel = 24
            self.DataTypeCode = 2
            self.Write_24bit()
        elif type == 'BGR16':
            self.BitsPerPixel = 16
            self.DataTypeCode = 2
            if self.RGBA.has_alpha: self.ImageDescriptor |= 1
            self.Write_16bit()
        elif type == 'BGR32RLE':
            self.BitsPerPixel = 32
            self.DataTypeCode = 10
            self.ImageDescriptor |= 8
            self.Write_32bit(rle=True)
        elif type == 'BGR24RLE':
            self.BitsPerPixel = 24
            self.DataTypeCode = 10
            self.Write_24bit(rle=True)
        elif type == 'BGR16RLE':
            self.BitsPerPixel = 16
            self.DataTypeCode = 10
            if self.RGBA.has_alpha: self.ImageDescriptor |= 1
            self.Write_16bit(rle=True)
        elif type == 'GREY16':
            self.BitsPerPixel = 16
            self.DataTypeCode = 3
            self.ImageDescriptor |= 8
            self.Write_grey(Bpp=2)
        elif type == 'GREY8':
            self.BitsPerPixel = 8
            self.DataTypeCode = 3
            self.Write_grey()
        elif type == 'GREY16RLE':
            self.BitsPerPixel = 16
            self.DataTypeCode = 11
            self.ImageDescriptor |= 8
            self.Write_grey(Bpp=2,rle=True)
        elif type == 'GREY8RLE':
            self.BitsPerPixel = 8
            self.DataTypeCode = 11
            self.Write_grey(rle=True)
        elif type == 'INDEX32':
            self.BitsPerPixel = 8
            self.DataTypeCode = 1
            self.ImageDescriptor |= 8
            self.Write_indexed(Bpp=4)
        elif type == 'INDEX24':
            self.BitsPerPixel = 8
            self.DataTypeCode = 1
            self.Write_indexed(Bpp=3)
        elif type == 'INDEX16':
            self.BitsPerPixel = 8
            self.DataTypeCode = 1
            self.Write_indexed(Bpp=2)
        elif type == 'INDEX32RLE':
            self.BitsPerPixel = 8
            self.DataTypeCode = 9
            self.ImageDescriptor |= 8
            self.Write_indexed(Bpp=4,rle=True)
        elif type == 'INDEX24RLE':
            self.BitsPerPixel = 8
            self.DataTypeCode = 9
            self.Write_indexed(Bpp=3,rle=True)
        elif type == 'INDEX16RLE':
            self.BitsPerPixel = 8
            self.DataTypeCode = 9
            self.Write_indexed(Bpp=2,rle=True)

    def Write_indexed(self,Bpp=3,rle=False):
        if self.RGBA.has_alpha: Manipulator(image=self.RGBA).Alpha_to_color()
        p,out = self.Create_indexed_image(flip=not self.flip)

        palette = ''
        l = len(p)
        x = 0
        self.ColorMapDepth = Bpp * 8
        self.ColorMapLength = len(p) / 4
        if Bpp == 4:
            palette = p
        elif Bpp == 3:
            while x < l:
                palette += p[x:x+3]
                x+=4
        elif Bpp == 2:
            palette = array.array('H',chr(0)*(len(p)/2))
            pos=0
            while x < l:
                palette[pos] = (((ord(p[x+2])   >> 3) << 10) |\
                                ((ord(p[x+1]) >> 3) << 5 ) |\
                                ((ord(p[x]) >> 3)     )) | 1
                pos+=1
                x+=4
            self.ColorMapDepth = 16
            self.ColorMapLength = len(palette)
        self.ColorMapType = 1

        self.Create_headers()

        if rle: out = self.RLE(array.array('B',out),bpp=1).tostring()
        
        f = openfile(self.file,'wb')
        f.write(self.header)
        f.write(palette)
        f.write(out)
        f.write(self.footer)
        f.close()

    def Write_32bit(self,rle=False):
        self.Create_headers()
        self.RGBA.Channel_mode()
        l=self.RGBA.Data_length()
        out = array.array('B',chr(0)* l)
        pos=0
        x=0
        row_l = self.width * 4
        if self.flip:
            y = 0
            compare = self.height * row_l
            it = row_l
        else:
            y = (self.height-1) * row_l
            it = 0 - row_l
            compare = it
            
        while y != compare:
            x=0
            while x < row_l:
                p = y + x
                out[pos]   = self.RGBA.data[p+2]
                out[pos+1] = self.RGBA.data[p+1]
                out[pos+2] = self.RGBA.data[p]
                out[pos+3] = self.RGBA.data[p+3]
                x+=4
                pos+=4
            y+=it
            
        if rle: out = self.RLE(out)

        f = openfile(self.file,'wb')
        f.write(self.header)
        f.write(out.tostring())
        f.write(self.footer)
        f.close()
        
    def Write_24bit(self,rle=False):
        self.Create_headers()
        if self.RGBA.has_alpha: Manipulator(image=self.RGBA).Alpha_to_color()
        if self.flip: Manipulator(image=self.RGBA).Flip() #FIX BGR conversion code to handle flipping ------------------------------------------------------FIX
        
        if rle:
            out = self.RLE(array.array('B',self.RGBA_to_BGR_string()),bpp=3).tostring()
        else:
            out = self.RGBA_to_BGR_string()
        if self.flip: Manipulator(image=self.RGBA).Flip() #FIX BGR conversion code to handle flipping ------------------------------------------------------FIX    
        f = openfile(self.file,'wb')
        f.write(self.header)
        f.write(out)
        f.write(self.footer)
        f.close()

    def Write_16bit(self,rle=False):
        self.Create_headers()
        self.RGBA.Channel_mode()
        out = array.array('H',chr(0)*((len(self.RGBA.data)/3)*2))
        pos=0
        x=0
        row_l = self.width * 4
        if self.flip:
            y = 0
            compare = self.height * row_l
            it = row_l
        else:
            y = (self.height-1) * row_l
            it = 0 - row_l
            compare = it
            
        while y != compare:
            x=0
            while x < row_l:
                p = y + x
                alpha = 0
                if self.RGBA.data[p+3]: alpha = 1
                out[pos] = (((self.RGBA.data[p] >> 3) << 10) |\
                            ((self.RGBA.data[p+1] >> 3) << 5 ) |\
                            ((self.RGBA.data[p+2]   >> 3)     )) | alpha
                pos +=1
                x+=4
            y+=it

        if rle: out = self.RLE(array.array('B',out.tostring()),bpp=2)
        
        f = openfile(self.file,'wb')
        f.write(self.header)
        f.write(out.tostring())
        f.write(self.footer)
        f.close()
        
    def Write_grey(self,Bpp=1,rle=False):
        self.Create_headers()
        if Bpp == 1:
            if self.RGBA.has_alpha: Manipulator(image=self.RGBA).Alpha_to_color()
            
        out = array.array('B')
        self.RGBA.Channel_mode()

        x=0
        l = len(self.RGBA.data)
        
        if not self.RGBA.grey:
            while x < l:
                out.append((self.RGBA.data[x] + self.RGBA.data[x+1] + self.RGBA.data[x+2])/3)
                if Bpp == 2: out.append(self.RGBA.data[x+3])
                x+=4
        else:
            while x < l:
                out.append(self.RGBA.data[x])
                if Bpp == 2: out.append(self.RGBA.data[x+3])
                x+=4
                
        if rle: out = self.RLE(out,bpp=Bpp)
        
        f = openfile(self.file,'wb')
        f.write(self.header)
        f.write(out.tostring())
        f.write(self.footer)
        f.close()
        
    def RLE(self,out,bpp=4):
        temp = out[:]
        out = array.array('B')
        x=0
        l = len(temp)
        r_len = 128 * bpp
        last = (99999,) * bpp
        rep = 0
        run = 0
        while x < l:
            y=0
            while y < r_len:
                if x + y+(bpp-1) > l: break
                val = temp[x+y:x+y+bpp]
                if val == last:
                    if run: break
                    rep += 1
                else:
                    if rep: break
                    run += 1
                last = val[:]
                y+=bpp
            p=0
            if rep:
                out.append(128 | rep-1)
                z=0
                while z < bpp:
                    out.append(temp[x+z])
                    z+=1
            else:
                out.append(run-1)
                while p < run*bpp:
                    out.append(temp[x+p])
                    p+=1
            run = 0
            rep = 0
            x+=y
        return out
        
    def Create_headers(self):
        format = '<3B2HB4H2B'

        self.header = pack(format,0,
                                  self.ColorMapType,
                                  self.DataTypeCode,
                                  self.ColorMapOrigin,
                                  self.ColorMapLength,
                                  self.ColorMapDepth,
                                  0, # xOrigin
                                  0, # yOrigin
                                  self.width,
                                  self.height,
                                  self.BitsPerPixel,
                                  self.ImageDescriptor)
        
        format = '<2L16scB'

        self.footer = pack(format,0,
                                  0,
                                  'TRUEVISION-XFILE',
                                  '.',
                                  0)

################################################################################
''' Class: RGBA_to_XPM '''
################################################################################
class RGBA_to_XPM(SaveImage_base):
    order = 'RGB'
    
    def __init__(self,rgba,file):
        self.RGBA = rgba
        self.file = file
        
        self.height = self.RGBA.height
        self.width = self.RGBA.width
        
        chrs = """.!"#$%&'*+,-/:;<=>@^_`~ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789()[]{}|"""
        cl = len(chrs)

        self.RGBA.Pixel_mode()
        self.RGBA.data.byteswap()
        l = len(self.RGBA.data)
        x=0
        pixels = {}
        while x < l:
            if self.RGBA.data[x] & 255:
                pix = (self.RGBA.data[x] >> 8)
                if not pixels.has_key(pix): pixels[pix] = 1
            x+=1
        colors = pixels.keys()
        num = len(colors)
        test = num
        color_width = 1
        while test > cl:
            test = test/cl
            color_width += 1
     
        pos=0
        done = []
        list = []
        space = ' ' * color_width
        f = openfile(self.file,'w')
        f.write('/* XPM */\nstatic char * Image_xpm[] = {\n')
        f.write('"'+ str(self.width) +' '+ str(self.height) +' '+ str(num+1) +' '+ str(color_width) +'",\n')
        f.write('"' + (' ' * color_width) + '\tc None",\n')
        palette = {'c None':' '*color_width}
        while pos < num:
            for c in chrs:
                if done:
                    for d in done:
                        if pos >= num: break
                        cc = d + c
                        list.append(cc)
                        char = (cc+space)[0:color_width]
                        val = 'c #' + Hex6(colors[pos])
                        f.write('"' + char + '\t' + val + '",\n')
                        palette[val] = char
                        pos+=1
                else:
                    if pos >= num: break
                    list.append(c)
                    cc=c
                    char = (cc+space)[0:color_width]
                    val = 'c #' + Hex6(colors[pos])
                    f.write('"' + char + '\t' + val + '",\n')
                    palette[val] = char
                    pos+=1
            done = list
            list = []
        y=0
        line = ''
        while y < self.height:
            if line: line += '",\n'
            f.write(line)
            line = '"'
            x=0
            while x < self.width:
                pix = self.RGBA.data[y*self.width+x]
                if not pix & 255:
                    line += palette['c None']
                else:
                    line += palette['c #' + Hex6(pix >> 8)]
                x+=1
            y+=1
            
        f.write(line + '"}\n')
        f.close()
        self.RGBA.data.byteswap()

################################################################################
''' Class: RGBA_to_XBM '''
################################################################################
class RGBA_to_XBM(SaveImage_base):
    order = 'RGB'
    
    def __init__(self,rgba,file):
        self.RGBA = rgba
        if self.RGBA.has_alpha: Manipulator(image=self.RGBA).Alpha_to_color()
        self.RGBA.Channel_mode()
        self.file = file
        
        self.height = self.RGBA.height
        self.width = self.RGBA.width

        l = len(self.RGBA.data)
        out = ''
        if self.RGBA.mono or self.RGBA.grey:
            print 'test'
            y=0
            x=0
            #row_l = self.width * 4
            while y < self.height:
                w=0
                row = ''
                while w < self.width:    
                    row += chr((self.RGBA.data[x]+self.RGBA.data[x+1]+self.RGBA.data[x+2])/3)
                    w+=1
                    x+=4
                if self.RGBA.mono:
                    out += imageop.grey2mono(row,self.width,1,127)
                else:
                    out += imageop.dither2mono(row,self.width,1)
                y+=1
        else:
            y=0
            x=0
            #row_l = self.width * 4
            while y < self.height:
                w=0
                row = ''
                while w < self.width:    
                    row += chr((self.RGBA.data[x]+self.RGBA.data[x+1]+self.RGBA.data[x+2])/3)
                    w+=1
                    x+=4
                out += imageop.dither2mono(row,self.width,1)
                y+=1
        f = openfile(self.file,'w')
        f.write('#define iu_width ' + str(self.width) + '\n' + '#define iu_height ' + str(self.height) + '\n' + 'static char iu_bits[] = {\n')

        out = array.array('B',out)
        x=0
        l = len(out)
        line = ''
        while x < l:
            if line: f.write(' ' + line + ',\n')
            line = ''
            y=0
            while y < 15:
                if x >= l: break
                if line: line += ','
                b = out[x]
                bb = 0
                k = 128
                c=7
                d=0
                while k:
                    bb |= (((b & k) >> c)<<d)
                    k>>=1
                    c-=1
                    d+=1
                val = hex(~bb)
                if len(val) < 4: val = val.replace('0x','0x0')
                line+=val
                x+=1
                y+=1
        f.write(' ' + line + '};\n')
        f.close()
            
def Hex4(val):
    return ('000' + hex(val).split('x')[1].replace('L',''))[-4:]

def Hex6(val):
    return ('00000' + hex(val).split('x')[1].replace('L',''))[-6:]

def Hex8(val):
    return ('0000000' + hex(val).split('x')[1].replace('L',''))[-8:]

################################################################################
### Function: Get_image
################################################################################    
def Get_image(mipmap=0,addr=0,size=None,file=None,process=True,options=None):
    if not file:
        return None

    f = openfile(file,'rb')
    f.seek(addr)
    file_type = unpack('4s', f.read(4))[0]
    f.seek(0)
    f.close()
    try:
        if file_type == 'XPR0':
            return XPR0_image(mipmap=mipmap,addr=addr,size=size,file=file,process=process)
        elif file_type == 'DDS ':
            return DDS_image(mipmap=mipmap,addr=addr,size=size,file=file,process=process)
        elif file_type[:2] == 'BM':
            return BMP_image(addr=addr,size=size,file=file,process=process)
        elif file_type == chr(255) + chr(216) + chr(255) + chr(224):
            return JPEG_image(addr=addr,size=size,file=file,process=process)
        elif file_type == chr(137) + 'PNG':
            return PNG_image(addr=addr,size=size,file=file,process=process)
        elif file_type == '/* X':
            return XPM_image(addr=addr,size=size,file=file,process=process)
        else:
            ext = ospath_splitext(file)[1].upper()
            if ext == '.TGA':
                return TGA_image(addr=addr,size=size,file=file,process=process)
            elif ext == '.ICO':
                return ICO_image(addr=addr,size=size,file=file,process=process,options=options)
            elif ext == '.XBM':
                return XBM_image(addr=addr,size=size,file=file,process=process)
            elif ext == '.XPM':
                return XPM_image(addr=addr,size=size,file=file,process=process) #Just in case the first check doesn't work
        return None
    except:
        print file
        raise #Image_Error([type[0:3],file,sys.exc_info()[1]])
