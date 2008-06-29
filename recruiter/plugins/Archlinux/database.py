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

repos = ('core', 'extra', 'community')

class sync(self):
    
    def refresh(self, repo, mirror):
        
        self.f = open('./'+repo+'.db.tar.gz')
        self.c=httplib.HTTPConnection(mirror)
        self.c.request("GET", repo+'/os/i686/'+repo+'.db.tar.gz')
        self.r=self.c.getresponse
        
        if self.r.status == 200:
            self.f.write(self.r.read())
        
        self.c.close()
        self.f.close()
    
    
    def expander(self, repo):
        
        if tarfile.is_tarfile(repo+'.db.tar.gz') == True:
            
            if os.path.exists('./'+repo) == False:
                os.path.mkdir('./'+repo)
            
            self.tar = tarfile.open(repo+'.db.tar.gz')
            self.tar.extractall('./'+repo)
            self.tar.close()
            
            self.wrt = ''
            
            for self.dir in os.listdir('./'+repo):
                self.wrt += dir+'\n'
            
            self.f = open(repo+'.db', 'w')
            self.f.write(self.wrt)
            self.f.close()
           
    def cleanup(self, repo):
        
        

#class for searching the package(very simple approach)

class search(self):
    
    def search(self, package):
        for self.repo in repos:
            self.f=open(self.repo+'.db', 'r')
            self.packages=self.f.read()
            self.f.close()
            
            for self.item in self.packages:
                if package == self.item:
                    return package
            
