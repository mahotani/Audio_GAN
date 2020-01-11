import os

'''
    This method retrieves words before underscore for given character.
'''
def TakeStringBeforeUnderscore(string):
    strs = list(string)
    answer = ''

    for char in strs:
        if char != '_':
            answer = answer + char
        else:
            break

    return answer

'''
    Make list removed characters before underscore for givne list.
'''
def MakeListBeforeUnderscore(charList):
    charsBeforeUnderscore = []
    for char in charList:
        charsBeforeUnderscore.append(TakeStringBeforeUnderscore(char))
    
    return charsBeforeUnderscore

'''
    This method make list removed duplication of giben list.
'''
def MakeListRemoveDuplication(charList):
    fileList = []
    for char in charList:
        if char not in fileList:
            fileList.append(char)

    return fileList

'''
    Main
'''
os.chdir('../audio')
files = os.listdir()

# List is added until the underscore of the original file name.
fileNames = MakeListBeforeUnderscore(files)

# List for directry name.
# This List is removed duplication of fileNames.
dirNames = MakeListRemoveDuplication(fileNames)

# Add new directries.
for directry in dirNames:
    os.makedirs('./../audio/%s' % directry)

# Assign files to new directries.
for fileName in files:
    originalPath = './../audio/%s' % fileName
    for directry in dirNames:
        if TakeStringBeforeUnderscore(fileName) == directry:
            newPath = './../audio/%s/%s' % (directry, fileName)
            os.rename(originalPath, newPath)
