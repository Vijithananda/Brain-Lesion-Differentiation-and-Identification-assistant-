import os
from dicom.DicomFile import DicomFile
import cv2
from pydicom import Dataset
from pydicom.data import get_testdata_files
import numpy as np
from fileprocess.datastore import readADCMatFromFile

class BImageSet:
    def __init__(self):
        pass

    def __init__(self,imageName):
        '''
            Constructor
            Args:
                imageName (str) : The name of the ADC file
        '''
        self.imageName = imageName
        self.adcImage=None
        self.b0Image = None
        self.b1000Image = None
        self.adcCreated = None
        self.originalROI = None
        self.generaedADCMat = None
        self._loadImages(imageName)
        

    def setOriginalROI(self,roiPointList):
        '''
            Set Original ROI point set

            Args:
                roiPointList (tuple list) : tuple list of points
        '''
        self.originalROI = roiPointList


    def _loadImages(self,imageName):
        '''
            Load images for b0,b1000 and adc

            Args:
                imageName (str) : The name of the ADC file
        '''
        if(imageName!=None):
            self.adcImage =BImage(DicomFile(str(os.path.join(os.getcwd(),"temp","adc",imageName)))) 

        if os.path.exists(str(os.path.join(os.getcwd(),"temp","sequence","b0",imageName))):
            self.b0Image = BImage(DicomFile(str(os.path.join(os.getcwd(),"temp","sequence","b0",imageName))))


        if os.path.exists(str(os.path.join(os.getcwd(),"temp","sequence","b1000",imageName))):
            self.b1000Image = BImage(DicomFile(str(os.path.join(os.getcwd(),"temp","sequence","b1000",imageName))))

        if os.path.exists(str(os.path.join(os.getcwd(),"temp","sequence","adc",imageName))):
            self.adcCreated = BImage(DicomFile(str(os.path.join(os.getcwd(),"temp","sequence","adc",imageName))))

        if os.path.exists(str(os.path.join(os.getcwd(),"temp","sequence","adc_mat",imageName))):
            self.generaedADCMat = readADCMatFromFile(str(os.path.join(os.getcwd(),"temp","sequence","adc_mat",imageName)))


    def getImageName(self):
        '''
            Returns:
                String : image name 
        '''
        return self.imageName



    def getADC(self):
        '''
            Returns:
                BImage : the adc image data
        '''
        if not self.adcImage is None:
            return self.adcImage
        else:
            return self._getEmptyImage()

    
    def getB0Image(self):
        '''
             Returns:
                BImage : the b0 image data
        '''
        if not self.b0Image is None:
            return self.b0Image
        else:
            return self._getEmptyImage()

    

    def getB1000Image(self):
        '''
             Returns:
                BImage : the b1000 image data
        '''
        if not self.b1000Image is None:
            return self.b1000Image
        else:
            return self._getEmptyImage()

    def getADCCreatedImage(self):
        '''
             Returns:
                BImage : the b1000 image data
        '''
        if not self.adcCreated is None:
            return self.adcCreated
        else:
            return self._getEmptyImage()

    def is_b0_b1000_available(self):
        if self.adcCreated is None:
            return False
        else:
            return True
    

    def _getEmptyImage(self):
        '''
            Create No image BImage if B0, B1000 not present

            Returns:
                BImage : empty image
        '''
        imag = cv2.imread(str(os.path.join(os.getcwd(),"assets","images","fill","no_image.png")))
        #convert to monochrome
        imag = cv2.cvtColor(imag,cv2.COLOR_BGR2GRAY)
        #change to uint16
        if imag.dtype != np.uint16:
            imag = imag.astype(np.uint16)
        #change scale
        imag =  imag*65535.0/255.0
        imag = imag.astype(np.uint16)

        df = DicomFile()
        df.setImageArray(imag)

        return BImage(df)


    def getGeneratedADCMat(self):
        '''
            Returns:
                
        '''
        if not self.generaedADCMat is None:
            return self.generaedADCMat
        else:
            return self.adcCreated.getOriginalImage()

    
        



class BImage:
    def __init__(self,dicomFile):
        '''
            Constructor

            Args:
                dicomFile (dicom.DicomFile) : Dicom file in image dataset
        '''
        self.dicomFile = dicomFile
        self.contrastAlpha = 0
        self.brightness = 0
        self.croppedCutSize = self._getCroppedCutSize(dicomFile)

    def getDicomFile(self):
        '''
            Returns:
                dicom.DicomFile : Created dicom file
        '''
        return self.dicomFile

    def getCroppedCutSize(self):
        return self.croppedCutSize

    def setBrightness(self,brightness):
        '''
            Args:
                brightness (double) : brightness value
        '''
        self.brightness = brightness

    def setContrast(self,alpha):
        '''
            Args:
                contrast (double) : contrast value
        '''
        self.contrastAlpha=alpha

    def getOriginalImage(self):
        '''
            Returns:
                np.uint8 : resized 8bit image for display
        '''
        image = self.dicomFile.getImageArray()
        image = image[0:self.croppedCutSize,0:self.croppedCutSize]
        
        return image

    def getResizedImage(self,width,height):
        '''
            Args:
                width (int) : width of desired image
                height (int) : height of desired image

            Returns:
                np.uint8 : resized 8bit image for display
        '''
        image = self.dicomFile.getImageArray()
        image = image[0:self.croppedCutSize,0:self.croppedCutSize]
        out = cv2.resize(image,(width,height),interpolation=cv2.INTER_CUBIC)
        return out

    def getProcessedImage(self):
        '''
            Apply image parameters to image

            Return:
                np.uint8 : processed 8bit image for display
        '''
        out = self.dicomFile.getImageArray()*255.0/65535.0
        out = out.astype(np.uint8)
        out = out[0:self.croppedCutSize,0:self.croppedCutSize]
        out = cv2.addWeighted(out,self.contrastAlpha,out,self.brightness,0)

        return out

    def getProcessedResizedImage(self,width,height):
        '''
            Get processed and resized Image
            Args:
                width (int) : width of desired image
                height (int) : height of desired image

            Returns:
                np.uint8 : Prcessed and resized 8bit image for display
        '''
        image = self.getProcessedImage()
        image = image[0:self.croppedCutSize,0:self.croppedCutSize]
        out = cv2.resize(image,(width,height),interpolation=cv2.INTER_CUBIC)
        return out

    
        
    def _getCroppedCutSize(self,dicomFile):
        image = dicomFile.getImageArray()
        imageWidth,imageHeight = image.shape[0],image.shape[1]
        cutSize = imageWidth
        if imageHeight<imageWidth:
            cutSize = imageHeight

        return cutSize
        