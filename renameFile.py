import os
import sys

oldPath = r'c:\Users\Marcel Fiedler\Documents\coding\text.txt'

if os.path.exists(oldPath):
	os.rename(oldPath, r'c:\Users\Marcel Fiedler\Documents\coding\newText.txt')
#	os.rename(oldPath, r'newText.txt')
else:
	print(f"Error: The file '{oldPath}' does not exist.")
