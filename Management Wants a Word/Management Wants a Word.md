# Management Wants a Word — Forensics

## 1. Extract Windows Credentials

```bash
python3 /usr/share/doc/python3-impacket/examples/secretsdump.py \
  -sam SAM -security SECURITY -system SYSTEM LOCAL
```

## 2. Find DPAPI Masterkeys

```bash
find . -type f -path '*Microsoft/Protect/*'
```

Decrypt the masterkey:

```bash
python3 /usr/share/doc/python3-impacket/examples/dpapi.py masterkey \
  -file <MASTERKEY_FILE> \
  -sid <USER_SID> \
  -password 'minivera'
```

## 3. Find Chrome Data

```bash
find . -type f -name 'Login Data' -o -name 'Local State'
```

Extract the encrypted password:

```sql
SELECT hex(password_value) FROM logins;
```

Decrypt it using the recovered Chrome key:

```bash
python3 chrome_decrypt.py \
  --local-state "<LOCAL_STATE>" \
  --blob-hex "<ENCRYPTED_BLOB>" \
  --key "<CHROME_KEY>"
```


## 4. Mount the VeraCrypt Volume

```bash
sudo cryptsetup open --type tcrypt backup backup_mapped
sudo mkdir -p /mnt/backup_mount
sudo mount /dev/mapper/backup_mapped /mnt/backup_mount
ls -la /mnt/backup_mount
```

