#!/usr/bin/python3

# INET4031
# Author: Fartun Rufai
# Date Created: 03/29/2026
# Date Last Modified: 03/29/2026

# os → allows the script to run Linux system commands (adduser, passwd, group assignments)
# re → used to detect comment lines in the input file using regular expressions
# sys → allows the script to read input from standard input (the input file piped into the script)
import os
import re
import sys

def main():
    for line in sys.stdin:

        # Check whether this line starts '#'- if so,it is a comment and should be ignored.
        match = re.match("^#", line)

        #  strip whitespace and split the line into 5 fields: username,password,last name, first name,and group list
        fields = line.strip().split(':')

        #  skip the line if it is a comment or does not contain exactly 5 fields to avoid processing bad input.
        if match or len(fields) != 5:
            continue

        #  extract the username and password, and build the GECOS field (full name) store in /etc/password.
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])

        # Split the  comma-separated group list so the user can be added to each group individually.
        groups = fields[4].split(',')

        # print a status message so the admin knows which user is being processed.
        print("==> Creating account for %s..." % (username))

        # Build the adduser command that creates the user account with the correct full name (GECOS field).
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)

        #  in dry-run mode this command is only printed; in real mode it actually creattes the user account.
        print(cmd)
        os.system(cmd)

        # Print a status message so the admin knows the password is now being set for this user.
        print("==> Setting the password for %s..." % (username))

        # Build the command that sends the password twice to the password program so it can be set automatically.
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)

        # In dry-run mode this command is only printed; in real mode it updates the users passwords.
        print(cmd)
        os.system(cmd)

        # Loop through each group listed forthis user so they can be added to each one
        for group in groups:

            # Only add the user to a group if the group name is not '-'; '-' means no extra groups.
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username, group))
                cmd = "/usr/sbin/adduser %s %s" % (username, group)
                print(cmd)
                os.system(cmd)

if __name__ == '__main__':
    main()

