import coverage, sys

cov = coverage.Coverage()
cov.start()

if sys.argv[1] == '0':
    print('0')
if sys.argv[1] == '1':
    print('1')

cov.stop()
#cov.save()
#cov.report()
cov.html_report(directory='covhtml')
