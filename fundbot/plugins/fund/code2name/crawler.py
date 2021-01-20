import requests
import time
import random
import sys


def decodeFundData(fund_data):
    data = fund_data
    if data[0:8] == 'jsonpgz(':
        return data[8:-2]
    else:
        return None

def getFundName(fund_id):
    fund_id = str(fund_id)
    recent_time = time.time()*1000 - random.randint(1,500)
    recent_time = str(int(recent_time))
    url = "https://fundgz.1234567.com.cn/js/%s.js?rt=%s" % (fund_id, recent_time)
    r = requests.get(url)
    json_data = decodeFundData(r.text)
    if not json_data:
        return None
    else:
        try:
            return eval(json_data)['name']
        except Exception as e:
            print("An exception occured:", e)
            print("Raw data is", r.text)
            return None


def main():
    print("Use -v option to verbose")
    print("Starting with? Give an input")
    start_point = int(input())
    with open("mappings.csv", 'w') as fout:
        for i in range(start_point, 999999):
            str_code = str(i)
            if len(str_code) < 6:
                str_code = (6 - len(str_code)) * '0' + str_code
                name = getFundName(str_code)
                if name:
                    fout.write(str_code + ',' + name + '\n')
                    if len(sys.argv) > 1 and sys.argv[1] == '-v':
                        print(str_code + ',' + name)


if __name__ == "__main__":
    main()