import os
import time

if __name__ == "__main__":
    while True:
        func_ret = os.system("curl -F myfile=@test.txt -F SourceID=test http://172.16.1.179:1890/submitfile")
        print func_ret
        time.sleep(0.1)
