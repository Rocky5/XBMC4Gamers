# Script by Rocky5
# This isn't the best way of doing this script but it works lol, hacky as I do :D

from binascii import hexlify, unhexlify
from os import getcwd, listdir, rename, remove
from os.path import getsize, isdir, isfile, join, splitext
from random import randrange
from shutil import copyfile, move
from struct import pack, unpack, calcsize
from xbmc import getFreeMem, log, LOGDEBUG, LOGERROR, LOGFATAL, LOGINFO
from xbmcgui import Dialog, DialogProgress

def extract_pf_titleid(xbe_file):
	with open(xbe_file, 'rb', buffering=4096) as xbe:
		xbe.seek(0x104)
		loadAddr=unpack('L', xbe.read(4))[0]
		xbe.seek(0x118)
		certLoc=unpack('L', xbe.read(4))[0]
		xbe.seek((certLoc - loadAddr)+8)
		id_data=unpack('L', xbe.read(4))
		xbe_title=''
		for dta in unpack("40H", xbe.read(calcsize("40H"))):
			try:
				if dta != 00:
					xbe_title += str(unichr(dta))
			except:
				pass
		return str(hex(id_data[0])[2:10]).upper().zfill(8)

def copy_file(list):
	for files in list.replace(' ','~').split():
		files=iter(' '.join(files.replace('|',' ').split()).split())
		for x in files:
			data=(x, next(files))
			data=[x.replace('~',' ') for x in data]
			old_names=data[0]
			new_names=data[1]
			if not isfile(join(file2patch,new_names)):
				copyfile(join(file2patch,old_names), join(file2patch,new_names))

def hex_raplace_file(list):
	for data in list.replace(' ','~').split():
		in_file=join(file2patch, data.replace('~',' ').split('|')[0])
		hex_bytes=iter(' '.join(data.replace('|',' ').split()[1:]).split())
		with open(in_file, 'r+b') as file:
			if getsize(in_file) >= (memory_left - (read_buffer / 2)): # Check if xbe fill fit in available memory
				file_cont=file.read(read_buffer)
				seek_file=0
				while file_cont:
					for x in hex_bytes:
						data=(x, next(hex_bytes), next(hex_bytes))
						data=[x.replace('~',' ') for x in data]
						patch_nub=data[0]
						old_bytes=data[1]
						new_bytes=data[2]
						if file_cont.find(old_bytes):
							file_cont=file_cont.replace(unhexlify(old_bytes),unhexlify(new_bytes),int(patch_nub))
					file.seek(seek_file)
					file.write(file_cont)
					seek_file+=read_buffer
					file_cont=file.read(read_buffer)
			else:
				file_cont=file.read()
				for x in hex_bytes:
					data=(x, next(hex_bytes), next(hex_bytes))
					data=[x.replace('~',' ') for x in data]
					patch_nub=data[0]
					old_bytes=data[1]
					new_bytes=data[2]
					if file_cont.find(old_bytes):
						file_cont=file_cont.replace(unhexlify(old_bytes),unhexlify(new_bytes),int(patch_nub))
				file.seek(0)
				file.write(file_cont)
				
def move_file(list):
	for files in list.replace(' ','~').split():
		files=iter(' '.join(files.replace('|',' ').split()).split())
		for x in files:
			data=(x, next(files))
			data=[x.replace('~',' ') for x in data]
			old_names=data[0]
			new_names=data[1]
			if isfile(join(file2patch,old_names)) and not isfile(join(file2patch,new_names)):
				move(join(file2patch,old_names), join(file2patch,new_names))

def offset_patch_file(list):
	for data in list.replace(' ','~').split():
		in_file=join(file2patch, data.replace('~',' ').split('|')[0])
		offsets_bytes=iter(' '.join(data.replace('|',' ').split()[1:]).split())
		with open(in_file, 'r+b', buffering=read_buffer) as file:
			for x in offsets_bytes:
				data=(x, next(offsets_bytes))
				data=[x.replace('~','') for x in data]
				offset=data[0]
				new_bytes=data[1]
				file.seek(int(offset))
				file.write(unhexlify(new_bytes))

def remove_file(list):
	for files in list.replace(' ','~').split():
		files=iter(' '.join(files.replace('|',' ').split()).split())
		files=[x.replace('~',' ') for x in files]
		for file_name in files:
			if isfile(join(file2patch,file_name)):
				remove(join(file2patch,file_name))

def rename_file(list):
	for files in list.replace(' ','~').split():
		files=iter(' '.join(files.replace('|',' ').split()).split())
		for x in files:
			data=(x, next(files))
			data=[x.replace('~',' ') for x in data]
			old_names=data[0]
			new_names=data[1]
			if isfile(join(file2patch,old_names)) and not isfile(join(file2patch,new_names)):
				rename(join(file2patch,old_names), join(file2patch,new_names))
				
if __name__ == "__main__":
	read_buffer=(1024 * 1024 * getFreeMem()) / 2 # left over memory divided by 2
	memory_left=(1024 * 1024 * getFreeMem()) # available memory in kb

	patches_folder=join(getcwd(), 'patches\\')
	files=[f[:-3] for f in sorted(listdir(patches_folder)) if f.endswith('.pf')]
	
	# this can be improved at a later date, but it works
	files=[splitext(x)[0].lower().replace('ct-','Certificate -').upper() for x in files]
	files=[splitext(x)[0].lower().replace('hd-','720p -').upper() for x in files]
	files=[splitext(x)[0].lower().replace('mp-','Multi Patch -').upper() for x in files]
	files=[splitext(x)[0].lower().replace('ot-','Other -').upper() for x in files]
	files=[splitext(x)[0].lower().replace('ws-','Widescreen Patch -').upper() for x in files]
	files=[splitext(x)[0].lower().replace('-a-','  -   Region Free\n  -  ').upper() for x in files]
	files=[splitext(x)[0].lower().replace('-p-','  -   PAL\n  -  ').upper() for x in files]
	files=[splitext(x)[0].lower().replace('-u-','  -   USA\n  -  ').upper() for x in files]
	files=[splitext(x)[0].lower().replace('-j-','  -   JPN\n  -  ').upper() for x in files]
	
	# select from list of found files
	choose_pf=Dialog().select("Select Patch File",files)
	
	if choose_pf != -1:
		patched_xbe=0; info_data=''; cp_data=''; hr_data=''; mv_data=''; of_data=''; rm_data=''; rn_data=''; title='Unknown'; pf_titleid='Unknown'; author='Unknown'; xbe_titleid=''; hr_file_check=''; of_file_check=''
		select_file=sorted(listdir(patches_folder))[choose_pf]
		patch_file=join(patches_folder, select_file)
		with open(patch_file, 'r') as patch_file:
			read_file=patch_file.readlines()
			for line in read_file:
				if '#' in line:
					if 'Game:' in line:
						title=line.rstrip().split('Game: ')[1]
					elif 'TitleID:' in line:
						pf_titleid=line.rstrip().split('TitleID: ')[1]
					elif 'Title ID:' in line:
						pf_titleid=line.rstrip().split('Title ID: ')[1]
					elif 'Author:' in line:
						author=line.rstrip().split('Author: ')[1]
					else:
						pass
				elif 'cp' in line.lower():
					cp_data=cp_data+line[3:]
				elif 'hr' in line.lower():
					hr_data=hr_data+line[3:]
				elif 'mv' in line.lower():
					mv_data=mv_data+line[3:]
				elif 'of' in line.lower():
					of_data=of_data+line[3:]
				elif 'rm' in line.lower():
					rm_data=rm_data+line[3:]
				elif 'rn' in line.lower():
					rn_data=rn_data+line[3:]
				else:
					pass

		file2patch=Dialog().browse(0, 'Select your "'+title+'" folder', "files") # select folder with file to patch

		if file2patch:

			pf_titleid = pf_titleid.upper()

			if cp_data != '': # copy is ran first so you can patch to different xbe name if you wish, worst case is you have a new xbe or file
				copy_file(cp_data)

			if hr_data != '': # check if hr_data is for an xbe and check is titleid
				check_if_xbe=join(file2patch, hr_data.split('|')[0])
				if hr_data.split('|')[0].lower().endswith('.xbe'):
					patched_xbe=1
					xbe_titleid=extract_pf_titleid(check_if_xbe).upper()
				else:
					patched_xbe=0
					xbe_titleid='Unknown'
			
			if of_data != '': # check if of_data is for an xbe and check is titleid
				check_if_xbe=join(file2patch, of_data.split('|')[0])
				if of_data.split('|')[0].lower().endswith('.xbe'):
					patched_xbe=1
					xbe_titleid=extract_pf_titleid(check_if_xbe).upper()
				else:
					patched_xbe=0
					xbe_titleid='Unknown'
			
			if xbe_titleid == pf_titleid or xbe_titleid == 'Unknown':

				if mv_data != '': # check for mv_data and move files
					move_file(mv_data)

				if hr_data != '': # check for hr_data and patch files
					hex_raplace_file(hr_data)

				if of_data != '': # check for of_data and patch files
					offset_patch_file(of_data)

				if rn_data != '': # check for rn_data and rename files
					rename_file(rn_data)

				if rm_data != '': # check for rm_data and remove files (this is last)
					remove_file(rm_data)

				if patched_xbe: # if it was an xbe then display this dialogue. Else its a file you patched
					Dialog().ok(title,'TitleId: '+pf_titleid,'Author: '+author,'Patch: '+select_file)
				else:
					Dialog().ok(title,'Patch applied','Author: '+author,'Patch: '+select_file)
			else: # error if the titleid doesn't match the xbe file
				Dialog().ok(title,'Error: Looking for ('+pf_titleid+') found ('+xbe_titleid+')','Author: '+author,'Patch: '+select_file)
