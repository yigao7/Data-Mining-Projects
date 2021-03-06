from pyspark import SparkContext
import json
from datetime import datetime
import sys

if __name__ == '__main__':
    sc = SparkContext('local[*]', 'task1')

    review_filepath = "review_filepath"
    output_filepath = "output_filepath"

    rdd = sc.textFile(review_filepath)
    row = rdd.map(lambda row: json.loads(row))
    result = {}

    # A. The total number of reviews
    num_of_reviews = row.count()
    # print("n_reviews: ", num_of_reviews)
    result['n_review'] = num_of_reviews

    # B. The number of reviews in 2018
    date = row.map(lambda x: datetime.strptime(x['date'][:10], '%Y-%m-%d').year)
    num_review_2018 = date.filter(lambda x: x == 2018).count()
    # print("n_review_2018: ", num_review_2018)
    result['n_review_2018'] = num_review_2018

    # C. The number of distinct users who wrote reviews
    unique_user = row.map(lambda x: x['user_id']).distinct().count()
    # print("n_user: ", unique_user)
    result['n_user'] = unique_user

    # D. The top 10 users who wrote the largest numbers of reviews and the number of reviews they wrote
    top10_user = row.map(lambda x: (x['user_id'], 1)) \
        .reduceByKey(lambda a, b: a + b) \
        .sortBy(lambda x: (-x[1], x[0])) \
        .take(10)
    # print("top10_user: ", top10_user)
    result['top10_user'] = top10_user

    # E. The number of distinct businesses that have been reviewed
    unique_bus = row.map(lambda x: x['business_id']).distinct().count()
    # print("n_business: ", unique_bus)
    result['n_business'] = unique_bus

    # F. The top 10 businesses that had the largest numbers of reviews and the number of reviews they had
    top10_bus = row.map(lambda x: (x['business_id'], 1)) \
        .reduceByKey(lambda a, b: a + b) \
        .sortBy(lambda x: (-x[1], x[0])) \
        .take(10)
    # print("top10_business: ", top10_user)
    result['top10_business'] = top10_bus

    # Wrapping up
    result_json = json.dumps(result)

    print(result_json)

    with open(output_filepath, 'w+') as output:
        output.write(result_json)
    output.close()
