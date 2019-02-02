import os
import datetime
import time
import random
import argparse

def _get_args():
    parser = argparse.ArgumentParser(description='generate files to test streaming')
    parser.add_argument('--folder', '-f', required=True, help='folder to stream to')
    parser.add_argument('--seconds', '-s', 
            type = int,
            required=True, help='seconds to sleep')
    return parser.parse_args()

def get_data():
    return '{date},{key},{intt}'.format(
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            intt = random.randint(1,100),
            key = random.randint(1,5)
            )

def create_file(the_dir):
    with open(os.path.join(the_dir, 'file_{date}.csv'.format(
        date = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        )), 'w') as write_obj:
        write_obj.write(get_data())


def stream_file(the_dir, time_between_creation):
    while 1:
        create_file(the_dir)
        time.sleep(time_between_creation)

if __name__ == '__main__':
    args = _get_args()
    print(args.folder)
    stream_file(args.folder, args.seconds)

