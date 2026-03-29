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

        # Check if the line begins with '#' which indicates a comment that should be skipped.
        match = re.match("^#", line)

        # Remove whitespace and split the line into fields using ':'.
        # Expected fields: username : password : last name : first name : groups
        fields = line.strip().split(':')

        # Skip this line if it is a comment or if it does not contain exactly 5 fields.
        # This prevents processing malformed or incomplete input lines.
        if match or len(fields) != 5:
            continue

        # Extract username and password, and build the GECOS field (full name info)
        # which is stored in /etc/passwd when the user is created.
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])

        # Split the group list into individual groups so the user can be added to each one.
        groups = fields[4].split(',')

        # Inform the admin that the script is about to create this user account.
        print("==> Creating account for %s..." % (username))

        # Build the Linux adduser command that creates the user with the GECOS information.
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)

        # During dry-run mode, this command is printed instead of executed.
        # When uncommented, os.system(cmd) will actually create the user account.
        # print(cmd)
        # os.system(cmd)

        # Inform the admin that the script is about to set the user's password.
        print("==> Setting the password for %s..." % (username))

        # Build the command that pipes the password twice into the passwd command
        # to set the user's password automatically.
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)

        # In dry-run mode, this is printed instead of executed.
        # print(cmd)
        # os.system(cmd)

        # Loop through each group the user should be added to.
        for group in groups:

            # Only assign the user to a group if the group field is not '-'.
            # '-' indicates that the user does not belong to any additional groups.
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username, group))
                cmd = "/usr/sbin/adduser %s %s" % (username, group)
                # print(cmd)
                # os.system(cmd)

if __name__ == '__main__':
    main()

