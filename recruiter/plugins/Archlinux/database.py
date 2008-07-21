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
import urllib
from confy import rstripng
from confy import diference
from confy import get
import simplejson

'''Execute both functions, one downloads the uncompressed tarfile and the other
decompresses it, remember to delete the temporal directory.'''

repos = ('core', 'extra', 'community')

class sync:
    
    def refresh(self, repo, mirror):
        '''gets database from mirror'''
        self.f = open('./'+repo+'.db.tar.gz', 'w')
        self.c=urllib.urlopen(mirror+'os/i686/'+repo+'.db.tar.gz').read()

        self.f.write(self.c)
        
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
    
    def updatedb(self, repo):
        
        self.conn = sqlite3.connect(repo+'.db')
        self.c = self.conn.cursor()
        
        for self.item in os.listdir('./'+repo):
            self.name = rstripng(rstripng(self.item, '-'), '-')
            self.t = (repo, self.name,
                      diference(self.item, self.name+'-'),
                      rstripng(get(repo+'/'+self.item+'/desc', '%DESC%\n')[1], '\n'))
            self.c.execute('''insert into packages values (?,?,?,?)''', self.t)
        
        self.conn.commit()
        self.c.close()
        
    
    def createaurdb(self):
        
        self.json = urllib.urlopen('http://aur.archlinux.org/rpc.php?type=search&arg=').read()
        self.K = simplejson.loads(self.json)
        
        self.conn = sqlite3.connect('aur.db')
        self.c = self.conn.cursor()
        
        self.c.execute('''create table packages (repo text, package text, version text, desc text)''')
        self.conn.commit()
        
        for self.elem in self.K['results']:
            self.t = ('aur', self.elem['Name'], 'None', 'none')
            
            self.c.execute('''insert into packages values (?,?,?,?)''', self.t)
        
        
        
    
    def cleandb(self, repo):
        if os.path.exists(repo+'.db'):
            os.remove(repo+'.db')
    


class search:
    
    def __init__(self):
        self.path = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.plugins_path = self.path + '/plugins/Archlinux/'
        self.repolist = []
        self.aurlist = []
    
    def sqlsearch(self, repo, package):
        
        if not os.path.exists(self.plugins_path+'update.lock'):
            if not os.path.exists(self.plugins_path+repo+'.db'):
                raise RepoError(repo)
            else:
                self.conn = sqlite3.connect(self.plugins_path+repo+'.db')
                self.c = self.conn.cursor()
                self.t = ('%'+package+'%',)
                self.c.execute('''select * from packages where ( package like ?)''',
                 self.t)
                
                self.res = self.c.fetchall()
                self.conn.commit()
                self.c.close()
            
                for self.line in self.res:
                    self.repolist.append(self.line[1])
        if os.path.exists(self.plugins_path+'update.lock') == True:
            self.repolist.append('Actualizando base de datos...')
        return self.repolist
    
    def aurlsearch(self, package):
        
        self.aur='http://aur.archlinux.org/rpc.php?type=search&arg='
        self.c = urllib.urlopen(self.aur+package).read()
        
        for self.element in simplejson.loads(self.c)[u'results']:
            self.aurlist.append(self.element[u'Name'])
            
        return self.aurlist
        
class info:
    def __init__(self):
        self.path = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.plugins_path = self.path + '/plugins/Archlinux/'
        
    def sqlinfo(self, repo, package):
        
        if not os.path.exists(self.plugins_path+repo+'.db'):
            raise RepoError(repo)
        
        self.conn = sqlite3.connect(self.plugins_path+repo+'.db')
        self.c = self.conn.cursor()
        
        self.t (package,)
        self.c.execute('''select * from packages where (package like ?)''',
         self.t)
        
        self.res = self.c.fetchall()
        self.conn.commit()
        self.c.close()
        
        try:
            self.resp = self.res[3]
        except IndexError:
            raise PackageError(package)
        else:
            return str(self.resp)
        
    def aurlinfo(self, package):
        pass
    

class Error(Exception):
    '''basic error class'''
    pass


class RepoError(Error):
    '''raised when repo not found'''
    def __init__(self, repo):
        self.message = repo + ' not found'
class PackageError(Error):
    '''raised when package not found'''
    def __init__(self, package):
        self.message = package + ' not found'

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
                sync().cleandb(repo)
                sync().refresh(repo, 'mir.archlinux.fr')
                sync().expander(repo)
                sync().createdb(repo)
                sync().updatedb(repo)
                sync().cleanup(repo)
                os.remove('update.lock')
        if sys.argv[1] == '-test-aur':
            
            print search().aurlsearch('kernel26')
        
        else:
            print 'wrong command -test for test and -update for update'
    
    except IndexError:
        
        print 'wrong command -test for test and -update for update or \
        -test-aur for teting aur search capabilities'
