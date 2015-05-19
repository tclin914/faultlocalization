import coverage, os, sys

#args = ["xpcmd.py", "demo/nstest1.xml"]

#sys.argv = args
#import __main__
#sys.path[0] = os.path.dirname(sys.argv[0])
#execfile(sys.argv[0], __main__.__dict__)

if __name__ == "__main__":
    coverage.start()
    
    args = ["test.py", "1"]

    sys.argv = args
    import __main__
    sys.path[0] = os.path.dirname(sys.argv[0])
    execfile(sys.argv[0], __main__.__dict__)

    coverage.stop()
    #coverage.save()
    coverage.report()

