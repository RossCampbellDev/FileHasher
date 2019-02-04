# FileHasher
This is a simple script for taking in a file name (optional hash mode and output file) and then hashing this file.

the hash is then compared with the output file (or a default file, if it exists).  If a matching filename is found in this 'library', the hashes are compared.  If the hashes are different, this indicates a change to the file, which is a potential indicator of compromise.

If no file match is found, the hash is appended to the 'library' file.  A 'replace' flag also allows for the old hash to be over-written.
