# SystemD test

## To run it


Put the systemd files in the user directory:

```sh
# Put them here:
# $HOME/.config/systemd/user

mkdir -p $HOME/.config/systemd/user/
cp myservice* $HOME/.config/systemd/user/
```


Load the services:

```sh
# after changing any of the files
systemctl --user daemon-reload

# Start the socket
systemctl --user start myservice.socket

```

See if the socket is running:

```sh
# See if it's running
systemctl --user list-unit-files
# or
systemctl --user list-units
```

Send something to the socket file:

```sh
# test it
echo "Hello World" | nc -U /tmp/mysocket_v1.sock


cat /etc/passwd | while read line; do
    echo "$line" | nc -U /tmp/mysocket_v1.sock
done
```