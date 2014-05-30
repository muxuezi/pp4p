import languages2common                      # from my dir
f = open('test-context-output.txt', 'w')     # in .. server dir
f.write(languages2common.inputkey)
f.close()
print('context-type: text/html\n\nDone.\n')


