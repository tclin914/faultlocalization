from __future__ import division
from coverage import coverage 
import os, sys, ast
import xml.etree.ElementTree as ET

passing = [("xpcmd.py", "XMLData/passing/com.adobe.versioncue.plist"),
           ("xpcmd.py", "XMLData/passing/com.apple.AppleFileServer.plist"),
           ("xpcmd.py", "XMLData/passing/com.apple.BezelServices.plist"),
           ("xpcmd.py", "XMLData/passing/com.apple.ByteRangeLocking.plist"),
           ("xpcmd.py", "XMLData/passing/com.apple.dockfixup.plist"),
           ("xpcmd.py", "XMLData/passing/com.apple.HIToolbox.plist"),
           ("xpcmd.py", "XMLData/passing/com.apple.iWork.Installer.plist"),
           ("xpcmd.py", "XMLData/passing/com.apple.keyboardtype.plist"),
           ("xpcmd.py", "XMLData/passing/com.apple.Keynote.plist"),
           ("xpcmd.py", "XMLData/passing/com.apple.networkConfig.plist"),
           ("xpcmd.py", "XMLData/passing/com.apple.print.defaultpapersize.plist"),
           ("xpcmd.py", "XMLData/passing/com.apple.print.FaxPrefs.plist"),
           ("xpcmd.py", "XMLData/passing/com.apple.RemoteManagement.plist"),
           ("xpcmd.py", "XMLData/passing/com.apple.SetupAssistant.plist"),
           ("xpcmd.py", "XMLData/passing/com.apple.SoftwareUpdate.plist"),
           ("xpcmd.py", "XMLData/passing/com.apple.windowserver.plist"),
           ("xpcmd.py", "XMLData/passing/com.apple.xgrid.agent.plist"),
           ("xpcmd.py", "XMLData/passing/com.apple.xgrid.controller.plist"),
           ("xpcmd.py", "XMLData/passing/com.skype.skype.plist")]

failing = [("xpcmd.py", "XMLData/failing/com.apple.Asteroid.plist"),
           ("xpcmd.py", "XMLData/failing/com.apple.Cell.plist"),
           ("xpcmd.py", "XMLData/failing/com.apple.Tiger.plist")]


def report(args):
    
    cov = coverage()
    cov.start()

    sys.argv = args
    import __main__
    sys.path[0] = os.path.dirname(sys.argv[0])
    try:
        execfile(sys.argv[0], __main__.__dict__)
    except UnboundLocalError:
        print("UnboundLocalError")
   
    cov.stop()
    cov.report()
    cov.xml_report()

if __name__ == "__main__":
    passData = {}
    failData = {}

    #pass 
    for item in passing:
        print item[1]
        report(item)
        tree = ET.parse('coverage.xml')
        root = tree.getroot()
        source = root[0][0].text

        packages = root[0]
        for package in packages:
            for classes in package:
                for class_ in classes:
                    test = {}
                    lines = class_[1]
                    if class_.attrib['filename'] in passData.keys():
                        test = ast.literal_eval(str(passData[class_.attrib['filename']]))
                        for line in lines:
                            # cover statement
                            if line.attrib['hits'] == '1':
                                if line.attrib['number'] in test.keys():
                                    test[line.attrib['number']] = test[line.attrib['number']] + 1
                                else:
                                    test[line.attrib['number']] = 1
                        passData[class_.attrib['filename']] = test
                    else:
                        for line in lines:
                            # cover statement
                            if line.attrib['hits'] == '1':
                                test[line.attrib['number']] = 1
                        passData[class_.attrib['filename']] = test
    #fail
    for item in failing:
        print item[1]
        report(item)
        tree = ET.parse('coverage.xml')
        root = tree.getroot()
        source = root[0][0].text

        packages = root[0]
        for package in packages:
            for classes in package:
                for class_ in classes:
                    test = {}
                    lines = class_[1]
                    if class_.attrib['filename'] in failData.keys():
                        test = ast.literal_eval(str(failData[class_.attrib['filename']]))
                        for line in lines:
                            # cover statement
                            if line.attrib['hits'] == '1':
                                if line.attrib['number'] in test.keys():
                                    test[line.attrib['number']] = test[line.attrib['number']] + 1
                                else:
                                    test[line.attrib['number']] = 1
                        failData[class_.attrib['filename']] = test
                    else:
                        for line in lines:
                            # cover statement
                            if line.attrib['hits'] == '1':
                                test[line.attrib['number']] = 1
                        failData[class_.attrib['filename']] = test
    

    Nf = 3
    Ns = 19
    print "\n======Tarantula======\n"
    rank = {}
    for key in failData.keys():
        if key != "hw.py":
            p = ast.literal_eval(str(passData[key]))
            f = ast.literal_eval(str(failData[key]))
            for line in f:
                Ncf = f[line]
                Ncs = p.get(line, 0) #if pass do not contain, set dault 0
                susp = ((float(Ncf) / Nf) / ((float(Ncf) / Nf) + (float(Ncs) / Ns)))
                s = '%s : susp(%s) = %.4f' % (key, line, susp)
                if len(rank) == 0:
                    rank[s] = susp
                else:
                    if rank.values()[0] < susp:
                        rank.clear()
                        rank[s] = susp
                    elif rank.values()[0] == susp:
                        rank[s] = susp
                print s

    print "\n======Rank of Tarantula======\n"
    for s in rank.keys():
        print s


    rank.clear()
    print "\n======The Ochiai similarity coefficient======\n"
    for key in failData.keys():
        if key != "hw.py":
            p = ast.literal_eval(str(passData[key]))
            f = ast.literal_eval(str(failData[key]))
            for line in f:
                Ncf = f[line]
                Ncs = p.get(line, 0) #if pass do not contain, set dault 0
                susp = float(Ncf) / ((Nf * (Ncf + Ncs)) ** (1./2))
                s =  '%s : susp(%s) = %.4f' % (key, line, susp)
                if len(rank) == 0:
                    rank[s] = susp
                else:
                    if rank.values()[0] < susp:
                        rank.clear()
                        rank[s] = susp
                    elif rank.values()[0] == susp:
                        rank[s] = susp
                print s

    print "\n======Rank of The Ochiai similarity coefficient======\n"
    for s in rank.keys():
        print s

    rank.clear()
    print "\n=======The Ochiai similarity coefficient O^p======\n"
    for key in failData.keys():
        if key != "hw.py":
            p = ast.literal_eval(str(passData[key]))
            f = ast.literal_eval(str(failData[key]))
            for line in f:
                Ncf = f[line]
                Ncs = p.get(line, 0) #if pass do not contain, set dault 0
                susp = Ncf - (float(Ncs) / (Ns + 1))
                s = '%s : susp(%s) = %.4f' % (key, line, susp)
                if len(rank) == 0:
                    rank[s] = susp
                else:
                    if rank.values()[0] < susp:
                        rank.clear()
                        rank[s] = susp
                    elif rank.values()[0] == susp:
                        rank[s] = susp
                print s

    print "\n======Rank of The Ochiai similarity coefficient O^p======\n"
    for s in rank.keys():
        print s

    rank.clear()
    print "\n======DStar (D*) with * = 1======\n"
    star = 1
    for key in failData.keys():
        if key != "hw.py":
            p = ast.literal_eval(str(passData[key]))
            f = ast.literal_eval(str(failData[key]))
            for line in f:
                Ncf = f[line]
                Ncs = p.get(line, 0) #if pass do not contain, set dault 0
                Nuf = Ns - Ncs
                susp = float(Ncf ** star) / (Nuf + Ncs)
                s = '%s : susp(%s) = %.4f' % (key, line, susp)
                if len(rank) == 0:
                    rank[s] = susp
                else:
                    if rank.values()[0] < susp:
                        rank.clear()
                        rank[s] = susp
                    elif rank.values()[0] == susp:
                        rank[s] = susp
                print s

    print "\n======Rank of DStar (D*) with * = 1======\n"
    for s in rank.keys():
        print s















