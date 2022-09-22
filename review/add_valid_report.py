import pandas as pd
import sys

github_issue = int(sys.argv[1])
if github_issue < 0 or github_issue > 1000:
    print('given github issue number seems incorrect: {}'.format(github_issue))
    exit(0)
reward_safe_address = sys.argv[2].lower()
if reward_safe_address[:2] != '0x' or len(reward_safe_address) != 42:
    print('given reward_safe_address seems incorrect: {}'.format(reward_safe_address))
    exit(0)

OVERWRITE = True if len(sys.argv) == 4 and sys.argv[3] == 'overwrite' else False

# Load current potential airdrop farming safes.
current = pd.read_csv('current.csv', index_col=0)
current.index = current.index.str.lower()

# Load current allocations
allocations = pd.read_csv('../safe_user_allocations_reworked.csv', index_col=0)
allocations.index = allocations.index.str.lower()

# Load valid reports
valid_reports = pd.read_csv('valid_reports.csv', index_col=0)
valid_reports.index = valid_reports.index.str.lower()
valid_reports['rewards_safe_address'] = valid_reports['rewards_safe_address'].str.lower()


# Go through current and drop all safes in allocations that fit.
current.reset_index()
for index, row in current.iterrows():
    if index in allocations.index:
        tokens = allocations.loc[index]['tokens']
        if tokens > 1000:
            print('WARNING: safe with many tokens will be eliminated: {}:{}'.format(index, tokens))
        allocations = allocations.drop(index)
        new_valid_report = pd.DataFrame([[github_issue, reward_safe_address]], columns=['github_issue', 'rewards_safe_address'], index=[index])
        valid_reports = pd.concat([valid_reports, new_valid_report], axis=0)
    elif OVERWRITE and index in valid_reports.index:
        valid_reports.loc[index, 'rewards_safe_address'] = reward_safe_address
        valid_reports.loc[index, 'github_issue'] = github_issue
    else:
        print('WARNING: safe not found: {}'.format(index))

valid_reports.index.name = 'safe_address'
valid_reports.to_csv('valid_reports.csv', sep=',')
allocations.to_csv('../safe_user_allocations_reworked.csv', sep=',', float_format='%.0f')