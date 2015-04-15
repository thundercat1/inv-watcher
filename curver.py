from __future__ import print_function

import csv
import sys
import requests
import json
import time


'''
[
  {style: abc1324, color: black, qty: 13, sizes: {S: 5, M: 3, XL: 5}},
]
'''

def get_items_from_csv(fname):
    items = []
    with open(fname) as csvfile:
        r = csv.DictReader(csvfile)
        for row in r:
            items.append({
                'style': row['style'],
                'color': row['color'],
                'qty': row['qty']
                })

    return items

def calculate_sizes(items, url):
    item_count = len(items)
    finished = 0
    for item in items:
        item_start_time = time.time()
        print('calculating size curve for', item['style'], item['color'])
        print('%s/%s complete' % (finished, item_count))
        r = requests.get(url + '/quantities',
                         params={'style': item['style'], 'qty': item['qty']})

        if r.status_code == 200:
            item['sizes'] = json.loads(r.text)

        else:
            print(r.status_code, r.text)
            item['sizes'] = None

        finished += 1
        #print('t=', time.time() - item_start_time)

def write_csv(items, fname):
    print('Writing output to', fname)
    with open(fname, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['style', 'color', 'size', 'qty'])

        for item in items:
            for size in item['sizes']:
                writer.writerow([
                    item['style'],
                    item['color'],
                    size,
                    item['sizes'][size]
                ])


if __name__ == '__main__':
    start_time = time.time()
    url = 'http://localhost:5000'
    args = sys.argv
    if len(args) < 2:
        print('Error. Please provide a single argument with the filename to curve.')
        exit()

    input_file = args[1]
    try:
        output_file = args[2]
    except IndexError:
        output_file = 'results.csv'

    items = get_items_from_csv(input_file)
    item_count = len(items)
    print('Found', item_count, 'items to curve.')
    calculate_sizes(items, url)
    write_csv(items, output_file)
    print('Curved', item_count, 'items in ', round(time.time() - start_time), 'seconds.')