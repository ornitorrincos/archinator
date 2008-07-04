#!/usr/bin/env python

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
import sys
import httplib
import tarfile
import sqlite3
from confy import rstripng
from confy import lstripng
from confy import diference

'''Execute both functions, one downloads the uncompressed tarfile and the other
decompresses it, remember to delete the temporal directory.'''

repos = ('core', 'extra', 'community')

class sync:
    
    def refresh(self, repo, mirror):
        '''gets database from mirror'''
        self.f = open('./'+repo+'.db.tar.gz', 'w')
        self.c=httplib.HTTPConnection(mirror)
        self.c.request("GET", '/'+repo+'/os/i686/'+repo+'.db.tar.gz')
        self.r=self.c.getresponse()
        
        if self.r.status == 200:
            print self.r.status, self.r.reason
            self.f.write(self.r.read())
        
        else:
            print self.r.status, self.r.reason
        
        self.c.close()
        self.f.close()
    
    
    def expander(self, repo):
        '''compresses and processes the database'''
        if tarfile.is_tarfile(repo+'.db.tar.gz') == True:
            
            if os.path.exists('./'+repo) == False:
                os.mkdir('./'+repo)
            
            self.tar = tarfile.open(repo+'.db.tar.gz')
            self.tar.extractall('./'+repo)
            self.tar.close()
            os.remove(repo+'.db.tar.gz')
           
    def cleanup(self, repo):
        '''Cleans the temporary directory'''
        self.path='./'+repo
        
        for self.dire in os.listdir(self.path):
            for self.file in os.listdir(self.path+'/'+self.dire):
                os.remove(self.path+'/'+self.dire+'/'+self.file)
            
            os.removedirs(self.path+'/'+self.dire)
        
    
    def createdb(self, repo):
        self.conn = sqlite3.connect(repo+'.db')
        self.c = self.conn.cursor()
        self.c.execute('''create table packages (repo text, package text, version text, desc text)''')
        self.conn.commit()
        self.c.close()
    
    def updatedb(self, repo, mirror):
        
        self.conn = sqlite3.connect(repo+'.db')
        self.c = self.conn.cursor()
        
        for self.item in os.listdir('./'+repo):
            self.name = rstripng(rstripng(self.item, '-'), '-')
            self.t = (repo, self.name,
                      diference(self.item, self.name+'-'), 'none')
            self.c.execute('''insert into packages values (?,?,?,?)''', self.t)
        
        self.conn.commit()
        
    


class search:
    
    def sqlsearch(self, repo, package):
    
        self.conn = sqlite3.connect(repo+'.db')
    
    def search(self, repo, package):
        '''search for a package(quick fix, should migrate to sqlite3)'''
        
        self.path = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.plugins_path = self.path + '/plugins/Archlinux/'

        self.f=open(self.plugins_path+repo+'.db', 'r')
        self.packages=self.f.readlines()
        self.f.close()
        
        #self.packages
        self.list = []
        if os.path.exists('update.lock') == False:
            for self.item in self.packages:
                if package in rstripng(rstripng(self.item, '-'), '-'):
                    self.list.append(rstripng(rstripng(self.item, '-'), '-'))
        if os.path.exists('update.lock') == True:
            self.list.append('Actualizando base de datos...')
        
        return self.list


if __name__ == '__main__':
    try:
        if sys.argv[1] == '-test':
            sync().refresh('core', 'mir.archlinux.fr')
            sync().expander('core')
            sync().cleanup('core')
        if sys.argv[1] == '-update':
            for repo in repos:
                f = open('update.lock', 'w')
                f.close()
                sync().refresh(repo, 'mir.archlinux.fr')
                sync().expander(repo)
                sync().cleanup(repo)
                os.remove('update.lock')
        if sys.argv[1] == '-first-run':
            '''when sqlite is ready
            '''
            for repo in repos:
                sync().createdb(repo)
                sync().updatedb(repo, 'mir.archlinux.fr')
        else:
            print 'wrong command -test for test and -update for update'
    
    except IndexError:
        
        print 'wrong command -test for test and -update for update'
