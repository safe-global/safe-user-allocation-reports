# Script to check if safes in current.csv still have an allocation in safe_user_allocations_reworked.csv

import pandas as pd
import sys

# Load current potential airdrop farming safes.
current = pd.read_csv('current.csv', index_col=0)
current.index = current.index.str.lower()

PRINT_ALLOCATIONS = False if len(sys.argv) == 1 or sys.argv[1] != 'a' else True

# Load current allocations
allocations = pd.read_csv('../safe_user_allocations_reworked.csv', index_col=0)
allocations.index = allocations.index.str.lower()

# List to collect safes already removed.
already_removed = []
# List to collect safes in current.csv that still have an allocation
available = []

# Iterate through current and check if the safes still have an allocation.
current.reset_index()
for index, row in current.iterrows():
    if index in allocations.index:
        if PRINT_ALLOCATIONS:
            tokens = allocations.loc[index]['tokens']
            print('{},{}'.format(index, tokens))
        else:
            print(index)
        available.append(index)
    else:
        already_removed.append(index)

print('{}/{} already removed.'.format(len(already_removed), len(current)))
print('{}/{} still available. (printed out above)'.format(len(available), len(current)))