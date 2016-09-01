# -*- coding: utf-8 -*-

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

from struct import *
import array , sys
import zlib
from os.path import getsize as ospath_getsize, splitext as ospath_splitext
from limpp import Get_image as GET_IMAGE

def Get_image(mipmap=0,addr=0,size=None,file=None,process=True,options=None):
    return GET_IMAGE(mipmap=mipmap,addr=addr,size=size,file=file,process=process,options=options)
    
################################################################################
''' Class: XBE_Error '''
################################################################################
class XBE_Error(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
################################################################################
''' Class: XBE '''
################################################################################
class XBE:
    def __init__(self,file=None):
        self.file = file
        self.header = {}
        self.certificate = {}
        try:
            self.Read_header()
        except IOError,(errno,strerror):
            raise XBE_Error , ['MainHeader','File',strerror]
        except:
            raise XBE_Error , ['MainHeader','Unhandled',sys.exc_info()[0]]
        try:
            self.Read_certificate()
        except IOError,(errno,strerror):
            raise XBE_Error , ['Certificate','File',strerror]
        except:
            raise XBE_Error , ['Certificate','Unhandled',sys.exc_info()[0]]
        
    def Read_header(self):
        format = '4s256s8L4B20L'
        f = open(self.file,'rb')
        
        self.header['magic'],\
        self.header['digsig'],\
        self.header['base'],\
        self.header['sizeof_headers'],\
        self.header['sizeof_image'],\
        self.header['sizeof_image_header'],\
        self.header['timedate'],\
        self.header['certificate_addr'],\
        self.header['sections'],\
        self.header['section_headers_addr'],\
        self.header['init_flags.mount_utility_drive'],\
        self.header['init_flags.format_utility_drive'],\
        self.header['init_flags.limit_64mb'],\
        self.header['init_flags.dont_setup_harddisk'],\
        self.header['entry'],\
        self.header['tls_addr'],\
        self.header['pe_stack_commit'],\
        self.header['pe_heap_reserve'],\
        self.header['pe_heap_commit'],\
        self.header['pe_base_addr'],\
        self.header['pe_sizeof_image'],\
        self.header['pe_checksum'],\
        self.header['pe_timedate'],\
        self.header['debug_pathname_addr'],\
        self.header['debug_filename_addr'],\
        self.header['debug_unicode_filename_addr'],\
        self.header['kernel_image_thunk_addr'],\
        self.header['nonkernel_import_dir_addr'],\
        self.header['library_versions'],\
        self.header['library_versions_addr'],\
        self.header['kernel_library_version_addr'],\
        self.header['xapi_library_version_addr'],\
        self.header['logo_bitmap_addr'],\
        self.header['logo_bitmap_size'] = unpack(format,f.read(calcsize(format)))
        
        f.close()
        
    def Read_certificate(self):    
        format = '3L80s64s5L16s16s256s'
        f = open(self.file,'rb')
        f.seek(self.header['sizeof_image_header'])
        
        self.certificate['size'],\
        self.certificate['timedate'],\
        self.certificate['titleid'],\
        self.certificate['title_name'],\
        self.certificate['alt_title_id'],\
        self.certificate['allowed_media'],\
        self.certificate['game_region'],\
        self.certificate['game_ratings'],\
        self.certificate['disk_number'],\
        self.certificate['version'],\
        self.certificate['lan_key'],\
        self.certificate['sig_key'],\
        self.certificate['title_alt_sig_key'] = unpack(format,f.read(calcsize(format)))

        f.close()
        
    def Read_section(self,section_number):
        format = '4B6L2L20s'
        size = calcsize(format)
        offset = self.header['section_headers_addr'] - self.header['base']
        offset += (section_number - 1) * size
        f = open(self.file,'rb')
        f.seek(offset)

        pSection_Header = {}
        flags_byte,\
        pSection_Header['flags.unused_b1'],\
        pSection_Header['flags.unused_b2'],\
        pSection_Header['flags.unused_b3'],\
        pSection_Header['virtual_addr'],\
        pSection_Header['virtual_size'],\
        pSection_Header['raw_addr'],\
        pSection_Header['sizeof_raw'],\
        pSection_Header['section_name_addr'],\
        pSection_Header['section_reference_count'],\
        pSection_Header['head_shared_ref_count_addr'],\
        pSection_Header['tail_shared_ref_count_addr'],\
        pSection_Header['section_digest'] = unpack(format,f.read(size))
        f.close()
        pSection_Header['flags.writable'] =         (flags_byte >> 0) % 2
        pSection_Header['flags.preload'] =          (flags_byte >> 1) % 2
        pSection_Header['flags.executable'] =       (flags_byte >> 2) % 2
        pSection_Header['flags.inserted_file'] =    (flags_byte >> 3) % 2
        pSection_Header['flags.head_page_ro'] =     (flags_byte >> 4) % 2
        pSection_Header['flags.tail_page_ro'] =     (flags_byte >> 5) % 2
        pSection_Header['flags.unused_a1'] =        (flags_byte >> 6) % 2
        pSection_Header['flags.unused_a2'] =        (flags_byte >> 7) % 2
      
        f = open(self.file,'rb')
        try:
            offset = pSection_Header['section_name_addr'] - self.header['base']
            f.seek(offset)
            name = ''
            val = unpack('20s',f.read(20))
            val = val[0]
            for i in range(0,20):
                    if val[i] == "\x00": break
                    name += val[i]
        except:
            name = ''
            
        f.close()
        
        return name,pSection_Header
    
    def Read_version(self,addr):
        format = '8s4H'
        f = open(self.file,'rb')
        f.seek(addr)
        
        Version = {}
        name,\
        major,\
        minor,\
        build,\
        flags = unpack(format,f.read(calcsize(format)))
        
        f.close()
        
        name += chr(0)
        Version['name'],x = name.split(chr(0),1)
        Version['version'] = str(major) + '.' + str(minor) + '.' + str(build)
        '''' We need to seperate out the flags
        Version['flags.qfe_version'] 13 bits
        Version['flags.approved'] 2 bits
        Version['flags.debug_build'] 1 bit
        '''
        return Version

    def Read_library_version(self,num_0_based):
        addr = self.header['library_versions_addr'] - self.header['base'] + (num_0_based * 16)
        return self.Read_version(addr)
    
    def Read_kernel_version(self):
        return self.Read_version(self.header['kernel_library_version_addr'] - self.header['base'])
    
    def Read_XAPI_version(self):
        return self.Read_version(self.header['xapi_library_version_addr'] - self.header['base'])
    
    def Read_TLS(self):
        f = open(self.file,'rb')
        f.seek(self.header['tls_addr'] - self.header['base'])
        
        TLS = {}
        TLS['data_start_addr'],\
        TLS['data_end_addr'],\
        TLS['tls_index_addr'],\
        TLS['tls_callback_addr'],\
        TLS['sizeof_zero_fill'],\
        TLS['characteristics'] = unpack('6L',f.read(calcsize('6L')))

        f.close()
        return TLS
    
    def Get_title(self):
        return self.certificate['title_name'].decode('utf-16').rstrip(chr(0))
        
    def Get_timedate(self):
        from time import ctime
        t = ctime(self.certificate['timedate'])
        del ctime
        return t

    def Get_game_region(self):
        regions = { 0x00000001:'NA',
                    0x00000002:'Japan',
                    0x00000004:'World',
                    0x80000000:'Manufacturing'}
        try:
            return regions[self.certificate['game_region']]
        except:
            return 'Unknown'

    def Get_title_id(self):
        #hexst = str(hex(self.certificate['titleid'])).split('x')[1][:-1]
        hexst = str(hex(self.certificate['titleid'])).split('x')[1]
        return '00000000'[0:8-len(hexst)] + hexst
    
    def Get_allowed_media_string(self):
        am = self.certificate['allowed_media']
        if am == 0xC00001FFL: return 'ALL'
        if am == 0x400001FFL: return 'ALL (except NONSECURE MODE)'
        am_string = ''
        am_string2 = ''
        dvd_string = ''
        if am%2:        am_string +=  'HARD DISK, '           #0x00000001
        if (am>>1)%2:   dvd_string += 'X2,'                   #0x00000002
        if (am>>2)%2:   dvd_string += 'CD,'                   #0x00000004
        if (am>>3)%2:   am_string +=  'CD, '                  #0x00000008
        if (am>>4)%2:   dvd_string += '5 RO,'                 #0x00000010
        if (am>>5)%2:   dvd_string += '9 RO,'                 #0x00000020
        if (am>>6)%2:   dvd_string += '5 RW,'                 #0x00000040
        if (am>>7)%2:   dvd_string += '9 RW,'                 #0x00000080
        if (am>>8)%2:   am_string2 += 'DONGLE, '              #0x00000100
        if (am>>9)%2:   am_string2 += 'MEDIA BOARD, '         #0x00000200
        if (am>>30)%2:  am_string2 += 'NONSECURE HARD DISK, ' #0x40000000
        if (am>>31)%2:  am_string2 += 'NONSECURE MODE, '      #0x80000000
        if dvd_string: am_string += 'DVD (' + dvd_string[:-2] + '), '
        if am_string2: am_string += am_string2
        return am_string[:-2]
        #MEDIA MASK 0x00FFFFFF


    def Get_image_magic(self,addr):
        f = open(self.file,'rb')
        f.seek(addr)
        magic = unpack('4s',f.read(4))
        f.close()
        return magic[0][:3]
        
    def Get_image_info(self,type_string):
        found = 0
        for n in range(1,self.header['sections']):
            s_name , section = self.Read_section(n)
            if section['flags.inserted_file']:
                if s_name == type_string:
                    found = 1
                    break
        img_hdr = {}
        if found:
            magic = self.Get_image_magic(section['raw_addr'])
            if magic == 'XPR':
                return section
            elif magic == 'DDS':
                pass
            
        return False
        
    def Get_title_image(self):
        img_section = self.Get_image_info('$$XTIMAGE')
        if img_section:
            return Get_image(addr=img_section['raw_addr'],size=img_section['sizeof_raw'],file=self.file)
        else:
            return None
        
    def Get_save_image(self):
        img_section = self.Get_image_info('$$XSIMAGE')
        if img_section:
            return Get_image(addr=img_section['raw_addr'],size=img_section['sizeof_raw'],file=self.file)
        else:
            return None
        

