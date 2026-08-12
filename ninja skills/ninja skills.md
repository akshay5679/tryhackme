                           files owned by the best-group
                          -------------------------------------
                          
find / -group best-group 2>/dev/null


                    2. file containing ip address 
                     ----------------------------
                     
#!/bin/bash

# Define the list of files to search for
files=(8V2L bny0 c4ZX D8B3 FHl1 oiMO PFbD rmfX SRSq uqyw v2Vb X1Uy)

echo "Searching for files and extracting IP addresses..."
echo "------------------------------------------------"

# Loop through each file in the array
for file in "${files[@]}"; do
    # Locate the file on the system, suppressing error messages
    filepath=$(find / -type f -name "$file" 2>/dev/null | head -n 1)
    
    # Check if the file was actually found
    if [ -n "$filepath" ]; then
        # Search the file content for a valid IP address pattern
        ip_found=$(grep -E -o "([0-9]{1,3}\.){3}[0-9]{1,3}" "$filepath" 2>/dev/null)
        
        # If an IP address is found, display the results
        if [ -n "$ip_found" ]; then
            echo "[+] Found File: $filepath"
            echo "[+] IP Address: $ip_found"
            echo "------------------------------------------------"
        fi
    fi
done


                            3.  file containing sha1 hash
                             ------------------------------
                             
#!/bin/bash

# Define the list of files to search for
files=(8V2L bny0 c4ZX D8B3 FHl1 oiMO PFbD rmfX SRSq uqyw v2Vb X1Uy)
target_hash="9d54da7584015647ba052173b84d45e8007eba94"

echo "Searching for the file matching SHA1 hash: $target_hash..."
echo "--------------------------------------------------------"

# Loop through each file name
for file in "${files[@]}"; do
    # Locate the file on the system, hiding access errors
    filepath=$(find / -type f -name "$file" 2>/dev/null | head -n 1)
    
    # If the file exists, calculate its SHA1 hash
    if [ -n "$filepath" ]; then
        current_hash=$(sha1sum "$filepath" | awk '{print $1}')
        
        # Check if the calculated hash matches our target hash
        if [ "$current_hash" == "$target_hash" ]; then
            echo "[+] Match Found!"
            echo "[+] File Name: $file"
            echo "[+] Full Path: $filepath"
            echo "--------------------------------------------------------"
            exit 0
        fi
    fi
done

echo "[-] No matching file found for that hash."






                       4.  file contains 230 lines
                         ---------------------------
                         
 
#!/bin/bash

files=(8V2L bny0 c4ZX D8B3 FHl1 oiMO PFbD rmfX SRSq uqyw v2Vb X1Uy)

echo "File Name | Line Count | Full System Path"
echo "--------------------------------------------------------"

for file in "${files[@]}"; do
    # Find the file on the system
    filepath=$(find / -type f -name "$file" 2>/dev/null | head -n 1)
    
    if [ -n "$filepath" ]; then
        # Count lines using both standard methods to compare
        lines_grep=$(grep -c '^' "$filepath" 2>/dev/null)
        
        echo "$file | $lines_grep lines | $filepath"
    else
        echo "$file | NOT FOUND on system"
    fi
done



                         5.  file's owner id 502?
                          ------------------------ 
                          
#!/bin/bash

# Define the list of files to search for
files=(8V2L bny0 c4ZX D8B3 FHl1 oiMO PFbD rmfX SRSq uqyw v2Vb X1Uy)
target_uid=502

echo "Searching for the file owned by UID: $target_uid..."
echo "--------------------------------------------------------"

# Loop through each file name
for file in "${files[@]}"; do
    # Locate the file on the system, hiding permission errors
    filepath=$(find / -type f -name "$file" 2>/dev/null | head -n 1)
    
    # If the file exists, check its owner ID
    if [ -n "$filepath" ]; then
        # stat -c '%u' extracts the numeric User ID (UID) of the file owner
        file_uid=$(stat -c '%u' "$filepath" 2>/dev/null)
        
        # Check if the UID matches our target
        if [ "$file_uid" -eq "$target_uid" ]; then
            echo "[+] Match Found!"
            echo "[+] File Name: $file"
            echo "[+] Owner UID: $file_uid"
            echo "[+] Full Path: $filepath"
            echo "--------------------------------------------------------"
            exit 0
        fi
    fi
done

echo "[-] No file found owned by UID $target_uid."




                       6. file executable by everyone 
                        ------------------------------
                        
#!/bin/bash

# Define the list of files to search for
files=(8V2L bny0 c4ZX D8B3 FHl1 oiMO PFbD rmfX SRSq uqyw v2Vb X1Uy)

echo "Searching for the file executable by everyone (777 or world-executable)..."
echo "------------------------------------------------------------------------"

# Loop through each file name
for file in "${files[@]}"; do
    # Locate the file on the system, hiding permission errors
    filepath=$(find / -type f -name "$file" 2>/dev/null | head -n 1)
    
    # If the file exists, check if it is executable by user, group, and others
    if [ -n "$filepath" ]; then
        # -perm -o+x checks if "others" have execute permissions
        # -perm -u+x -a -perm -g+x -a -perm -o+x ensures EVERYONE has execute permissions
        if [ -x "$filepath" ] && [ -w "$filepath" ] || find "$filepath" -perm -111 &>/dev/null; then
            # Let's get the exact octal permissions to verify (e.g., 755 or 777)
            perms=$(stat -c "%a" "$filepath" 2>/dev/null)
            
            # Check if the last digit (others) is odd (1, 3, 5, 7 mean executable)
            # A file executable by *everyone* typically has permissions like 755 or 777
            other_perm=$((perms % 10))
            if (( other_perm % 2 != 0 )); then
                echo "[+] Match Found!"
                echo "[+] File Name: $file"
                echo "[+] Permissions (Octal): $perms"
                echo "[+] Full Path: $filepath"
                echo "------------------------------------------------------------------------"
                exit 0
            fi
        fi
    fi
done

echo "[-] No file found that is executable by everyone."
                                                 



                          
