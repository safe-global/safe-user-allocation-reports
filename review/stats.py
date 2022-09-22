# Script to check if safes in current.csv still have an allocation in safe_user_allocations_reworked.csv

import pandas as pd
import sys

reports = pd.read_csv('valid_reports.csv', index_col=0)
reports.index = reports.index.str.lower()

allocations = pd.read_csv('safe_user_allocations_reworked_original.csv', index_col=0)
allocations.index = allocations.index.str.lower()

count_per_reward_address = reports.groupby(['rewards_safe_address'])['rewards_safe_address'].count().sort_values(ascending=False)
count_per_reward_address.to_csv('stats_count_per_reward_address.csv', sep=',')

safe_per_reward_address_dict = {}

reports.reset_index()
for index, row in reports.iterrows():
    current_rewards_address = row['rewards_safe_address']

    if current_rewards_address not in safe_per_reward_address_dict:
        safe_per_reward_address_dict[current_rewards_address] = 0

    safe_per_reward_address_dict[current_rewards_address] += allocations.loc[index]['tokens']

safe_per_reward_address_list = [(k, v) for k, v in safe_per_reward_address_dict.items()]

safe_per_reward_address = pd.DataFrame(safe_per_reward_address_list, columns=['safe_address', 'safe_saved'])
safe_per_reward_address = safe_per_reward_address.set_index('safe_address')
safe_per_reward_address['safe_reward'] = safe_per_reward_address['safe_saved'] / 4
safe_per_reward_address = safe_per_reward_address.sort_values('safe_reward', ascending=False)
safe_per_reward_address.to_csv('stats_safe_per_reward_address.csv', sep=',')

print('{} SAFE saved'.format(safe_per_reward_address.sum()['safe_saved']))

print('{} Safes removed'.format(reports.count()[0]))
print('{} SAFE rewarded'.format(safe_per_reward_address.sum()['safe_reward']))
print('{} Safes rewarded'.format(safe_per_reward_address.count()[0]))