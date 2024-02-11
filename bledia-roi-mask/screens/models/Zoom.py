import cv2

class Zoom:
    def __init__(self):
        self.currentCanvasPoint = None
        self.zoomCycle = 0
        self.previousZoomCycle = 0
        self.lastCropStart = (0,0)
        self.lastZoomOriginalCenter = None
        self.zoomCenter = None
        self.zoomFactor = 80

    def setZoomFactor(self,factor):
        '''
            Args:
                factor (int) : crop cut size of square image
        '''
        self.zoomFactor = factor/3

    def zoomWithScroll(self,event):
        self.previousZoomCycle = self.zoomCycle
        if event.delta>0 or event.num==5: #scroll up
            if self.zoomCycle !=9 : 
                self.zoomCycle =self.zoomCycle+1
        elif event.delta<0 or event.num==4: #scrol down
            if self.zoomCycle!=0: 
                self.zoomCycle = self.zoomCycle-1
        self.currentCanvasPoint = (event.x,event.y)
        self.zoomCenter = (event.x,event.y)

    def zoomCropImage(self,image):
        '''
            For only square images
        '''
        if self.zoomCycle!=0 :
            # get zoom locatoin previous zoomed view
            x,y = self.getOriginalZoomCenter(image.shape)

            zoomValue = int(self.zoomFactor * self.zoomCycle)
            width, height = image.shape[0], image.shape[1]
            # get resized resolution            
            resizedImageDimension = (width+zoomValue,height+zoomValue)
            # resize image
            zoomedImage = cv2.resize(image,resizedImageDimension,interpolation=cv2.INTER_CUBIC)
            # new location of zoomed point
            zoomedX = int(x*float(resizedImageDimension[0])/width)
            zoomedY = int(y*float(resizedImageDimension[1])/height)

            # new crop
            startX,startY = zoomedX-x,zoomedY-y
            endX,endY = startX+width,startY+height

            croppedImage = zoomedImage[startY:endY,startX:endX]
            self.lastCropStart = (startX,startY)

            return croppedImage

        self.lastCropStart = (0,0)
        return image


    def getOriginalZoomCenter(self,imageDimension):

        if self.zoomCycle==9 and self.previousZoomCycle==9:
            return self.lastZoomOriginalCenter
        else:
            # here we get previous zoom cycle because, when zoomed the location may get changed
            # so we need the pointer location before current zoom
            zoomValue = self.zoomFactor*self.previousZoomCycle
            imageWidth,imageHeight = imageDimension[0],imageDimension[1]
            # resized resolution
            resizedWidth,resizedHeight = imageWidth+zoomValue,imageHeight+zoomValue

            # get zoom center real location on zoomed image
            croppedStartX = self.lastCropStart[0]+self.zoomCenter[0]
            croppedStartY = self.lastCropStart[1]+self.zoomCenter[1]

            originalImageX = int(croppedStartX*float(imageWidth)/resizedWidth)
            originalImageY = int(croppedStartY*float(imageHeight)/resizedHeight)
            self.lastZoomOriginalCenter = (originalImageX,originalImageY)

            return self.lastZoomOriginalCenter
        