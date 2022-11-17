import os, shutil, glob
root_folder = 'F:\\Games Dummy XISOs\\'
for folder in sorted(os.listdir(root_folder)):
	sub_folder = os.path.join(root_folder,folder)
	for iso in glob.iglob(sub_folder + '\\*.iso'):
		print os.path.join(sub_folder,iso)
		shutil.move(os.path.join(sub_folder,iso),'F:\\Test')
		
print "Done"