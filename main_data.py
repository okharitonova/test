#!/usr/bin/python
import MySQLdb
import argparse
from random import (
    randint,
    choice
)
import string
import time


def _connect():
    return MySQLdb.connect(host='192.168.50.1', port=3301,
                           user='oxana', passwd='123456', db='test_db')

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('number', metavar='N', type=int, nargs='?', default=1,
                        help='an integer for the intensive insert')
    args = parser.parse_args()

    if args.number < 1:
        return

    db = _connect()
    key = 'interation-1'
    numbers_row = args.number
    interval = 1.0 / float(numbers_row)
    last_called = 0
    first_called = time.clock()
    for i in xrange(0, numbers_row):
        if time.clock() > first_called + 1:
            break;
        wait = interval - (time.clock() - last_called)
        #print 'wait = ' + str(wait)
        if wait > 0:
            time.sleep(wait)
        code = randint(0, 100)
        value = "".join([choice(string.letters) for i in xrange(15)])
        cur = db.cursor()
        cur.execute("""
                    INSERT INTO `main_data` (`key`, `code`, `value`)
                    VALUES (%(key)s, %(code)s, %(value)s)
                    """, {'key': key, 'code': str(code), 'value': value}
        )
        last_called = time.clock()
    db.commit()
    cur.execute("SELECT * FROM main_data")

    for row in cur.fetchall():
        print row

    db.close()

if __name__ == '__main__':
    main()