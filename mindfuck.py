#! /usr/bin/env python

"""Mindfuck - python brainfuck interpreter

main module, uses pyfuk module for interpretation"""

import sys, string, getopt
import pyfuk

version = "1.01"

def main():
    """main(), main mindfuck function
    
    tries to interpret code that is given from
    file from argument - only frontend for pyfuk
    """
    try:
        (selection, arguments) = getopt.getopt(sys.argv[1:],'e:vhdt')
        selection = dict(selection)
        if (len(selection) == 0) and (len(arguments) == 0):
            print sys.argv[0], "[-v|-h|-d|-t|-e X] inputfile"
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
            print sys.argv[0], "[-v|-h|-d|-t|-e X] inputfile, where:"
            print "-v prints version of mindfuck and exits"
            print "-h prints this help and exits"
            print "-d if you want to debug your program"
            print "-t if you want to show hud text (End of int., input: etc)"
            print "-e X for some EOF standards - default is that"
            print "EOF as an input puts 0 - replace X with 1 to"
            print "EOF leaving block unchanged, 2 to putting -1"
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
        eof = 0
        if selection.has_key('-e'):
            token = int(selection['-e'])
            eof = token if token in [0,1,2] else 0
        showHud = 0 # workaround not to get error undef showHud if exception
        if selection.has_key('-t'): showHud = 1
        sourcefile = open(arguments[0])
        interpreter = pyfuk.BrainInterpreter(debug=deb,eof=eof,hud=showHud)
        code = string.strip(string.join(sourcefile.readlines(),""))
        sourcefile.close()
        interpreter.interpret(code)
        if showHud: print "\nEnd of interpretation."
    except IOError, chyba:
        print "Cannot read file,", chyba
    except EOFError:
        print "EOF catched."
    except IndexError, chyba:
        print "Something goes wrong with some list (maybe stack?)", chyba
    except pyfuk.InterpretationError, chyba:
        print "Cannot interpret,", chyba
    except KeyboardInterrupt:
        print "End of program."
    except getopt.GetoptError, chyba:
        print "Bad arguments, ", chyba

if __name__ == '__main__':
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    main()
