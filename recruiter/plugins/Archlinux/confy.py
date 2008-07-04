#!/usr/bin/env python

"""Simple config parser

Example:

[ConfigOption]
ConfigValue

"""

"""
url: http://sourceforge.net/projects/pymusicpd/

Copyright (c) 2008 Imanol Celaya

Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 THE SOFTWARE.
 """
 
def get(conflc, task):
    """Searchs a section in a config file
    
    Arguments
    conflc = config file location
    task = section to search
    
    """
    
    f = open(conflc, 'r')
    sch = f.readlines()
    product = sch.index(task) + 1
    f.close()
    del f
    
    values = ['']
    for i in range(product, len(sch)):
        if sch[i] != '\n':
            values.append(sch[i])
        if sch[i] == '\n':
            break
    
    
    return values
    
def exists(location):
    """Says if a file exists(under development)
    
    Arguments
    location = file location
    
    """

def lstripng(name, until):
    
    noun = name
    
    for i in range(0, len(name)):
        if name[i] == until:
            noun = str(name[i+1:])
    
    return noun

'''Added to the original file, '''
def diference(complete, name):
    
    
    for i in range(0, len(complete)):
        try:
            tmp = name[i]
        
        except IndexError:
            noun = complete[i:]
            break
    
    return noun

def rstripng(name, until):
    
    noun = name
    
    for i in range(0, len(name)):
        if name[i] == until:
            noun = str(name[:i])
    
    return noun

def put(conflc, task, value):
    """Adds a task and/or value(under development)
    
    Arguments
    conflc = config file location
    task = section to search
    value = value of the secion
    
    """
    
    
    f = open(conflc, 'r')
    sch = f.readlines()
    f.close()
    try:
        product = sch.index(task)
        
        for i in range(1, len(value)):
            sch[product + i] = value[i]
            rstripng(sch[product + i], '\n')
            sch[product + i] += '\n'
        
        escribir = ''
        for i in range(0, len(sch)):
            escribir += sch[i]
            
        f=open(conflc, 'w')
        f.write(escribir)
        f.close()
    
        del f
    
    
    except ValueError:
        info = ''
        
        for i in range(0, len(sch)):
            info += sch[i]
        
        info += rstripng(task, '\n') + '\n'
        
        for i in range(1, len(value)):
            info += rstripng(value, '\n') + '\n'
        
        
        f=open(conflc, 'w')
        f.write(info)
        f.close()
        
        del f
