#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Filename:
# Author:    E-mail:qingant@gmail.com
# Lisence: GPL-2.0 
import re
import types
import sys
import os


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

    def __init__(self,module,nodes):

        self.nodes = nodes
        #self.arrows = arrows
        self.head = dotoutput.head%module.__name__
    def label(self,node):
        

        tmp = node.title+'\\n\\n\\n'+'<f0>attributes:\\n\\n'+''.join([x+'\\n' for x in node.attrlist])+'|<f1>newlyadded:\\n\\n'+''.join([x+'\\n' for x in node.addedmethod])+'\\n\\n'+ 'rewritedmethod:\\n\\n'+''.join([x+'\\n' for x in node.rewritefunclist])
        #print tmp
        return tmp


    def out(self,output=False):
        if output :
            sys.stdout = open(output,'w')
        print self.head
        #print '----------------------',self.nodes
        for i in self.nodes  :
            print '"%s"[\nstyle=filled,\n'%i.title
            print 'shape=record,\n'
            print 'label="%s"\n'%self.label(i)
   
            print 'color="#eecc80"\n];'
        for i in self.nodes :
            if not i.fathers == []:
                for j in i.fathers:
                    print '  %s->%s;\n'%(j.title,i.title)
            
        print '}'

        
        
        
class Map(object):
    def __init__(self,module,eager=False):
        self.module = __import__(module)
        self.nodes =[]
        for i in dir(module) :
            lei = getattr(module,i)

            if type(lei) == types.ClassType :

                self.nodes.append(Node(lei))
        if eager :
            def f(node) :
                return [node]+[node.fathers]
            for i in self.nodes :
                self.nodes += f(i)

            self.nodes = list(set(self.nodes))


if __name__=='__main__' :
    x=Map(sys.argv[1],True)
    dotoutput(x.module,x.nodes).out('te')
