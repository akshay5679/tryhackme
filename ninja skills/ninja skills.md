# Linux File Hunting Scripts

A collection of Bash scripts for finding specific files on a Linux system based on different properties.

These scripts are useful for **Linux enumeration, CTFs, TryHackMe, Hack The Box, and cybersecurity labs**.

> **Note:** Use these scripts only on systems you own or have permission to test.

---

## Files Used

The scripts search for the following files:

```bash
8V2L
bny0
c4ZX
D8B3
FHl1
oiMO
PFbD
rmfX
SRSq
uqyw
v2Vb
X1Uy
```

---

# 1. Files Owned by `best-group`

### Command

```bash
find / -group best-group 2>/dev/null
```

### Explanation

* `find /` → Search from the root directory.
* `-group best-group` → Find files belonging to the `best-group` group.
* `2>/dev/null` → Hide permission-denied errors.

### Example

```text
/var/tmp/example
/home/user/example
```

---

# 2. File Containing an IP Address

This script searches the listed files and checks their contents for an IPv4 address.

### Script

```bash
#!/bin/bash

# List of files to search
files=(8V2L bny0 c4ZX D8B3 FHl1 oiMO PFbD rmfX SRSq uqyw v2Vb X1Uy)

echo "Searching for files containing an IP address..."
echo "------------------------------------------------"

for file in "${files[@]}"; do

    # Find the file anywhere on the system
    filepath=$(find / -type f -name "$file" 2>/dev/null | head -n 1)

    # Check if the file was found
    if [ -n "$filepath" ]; then

        # Search the file for an IPv4 address
        ip_found=$(grep -E -o \
            '([0-9]{1,3}\.){3}[0-9]{1,3}' \
            "$filepath" 2>/dev/null)

        # Display the result
        if [ -n "$ip_found" ]; then
            echo "[+] File: $filepath"
            echo "[+] IP Address: $ip_found"
            echo "------------------------------------------------"
        fi
    fi
done
```

### Key command

```bash
grep -E -o '([0-9]{1,3}\.){3}[0-9]{1,3}' file
```

This searches for an IPv4-style pattern such as:

```text
192.168.1.10
10.10.10.5
172.16.0.1
```

---

# 3. File Containing a Specific SHA1 Hash

This script calculates the SHA1 hash of each file and compares it with the target hash.

### Target SHA1

```text
9d54da7584015647ba052173b84d45e8007eba94
```

### Script

```bash
#!/bin/bash

# List of files to search
files=(8V2L bny0 c4ZX D8B3 FHl1 oiMO PFbD rmfX SRSq uqyw v2Vb X1Uy)

# Target SHA1 hash
target_hash="9d54da7584015647ba052173b84d45e8007eba94"

echo "Searching for the file matching SHA1 hash:"
echo "$target_hash"
echo "------------------------------------------------"

for file in "${files[@]}"; do

    # Find the file anywhere on the system
    filepath=$(find / -type f -name "$file" 2>/dev/null | head -n 1)

    # Check if the file was found
    if [ -n "$filepath" ]; then

        # Calculate SHA1 hash
        current_hash=$(sha1sum "$filepath" | awk '{print $1}')

        # Compare hashes
        if [ "$current_hash" = "$target_hash" ]; then
            echo "[+] Match Found!"
            echo "[+] File Name: $file"
            echo "[+] Full Path: $filepath"
            echo "[+] SHA1: $current_hash"
            echo "------------------------------------------------"
            exit 0
        fi
    fi
done

echo "[-] No matching file found."
```

### Key command

```bash
sha1sum file
```

Example:

```text
9d54da7584015647ba052173b84d45e8007eba94  example
```

---

# 4. File Containing Exactly 230 Lines

This script checks each file and identifies the file containing exactly **230 lines**.

### Script

```bash
#!/bin/bash

# List of files to search
files=(8V2L bny0 c4ZX D8B3 FHl1 oiMO PFbD rmfX SRSq uqyw v2Vb X1Uy)

# Target number of lines
target_lines=230

echo "Searching for a file containing exactly $target_lines lines..."
echo "-------------------------------------------------------------"

for file in "${files[@]}"; do

    # Find the file anywhere on the system
    filepath=$(find / -type f -name "$file" 2>/dev/null | head -n 1)

    # Check if the file was found
    if [ -n "$filepath" ]; then

        # Count the number of lines
        line_count=$(wc -l < "$filepath")

        # Compare with the target
        if [ "$line_count" -eq "$target_lines" ]; then
            echo "[+] Match Found!"
            echo "[+] File Name: $file"
            echo "[+] Line Count: $line_count"
            echo "[+] Full Path: $filepath"
            echo "------------------------------------------------"
            exit 0
        fi
    fi
done

echo "[-] No file containing exactly $target_lines lines was found."
```

### Key command

```bash
wc -l < file
```

This returns the number of lines in a file.

Example:

```text
230
```

---

# 5. File Owned by UID 502

Linux uses a numeric **UID (User ID)** to identify users.

This script searches for the file whose owner has UID `502`.

### Script

```bash
#!/bin/bash

# List of files to search
files=(8V2L bny0 c4ZX D8B3 FHl1 oiMO PFbD rmfX SRSq uqyw v2Vb X1Uy)

# Target UID
target_uid=502

echo "Searching for a file owned by UID: $target_uid"
echo "------------------------------------------------"

for file in "${files[@]}"; do

    # Find the file anywhere on the system
    filepath=$(find / -type f -name "$file" 2>/dev/null | head -n 1)

    # Check if the file was found
    if [ -n "$filepath" ]; then

        # Get the numeric UID of the owner
        file_uid=$(stat -c '%u' "$filepath" 2>/dev/null)

        # Compare UID
        if [ "$file_uid" -eq "$target_uid" ]; then
            echo "[+] Match Found!"
            echo "[+] File Name: $file"
            echo "[+] Owner UID: $file_uid"
            echo "[+] Full Path: $filepath"
            echo "------------------------------------------------"
            exit 0
        fi
    fi
done

echo "[-] No file found owned by UID $target_uid."
```

### Key command

```bash
stat -c '%u' file
```

This displays the numeric UID of the file owner.

Example:

```text
502
```

You can also find the username associated with the UID:

```bash
getent passwd 502
```

---

# 6. File Executable by Everyone

A file is executable by everyone when:

* The **owner** has execute permission.
* The **group** has execute permission.
* **Others** have execute permission.

For example:

```text
-rwxr-xr-x
```

The execute permissions are:

```text
Owner   Group   Others
  x       x       x
```

### Script

```bash
#!/bin/bash

# List of files to search
files=(8V2L bny0 c4ZX D8B3 FHl1 oiMO PFbD rmfX SRSq uqyw v2Vb X1Uy)

echo "Searching for a file executable by everyone..."
echo "------------------------------------------------"

for file in "${files[@]}"; do

    # Find the file anywhere on the system
    filepath=$(find / -type f -name "$file" 2>/dev/null | head -n 1)

    # Check if the file was found
    if [ -n "$filepath" ]; then

        # Check execute permission for:
        # Owner, Group, and Others
        if [ -x "$filepath" ] && \
           [ "$(stat -c '%A' "$filepath" | cut -c7)" = "x" ] && \
           [ "$(stat -c '%A' "$filepath" | cut -c10)" = "x" ]; then

            # Get numeric permissions
            perms=$(stat -c '%a' "$filepath")

            echo "[+] Match Found!"
            echo "[+] File Name: $file"
            echo "[+] Permissions: $perms"
            echo "[+] Full Path: $filepath"
            echo "------------------------------------------------"

            exit 0
        fi
    fi
done

echo "[-] No file executable by everyone was found."
```

### Easier `find` method

The same requirement can be checked using:

```bash
find / -type f -name "FILENAME" -perm -111 2>/dev/null
```

`-perm -111` means the file has execute permission for:

```text
Owner  → x
Group  → x
Others → x
```

For example:

```text
755 → rwxr-xr-x
777 → rwxrwxrwx
```

Both are executable by everyone.

---

# Quick Reference

| Requirement            | Command / Method                           |
| ---------------------- | ------------------------------------------ |
| Group is `best-group`  | `find / -group best-group 2>/dev/null`     |
| Contains IP address    | `grep -E -o '([0-9]{1,3}\.){3}[0-9]{1,3}'` |
| Matches SHA1           | `sha1sum`                                  |
| Contains 230 lines     | `wc -l`                                    |
| Owner UID is 502       | `stat -c '%u'`                             |
| Executable by everyone | `-perm -111`                               |

---

## Running a Script

Save the script:

```bash
nano script.sh
```

Make it executable:

```bash
chmod +x script.sh
```

Run it:

```bash
./script.sh
```

Or:

```bash
bash script.sh
```

---

## Useful Linux Enumeration Commands

```bash
# Find files by name
find / -type f -name "filename" 2>/dev/null

# Find files by group
find / -group best-group 2>/dev/null

# Find files by owner UID
find / -uid 502 2>/dev/null

# Find world-executable files
find / -type f -perm -111 2>/dev/null

# Count file lines
wc -l file

# Calculate SHA1
sha1sum file

# Show file owner and permissions
ls -la file

# Show numeric UID/GID and permissions
stat file
```

## Disclaimer

These scripts are intended for **authorized security testing, CTFs, cybersecurity labs, and systems you have permission to assess**.
