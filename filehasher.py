#!/usr/bin/env python3
import sys
import argparse
import hashlib
import re

# take a file name and hash type in, and return the hex digest of that file
def hashFile(fileIn, hashType):
    # select hashing type, default to MD5
    if hashType==2:
        hasher = hashlib.sha256()
    elif hashType==3:
        hasher = hashlib.sha512()
    else:
        hasher = hashlib.md5()

    # create hash of file and write result to output file
    f = open(fileIn, "r").read().encode('utf-8')
    hasher.update(f)

    return hasher.hexdigest()


def main():
    parser = argparse.ArgumentParser(description='hash files and compare to previous hashes')
    parser.add_argument('-f', metavar='filein', dest='fileIn', required=True, help="name of the file to be hashed.  required.")
    parser.add_argument('-o', metavar='fileout', dest='fileOut', required=False, default='hashout.txt', help="name of output file to write result.  will use \'hashout.txt\' if none given.  Hashes will be recorded in the format 'filename,<hash>'")
    parser.add_argument('-m', metavar='hashtype', dest='hashType', type=int, required=False, default=1, help="number indicating hash type to use.\n 1\tMD5\n2\tSHA256\n3\tSHA512")
    parser.add_argument('-r',  action='store_true', required=False, help="flag indicates that old hashes should be replaced with newly generated ones")

    args = parser.parse_args()

    currentHash = hashFile(args.fileIn, args.hashType)
    print("New hash result: \n%s" % currentHash)

    f = open(args.fileOut, "r+")
    originalFile = f.readlines()
    f.seek(0)
    hashLibrary = f.read().split("\n")# originalFile.split("\n")

    # traverse the library of hashes.  if we find the file already has a hash, compare them.
    # alert if the hash is different.
    # if the file is not found, append the hash to the end of the file
    found = False
    lineNo = 0
    x = 0
    for line in hashLibrary:
        if len(re.findall("^" + args.fileIn, line)) > 0:
            l = line.split(",")
            oldHash = l[1]
            found = True
            
            if oldHash != currentHash:
                lineNo = x
                print("HASH MISMATCH FOUND")

                if len(oldHash) != len(currentHash):
                    print("hashes of different length, potential type clash")

                print("Previous hash: \n%s" % oldHash)
            else:
                print("File found, hash is consistent!")
        
        x=x+1


    # either append a new hash, or replace an old one if that flag is given
    f.close()
    if not found:
        f = open(args.fileOut, "a")
        f.write(args.fileIn + "," + currentHash + "\n")
    elif args.r is not None:
        f = open(args.fileOut, "w")
        for line in originalFile:
            if len(re.findall("^" + args.fileIn, line)) > 0:
                f.write(args.fileIn + "," + currentHash)
            else:
                f.write(line)

    f.close()


if __name__ == "__main__":
    main()
