"""
A python application which scrape all of the filenames, download links and filesizes in all of the inside pages
of http://mirror.rise.ph/centos/7/
"""

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import contextlib
import csv
from datetime import datetime
csv_name = ['']


def is_good_response(response):
    # check if the url is a good url
    content_type = response.headers['Content-Type'].lower()
    return (response.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def get_content(url_to_access):
    # open the content of the url
    try:
        url_to_open = requests.get(url_to_access, stream=True)
        with contextlib.closing(url_to_open) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        print('Error during requests to {} : {}'.format(url_to_access, str(e)))


def get_link(resp):
    # return the links found
    if resp is not None:
        html = BeautifulSoup(resp, 'html.parser')
        links = html.find('table').find_all('a')
        found_links = []
        for link in links:
            found_links.append(link.get('href'))
        return found_links


def get_the_links(connected_url, links):
    receive_links = links[4:]
    for link in receive_links:
        if '/' in link:
            new_url = '{}{}'.format(connected_url, link)
            go_to_url(new_url)
        else:
            return receive_links


def go_to_url(url_to_connect):
    response = get_content(url_to_connect)
    return_links = get_link(response)
    csv_write(url_to_connect, return_links)


def get_size(url_to_go):
    # getting the size of the file
    html_content = get_content(url_to_go)
    html = BeautifulSoup(html_content, 'html.parser')
    data = []
    for td in html.find_all('td'):
        data.append(td.string)
    return data[7::4]


def csv_date_time():
    # add date and time to the output
    now = datetime.now()
    datetime_now = now.strftime("%Y-%m-%d-%H-%M")
    csv_filename_now = "output-{}.csv".format(datetime_now)
    return csv_filename_now


def csv_write(url, links):
    global csv_name
    csv_file_name = csv_name[0]
    file_names = get_the_links(url, links) # return the list of filenames
    file_size = get_size(url) # return the list of sizes
    with open(csv_file_name, "a", newline='', encoding='utf-8') as csv_file:
        # content of the csv file
        if file_names is not None:
            for filename, size in zip(file_names, file_size):
                output = [filename, url+filename, size]
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(output)
                print(output)


def csv_header():
    global csv_name
    csv_file_name = csv_date_time()
    with open(csv_file_name, "w+", newline='', encoding='utf-8') as csv_file:
        # header for the csv file
        field_header = ['Filename', 'Download link', 'Filesize']
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(field_header)
    csv_name[0] = csv_file_name


def main(base_url):
    global csv_name
    response = get_content(base_url) # get the content of the url
    return_links = get_link(response) # get the links found
    received_links = get_the_links(base_url, return_links)
    if received_links is not None:
        main()
    elif received_links is None:
        print("Complete {} saved.".format(csv_name[0]))


if __name__ == '__main__':
    csv_header()
    main('http://mirror.rise.ph/centos/7/')
