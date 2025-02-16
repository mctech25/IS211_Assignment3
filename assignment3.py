import csv
import argparse
import urllib.request
import re
import io
import datetime


def main(url):
    imageFinder(downloadData(url))
    topBrowser(downloadData(url))
    hitTimes(downloadData(url))
    print(input("Press <Enter> to exit"))

def downloadData(url):
    with urllib.request.urlopen(url) as response:
        response = response.read().decode('utf-8')
    data = csv.reader(io.StringIO((response)))
    return data

def imageFinder(data):
    pattern = '(.jpg|.gif|.png)'
    row_count = 0
    image_count = 0

    for row in data:
        row_count += 1
        try:
            if re.search(pattern, row[0]):
                image_count += 1
        except Exception:
            row_count -= 1

    print(f'There were a total of {image_count} hits for images today.')
    print(f'Image requests account for {(image_count/row_count)*100}% of all requests.')

def topBrowser(data):
    firefox = 0
    chrome = 0
    internet_explorer = 0
    safari = 0
    browser = {}

    for row in data:
        try:
            if re.search('Firefox', row[2]):
                firefox += 1
            elif re.search('Chrome', row[2]):
                chrome += 1
            elif re.search('Internet Explorer', row[2]):
                internet_explorer += 1
            elif re.search('Safari', row[2]):
                safari += 1
        except Exception as err:
            pass

    browser["Firefox"] = firefox
    browser["Chrome"] = chrome
    browser["Internet Explorer"] = internet_explorer
    browser["Safari"] = safari
    popular = max(browser, key=browser.get)
    print(f"The most popular browser today was {popular}"
          f" with {browser[popular]} hits.")

def hitTimes(data):
    time_list = []

    for row in data:
        try:
            format = '%Y-%m-%d %H:%M:%S'
            time = datetime.datetime.strptime(row[1], format)
            hour = time.hour
            time_list.append(hour)
        except Exception as err:
            print(err)

    print("Total hourly hits for all browsers are as follows:")
    print(f"Hour 0 had {time_list.count(0)} hits")
    print(f"Hour 1 had {time_list.count(1)} hits")
    print(f"Hour 2 had {time_list.count(2)} hits")
    print(f"Hour 3 had {time_list.count(3)} hits")
    print(f"Hour 4 had {time_list.count(4)} hits")
    print(f"Hour 5 had {time_list.count(5)} hits")

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
