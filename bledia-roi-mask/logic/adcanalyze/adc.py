from dicom.DicomFile import DicomFile
from fileprocess.FileProcess import FileProcess
from fileprocess.datastore import writeADCMatFile
import numpy as np
import pydicom
import os
import matplotlib.pyplot as plt
np.seterr(divide='ignore', invalid='ignore')

# def createADCfromB0andB1000(def,)

def readAllB0B1000():

    # abosolute paths of temp directories
    absMergedDirectoryb0 =  os.path.abspath(os.path.join(os.getcwd(),"temp","sequence","b0"))
    absMergedDirectoryb1000 =  os.path.abspath(os.path.join(os.getcwd(),"temp","sequence","b1000"))
    absMergedDirectoryADC=  os.path.abspath(os.path.join(os.getcwd(),"temp","sequence","adc"))
    absMergedDirectoryADCMat=  os.path.abspath(os.path.join(os.getcwd(),"temp","sequence","adc_mat"))



    b0list = FileProcess().listFiles(str(absMergedDirectoryb0))
    test = False

    for file in b0list:
        absFileB0Path = os.path.join(absMergedDirectoryb0,file)
        absFileB10000Path = os.path.join(absMergedDirectoryb1000,file)
        absFileADCPath = os.path.join(absMergedDirectoryADC,file)
        absFileADCMatPath = os.path.join(absMergedDirectoryADCMat,file)


        # read b0 and b1000

        dicomB0 = DicomFile(absFileB0Path)
        dicomB1000 =  DicomFile(absFileB10000Path)


        # if not test:
        #     x = np.range(0,192,1)
        #     y = np.range(0,192,1)
        #     xs, ys = np.meshgrid(x,y)

        #     plotHistogram(adc)

        S1 = dicomB1000.getImageArray().astype('float64')
        # S1[S1<50] = 0

        S0 = dicomB0.getImageArray().astype('float64')
        S0[S0<50] = 0

        # adc equation
        adc = (-1)*np.log(np.divide(S1,S0))/1000

        

        # removing nans and infs
        adc = np.nan_to_num(adc,nan=0.0,posinf=0.001,neginf=-0.0006)

        # write to Mat Text files
        writeADCMatFile(absFileADCMatPath, adc)




        # print(adc.min())
        # print(adc.max())
        # print()        

     

        # limit to range 0 - 1
        adc = (adc-adc.min())/(adc.max()-adc.min())

      

        # adc[adc<0.4] = 0
        # adc[adc>0.75] = 1
        # writeMatToFile(adc,"adc")

        # convert to uint16
        adc = (adc*5000.0).astype(np.uint16)


        adcCreated = DicomFile()
        adcCreated.setDicomFile(dicomB0.dataset)
        adcCreated.setImageArray(adc)

        adcCreated.dataset.save_as(absFileADCPath)

def plotHistogram(mat):
    m = mat.shape[0]
    n = mat.shape[1]
    mat = np.reshape(mat, (m*n))
    plt.hist(mat,density=1,bins=100)
    plt.show()
