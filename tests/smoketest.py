import failprint
import sys
import time

def passing():
    time.sleep(1)
    print("I'm passing")
    return 0

def failing():
    time.sleep(1)
    print("I'm failing")
    return 1

failprint.run(vars()[sys.argv[1]], capture=sys.argv[2])
