
# INET4031 Add User Script

This project contains a python script that automates the creation of linux useraccounts using an input file. the script reads each line,skips comments, and creates users with their full names, password, and group assignmnet

## how to run (Dry Run)

Dry run mode prints the commands thta *would* be executed, but does Not create users.


./create-users.py < create-users.input
## How to run (real Run)

Real run mode actully creates the users, sets passwords , and assigns groups. Requires sudo.

sudo ./creates-users.py <creates-users.input

## Files Included

-'Creates-users.py' - Python script that creates users 
-'creates-users.input' -Input file containing user information
