# -*- coding: utf-8 -*-
# Script by Rocky5

import logging
import traceback
import time
from binascii import hexlify, unhexlify
from os import getcwd, listdir, rename, remove
from os.path import getsize, isfile, join, splitext
from shutil import copyfile, move
from struct import unpack, calcsize
from xbmc import getFreeMem
from xbmcgui import Dialog

# set up logging
# logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO, format='\nFile Patcher:\n%(message)s')

def copy_file(file_list):
	for line in file_list.splitlines():
		old_names, _, new_names = line.partition('|')
		logging.info('Copying file from %s to %s', old_names, new_names)
		if old_names.lower().endswith('.xbe'):
			check_if_xbe = join(file2patch, old_names)
			xbe_titleid = extract_titleid(check_if_xbe).upper()
			if xbe_titleid != pf_titleid and pf_titleid != 'MULTI':
				logging.error('TitleID mismatch: expected %s, found %s', pf_titleid, xbe_titleid)
				Dialog().ok('ERROR', 'Title: ' + title,
							'Looking for (' + pf_titleid + ') found (' + xbe_titleid + ')',
							'Patch: ' + arg.lower())
				raise error('TitleID mismatch: expected %s, found %s', pf_titleid, xbe_titleid)
		if isfile(join(file2patch, old_names)) and not isfile(join(file2patch, new_names)):
			copyfile(join(file2patch, old_names), join(file2patch, new_names))
			logging.info('File copied successfully')

def extract_titleid(xbe_file):
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

def check_memory():
	return 1024 * 1024 * getFreeMem() # Available memory in bytes

def hex_replace_file(file_list):
	read_buffer = 2 * 1024 * 1024 # 2MB

	for data in file_list.splitlines():
		parts = data.split('|')
		in_file = join(file2patch, parts[0])
		hex_bytes = iter(parts[1:])
		logging.info('Hex replacing in file %s', in_file)
		with open(in_file, 'r+b') as file:
			file_size = getsize(in_file)
			try:
				# Replace directly in memory
				# If there isn't enough memory it just goes to buffer without displaying the "realloc failed, crash imminent (Out of memory)" error
				if file_size >= (check_memory() - (file_size * 2)):
					raise MemoryError("MemoryError occurred. Retrying with buffering...")
				file_cont = file.read()
				for x in hex_bytes:
					patch_nub, old_bytes, new_bytes = x, next(hex_bytes), next(hex_bytes)
					old_bytes_bytes = unhexlify(old_bytes)
					new_bytes_bytes = unhexlify(new_bytes)
					replacements_info = []
					replacements_left = int(patch_nub)
					instance_counter = 1
					pos = file_cont.find(old_bytes_bytes)
					while pos != -1 and replacements_left > 0:
						file_cont = file_cont[:pos] + new_bytes_bytes + file_cont[pos + len(old_bytes_bytes):]
						replacements_info.append((instance_counter, pos, old_bytes, new_bytes))
						pos = file_cont.find(old_bytes_bytes, pos + len(new_bytes_bytes))
						replacements_left -= 1
						instance_counter += 1
				file.seek(0)
				file.write(file_cont)
				for instance, offset, old, new in replacements_info:
					logging.info('Inst: %s\n\t Off: %s\n\t Fnd: %s\n\tRepl: %s', instance, hex(offset), old, new)
				logging.info('Hex replace completed in memory')
			except MemoryError as memerror:
				# Use buffering
				logging.error('%s', memerror)
				file.seek(0)
				while True:
					chunk = file.read(read_buffer)
					if not chunk:
						break
					buffer = bytearray(chunk)
					for x in hex_bytes:
						patch_nub, old_bytes, new_bytes = x, next(hex_bytes), next(hex_bytes)
						old_bytes_bytes = unhexlify(old_bytes)
						new_bytes_bytes = unhexlify(new_bytes)
						replacements_info = []
						replacements_left = int(patch_nub)
						instance_counter = 1
						pos = buffer.find(old_bytes_bytes)
						while pos != -1 and replacements_left > 0:
							buffer[pos:pos + len(old_bytes_bytes)] = new_bytes_bytes
							replacements_info.append((instance_counter, pos, old_bytes, new_bytes))
							pos = buffer.find(old_bytes_bytes, pos + len(new_bytes_bytes))
							replacements_left -= 1
							instance_counter += 1
					file.seek(-len(chunk), 1)
					file.write(buffer)
				for instance, offset, old, new in replacements_info:
					logging.info('Inst: %s\n\t Off: %s\n\t Fnd: %s\n\tRepl: %s', instance, hex(offset), old, new)
				logging.info('Hex replace completed with buffering')

def move_file(file_list):
	for data in file_list.splitlines():
		parts = data.split('|')
		old_names, new_names = parts[0], parts[1]
		old_path = join(file2patch, old_names)
		new_path = join(file2patch, new_names)
		logging.info('Moving file from %s to %s', old_path, new_path)
		if isfile(old_path) and not isfile(new_path):
			move(old_path, new_path)
			logging.info('File moved successfully')

def offset_patch_file(file_list):
	for data in file_list.splitlines():
		parts = data.split('|')
		in_file = join(file2patch, parts[0])
		offsets_bytes = iter(parts[1:])
		logging.info('Offset patching file %s', in_file)
		with open(in_file, 'r+b', buffering=4096) as file:
			for x in offsets_bytes:
				offset, new_bytes = x, next(offsets_bytes)
				file.seek(int(offset))
				file.write(unhexlify(new_bytes))
				logging.info('Patched offset %s with new bytes %s', offset, new_bytes)

def remove_file(file_list):
	for data in file_list.splitlines():
		parts = data.split('|')
		for file_name in parts:
			file_path = join(file2patch, file_name)
			logging.info('Removing file %s', file_path)
			if isfile(file_path):
				os.remove(file_path)
				logging.info('File removed successfully')

def rename_file(file_list):
	for data in file_list.splitlines():
		parts = data.split('|')
		old_names, new_names = parts[0], parts[1]
		old_path = join(file2patch, old_names)
		new_path = join(file2patch, new_names)
		logging.info('Renaming file from %s to %s', old_path, new_path)
		if isfile(old_path) and not isfile(new_path):
			os.rename(old_path, new_path)
			logging.info('File renamed successfully')

def supported_media(file_list):
	for data in file_list.splitlines():
		parts = data.split('|')
		in_file = join(file2patch, parts[0])
		new_bytes = iter(parts[1:])
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
	for data in file_list.splitlines():
		parts = data.split('|')
		in_file = join(file2patch, parts[0])
		new_bytes = iter(parts[1:])
		logging.info('Updating supported media in file %s', in_file)
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
		try:
			patch_file = join(os.getcwd(), 'patches', arg)
			logging.info('Patch file: %s', patch_file)

			# Initialize data vars
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

			if file2patch:
				logging.info('Selected folder: %s', file2patch)
				xbmc.executebuiltin('ActivateWindow(1100)')
				pf_titleid = pf_titleid.upper()

				if cp_data:
					logging.info('Copying files...')
					copy_file(cp_data)

				xbe_titleid = 'Unknown'
				if sr_data:
					check_if_xbe = join(file2patch, sr_data.split('|')[0])
					if hr_data.split('|')[0].lower().endswith('.xbe'):
						xbe_titleid = extract_titleid(check_if_xbe).upper()
				
				if sm_data:
					check_if_xbe = join(file2patch, sm_data.split('|')[0])
					if hr_data.split('|')[0].lower().endswith('.xbe'):
						xbe_titleid = extract_titleid(check_if_xbe).upper()

				if hr_data:
					check_if_xbe = join(file2patch, hr_data.split('|')[0])
					if hr_data.split('|')[0].lower().endswith('.xbe'):
						xbe_titleid = extract_titleid(check_if_xbe).upper()

				if of_data:
					check_if_xbe = join(file2patch, of_data.split('|')[0])
					if of_data.split('|')[0].lower().endswith('.xbe'):
						xbe_titleid = extract_titleid(check_if_xbe).upper()

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

					xbmc.executebuiltin('Dialog.Close(1100)')
					Dialog().ok('PATCH APPLIED', title, 'Author: ' + author, 'File: ' + arg.lower())
					logging.info('Patch applied successfully: %s', title)
				else:
					xbmc.executebuiltin('Dialog.Close(1100)')
					Dialog().ok('ERROR', 'Title: ' + title, 'Looking for (' + pf_titleid + ') found (' + xbe_titleid + ')', 'Patch: ' + arg.lower())
					logging.error('TitleID mismatch: expected %s, found %s', pf_titleid, xbe_titleid)
			
		except Exception as error:
			xbmc.executebuiltin('Dialog.Close(1100)')
			time.sleep(0.5)
			xbmc.executebuiltin('SetFocus(3000)')
			logging.error('Caught an exception: %s', error)

xbmc.executebuiltin('SetFocus(3000)')