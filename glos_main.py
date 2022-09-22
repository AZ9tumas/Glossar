from glos_scan import *
from glos_parse import *
from glos_vm import *
import sys

while True:
    line = ''
    fileName = "<stdin>"

    try:
        line = input("> ")
    except KeyboardInterrupt:
        print("\nExit")
        exit()

    #print(sys.argv)

    sc = Scanner(line, fileName, 1)
    scan_status = sc.scan() # Scanning the literals

    if not scan_status: exit()

    #sc.printTokens() # Tokens displayed for debugging purposes

    parsing = Parse(sc.tokens, fileName)

    parseStatus = parsing.exp()
    if not parseStatus: exit()

    #print(parsing.instructions)

    execution = VM(parsing.instructions, fileName)
    runStatus = execution.execute()

    if fileName == '<stdin>': print(execution.stack[0])

    if not runStatus: exit()