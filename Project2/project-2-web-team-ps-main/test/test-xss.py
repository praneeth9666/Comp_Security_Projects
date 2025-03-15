import atexit
import sys
import os
import os.path
import time
import socket
import concurrent.futures
import multiprocessing

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def sleep(t=0.4):
    time.sleep(t)

def extract(path):
    with open(path) as f:
        return f.read().strip()

service = Service(executable_path='./test/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument('-headless')
options.add_argument('-no-sandbox')
options.add_argument('-disable-dev-shm-usage')
browser = webdriver.Chrome(service=service, options=options)


def close_browser():
    try:
        browser.quit()
    except:
        pass

atexit.register(close_browser)



def grade_xss(file, i):
    browser.delete_all_cookies()

    # login as victim (Using an XSS to post to the /login endpoint, of course!)
    victim_pw = "fcfd7d49552dcbd5b21ca3ba"
    browser.get("https://project2.ecen4133.org/search?q=%3Cbody+onload%3D%22%24.post%28%27https%3A%2F%2Fproject2.ecen4133.org%2Flogin%27%2C+%27username%3Dvictim%26password%3D9a49b3f1c0a175e80d78d6c14a6561f8%27%29%22%3E")
    sleep()
 
    # perform a search!
    browser.get("https://project2.ecen4133.org/search?q=foobar")
    sleep()

    print('(logged in as victim)')

    xss_grades = []
    prev_input = set()

    #file_list = ['xss_payload.html', 'xss_0.txt', 'xss_1.txt', 'xss_2.txt',
    #             'xss_3.txt', 'xss_4.txt']

    path = "./"

    
    p1 = os.path.normpath(os.path.join(path, file))
    print('Grading "%s"' % p1)
    if not os.path.exists(p1):
        print('Did not find file "%s"' % file)
        xss_grades.append((0, "No file submitted"))
        print(xss_grades)
        return

    # Set XSS defense (using XSS!)
    xssdefense = str(i-1)
    browser.get("https://project2.ecen4133.org/search?q=%3Cbody+onload%3D%22%24.post%28%27https%3A%2F%2Fproject2.ecen4133.org%2Fsetdefenses%27%2C+%27xssdefense%3D"+xssdefense+"%26csrfdefense%3D1%27%29%22%3E")
    time.sleep(0.5)


    # perform a search!
    browser.get("https://project2.ecen4133.org/search?q=secrit-foobar-is-" + str(i))
    time.sleep(0.5)

    xss = extract(p1)

    with concurrent.futures.ThreadPoolExecutor() as ex:
        future = ex.submit(xss_local_server)

        print('  Loading "%s"...' % xss)
        browser.get(xss)

        grade, comment = future.result()

    # Ensure grade is >= 0
    xss_grades.append((max(grade, 0), comment))



    print(xss_grades)



def xss_local_server():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(5)
    s.bind(('127.0.0.1', 31337))
    s.listen(10)

    try:
        sock, info = s.accept()
        print('  Got connection on localhost')
        data = recv_timeout(sock)
        print('  Got %d bytes data' % len(data))
        if b'stolen' in data and b'user=victim' in data:
            #b'last_search=secrit-foobar-is' in data:
            return (2, 'Correct')
    except socket.timeout:
        return (0,'Did not receive connection to localhost')
    except Exception as e:
        return (0, 'Exception: %s' % e)

    return (0, 'Did not receive stolen data from localhost connection')


def recv_timeout(s, timeout=.2):
    s.setblocking(0)

    begin = time.time()
    data = b''
    while len(data)==0 and time.time()-begin < timeout:
        try:
            buf = s.recv(8192)
            if len(buf)>0:
                data += buf
            else:
                time.sleep(0.1)
        except:
            pass
    s.send(b'HTTP/1.1 200 OK\r\n\r\n<html>ok</html>')
    return data


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: %s XSS_FILE XSS_DEFENSE_LEVEL" % (sys.argv[0]), file=sys.stderr)
        sys.exit(-1)
    grade_xss(sys.argv[1], int(sys.argv[2]))
