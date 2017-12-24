#!flask/bin/python
from flask import Flask, send_file
import matplotlib.pyplot as plt
import time
from pymongo import MongoClient
from configuration import get_db_creds

app = Flask(__name__)
env = get_db_creds('env')
test_uri = get_db_creds('test_uri')
prod_uri = get_db_creds('prod_uri')
if env == 'test':
    client = MongoClient(test_uri)
    db = client.raspgen_test
else:
    client = MongoClient(prod_uri)
    db = client.raspgen
print(db)


def get_time_spent(month):
    sec_sum =[]
    cursor = db.time_spent.find({})
    for document in cursor:
        if month == document['time_stamp'].month:
            sec_sum.append(document['time_span'])
    total_sec = sum(sec_sum)
    total_time = time.strftime("%H:%M", time.gmtime(total_sec))
    return total_time


@app.route('')
def get_usage():
    my_xticks = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    y = []
    for month in x:
        hours_spent = get_time_spent(month)
        y.append(hours_spent)
    print(y)
    plt.bar(x, y, label='Bars1')
    plt.xlabel('Month')
    plt.ylabel('Usage')
    plt.xticks(x, my_xticks)
    plt.title('Generator usage')
    plt.savefig('foo.png')
    return send_file('foo.png', mimetype='image/gif')
    # plt.show()


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)