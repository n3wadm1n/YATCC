#!/usr/bin/python3
####################
################
### n3wadm1n #####
### Euribot  #####
#####################

import requests, readline, argparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from colored import fg, attr

readline.set_completer_delims(' \t\n=')
readline.parse_and_bind("tab: complete")

def check_x_frame_options(url):
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url, verify=False)
        if 'X-Frame-Options' in response.headers:
            return f"\n{fg(226)}URL: {url}\n{fg(46)}Doesn't seems to be vulnerable to ClickJacking. Value: {response.headers['X-Frame-Options']}\n--------------------------------------------------------------------\n"
        else:
            return f"\n{fg(226)}URL: {url}\n{fg(196)}It's VULNERABLE to Clickjacking!\n--------------------------------------------------------------------\n"
    except requests.exceptions.RequestException as e:
        return f"\n{fg(226)}URL: {url}\n{fg(196)}Error accessing URL {url}: {e}!\n---------------------------------------------------------------------------------------------\n"

def read_urls_from_file(file_path):
    with open(file_path, "r") as file:
        return [url.strip() for url in file.readlines()]

if __name__ == "__main__":
    excomm = '''Yet Another Tool To Check Clickjacking\n\nExample 1: YATCC.py -c 1 https://example.com -o output.txt\nExample 2: YATCC.py -c 1 https://example.com\nExample 3: YATCC.py -c 2 urls.txt -o output.txt'''
    parser = argparse.ArgumentParser(description=excomm,formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-c", "--choice", help="Input type: 1 for a single URL or 2 for a file containing multiple URLs", type=int, choices=[1, 2], required=True)
    parser.add_argument("UPATH", help="URL or path to the file with URLs")
    parser.add_argument("-o", "--output", help="Filename (w/ or w/o path) to save the output")

    args = parser.parse_args()

    if args.choice == 1:
        print("\nChecking URL...")
        output = check_x_frame_options(args.UPATH)
    elif args.choice == 2:
        print("\nChecking URLs...")
        urls = read_urls_from_file(args.UPATH)
        output = ""
        for url in urls:
            output += check_x_frame_options(url)
    else:
        print("Invalid input. 1 for a single URL or 2 for a file containing multiple URLs.")
        exit()

    print("\nVerification completed.")

    if args.output:
        with open(args.output, "w") as file:
            file.write(output)
        print(f"The output has been saved to the file '{args.output}'.")
    else:
        print(output)

print(attr(0))
