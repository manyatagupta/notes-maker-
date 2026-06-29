import subprocess
import os
import sys

env = os.environ.copy()

cmd = [
    'git', 'filter-branch', '-f', '--env-filter',
    """
    CORRECT_NAME='Manyata Gupta'
    CORRECT_EMAIL='manyatagupta1555@gmail.com'
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
    """,
    '--tag-name-filter', 'cat', '--', '--branches', '--tags'
]

# When git filter-branch runs, it actually executes the env-filter string in bash.
# Python passes it correctly without Windows cmd interference.
result = subprocess.run(cmd, env=env)
print("Return code:", result.returncode)
