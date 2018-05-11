# SystemD test

## To run it


Put the systemd files in the user directory:

```sh
# Put them here:
# $HOME/.config/systemd/user

mkdir -p $HOME/.config/systemd/user/
cp web* $HOME/.config/systemd/user/
```

Every time the source code changes:

```
 systemctl --user stop web@{1..2}.socket && \
 systemctl --user stop web@{1..2}.service && \
 cp web* $HOME/.config/systemd/user/ && \
 systemctl --user daemon-reload && \
 systemctl --user start web@{1..2}.socket

```

Test it:


```sh
echo "Hello World" | nc -l -p 8889

# or
cat /etc/passwd | while read line; do
    echo "$line" | nc -U /tmp/mysocket_v1.sock
done

```

To watch it:

```sh
journalctl -f --user-unit web@.service
```