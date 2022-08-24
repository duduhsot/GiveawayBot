import os
import os.path

score = 3

mypath = './'
newDirs = 'Newly created dirs:'

dic = {
    'The Prodigy': '_DJs', 
    'Mo-Do': '_DJs', 
    'Falco': '_DJs', 

    'Eminem': '_Rap', 
    'Eminem feat Nate Dogg': '_Rap', 
    'Mobb Deep': '_Rap', 

    'Dio': '_Classic rock',
    'Rainbow': '_Classic rock',
    'ozzy osborne': '_Classic rock',
    'Accept': '_Classic rock',
    'Iron Maiden': '_Classic rock',
    'Judas Priest': '_Classic rock',
    'ACDC': '_Classic rock',
    'Queen': '_Classic rock',
    'Rammstein': '_Classic rock',
    'WASP': '_Classic rock',
    'White Zombie': '_Classic rock',
    'Rush': '_Classic rock',
    'Van Halen': '_Classic rock',
    'Europe': '_Classic rock',
    'Bon Jovi': '_Classic rock',
    }

# get all .mp3 files names
files = [f for f in os.listdir(mypath) if os.path.isfile(
    os.path.join(mypath, f)) & f.endswith('.mp3')]

# calculate potential for new folders
potentialFolders = {}
for f in files:
    band = f.split(' - ')[0].strip()
    if band in dic:
        band = dic[band] 
    folderPath = os.path.join(mypath, band)
    if not os.path.exists(folderPath):
        if folderPath in potentialFolders:
            potentialFolders[folderPath] += 1
        else:
            potentialFolders[folderPath] = 1

# create new folders if score is good enough
for folderPath, folderScore in potentialFolders.items():
    if score <= folderScore:
        os.makedirs(folderPath)
        newDirs += folderPath + '\n'

# send songs to existing folders
for f in files:
    band = f.split(' - ')[0].strip()
    if band in dic:
        band = dic[band] 
    folderPath = os.path.join(mypath, band)
    if os.path.exists(folderPath):
        os.rename(f, os.path.join(folderPath, f))

print(newDirs)
