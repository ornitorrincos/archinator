"""
Copyright (c) 2008, Imanol celaya <ilcra1989@gmail.com>

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

import os
import httplib
import tarfile

#Execute both functions, one downloads the uncompressed tarfile and the other
#decompresses it, remember to delete the temporal directory.

repos= ('core', 'extra', 'community')

class sync(self):
    
    def refresh(repo, mirror):
        
        f = open('./'+repo+'.db.tar.gz')
        c=httplib.HTTPConnection(mirror)
        c.request("GET", repo+'/os/i686/'+repo+'.db.tar.gz')
        r=c.getresponse
        
        if r.status == 200:
            f.write(r.read())
        
        c.close()
        f.close()
    
    
    def expander(repo):
        
        if tarfile.is_tarfile(repo+'.db.tar.gz') == True:
            
            if os.path.exists('./'+repo) == False:
                os.path.mkdir('./'+repo)
            
           tar = tarfile.open(repo+'.db.tar.gz')
           tar.extractall('./'+repo)
           tar.close()
           
           wrt = ''
           
           for dir in os.listdir('./'+repo):
               wrt += dir+'\n'
           
           f = open(repo+'.db', 'w')
           f.write(wrt)
           f.close()
           

#class for searching the package(very simple approach)

class search(self):
    
    def search(package):
        for repo in repos:
            f=open(repo+'.db', 'r')
            packages=f.read()
            f.close()
            
            for item in packages:
                if package == item:
                    return package
            
