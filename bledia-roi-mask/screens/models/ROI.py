

class ROI:
    def __init__(self,canvas,zoom,imageSet,viewingDimension):
        self.drawROI = False
        self.pointsROI = []
        self.originalPointsROI = []
        self.lineROIids = []
        self.canvas = canvas
        self.movingRoiLine = None
        self.zoom = zoom
        self.viewImageSet = imageSet
        self.viewDimension = viewingDimension

    
    def isDrawing(self):
        return self.drawROI

    def setDrawROI(self):
        self.drawROI = not self.drawROI

    def clearROI(self):
        self.pointsROI = []
        for line in self.lineROIids:
            self.canvas.delete(line)

    def removeLastPoint(self):
        self.pointsROI.pop()
        line = self.lineROIids.pop()
        self.canvas.delete(line)


    def createROI(self,event):
        if(self.drawROI):
            newPoint = (event.x,event.y)

            # check ending 
            if self._isEndingPoint(newPoint):
                newPoint = (self.pointsROI[0][0],self.pointsROI[0][1])
                self.pointsROI.append(newPoint)
                self.drawROI = False
                self._calculateOriginalROIPoints()
                if not self.movingRoiLine is None:
                    self.canvas.delete(self.movingRoiLine)
            else:
                self.pointsROI.append(newPoint)

            if len(self.pointsROI)>1:
                self._drawLines()


    def drawCursorFollwingLine(self,event):
        if not self.drawROI:
            return

        if not self.movingRoiLine is None:
            self.canvas.delete(self.movingRoiLine)

        newPoint = (event.x,event.y)

        # set current point for zoom
        currentCanvasPoint = newPoint
        if len(self.pointsROI)>0:
            count = len(self.pointsROI)
            lastPoint = self.pointsROI[count-1]
            line = self.canvas.create_line(lastPoint[0],lastPoint[1],newPoint[0],newPoint[1],fill="yellow",width=2)
            self.movingRoiLine = line


    def _drawLines(self):
        if len(self.pointsROI)>1:
            size = len(self.pointsROI)
            point1 = self.pointsROI[size-2]
            point2 = self.pointsROI[size-1]
            line  = self.canvas.create_line(point1[0],point1[1],point2[0],point2[1],fill="yellow",width=2)
            self.lineROIids.append(line)


    def _isEndingPoint(self,newPoint):
        if len(self.pointsROI)>2:
            firstPoint = self.pointsROI[0]

            # check differ by 10 pixel
            return abs(newPoint[0]-firstPoint[0])<10 and abs(newPoint[1]-firstPoint[1])<10 

    # this should called after zoomed
    def _calculateOriginalROIPoints(self):
        # original square size 
        originalImageDimension = self.viewImageSet.getADC().getCroppedCutSize()
        viewingDimension = self.viewDimension
        self.originalPointsROI = []

        if not self.zoom.zoomCycle==0:
            zoomValue = self.zoom.zoomFactor*self.zoom.zoomCycle
            zoomedDimension = (viewingDimension[0]+zoomValue,viewingDimension[1]+zoomValue)


            xC,yC = self.zoom.zoomCenter[0],self.zoom.zoomCenter[1]
            # new location of zoomed point
            zoomedX,zoomedY = int(xC*float(zoomedDimension[0])/viewingDimension[0]),int(yC*float(zoomedDimension[1])/viewingDimension[1])
            # getting start pixel location cropped viewing box
            startX,startY = zoomedX-xC,zoomedY-yC

            scaledROIPoints = []
            for point in self.pointsROI:
                scaledPoint = self._getViewDimensionPoint(point,viewingDimension)
                scaledROIPoints.append(scaledPoint)

            for point in scaledROIPoints:
                realPoint = self._getOriginalDemensionPoint(point,(originalImageDimension,originalImageDimension),viewingDimension)
                self.originalPointsROI.append(realPoint)                        

        
        else:
            for point in self.pointsROI:
                realPoint = self._getOriginalDemensionPoint(point,(originalImageDimension,originalImageDimension),viewingDimension)
                self.originalPointsROI.append(realPoint)     


    def _getViewDimensionPoint(self,point,viewDimension):

        zoomValue = self.zoom.zoomFactor*self.zoom.zoomCycle
        # resized resolution
        resizedWidth, resizedHeight = viewDimension[0]+zoomValue, viewDimension[1]+zoomValue

        # get zoomed location
        zoomedX = point[0]+self.zoom.lastCropStart[0]
        zoomedY = point[1]+self.zoom.lastCropStart[1]

        viewImageX = int(zoomedX*float(viewDimension[0])/resizedWidth)
        viewImageY = int(zoomedY*float(viewDimension[1])/resizedHeight)

        return (viewImageX,viewImageY)


    def _getOriginalDemensionPoint(self,point,originalImageDimension,viewingDimension):
        realPointX = int(point[0]*float(originalImageDimension[0])/viewingDimension[0])       
        realPointY = int(point[1]*float(originalImageDimension[1])/viewingDimension[1])
        return (realPointX,realPointY)

    def redrawROIPointsWithZoom(self):
        if self.drawROI:
            return

        # original square size 
        originalImageDimension = self.viewImageSet.getADC().getCroppedCutSize()
        viewingDimension = self.viewDimension

        self.pointsROI = []

        if len(self.originalPointsROI)>2:
            # convert to viewing dimenstion
            viewROI = []

            for point in self.originalPointsROI:
                newPoint = (int(point[0]*float(viewingDimension[0])/originalImageDimension),int(point[1]*float(viewingDimension[1])/originalImageDimension))
                viewROI.append(newPoint)

            if len(self.lineROIids)>0:
                for line in self.lineROIids:
                    self.canvas.delete(line)

            # if image is  zoomed
            if not self.zoom.zoomCycle == 0:
                zoomValue = self.zoom.zoomFactor*self.zoom.zoomCycle
                zoomedDimension = (viewingDimension[0]+zoomValue,viewingDimension[1]+zoomValue)

                for point in viewROI:
                    newPoint = (int(point[0]*float(zoomedDimension[0])/viewingDimension[0]),int(point[1]*float(zoomedDimension[1])/viewingDimension[1]))
                    newPoint = (newPoint[0]-self.zoom.lastCropStart[0],newPoint[1]-self.zoom.lastCropStart[1])
                    self.pointsROI.append(newPoint)

            else:
                for point in viewROI:
                    self.pointsROI.append(point)


            for i in range(len(self.pointsROI)-1):
                point1 = self.pointsROI[i]
                point2 = self.pointsROI[i+1]
                line  = self.canvas.create_line(point1[0],point1[1],point2[0],point2[1],fill="yellow",width=2)
                self.lineROIids.append(line)


                


