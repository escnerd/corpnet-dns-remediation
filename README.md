# corpnet-dns-remediation
CLI based text parser used to fix a large DNS zone file.

This is a script I wrote back in 2015 when I first began learning how to write Python. I was tasked to parse each line of a 7000+ entry DNS zone file, and it was too daunting for a manual task, hence the drive to learn how to write some Python code.

The script takes in one argument, which is the DNS zone text file, which I will not include on the repo for security purposes (contains many internal IP addresses).

Unfortunately, when I started learning how to write Python, I did not know anything about using GIT nor even CVS. It would have been nice to have a history of commits and branches because while writing this tool, things became messy with the amount of folders of different instances of the script I tried to maintain.
