#! /usr/bin/env python

"""Mindfuck - python brainfuck interpreter

main module, uses pyfuk module for interpretation"""

import sys, string, getopt
import pyfuk

version = "0.88"

def main():
    """main(), main mindfuck function
    
    tries to interpret code that is given from
    file from argument - only frontend for pyfuk
    """
    try:
        (selection, arguments) = getopt.getopt(sys.argv[1:],'vhd')
        selection = dict(selection)
        if (len(selection) == 0) and (len(arguments) == 0):
            print sys.argv[0], "[-v|-h|-d] inputfile"
            return
        if selection.has_key('-v'):
            print version
            return
        #TODO: argumenty i/o?
        if selection.has_key('-h'):
            print "Mindfuck ", version, "\n"
            print "an opensource brainfuck interpreter"
            print "includes pyfuk python module for direct brainfuck interpreting"
            print "from python projects\n"
            print "Run as:"
            print sys.argv[0], "[-v|-h|-d] inputfile, where:"
            print "-v prints version of mindfuck and exists"
            print "-h prints this help and exists"
            print "-d if you want to debug your program"
            print "inputfile if path to file with bf code, that you"
            print "want to interpret.\n"
            print "(g) 2010 Garret Raziel, released under GNU/GPL"
            return
        deb = 0
        if selection.has_key('-d'):
            deb = 1
        if len(arguments) == 0:
            print "No input file!"
            return
        sourcefile = open(arguments[0])
        interpreter = pyfuk.BrainInterpreter(debug=deb)
        code = string.strip(string.join(sourcefile.readlines(),""))
        sourcefile.close()
        interpreter.interpret(code)
    except IOError, chyba:
        print "Cannot read file,",chyba
    except EOFError:
        print "EOF catched."
    except IndexError, chyba:
        print "Something goes wrong with some list (maybe stack?)", chyba
    except pyfuk.InterpretationError, chyba:
        print "Cannot interpret,", chyba
    except KeyboardInterrupt:
        print "End of program."
    print "\nEnd of interpretation."

if __name__ == '__main__':
    main()
