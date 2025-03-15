import atexit
import sys
import os
import os.path
import time
import traceback

from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
#from pyvirtualdisplay import Display

#display = Display(visible=0, size=(800, 600))
#display.start()

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


def set_cookie(browser, name, value):
    cookie = {'domain': 'project2.ecen4133.org', 'name': name, 'value': value}
    browser.execute_cdp_cmd('Network.enable', {})
    browser.execute_cdp_cmd('Network.setCookie', cookie)

def grade_csrf(file, i):
    path = "./"
    csrf_grades = []

    p1 = os.path.normpath(os.path.join(path, file))
    print('Grading "%s"' % p1)
    if os.path.exists(p1):
        try:
            browser.delete_all_cookies()
            browser.get("https://project2.ecen4133.org/")
            time.sleep(0.1)

            # Set CSRF defense (using XSS!)
            csrfdefense = i
            xssdefense = "4" if i=="0" else "0"
            browser.add_cookie({'name': 'xssdefense', 'value': xssdefense})
            browser.add_cookie({'name': 'csrfdefense', 'value': csrfdefense, 'sameSite': 'Lax'})


            time.sleep(0.1)

            # Load CSRF page
            csrf_url = "file://" + os.path.abspath(p1)
            browser.get(csrf_url)
            time.sleep(0.2)

            # Check that CSRF is silent
            try:
                if csrf_url != browser.current_url:
                    csrf_grades.append((0,
                            'CSRF page redirected to another page'))
                    print(csrf_grades)
                    sys.exit(1)
            except UnexpectedAlertPresentException:
                csrf_grades.append((0,
                        'Unexpected alert box'))
                print(csrf_grades)
                sys.exit(1)
            time.sleep(0.2)

            # Load bungle again
            browser.get("https://project2.ecen4133.org/")
            time.sleep(0.2)
            print(browser.get_cookies())

            # Check cookies
            cd_cookie = browser.get_cookie('csrfdefense')
            assert cd_cookie != None
            if cd_cookie['value'] != str(i):
                csrf_grades.append((0, 'Wrong csrfdefense level, %s != %s' % (cd_cookie['value'], str(i))))
                print(csrf_grades)
                sys.exit(1)

            # Check logged in user
            try:
                if (browser.find_element(By.ID, 'logged-in-user').text
                        != 'attacker'):
                    csrf_grades.append((0, 'Logged as wrong user'))
                    print(csrf_grades)
                    sys.exit(1)
            except Exception as e:
                print(e)
                csrf_grades.append((0, 'Not logged in'))
                print(csrf_grades)
                sys.exit(1)

            # Passed CSRF
            #if file_list[i] == 'csrf_2.html':
            #    with open('extra-credit.todo', 'a+'):
            #        print('csrf_2.html: %s' % path, file=f)
            #        print('TODO: grade extra credit csrf_2 for %s' % path)
            #else:
            if(len(csrf_grades) == 0):
                csrf_grades.append((5, ''))
        except:
            # Unexpected error
            print(traceback.format_exc())
            browser.close()
            sys.exit(1)
    else:
        csrf_grades.append((0, "No file submitted"))
        print('No file...')
        #continue

    print(csrf_grades)
    sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: %s CSRF_FILE DEFENSE_LEVEL" % (sys.argv[0]), file=sys.stderr)
        sys.exit(-1)
    grade_csrf(sys.argv[1], sys.argv[2])
