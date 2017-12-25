#!flask/bin/python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pymongo import MongoClient
from configuration import get_db_creds
from flask import Flask, send_file
import time


app = Flask(__name__)
generated_image_file = 'generator_usage.png'
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


def calculate_hours(sec):
    if sec <= 3600:
        return 0
    elif sec >= 3600:
        hours = sec // 3600
        minutes = sec % 60
        return hours


def get_time_spent(month):
    sec_sum = []
    cursor = db.time_spent.find({})
    for document in cursor:
        if month == document['time_stamp'].month:
            sec_sum.append(document['time_span'])
    total_sec = sum(sec_sum)
    total_time = calculate_hours(total_sec)
    return total_time


@app.route('/')
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
    plt.savefig(generated_image_file)
    return send_file(generated_image_file, mimetype='image/gif')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)