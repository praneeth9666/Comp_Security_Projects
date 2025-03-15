#!/usr/bin/env python

import re
import sys
import os
import os.path
import subprocess
import shutil
import time
import signal

def run_shell_test(shell_string, wait_period=.5):
    try:
        proc = subprocess.Popen([shell_string], stdout=subprocess.PIPE, shell=True)
        time.sleep(wait_period)
        retcode = proc.poll()
        if retcode is None:
            # this indicates process is still running ie. shell is executing
            proc.send_signal(signal.SIGINT)
            proc.kill()
            proc.wait()

            return 7
    except KeyboardInterrupt:
        return 7
    except Exception as e:
        print("Exception occured:%s" % e)
        return 2

    # This indicates the program exited with no problems
    return 1

def grade_app(proj_dir, num):
    tar = "target%d" % num
    sol = "sol%d.py" % num

    if not os.path.exists(sol):
        return 0

    if num == 0 or num == 1:
        print("%s %d" % (os.path.basename(proj_dir), num))
        stdout = subprocess.Popen(['python3 %s | ./%s' % (sol, tar)], stdout=subprocess.PIPE, shell=True).communicate()[0]
        print(stdout)
        # Grade respective for both parts
        if b"Your grade is perfect" in stdout or b'A+' in stdout:
            return 7
        else:
            return 1
    elif num <= 8:
        if num == 4:
            shellString = "python3 sol4.py > tmp; ./target4 tmp"
        elif num == 7:
            shellString = './%s "$(python3 %s 1)" "$(python3 %s 2)" "$(python3 %s 3)"' % (tar, sol, sol, sol)
        else:
            shellString = './%s "$(python3 %s)"' %(tar, sol)

        print(shellString)

        if num != 6:
            return run_shell_test(shellString)
        else:
            # This input is random... run it multiple times
            correct = 0
            wrong = 0
            for i in range(100):
                if run_shell_test(shellString, .2) == 7:
                    correct += 1
                else:
                    wrong += 1
                if wrong > 0 and i >= 20:
                    print("Random Sample, Correct:", correct, "Wrong:", wrong)
                    if (float(wrong) / float(i)) < .2:
                        return 3
                    else:
                        return 1

            if correct == 100:
                return 7
            else:
                return 1
    else:
        print("Invalid question number given to grader")
        return 0


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: %s DIR TARGET" % (sys.argv[0]), file=sys.stderr)
        sys.exit(-1)

    #subprocess.check_output(['make', 'clean'])
    #subprocess.check_output(["sudo", "make"])


    grade = grade_app(sys.argv[1], int(sys.argv[2]))
    comment = "Full Credit"
    if grade == 3:
        comment = "too many failures"
    elif grade == 2:
        comment = "an error occured when running the target"
    elif grade == 1:
        comment = "shell did not start"
    elif grade == 0:
        comment = "no submission"

    print("Result: %s" % comment)
