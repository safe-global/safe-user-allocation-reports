# Script to check if safes in current.csv still have an allocation in safe_user_allocations_reworked.csv

import pandas as pd
import sys

reports = pd.read_csv('valid_reports.csv', index_col=0)

count_per_reward_address = reports.groupby(['rewards_safe_address'])['rewards_safe_address'].count()

count_per_reward_address.to_csv('stats_per_reward_address.csv', sep=',')