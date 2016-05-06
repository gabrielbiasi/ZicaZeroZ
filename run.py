import sys, os, filecmp
try:
	choice = int(sys.argv[1])
	if choice == 1:
		path_in = 'instances/worst/'
		path_out = 'instances/worst/'
	elif choice == 2:
		path_in = 'instances/best/'
		path_out = 'instances/best/'
	elif choice == 3:
		path_in = 'instances/media/'
		path_out = 'instances/media/'

except:
	path_in = 'instances/'
	path_out = 'instances/'

counter = 0
while True:
	if not os.path.isfile(path_in + '/in' + str(counter)):
		if os.path.isfile('test_file'):
			os.remove('test_file')
		break

	print counter,
	#####
	os.system('python main.py %s/in%d test_file' % (path_in, counter))
	#####

	f1 = open('test_file', 'r')
	test1 = f1.read()
	f1.close()

	f2 = open('%s/out%d' % (path_out, counter), 'r')
	test2 = f2.read()
	f2.close()

	if test1 == test2:
		print '\tACCEPTED'
	else:
		print '\tWRONG'
		print '\t\t\tGET:\t', test1,'\t\t\tANSWER:\t', test2,

	counter += 1
