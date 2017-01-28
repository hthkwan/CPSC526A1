How to Run:

Run the python program on machine 1

    python3 main.py

With the second machine connect to the machine 1 using netcat on port 9999
    netcat <IP address of machine 1>|<machine name> 9999

Handshake details:
    When client first connects he will be asked for the password
    the password is: password (the worst password ever...)
    if the user does not know the password they can disconnect by inputting off

Supported Commands:
    pwd
    ls
    cat <file> both relative and absolute
    cd <dir> both relative and absolute
    help
    off
    net
    ps
    who