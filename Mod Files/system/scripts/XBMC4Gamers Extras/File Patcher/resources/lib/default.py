# -*- coding: utf-8 -*-
# Script by Rocky5

import logging
from binascii import hexlify, unhexlify
from os import getcwd, listdir, rename, remove
from os.path import getsize, isfile, join, splitext
from shutil import copyfile, move
from struct import unpack, calcsize
from xbmc import getFreeMem
from xbmcgui import Dialog

# set up logging
# logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO, format='\nFile Patcher:\n\t%(message)s')

def copy_file(file_list):
	for files in file_list.split():
		files = iter(' '.join(files.split('|')).split())
		for x in files:
			old_names, new_names = x, next(files)
			logging.info('Copying file from %s to %s', old_names, new_names)
			if old_names.lower().endswith('.xbe'):
				check_if_xbe = join(file2patch, old_names)
				xbe_titleid = extract_pf_titleid(check_if_xbe).upper()
				if xbe_titleid != pf_titleid and pf_titleid != 'MULTI':
					logging.error('TitleID mismatch: expected %s, found %s', pf_titleid, xbe_titleid)
					Dialog().ok('ERROR', 'Title: ' + title, 
								'Looking for (' + pf_titleid + ') found (' + xbe_titleid + ')', 
								'Patch: ' + arg.lower())
					raise Exception("TitleID doesn't match.")
			if isfile(join(file2patch, old_names)) and not isfile(join(file2patch, new_names)):
				copyfile(join(file2patch, old_names), join(file2patch, new_names))
				logging.info('File copied successfully')

def extract_pf_titleid(xbe_file):
	with open(xbe_file, 'rb', buffering=4096) as xbe:
		xbe.seek(0x104)
		loadAddr = unpack('L', xbe.read(4))[0]
		xbe.seek(0x118)
		certLoc = unpack('L', xbe.read(4))[0]
		xbe.seek((certLoc - loadAddr) + 8)
		id_data = unpack('L', xbe.read(4))
		xbe_title = ''
		for dta in unpack("40H", xbe.read(calcsize("40H"))):
			try:
				if dta != 0:
					xbe_title += str(unichr(dta))
			except:
				pass
		return str(hex(id_data[0])[2:10]).upper().zfill(8)

def hex_replace_file(file_list):
	memory_left = 1024 * 1024 * getFreeMem() # available memory in bytes
	read_buffer = 1024 * 1024 * 2 # 2MB

	for data in file_list.split():
		in_file = join(file2patch, data.split('|')[0])
		hex_bytes = iter(' '.join(data.split('|')[1:]).split())
		logging.info('Hex replacing in file %s', in_file)
		
		with open(in_file, 'r+b') as file:
			file_size = getsize(in_file)
			if file_size <= (memory_left - (memory_left / 4)): # if there isn't enough memory left to hold the xbe jump to a buffer.
				file_cont = file.read()
				for x in hex_bytes:
					patch_nub, old_bytes, new_bytes = x, next(hex_bytes), next(hex_bytes)
					if file_cont.find(old_bytes):
						logging.info('Found:\t%s\n Replaced:\t%s',old_bytes, new_bytes)
						file_cont = file_cont.replace(unhexlify(old_bytes), unhexlify(new_bytes), int(patch_nub))
				file.seek(0)
				file.write(file_cont)
				logging.info('Hex replace completed in memory')
			else:
				seek_file = 0
				while True:
					file_cont = file.read(read_buffer)
					if not file_cont: # end of file
						break
					for x in hex_bytes:
						patch_nub, old_bytes, new_bytes = x, next(hex_bytes), next(hex_bytes)
						if file_cont.find(old_bytes):
							logging.info('Found:\t%s\n Replaced:\t%s',old_bytes, new_bytes)
							file_cont = file_cont.replace(unhexlify(old_bytes), unhexlify(new_bytes), int(patch_nub))
					file.seek(seek_file)
					file.write(file_cont)
					seek_file += read_buffer
				logging.info('Hex replace completed with buffering')

def move_file(file_list):
	for files in file_list.split():
		files = iter(' '.join(files.split('|')).split())
		for x in files:
			old_names, new_names = x, next(files)
			old_path = join(file2patch, old_names)
			new_path = join(file2patch, new_names)
			logging.info('Moving file from %s to %s', old_path, new_path)
			if isfile(old_path) and not isfile(new_path):
				move(old_path, new_path)
				logging.info('File moved successfully')

def offset_patch_file(file_list):
	for data in file_list.split():
		in_file = join(file2patch, data.split('|')[0])
		offsets_bytes = iter(' '.join(data.split('|')[1:]).split())
		logging.info('Offset patching file %s', in_file)
		with open(in_file, 'r+b', buffering=4096) as file:
			for x in offsets_bytes:
				offset, new_bytes = x, next(offsets_bytes)
				file.seek(int(offset))
				file.write(unhexlify(new_bytes))
				logging.info('Patched offset %s with new bytes %s', offset, new_bytes)

def remove_file(file_list):
	for files in file_list.split():
		files = iter(' '.join(files.split('|')).split())
		for file_name in files:
			file_path = join(file2patch, file_name)
			logging.info('Removing file %s', file_path)
			if isfile(file_path):
				os.remove(file_path)
				logging.info('File removed successfully')

def rename_file(file_list):
	for files in file_list.split():
		files = iter(' '.join(files.split('|')).split())
		for x in files:
			old_names, new_names = x, next(files)
			old_path = join(file2patch, old_names)
			new_path = join(file2patch, new_names)
			logging.info('Renaming file from %s to %s', old_path, new_path)
			if isfile(old_path) and not isfile(new_path):
				os.rename(old_path, new_path)
				logging.info('File renamed successfully')

def supported_media(file_list):
	for data in file_list.split():
		in_file = join(file2patch, data.split('|')[0])
		new_bytes = iter(' '.join(data.split('|')[1:]).split())
		logging.info('Updating supported media in file %s', in_file)
		with open(in_file, 'r+b', buffering=4096) as xbe:
			xbe.seek(0x104)
			loadAddr = unpack('L', xbe.read(4))[0]
			xbe.seek(0x118)
			certLoc = unpack('L', xbe.read(4))[0]
			for x in new_bytes:
				xbe.seek((certLoc - loadAddr) + 156)
				xbe.write(unhexlify(swap_order(x)))
				logging.info('Patched media support with new bytes %s', x)

def supported_region(file_list):
	for data in file_list.split():
		in_file = join(file2patch, data.split('|')[0])
		new_bytes = iter(' '.join(data.split('|')[1:]).split())
		logging.info('Updating supported region in file %s', in_file)
		with open(in_file, 'r+b', buffering=4096) as xbe:
			xbe.seek(0x104)
			loadAddr = unpack('L', xbe.read(4))[0]
			xbe.seek(0x118)
			certLoc = unpack('L', xbe.read(4))[0]
			for x in new_bytes:
				xbe.seek((certLoc - loadAddr) + 160)
				xbe.write(unhexlify(swap_order(x)))
				logging.info('Patched region support with new bytes %s', x)
				
def swap_order(data, wsz=16, gsz=2): # https://stackoverflow.com/posts/36744477/revisions
	chunks = [data[i:i+wsz] for i in range(0, len(data), wsz)]
	swapped_chunks = ["".join([m[i:i+gsz] for i in range(wsz-gsz, -gsz, -gsz)]) for m in chunks]
	return "".join(swapped_chunks)
				
if __name__ == "__main__":
	arg = sys.argv[1] if len(sys.argv) > 1 else 0
	
	if arg != 0:
		patch_file = join(os.getcwd(), 'patches', arg)
		logging.info('Patch file: %s', patch_file)

		# initialize data vars
		info_data, cp_data, hr_data, mv_data, of_data, rm_data, rn_data, sm_data, sr_data = ('',) * 9
		title, pf_titleid, author = 'Unknown', 'Unknown', 'Unknown'
		
		with open(patch_file, 'r') as patch_file:
			for line in patch_file:
				line = line.strip()
				if line.startswith('#'):
					if 'Title:' in line:
						title = line.split('Title: ')[1]
					elif 'TitleID:' in line or 'Title ID:' in line:
						pf_titleid = line.split(': ')[1]
					elif 'Author:' in line:
						author = line.split('Author: ')[1]
				elif line.lower().startswith(('cp', 'hr', 'mv', 'of', 'rm', 'rn', 'sm', 'sr')):
					data_type = line[:2].lower()
					data_value = line[3:] + '\n'
					if data_type == 'cp':
						cp_data += data_value
					elif data_type == 'hr':
						hr_data += data_value
					elif data_type == 'mv':
						mv_data += data_value
					elif data_type == 'of':
						of_data += data_value
					elif data_type == 'rm':
						rm_data += data_value
					elif data_type == 'rn':
						rn_data += data_value
					elif data_type == 'sm':
						sm_data += data_value
					elif data_type == 'sr':
						sr_data += data_value

		file2patch = Dialog().browse(0, 'Select folder', "files") # select folder with file to patch
		logging.info('Selected folder: %s', file2patch)

		if file2patch:
			pf_titleid = pf_titleid.upper()

			if cp_data:
				logging.info('Copying files...')
				copy_file(cp_data)

			xbe_titleid = 'Unknown'
			if sr_data:
				check_if_xbe = join(file2patch, sr_data.split('|')[0])
				if hr_data.split('|')[0].lower().endswith('.xbe'):
					xbe_titleid = extract_pf_titleid(check_if_xbe).upper()
			
			if sm_data:
				check_if_xbe = join(file2patch, sm_data.split('|')[0])
				if hr_data.split('|')[0].lower().endswith('.xbe'):
					xbe_titleid = extract_pf_titleid(check_if_xbe).upper()

			if hr_data:
				check_if_xbe = join(file2patch, hr_data.split('|')[0])
				if hr_data.split('|')[0].lower().endswith('.xbe'):
					xbe_titleid = extract_pf_titleid(check_if_xbe).upper()

			if of_data:
				check_if_xbe = join(file2patch, of_data.split('|')[0])
				if of_data.split('|')[0].lower().endswith('.xbe'):
					xbe_titleid = extract_pf_titleid(check_if_xbe).upper()

			if xbe_titleid == pf_titleid or xbe_titleid == 'Unknown' or pf_titleid == 'MULTI':
				if mv_data:
					logging.info('Moving files...')
					move_file(mv_data)

				if hr_data:
					logging.info('Hex replacing files...')
					hex_replace_file(hr_data)

				if of_data:
					logging.info('Offset patching files...')
					offset_patch_file(of_data)

				if rn_data:
					logging.info('Renaming files...')
					rename_file(rn_data)

				if rm_data:
					logging.info('Removing files...')
					remove_file(rm_data)

				if sm_data:
					logging.info('Patching supported media...')
					supported_media(sm_data)

				if sr_data:
					logging.info('Patching supported region...')
					supported_region(sr_data)

				Dialog().ok('PATCH APPLIED', title, 'Author: ' + author, 'File: ' + arg.lower())
				logging.info('Patch applied successfully: %s', title)
			else:
				Dialog().ok('ERROR', 'Title: ' + title, 'Looking for (' + pf_titleid + ') found (' + xbe_titleid + ')', 'Patch: ' + arg.lower())
				logging.error('TitleID mismatch: expected %s, found %s', pf_titleid, xbe_titleid)

xbmc.executebuiltin('SetFocus(3000)')