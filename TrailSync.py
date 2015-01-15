#!/usr/bin/env python

# Sync Images


import argparse
import sys
import os, os.path
import shutil

def Log(level, *args):
	print ' '.join(args)
	

def ParseArgs():
	parser = argparse.ArgumentParser()
	parser.add_argument('src_path', help='Source path')
	parser.add_argument('dest_path', help='Destination path')
	return parser.parse_args()

def ValidArgs(OPTIONS):
	srcdst = [OPTIONS.src_path, OPTIONS.dest_path]
	for p in srcdst:
		if not os.path.isdir(p):
			Log(0, 'ERROR: "{}" is not a directory.'.format(p))
			return False

	OPTIONS.src_path	= os.path.realpath(OPTIONS.src_path)
	OPTIONS.dest_path	= os.path.realpath(OPTIONS.dest_path)
	if os.path.commonprefix(srcdst) in srcdst:
		Log(0, 'ERROR: source and destination paths overlap')
		return False
			
	return True
	
def BuildFileList(path):
	fileList = []
	for root, dirs, files in os.walk(path):
		files = [os.path.join(root, f) for f in files if os.path.splitext(f)[1].lower() == '.jpg']
		fileList.extend([f for f in files])

	return sorted([os.path.relpath(f, path) for f in fileList])

def CopyFilesToDest(fileList, srcRoot, destRoot):
	i = 0
	for f in fileList:
		ext		= os.path.splitext(f)[1]
		src		= os.path.join(srcRoot, f)
		dest	= os.path.join(destRoot, 'EK{:06d}{}'.format(i, ext))

		print src, '->', dest
		shutil.copy2(src, dest)
		
		i += 1
			
	
def Main():
	options = ParseArgs()
	if not ValidArgs(options):
		return 1
	
	fileList = BuildFileList(options.src_path)
	CopyFilesToDest(fileList, options.src_path, options.dest_path)
	
	
	return 0
	
sys.exit( Main() )