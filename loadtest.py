import random
import argparse


def positive_int(x):
    try:
        n = int(x)
    except ValueError:
        raise argparse.ArgumentTypeError('Non-int value passed')

    if n <= 0:
        raise argparse.ArgumentTypeError('Positive int needed')
    return n


parser = argparse.ArgumentParser()
parser.add_argument('-requests',
                    type=positive_int,
                    help='Number of requests to generate',
                    default=100)
args = parser.parse_args()

for i in range(args.requests):
    request = 'GET http://localhost:8000/api/steps/text/?lesson={lesson_id}'
    print(request.format(lesson_id=random.randint(0, 5000)))

