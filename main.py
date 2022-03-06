import requests
import os
import multiprocessing
import traceback
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from pathlib import Path
import get_data_proxies

PATH_driver = str(Path().resolve()) + r'\chromedriver\chromedriver.exe'


class ProxyChecker:
    @staticmethod
    def check_status(proxy_dict):
        status_code = None
        try:
            response = requests.get('https://google.com', proxies=proxy_dict)
            status_code = response.status_code

        except:
            print('Something went wrong')
            print(traceback.print_exc())
        finally:
            print(status_code, proxy_dict)
            if status_code == 200:
                return proxy_dict['http']

    def multiprocess_initiator(self):
        pass

    def get_data(self):
        pass


if __name__ == '__main__':

    all_proxy_data = get_data_proxies.GettingData.get_json_proxies()
    all_proxies_in_dict_list_format = []

    print(all_proxy_data)

    all_proxy_keys = []

    for key in all_proxy_data['all_proxies']['http']:
        all_proxy_keys.append(key)

    print(all_proxy_keys)

    for key in all_proxy_keys:
        temp_proxy = {'http': all_proxy_data['all_proxies']['http'][key]}
        all_proxies_in_dict_list_format.append(temp_proxy)

    pool_of_processes = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    all_workable_proxies = pool_of_processes.map(ProxyChecker.check_status, all_proxies_in_dict_list_format)

    pool_of_processes.close()
    pool_of_processes.join()

    print(all_workable_proxies)
    print(all_workable_proxies[1])

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % all_workable_proxies[0])
    driver = webdriver.Chrome(executable_path=PATH_driver, options=chrome_options)

    driver.get('https://whatismyipaddress.com/')