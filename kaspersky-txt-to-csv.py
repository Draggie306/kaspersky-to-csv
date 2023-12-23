# Converts Kaspersky Password Manager export to Chromium Password Manager CSV export

# Permission is granted to anyone to use this software for any purpose, including commercial applications, providing that the following conditions are met:
# 1. Give appropriate credit, provide a link to the original source (https://github.com/Draggie306/kaspersky-to-csv) and indicate if changes were made.
# 2. Do not use this software for illegal purposes.
# 3. If you find a bug, report it to me so I can fix it.
# 4. If you make any changes, you must release them under the same license (i.e. include these comment blocks in an unobfuscated form in the source code).
# 5. Do not claim this software as your own.
# 6. Have fun!

import csv
import os
import time


def process_text_file(text_file_path):
    # get directoy path
    """Example text file:
    Websites

    Website name: *****
    Website URL: https://*****.co.uk
    Login name: 
    Login: *****
    Password: *****
    Comment: 

    ---

    Website name: *****
    Website URL: https://*****.com
    Login name: 
    Login: *****@gmail.com
    Password:*****
    Comment: 

    ---

    REST OF WEBISTES

    ---

    Applications

    Application: Kaspersky Password Manager
    Login name: 
    Login: a*****
    Password: *****
    Comment: 

    ---

    Application: Os maps
    Login name: 
    Login: *****@ibaguette.com
    Password: *****
    Comment: 

    ---
    
    """

    directory = os.path.dirname(text_file_path)
    websites = []

    with open(text_file_path, 'r') as file:
        lines = file.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if 'Websites' in line:
            i += 1
            while i < len(lines) and 'Applications' not in lines[i]:
                if '---' in lines[i]:
                    i += 1
                    continue
                record = {}
                while i < len(lines) and '---' not in lines[i]:
                    if 'Website name:' in lines[i]:
                        record['Website name'] = lines[i].split(':')[1].strip()
                    elif 'Website URL:' in lines[i]:
                        fixed_url = (lines[i].split('Website URL: ')[1]).strip()
                        if not fixed_url.startswith('http'):
                            fixed_url = 'https://' + fixed_url
                        record['Website URL'] = fixed_url
                    elif 'Login:' in lines[i]:
                        record['Login'] = lines[i].split(':')[1].strip()
                    elif 'Password:' in lines[i]:
                        record['Password'] = lines[i].split(':')[1].strip()

                    # application records have no 'Website name' or 'Website URL' fields, just 'Application', 'Login Name', Login', 'Password', 'Comment'
                    elif 'Application:' in lines[i]:
                        record['Application'] = lines[i].split(':')[1].strip()
                    elif 'Login:' in lines[i]:
                        record['Login'] = lines[i].split(':')[1].strip()
                    elif 'Password:' in lines[i]:
                        record['Password'] = lines[i].split(':')[1].strip()
                    elif 'Comment:' in lines[i]:
                        record['Comment'] = lines[i].split(':')[1].strip()
                    i += 1
                print((f"Added {record['Website name']} (account #{len(websites) + 1})") if 'Website name' in record else 'Non-website record added')
                websites.append(record)

        print(f"Found {len(websites)} websites")

    unix_time_seconds = int(time.time())
    with open(os.path.join(directory, f'kaspersky_export_{unix_time_seconds}.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        # ...
        writer.writerow(['name', 'url', 'username', 'password', 'note', 'application', 'comment'])

        for account in websites:
            if 'Website name' in account and 'Website URL' in account:
                # This is a website record
                writer.writerow([account['Website name'], account['Website URL'], account['Login'], account['Password'], ''])
            elif 'Application' in account:
                # This is an application record
                writer.writerow([account['Application'], '', account['Login'], account['Password'], '', account['Comment']])

    print(f'CSV file \'kaspersky_export_{unix_time_seconds}.csv\' created successfully!')
    os.startfile(os.path.join(directory, f'kaspersky_export_{unix_time_seconds}.csv'))


text_file_path = input('Enter the path of the text file: ')
# text_file_path = "Z:\\23-12-2023.txt"
process_text_file(text_file_path)
