import os
import shutil
import time
import zipfile

def all(_in, _out, source_name, rename_stuff, dp=None):
	if dp:
		return allWithProgress(_in, _out, source_name, rename_stuff, dp)

	return allNoProgress(_in, _out)


def allNoProgress(_in, _out):
	try:
		zin = zipfile.ZipFile(_in, 'r')
		root = zin.namelist()[0]        
		zin.extractall(_out)

	except Exception as e:
		print str(e)
		return False

	return True


def allWithProgress(_in, _out, source_name, rename_stuff, dp):

	zin = zipfile.ZipFile(_in, 'r')
	root = zin.namelist()[0]
	
	if rename_stuff == "emulator":
		# Check if the original folder already exists
		if os.path.exists(os.path.join(_out, root)) and not os.path.exists(os.path.join(_out, source_name)):
			# If it does, rename the original folder
			os.rename(os.path.join(_out, root), os.path.join(_out, source_name))

	nFiles = float(len(zin.infolist()))
	count  = 0

	try:
		for item in zin.infolist():
			count += 1
			update = count / nFiles * 100
			dp.update(int(update))
			if rename_stuff == "emulator":
				# Change the directory structure on-the-fly
				if source_name and item.filename.startswith(root):
					new_filename = source_name + '/' + item.filename[len(root):]
				else:
					new_filename = item.filename
				# Create directories as needed
				if not os.path.isdir(os.path.join(_out, os.path.dirname(new_filename))):
					os.makedirs(os.path.join(_out, os.path.dirname(new_filename)))
				# Extract file
				if not item.filename.endswith('/'):  # Check if the item is a file
					with zin.open(item) as src, open(os.path.join(_out, new_filename), 'wb') as dst:
						shutil.copyfileobj(src, dst)
			elif rename_stuff == "msdash":
				if item.filename == "xboxdash.xbe":  # Check if the item is the specific file
					new_filename = "xb0xdash.xbe"
					with zin.open(item) as src, open(os.path.join(_out, new_filename), 'wb') as dst:
						shutil.copyfileobj(src, dst)
				elif item.filename == "xodash/xonlinedash.xbe":  # Check if the item is the specific file
					new_filename = "xodash/xonlinedash.xbe"
					with zin.open(item) as src, open(os.path.join(_out, new_filename), 'wb') as dst:
						shutil.copyfileobj(src, dst)
					# Patch xolinedash.xbe to see new xb0xdash.xbe, C:\xbox.xtf and save a shortcut to the new msdash path.
					print os.path.join(_out, new_filename)
					with open(os.path.join(_out, new_filename), "rb") as inputfile:
						with open(os.path.join(_out, new_filename + ".temp"), "wb") as outputfile:
							while True:
								file_content = inputfile.read(1024 * 1024)
								if not file_content:
									break
								find_xboxdash1 = file_content.find(b'\x78\x62\x6F\x78\x64\x61\x73\x68\x2E\x78\x62\x65')
								if find_xboxdash1 != -1:
									file_content = file_content.replace(b'\x78\x62\x6F\x78\x64\x61\x73\x68\x2E\x78\x62\x65',b'\x78\x62\x30\x78\x64\x61\x73\x68\x2E\x78\x62\x65')
								find_xboxfont = file_content.find(b'\x70\x61\x72\x74\x69\x74\x69\x6F\x6E\x32\x5C\x78\x6F\x64\x61\x73\x68\x5C\x58\x62\x6F\x78\x2E\x78\x74\x66')
								if find_xboxfont != -1:
									file_content = file_content.replace(b'\x70\x61\x72\x74\x69\x74\x69\x6F\x6E\x32\x5C\x78\x6F\x64\x61\x73\x68\x5C\x58\x62\x6F\x78\x2E\x78\x74\x66', b'\x70\x61\x72\x74\x69\x74\x69\x6F\x6E\x32\x5C\x78\x62\x6F\x78\x2E\x78\x74\x66\x00\x00\x00\x00\x00\x00\x00')
								outputfile.write(file_content)
					os.remove(os.path.join(_out, new_filename))
					os.rename(os.path.join(_out, new_filename + ".temp"), os.path.join(_out, new_filename))
				else:
					zin.extract(item, _out)
			else:
				zin.extract(item, _out)    

	except Exception as e:
		print str(e)
		return False

	return True
