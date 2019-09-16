Title: Find ports in use on macOS
Date: 2019-09-16
Category: programming
Tags: macos, shell
Slug: find-ports-in-use-on-macos
Authors: Micah Smith

How to find ports that are already "in use" on macOS:

```bash
sudo lsof -P -i TCP -s TCP:LISTEN
```

This is helpful if you are trying to figure out which process is using a port so that you can kill that process — for example, if you have a web server running in the background but now want to re-use that port for a different server.

Output of this command looks as follows:
```text
COMMAND     PID       USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
node      65167 micahsmith   23u  IPv4 0x86f43d8b9392d21f      0t0  TCP *:8080 (LISTEN)
```

This shows the results for a node http-server listening on port 8080. One could then kill this server using the PID shown.

## Explanation

`lsof` is a program to "list open files" and variants exist for major UNIX dialects such as macOS and Linux.

- `sudo`: you need sudo privileges to determine which files are open by other users on your system (and ports are just open files in a large sense)
- `-P`: "inhibits the conversion of port numbers to port names for network files". Port numbers can be mapped to names for commonly used services, such as `http` for port `80`. If you are trying to find which which process is running on a port number, it makes it more difficult if you need to think through the names as well. You can see which names are mapped on your system by viewing the `/etc/services` files.
- `-i TCP`: filter the listing of files to internet addresses matching the argument. The argument here is just `TCP` but more general internet addresses of the form `[46][protocol][@hostname|hostaddr][:service|port]` are accepted as well. For example, if you are looking for processes using port `8080`, you could provide that here, such as `-i TCP:8080`.
- `-s TCP:LISTEN`: used together with `-i TCP`, causes only network files with TCP state LISTEN to be listed.

The command output varies significantly based on the type of file, but here, as we have filtered to only TCP network files with a LISTEN state, the output can be understood as follows:

- `command`: partial command name
- `PID`: process ID
- `NAME`: the local host name or IP number followed by a colon, the port, and the two-part remote address (if applicable)

Source: `man lsof`
