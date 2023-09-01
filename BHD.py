import requests
import json
import time

# enter api key here
api_key = "API"
api_url = f'https://beyond-hd.me/api/torrents/{api_key}'

# enter search term
search_term = input("Enter search term: ")

all_results = []
page = 1

# timer
start_time = time.time()

while True:
    search_params = {
        'action': 'search',
        'search': search_term,
        'sort': 'name',
        'order': 'asc',
        'page': page,
    }

    # post request
    response = requests.post(api_url, data=search_params)

    if response.status_code == 200:
        data = json.loads(response.text)

        if data['success']:
            all_results.extend(data['results'])
            if page < data['total_pages']:
                page += 1
            else:
                break  # break loop
        else:
            print('Error: API request failed')
            break
    else:
        print('Error: Failed to make the API request')
        break

# show time elapsed
elapsed_time = time.time() - start_time
elapsed_time_formatted = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
print(f'Elapsed time: {elapsed_time_formatted}')

output_file_name = f'{search_term}-Releases.txt'

with open(output_file_name, 'w', encoding='utf-8') as file:
    for result in all_results:
        torrent_name = result['name']
        file.write(torrent_name + '\n')

print(f'Total {len(all_results)} Release Names Saved to {output_file_name}')
