#!/usr/bin/python

# Grapher, a trivial graphing tool
# Copyright (C) 2014 Johan Thelin
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
from PyQt4 import Qt, QtCore, QtGui

class Bar():
    def __init__(self, value, color, label, valueLabel):
        self.value = value
        self.color = color
        self.label = label
        self.valueLabel = valueLabel

class BarGraph():
    def __init__(self):
        self.height = 80
        self.width = 100
        self.maxValue = -1;
        self.title = ""
        self.indent = 10

        self.bars = []

    def setTitle(self, title):
        self.title = title
        
    def setWidth(self, width):
        self.width = width

    def setHeight(self, height):
        self.height = height

    def getHeight(self):
        return self.height

    def addBar(self, bar):
        self.bars.append(bar);
        self.maxValue += bar.value

    def render(self, painter):
        titleHeight = 24
        titleMargin = 6
        labelHeight = 12
        labelMargin = 3
        
        titleFont = QtGui.QFont("Futura LT Pro Light")
        titleFont.setPixelSize(titleHeight)
        labelFont = QtGui.QFont("Liberation Sans")
        labelFont.setPixelSize(labelHeight)

        # Draw title
        painter.save()
        painter.setPen(Qt.Qt.darkGray)
        painter.setFont(titleFont)
        painter.drawText(0, titleHeight, self.title)
        painter.restore()
        
        x = self.indent
        for b in self.bars:
            # Draw bar
            w = (b.value*(self.width-self.indent))/self.maxValue
            painter.setBrush(b.color)
            painter.drawRect(x, titleHeight+titleMargin, w, self.height-titleHeight-labelHeight-titleMargin-labelMargin)
            x += w
            if x > self.width:
                x = self.width

            # Draw value label
            painter.save()
            painter.setPen(Qt.Qt.white)
            painter.setFont(labelFont)
            painter.drawText(0, self.height-(labelHeight+labelMargin)*2, x-1, labelHeight+labelMargin, Qt.Qt.AlignRight, b.valueLabel)
            painter.restore()

            # Draw label
            painter.save()
            painter.setPen(Qt.Qt.lightGray)
            painter.setFont(labelFont)
            painter.drawText(0, self.height-labelHeight-labelMargin, x, labelHeight+labelMargin, Qt.Qt.AlignRight, b.label)
            painter.restore()

class BarGraphStack():
    def __init__(self):
        self.width = 100
        self.spacing = 10
        self.graphs = []

    def setWidth(self, width):
        self.width = width

    def setSpacing(self, spacing):
        self.spacing = spacing

    def addBarGraph(self, graph):
        self.graphs.append(graph)

    def render(self):
        height = 0
        for g in self.graphs:
            g.setWidth(self.width-2)
            height += g.getHeight()

        if len(self.graphs) > 1:
            height += (len(self.graphs)-1)*self.spacing

        image = QtGui.QImage(self.width, height, QtGui.QImage.Format_RGB888)
        image.fill(Qt.Qt.white)
        painter = QtGui.QPainter()
        painter.begin(image)
        painter.setPen(Qt.Qt.white)

        y=0
        for g in self.graphs:
            painter.save()
            painter.translate(0, y)
            g.render(painter)
            painter.restore()
            y += g.getHeight() + self.spacing

        painter.end()
            
        return image

def main():
    app = QtGui.QApplication(sys.argv)
    
    output = "graph.png"
    if len(sys.argv) == 2:
        output = sys.argv[1]
    
    bs = BarGraphStack()
    
    bg = BarGraph()
    bg.setTitle("Image Size")
    bg.addBar(Bar(6349, Qt.Qt.darkGray, "6 349KiB", "kernel(bz)"))
    bg.addBar(Bar(25240, Qt.Qt.lightGray, "25 240KiB", "rootfs"))

#    bg.addBar(Bar(6349, Qt.Qt.darkGray, "6 349KiB", "kernel(bz)"))
#    bg.addBar(Bar(23840, Qt.Qt.lightGray, "23 840KiB", "rootfs"))
#    bg.addBar(Bar(1400, Qt.Qt.red, "", ""))

#    bg.addBar(Bar(6349, Qt.Qt.darkGray, "6 349KiB", "kernel (bz)"))
#    bg.addBar(Bar(13840, Qt.Qt.lightGray, "13 840KiB", "rootfs"))
#    bg.addBar(Bar(10000, Qt.Qt.red, "", ""))
#    bg.addBar(Bar(1400, QtGui.QColor(Qt.Qt.red).lighter(), "", ""))
    bs.addBarGraph(bg)

    bg = BarGraph()
    bg.setTitle("Boot time")
    bg.addBar(Bar(6400, Qt.Qt.darkGray, "6.4s", "kernel"))
    bg.addBar(Bar(4900, Qt.Qt.lightGray, "4.9s", "userspace"))
    bs.addBarGraph(bg)
    
    bs.setWidth(600)
    i = bs.render()
    i.save(output)

if __name__ == '__main__': 
    main()