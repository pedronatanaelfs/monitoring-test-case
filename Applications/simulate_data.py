import random
import datetime
import time
import csv
import os

transactions_folder = "data/Transactions"
transactions_file = "transactions_new_data.csv"

while True:
    time_now = datetime.datetime.now().strftime('%Hh %M %Ss')
    
    # Determining Approved
    approved_stts = random.randint(1, 100)

    if approved_stts < 31:

        approved_rd = random.randint(1, 100)

        if approved_rd < 25:
            approved = random.randint(1, 24)
        elif approved_rd < 50:
            approved = random.randint(25, 124)
        elif approved_rd < 75:
            approved = random.randint(125, 291)
        else:
            approved = random.randint(292, 782)
    else: approved = 0

    # Determining Failed
    failed_stts = random.randint(1, 100)

    if failed_stts <= 2:

        failed_rd = random.randint(1, 100)

        if failed_rd < 25:
            failed = random.randint(1, 5)
        elif failed_rd < 50:
            failed = random.randint(25, 124)
        elif failed_rd < 75:
            failed = random.randint(125, 291)
        else:
            failed = random.randint(292, 782)
    
    else: failed = 0

    # Determining Reversed
    reversed_stts = random.randint(1, 100)

    if reversed_stts <= 18:

        reversed_rd = random.randint(1, 100)

        if reversed_rd < 25:
            reversed = 1
        elif reversed_rd < 50:
            reversed = random.randint(1, 2)
        elif reversed_rd < 75:
            reversed = random.randint(3, 13)
        else:
            reversed = random.randint(14, 20)

    else: reversed = 0

    # Determining Denied
    denied_stts = random.randint(1, 100)

    if denied_stts <= 27:

        denied_rd = random.randint(1, 100)

        if denied_rd < 25:
            denied = random.randint(1, 7)
        elif denied_rd < 50:
            denied = random.randint(7, 20)
        elif denied_rd < 75:
            denied = random.randint(20, 32)
        else:
            denied = random.randint(32, 133)
    
    else: denied = 0

    

    if not os.path.exists(transactions_folder):
        os.makedirs(transactions_folder)

    if any(data != 0 for data in [approved, failed, reversed, denied]):
        csv_path = os.path.join(transactions_folder, transactions_file)
        with open(csv_path, 'a', newline='') as csvfile:
            fieldnames = ['time', 'status', 'count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if approved != 0:
                writer.writerow({'time': time_now, 'status': 'approved', 'count': approved})

            if failed != 0:
                writer.writerow({'time': time_now, 'status': 'failed', 'count': failed})

            if reversed != 0:

                writer.writerow({'time': time_now, 'status': 'reversed', 'count': reversed})

            if denied != 0:
                writer.writerow({'time': time_now, 'status': 'denied', 'count': denied})

    time.sleep(1)