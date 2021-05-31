#!/usr/bin/python3.9

import argparse
import subprocess
import shlex

parser = argparse.ArgumentParser(description="Python module to execute simple bash commands.")
parser.add_argument("cmd", help="Commands to be executed")
args = parser.parse_args()

def exec_bash_cmd(cmd_parts, prev_process=None):
    """
	Executes non-complex bash commands.

    Parameters
    -----------

    	cmd_parts		Commands to be executed.
    	prev_process	Previous command process in case of piping commands.

    Returns
    -----------
    The stdout and stderr obtained from the execution of the bash command.

    If a single command was passed, they are retrieved from a CompletedProcess class 
    instance (which allows access to args, returncode, stdout and stderr). If some
    commands were passed using Unix Pipelines ("|"), they are retrieved from the 
    process.communicate() function.
    """

    cmds_list = cmd_parts.split("|")
    cmd = cmds_list.pop(0)
    next_cmd_parts = "|".join(cmds_list)
    
    args = shlex.split(cmd)

    if prev_process == None and len(cmds_list) == 0:
        process = subprocess.run(args, capture_output=True, encoding="utf-8")
        return process.stdout + process.stderr
    elif prev_process == None:
        process = subprocess.Popen(args, stdout=subprocess.PIPE)
        return exec_bash_cmd(next_cmd_parts, process)    
    elif len(cmds_list) > 0:
        process = subprocess.Popen(args, stdin=prev_process.stdout, stdout=subprocess.PIPE)
        prev_process.stdout.close()
        return exec_bash_cmd(next_cmd_parts, process)
    else:
        process = subprocess.Popen(args, stdin=prev_process.stdout, stdout=subprocess.PIPE, encoding="utf-8")
        prev_process.stdout.close()
        stdout, stderr = process.communicate()
        return stdout

if __name__ == "__main__":
    print(exec_bash_cmd(args.cmd), end='')
