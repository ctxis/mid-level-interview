# This is the script that is used to generate the `logins.csv` file.
# It's merely included for reference, please do not run it and re-generate
# the csv file.

from faker import Faker
import random
import csv
import itertools

date_format_chars = ('%y', '%m', '%d')
date_format_combos = list(itertools.permutations(date_format_chars))

fake = Faker('en_GB')

server_data = [
    {
        'server-name': fake.domain_word(),
        'server-ip': fake.ipv4(network=False),
    }
    for _ in range(10)
]

user_data = [
    {
        'username': fake.user_name(),
        'full-name': fake.name(),
        'contact': [
            random.choice((fake.phone_number(), fake.email()))
            for _ in range(3)
        ]
    }
    for _ in range(20)
]


login_rows = [
    {**server, **user, 'login-time': fake.date_time_this_year(before_now=False)}
    for server in server_data
    for user in random.sample(user_data, random.randint(2, len(user_data)))
]

random.shuffle(login_rows)


def generate_rows():
    for row in login_rows:
        if random.random() > 0.8:
            # Convert the datetime to a date
            row['login-time'] = row['login-time'].date()
        elif random.random() > 0.8:
            # Mange the datetime a bit
            choice = random.choice(date_format_combos)
            joiner = random.choice(('/', '\\', '|'))
            row['login-time'] = row['login-time'].strftime(joiner.join(choice))

        for contact in row['contact']:
            contact = '' if random.random() > 0.8 else contact
            server_name = '' if random.random() > 0.8 else row['server-name']

            yield {**row, 'server-name': server_name, 'contact': contact}


with open('logins.csv', 'w') as fd:
    fieldnames = ('server-name', 'server-ip', 'username', 'full-name', 'contact', 'login-time')
    writer = csv.DictWriter(fd, fieldnames=fieldnames)
    writer.writeheader()
    results = list(generate_rows())
    random.shuffle(results)
    writer.writerows(results)
