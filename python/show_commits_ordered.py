#!/usr/bin/python3.9

import argparse
from exec_bash_cmd import exec_bash_cmd

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shows a list of commits sorted by the parent")
    parser.add_argument("base_dir", help="Directory where commits are located")
    args = parser.parse_args()

    commits_dict = {}
    commits = exec_bash_cmd(f'ls {args.base_dir}')

    for commit in commits.splitlines():
        commit_id = commit.split('-')[1]
        parent=None

        grep = exec_bash_cmd(f'cat {args.base_dir}/{commit}/commit-meta.txt | grep parent').split()

        if not grep:
            parent = 'root'
        else:
            parent = grep[1]
        
        commits_dict[parent] = commit_id

    key = 'root'
    while key in commits_dict:
        print(commits_dict[key])
        key = commits_dict[key]
