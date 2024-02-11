import pydicom
import os
import unicodedata

class DicomFile:
    def __init__(self):
        pass
    
    def __init__(self,path=None):
        '''
            Constructor
            Args:
                path (str) : the absolute path read dicom file
        '''
        if(path!=None):
            self.dataset = pydicom.dcmread(path)
        else:
            self.dataset = self._loadTestImage()

    def setDicomFile(self,dataset):
        '''
            Args:
                dataset (pydicom.Dataset)
        '''
        self.dataset = dataset

    def setImageArray(self,npArray):
        '''
            Set image array to dataset file
            
            Args:
                npArray (np.uint16): 2D array of MRI image
        '''
        self.dataset.Rows = npArray.shape[1]
        self.dataset.Columns = npArray.shape[0]
        self.dataset.PixelData = npArray.tobytes()

    def getImageArray(self):
        '''
            Returns:
                np.uint16 : image array of dataset 
        '''
        try :
            return self.dataset.pixel_array

        except:
            print('dataset not intiated')

    def getPersonId(self):
        '''
            Returns:
                str : patient id
        '''
        return self.dataset.PatientID.encode('ascii','ignore')

    def getSliceLocation(self):
        '''
            Returns:
                str : slice location
        '''
        return self.dataset.SliceLocation

    def _loadTestImage(self):
        testPath = os.path.join(os.getcwd(),"assets","dicom","TEST.IMA")
        return pydicom.dcmread(str(testPath))

    def getSequenceName(self):
        '''
            Returns:
                str: sequene name
        '''
        return self.dataset.SequenceName

    