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

cp web* $HOME/.config/systemd/user/ && \
systemctl --user daemon-reload && \
systemctl --user start web@{1..2}.socket

```



```sh
# test it

echo -e "GET / HTTP/1.1\nHost: localhost\nConnection: close\n\n" | nc -v localhost 8888


```
