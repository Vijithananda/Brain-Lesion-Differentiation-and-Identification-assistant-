import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

import cv2
from PIL import Image, ImageTk

import screens.models.mask as mask
from dicom.DicomFileProcess import DicomFileProcess
from fileprocess.FileProcess import FileProcess
from fileprocess.datastore import writeToCSV
from fileprocess.roi_datastore import exportMaskedMat, deleteRoiMaskedImages
from logic.math.GLCM import GLCM
from logic.math.Math import Math
from screens.models.BImageSet import BImageSet
from screens.models.ROI import ROI
from screens.models.Zoom import Zoom


class Bledia:
    def __init__(self):
        self.constants = {
            "bHeight": 150,
            "bWidth": 150,
            "adcHeight": 500,
            "adcWidth": 500
        }
        self.fileProcess  = FileProcess()
        self.dicomFileProcess= DicomFileProcess()
        self.viewImageSet = None

        self.currentImage = 0
        self.roi = None

        # Zoom
        self.zoom = Zoom()

        self._loadImages()

    def start(self):
        root = tk.Tk()

        # width x height + x_offset + y_offset:
        root.geometry("1000x700+30+100")
        # root.config(bg="lightgray")

        header = tk.Label(text="Bledia Python")
        header.grid(row=0,column=1,pady=20, padx=10,ipadx=10,sticky=tk.W+tk.E+tk.N+tk.S)

        # left column
        leftIconFrame = tk.Frame(master=root)

        # canvas set
        self.canvasb0 = tk.Canvas(master=leftIconFrame,width=150,height=150)
        self.canvasb1000 = tk.Canvas(master=leftIconFrame,width=150,height=150)
        self.canvasadc = tk.Canvas(master=leftIconFrame,width=150,height=150)
        self.mainCanvas = tk.Canvas(master=root,width=500,height=500)

        # load intial
        self.roi = ROI(self.mainCanvas,self.zoom,self.viewImageSet,(self.constants["adcWidth"],self.constants["adcHeight"]))
        

        # create empty image for inigues font colors for background opencvtial load
        self.imageadc = ImageTk.PhotoImage(image=Image.fromarray(self._getEmptyImage(self.constants["bWidth"],self.constants["bHeight"])))
        self.canvasAdcImage = self.canvasadc.create_image(0,0, anchor="nw",image=self.imageadc)      

        # B0 Image canvas

        # create empty image for initial load
        self.imageb0 = ImageTk.PhotoImage(image=Image.fromarray(self._getEmptyImage(self.constants["bWidth"],self.constants["bHeight"])))
        self.canvasb0Image = self.canvasb0.create_image(0,0, anchor="nw",image=self.imageb0)                

        # create empty image for inigues font colors for background opencvtial load
        self.imageb1000 = ImageTk.PhotoImage(image=Image.fromarray(self._getEmptyImage(self.constants["bWidth"],self.constants["bHeight"])))
        self.canvasb1000Image = self.canvasb1000.create_image(0,0, anchor="nw",image=self.imageb1000)        


        # lef column labels
        adcLabel = tk.Label(master=leftIconFrame,text="ADC")
        b0Label = tk.Label(master=leftIconFrame,text="b0")
        b1000Label = tk.Label(master=leftIconFrame,text="b1000")



        # pack in UI
        adcLabel.pack()
        self.canvasadc.pack()
        b0Label.pack()
        self.canvasb0.pack()
        b1000Label.pack()
        self.canvasb1000.pack()
        leftIconFrame.grid(row=1,column=1,padx=10,)        

        # Main image View
        # create empty image for initial load
        self.mainImage = ImageTk.PhotoImage(image=Image.fromarray(self._getEmptyImage(self.constants["adcWidth"],self.constants["adcHeight"])))
        self.mainCanvas.grid(row=1,column=2,rowspan=6,columnspan=2, padx=10,sticky=tk.W+tk.E+tk.N+tk.S)
        self.mainCanvasImage = self.mainCanvas.create_image(0,0, anchor="nw",image=self.mainImage)   
        self.mainCanvas.bind("<Button-1>",self._onClickCanvas) 
        self.mainCanvas.bind("<Key>",self._onPressEscapeCanvas)
        self.mainCanvas.bind("<Motion>",self._onMouseOverCanvas)
        self.mainCanvas.bind("<MouseWheel>",self._zoomer)
        self.mainCanvas.bind("<Button-5>",self._zoomer)
        self.mainCanvas.bind("<Button-4>",self._zoomer)


        rightFrame = tk.Frame(master=root)
        rightFrame.grid(row=1,column=5,columnspan=2, padx=10,sticky=tk.W+tk.E+tk.N+tk.S)

        # Option Columns
        navigationFrame = tk.Frame(master=rightFrame,pady=15)
        self.nextButton = tk.Button(navigationFrame,text="Next",command=self._nextImage)
        self.previousButton = tk.Button(navigationFrame,text="Previos",command=self._previousImage)
        # self.previousButton.grid(row=0,column=0, padx=5,sticky=tk.W+tk.E+tk.N+tk.S)
        # self.nextButton.grid(row=0,column=1, padx=5,sticky=tk.W+tk.E+tk.N+tk.S)

        navigationLabel = tk.Label(master=navigationFrame,text="Navigation",pady=5)

        navigationLabel.pack()
        self.previousButton.pack(side="left")
        self.nextButton.pack(side="left")

        navigationFrame.pack()


        # ROI - 
        roiFrame = tk.Frame(master=rightFrame)
        
        roiLabel = tk.Label(master=roiFrame,text="ROI Options",pady=5)
        roiLabel.pack()

        self.enableRoiButton = tk.Button(roiFrame,text="ROI",command=self._enableROI)
        self.enableRoiButton.pack(side="left")

        self.clearRoiButton = tk.Button(roiFrame,text="Reset",command=self._clearROI)
        self.clearRoiButton.pack(side="left")

        roiFrame.pack()



        # Load New Image set
        newImageSetFrame = tk.Frame(master=rightFrame,pady=15)

        newFrameLabel = tk.Label(master=newImageSetFrame,text="Sequence Set Options",pady=5)
        newFrameLabel.pack()

        self.loadSequenceButton = tk.Button(newImageSetFrame,text="Load New Sequence",command=self._loadSequence)
        self.loadSequenceButton.pack(side="left")        

        newImageSetFrame.pack()


        # Data set
        dataSetFrame = tk.Frame(master=rightFrame,width=150)
        dataSetLabel = tk.Label(master=dataSetFrame,text="ROI Properties")
        dataSetLabel.pack()

        self.calculateROIData = tk.Button(master=dataSetFrame,text="Calculate Properties",command=self._calculateDataset)
        self.calculateROIData.pack()

        self.dataTree = ttk.Treeview(master=dataSetFrame)
        self.dataTree["columns"] = ("one")
        self.dataTree.column("#0", width=75)
        self.dataTree.column("one", width=100)

        self.dataTree.heading("#0", text="Property", anchor=tk.W)
        self.dataTree.heading("one", text="Value", anchor=tk.W)

        self.dataTree.pack(side="bottom")

        self.dataTree.insert("", 0, text="glcm shade", values=("0"))
        self.dataTree.insert("", 0, text="glcm prominence", values=("0"))
        self.dataTree.insert("", 0, text="glcm correlation", values=("0"))
        self.dataTree.insert("", 0, text="glcm homogenity", values=("0"))
        self.dataTree.insert("", 0, text="glcm contrast", values=("0"))
        self.dataTree.insert("", 0, text="glcm entrophy", values=("0"))
        self.dataTree.insert("", 0, text="glcm energy", values=("0"))
        self.dataTree.insert("", 0, text="glcm variance j", values=("0"))
        self.dataTree.insert("", 0, text="glcm variance i", values=("0"))
        self.dataTree.insert("", 0, text="glcm mean j", values=("0"))
        self.dataTree.insert("", 0, text="glcm mean i", values=("0"))
        self.dataTree.insert("", 0, text="kurtosis", values=("0"))
        self.dataTree.insert("", 0, text="skewness", values=("0"))
        self.dataTree.insert("", 0, text="mean", values=("0"))

        dataSetFrame.pack()

        self._setCurrentImage(0)
        root.mainloop()


    # #####################################################
    #           Intial Loadiding
    # #####################################################
    def _loadImages(self):
        adcImageDirectory =  os.path.abspath(os.path.join(os.getcwd(),"temp","adc"))
        fileList = self.fileProcess.listFiles(str(adcImageDirectory))
        self.imageList = fileList
        if len(self.imageList)>0:
            self.viewImageSet = BImageSet(self.imageList[0])



    # #####################################################
    #           Update Image
    # #####################################################
    def _setCurrentImage(self,index):

        if len(self.imageList) > 0:
            self.viewImageSet = BImageSet(self.imageList[index])
            self.zoom.setZoomFactor(self.viewImageSet.getADC().getCroppedCutSize())
        
        else:
            return
            # self.viewImageSet = BImageSet()
        
        b0Image = self.viewImageSet.getB0Image()
        b0Image.setContrast(15)
        b0Image = b0Image.getProcessedResizedImage(self.constants["bWidth"],self.constants["bHeight"])
        self.imageb0 = ImageTk.PhotoImage(image=Image.fromarray(b0Image))
        self.canvasb0.itemconfig(self.canvasb0Image,image=self.imageb0)


        b1000Image = self.viewImageSet.getB1000Image()
        b1000Image.setContrast(15)
        b1000Image.setBrightness(20)
        b1000Image = b1000Image.getProcessedResizedImage(self.constants["bWidth"],self.constants["bHeight"])
        self.imageb1000 = ImageTk.PhotoImage(image=Image.fromarray(b1000Image))
        self.canvasb1000.itemconfig(self.canvasb1000Image,image=self.imageb1000)

        adcImage = self.viewImageSet.getADC()
        adcImage.setContrast(15)
        adcImage = adcImage.getProcessedResizedImage(self.constants["bWidth"],self.constants["bHeight"])
        self.imageadc = ImageTk.PhotoImage(image=Image.fromarray(adcImage))
        self.canvasadc.itemconfig(self.canvasb1000Image,image=self.imageadc)

        # If created image is available
        mainImage = self.viewImageSet.getADCCreatedImage()
        if not self.viewImageSet.is_b0_b1000_available():
            mainImage = self.viewImageSet.getADC()

        mainImage.setContrast(15)
        mainImage = mainImage.getProcessedResizedImage(self.constants["adcWidth"],self.constants["adcHeight"])
        mainImage = self._zoomCropImage(mainImage)
        self.mainImage = ImageTk.PhotoImage(image=Image.fromarray(mainImage))
        self.mainCanvas.itemconfig(self.mainCanvasImage,image=self.mainImage)

        
    def _getEmptyImage(self,width,height):
        imag = cv2.imread(str(os.path.join(os.getcwd(),"assets","images","fill","no_image.png")))
        imag = cv2.cvtColor(imag,cv2.COLOR_BGR2GRAY)
        return cv2.resize(imag,(width,height),interpolation=cv2.INTER_CUBIC)

    def _nextImage(self):
        imageCount = len(self.imageList)
        currentIndex = self.currentImage
        self._resetMainCanvas()

        if currentIndex+1<imageCount:
            currentIndex = currentIndex+1

        self.currentImage = currentIndex
        self._setCurrentImage(currentIndex)

    
    def _previousImage(self):
        currentIndex = self.currentImage
        self._resetMainCanvas()

        if currentIndex-1>=0:
            currentIndex = currentIndex-1

        self.currentImage = currentIndex
        self._setCurrentImage(currentIndex)

    def _resetMainCanvas(self):
        self.roi.clearROI()     
        self.zoom = Zoom() 
        self._clearDataset()
        self.roi = ROI(self.mainCanvas,self.zoom,self.viewImageSet,(self.constants["adcWidth"],self.constants["adcHeight"]))

    # #####################################################
    #           Button callback
    # #####################################################

    def _enableROI(self):
        self.roi.setDrawROI()

    def _clearROI(self):
        self.roi.clearROI()

    def _removeLastPoint(self):
        self.roi.removeLastPoint()

    # #####################################################
    #           Canvas event callback
    # #####################################################

    def _onClickCanvas(self,event):
        self.roi.createROI(event)

    def _onPressEscapeCanvas(self,event):
        print ("pressed"+ repr(event.char))

    def _onMouseOverCanvas(self,event):
        self.roi.drawCursorFollwingLine(event)



    # #####################################################
    #           Zoom Image
    # #####################################################
    def _zoomer(self,event):
        if self.roi.isDrawing():
            return

        self.zoom.zoomWithScroll(event)
        # change image
        self._setCurrentImage(self.currentImage)
        # change roi
        self.roi.redrawROIPointsWithZoom()        


    def _zoomCropImage(self,image):
        '''
            For only square images
        '''
        return self.zoom.zoomCropImage(image)


    # #####################################################
    #           Select Sequence
    # #####################################################


    def _loadSequence(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        filename = filedialog.askdirectory()
        if filename:
            self.dicomFileProcess.deleteMerged()
            self.dicomFileProcess.deleteSortedFiles()
            deleteRoiMaskedImages()
            self.dicomFileProcess.sortB0B1000Files(filename)
            self._loadImages()
            self._setCurrentImage(0)


    # #####################################################
    #           Select Sequence
    # #####################################################

    def _calculateDataset(self):
        imageObject = self.viewImageSet.getADC()
        # image = imageObject.getOriginalImage()
        image = self.viewImageSet.getGeneratedADCMat()
        imageDimension = imageObject.getCroppedCutSize()
        if  not self.roi.isDrawing() and len(self.roi.originalPointsROI)>2: 
            # generate mask for the ROI
            generatedMask = mask.generateMask((imageDimension,imageDimension),self.roi.originalPointsROI)

            # save roi
            maskedImageName = ""+str(self.viewImageSet.getB0Image().getDicomFile().getPersonId()).replace("/","").replace(" ","_")+"_"+str(self.viewImageSet.getImageName())
            exportMaskedMat(generatedMask,self.viewImageSet.getADCCreatedImage().getProcessedImage(),maskedImageName)

            # calculate basic features and glcm features
            basicProperties = Math(generatedMask,image)
            glcmFeatures = None
            if not self.viewImageSet.generaedADCMat is None:
                generatedImage =  (image-image.min())/(image.max()-image.min())*255
                generatedImage = generatedImage.astype(int)
                glcmFeatures = GLCM(generatedImage,generatedMask,maxValue=256)
            else:
                glcmFeatures = GLCM(image,generatedMask)

            child = self.dataTree.get_children()
            for item in child:
                # self.dataTree.item(item,text="skewness",values=("45"))
                if self.dataTree.item(item)["text"]=="skewness":
                    self.dataTree.item(item,text="skewness",values=(str(basicProperties.getSkewness())))
                elif self.dataTree.item(item)["text"]=="kurtosis":
                    self.dataTree.item(item,text="kurtosis",values=(str(basicProperties.getKurtosis())))
                elif self.dataTree.item(item)["text"]=="mean":
                    self.dataTree.item(item,text="mean",values=(str(basicProperties.mean)))
                elif self.dataTree.item(item)["text"]=="glcm mean i":
                    self.dataTree.item(item,text="glcm mean i",values=(str(glcmFeatures.mean[0])))
                elif self.dataTree.item(item)["text"]=="glcm mean j":
                    self.dataTree.item(item,text="glcm mean j",values=(str(glcmFeatures.mean[1])))
                elif self.dataTree.item(item)["text"]=="glcm variance i":
                    self.dataTree.item(item,text="glcm variance i",values=(str(glcmFeatures.variance[0])))
                elif self.dataTree.item(item)["text"]=="glcm variance j":
                    self.dataTree.item(item,text="glcm variance j",values=(str(glcmFeatures.variance[1])))
                elif self.dataTree.item(item)["text"]=="glcm energy":
                    self.dataTree.item(item,text="glcm energy",values=(str(glcmFeatures.energy)))
                elif self.dataTree.item(item)["text"]=="glcm entrophy":
                    self.dataTree.item(item,text="glcm entrophy",values=(str(glcmFeatures.entrophy)))
                elif self.dataTree.item(item)["text"]=="glcm contrast":
                    self.dataTree.item(item,text="glcmabsFileADCPath contrast",values=(str(glcmFeatures.contrast)))
                elif self.dataTree.item(item)["text"]=="glcm homogenity":
                    self.dataTree.item(item,text="glcm homogenity",values=(str(glcmFeatures.homogenity)))
                elif self.dataTree.item(item)["text"]=="glcm correlation":
                    self.dataTree.item(item,text="glcm correlation",values=(str(glcmFeatures.correlation)))
                elif self.dataTree.item(item)["text"]=="glcm shade":
                    self.dataTree.item(item,text="glcm shade",values=(str(glcmFeatures.shade)))
                elif self.dataTree.item(item)["text"]=="glcm prominence":
                    self.dataTree.item(item,text="glcm prominence",values=(str(glcmFeatures.prominence)))
            writeToCSV(imageObject,self.roi.originalPointsROI,basicProperties,glcmFeatures)
                                
                



    def _clearDataset(self):
        child = self.dataTree.get_children()
        for item in child:
            self.dataTree.item(item,text=self.dataTree.item(item)["text"],values=("0"))
