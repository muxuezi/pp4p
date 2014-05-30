import os
for (thisDirLevel, subsHere, filesHere) in os.walk('.'):
    for filename in filesHere:
        if filename.endswith('.pyc'):
            fullname = os.path.join(thisDirLevel, filename)
            #os.remove(fullname)
            print(fullname)
