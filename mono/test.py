import sys

for i in range(11):
    for j in range(10):
        n = 10 * i + j
        if n > 108:
            break
        sys.stdout.write("\033[%dm %3d\033[m" % (n, n))
    sys.stdout.write("\n")
