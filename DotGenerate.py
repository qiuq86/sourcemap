#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Filename:
# Author:    E-mail:qingant@gmail.com
# Lisence: GPL-2.0 
import re
import types
import sys



class Node (object):
    def __init__(self,obj):
        attr = dir(obj)
        self.rewritefunclist = []
        self.attrlist = []
        self.addedmethod = []
        f = lambda x:Node(x)
        ## if len(obj.__bases__) == 0 :
        ##     self.fathers = []
        ## elif len(obj.__bases__) == 1 :
        ##     self.fathers = f(obj.__bases__[0])
        self.fathers = [Node(x) for x in obj.__bases__]    
        ## else :
        ##     self.fathers =map(obj.__bases__,f)
        for x in attr :
            if type(getattr(obj,x)) == types.MethodType :
                fathermethod = [getattr(i,x,False) for i in obj.__bases__]
                if fathermethod == [False]*len(fathermethod) :
                    self.addedmethod.append(x)
                elif not getattr(obj,x) in fathermethod :
                    
                    self.rewritefunclist.append(x)

                else  :
                    pass
                

            else :
                self.attrlist.append(x)
        self.title = obj.__name__


class dotoutput(object) :
    """a class translate structure to dot source"""
    head = """digraph G {

        graph [
         ratio="auto"
         label="%s" 
         labelloc=t
            fontname="simyou.ttf"
        ];
     node  [
      shape="box",
      style="dotted",
      fontname="simyou.ttf",
      fontsize="10"
     ];
     edge  [ fontname="simyou.ttf"];"""

    def __init__(self,module,nodes,arrows):

        self.nodes = nodes
        self.arrows = arrows
        self.head = dotoutput.head%module.__name__
    def label(self,node):
        

        tmp = node.title+'\\n\\n\\n'+'attributes:\\n\\n'+''.join([x+'\\n' for x in node.attrlist])+'\\n\\n\\nnewlyadded:\\n\\n'+''.join([x+'\\n' for x in node.addedmethod])+'\\n\\n'+ 'rewritedmethod:\\n\\n'+''.join([x+'\\n' for x in node.rewritefunclist])
        #print tmp
        return tmp


    def out(self):
        print self.head
        #print '----------------------',self.nodes
        for i in self.nodes  :
            print '"%s"[\nstyle=filled,\n'%i.title
            print 'label="%s"\n'%self.label(i)
            print 'color="#eecc80"\n];'
        for i in self.arrows :
            if not i[1] == ():
                for j in i[1]:
                    print '  %s->%s;\n'%(i[0].title,j.title)
            
        print '}'
        
def main(file):
    module = __import__(file)
    nodes =[]
    for i in dir(module) :
        lei = getattr(module,i)

        if type(lei) == types.ClassType :

            nodes.append(Node(lei))
    arrows = []
    for i in nodes :
        arrows.append((i,i.fathers))
        
    return module,nodes,arrows

if __name__=='__main__' :
    x=main(sys.argv[1])
    dotoutput(x[0],x[1],x[2]).out()
