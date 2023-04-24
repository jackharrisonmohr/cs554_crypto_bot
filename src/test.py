import sys

# Test calling with cli args
print("arg 0: " + sys.argv[0])
print("first arg: " + sys.argv[1])
print("second arg: " + sys.argv[2])
print("arg1 + arg2 = " + str(int(sys.argv[1]) + int(sys.argv[2])))
