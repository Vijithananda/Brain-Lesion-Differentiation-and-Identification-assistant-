from fileprocess.FileProcess import FileProcess
from dicom.DicomFile import DicomFile
import os
from logic.adcanalyze.adc import readAllB0B1000


class DicomFileProcess:
    def __init__(self):
        self.fileProcess  = FileProcess()

    def deleteMerged(self):
        absMergedDirectory =  os.path.abspath(os.path.join(os.getcwd(),"temp","adc"))
        fileList = self.fileProcess.listFiles(str(absMergedDirectory))
        
        for file in fileList:
            fileName = os.path.join(absMergedDirectory,file)
            self.fileProcess.deleteFile(str(fileName))

    def deleteSortedFiles(self):
        absMergedDirectoryb0 =  os.path.abspath(os.path.join(os.getcwd(),"temp","sequence","b0"))
        absMergedDirectoryb1000 =  os.path.abspath(os.path.join(os.getcwd(),"temp","sequence","b1000"))
        absMergedDirectoryADC=  os.path.abspath(os.path.join(os.getcwd(),"temp","sequence","adc"))
        absMergedDirectoryADCMatat=  os.path.abspath(os.path.join(os.getcwd(),"temp","sequence","adc_mat"))


        b0list = self.fileProcess.listFiles(str(absMergedDirectoryb0))
        b10000list = self.fileProcess.listFiles(str(absMergedDirectoryb1000))
        adclist = self.fileProcess.listFiles(str(absMergedDirectoryADC))
        adcMatlist = self.fileProcess.listFiles(str(absMergedDirectoryADCMatat))


        for file in b0list:
            fileName = os.path.join(absMergedDirectoryb0,file)
            self.fileProcess.deleteFile(str(fileName))  

                
        for file in b10000list:
            fileName = os.path.join(absMergedDirectoryb1000,file)
            self.fileProcess.deleteFile(str(fileName))

        for file in adclist:
            fileName = os.path.join(absMergedDirectoryADC,file)
            self.fileProcess.deleteFile(str(fileName))

        for file in adcMatlist:
            fileName = os.path.join(absMergedDirectoryADCMatat,file)
            self.fileProcess.deleteFile(str(fileName))


    


    def sortB0B1000Files(self,directory):
        '''
            Move ADC, B0 and B1000 files

            Args:
                directory (str): absolute path of directory
        '''

        # get a string directory path
        directoryList = self.fileProcess.listDirectories(directory)

        adcDirectory = None
        b0Directory = None

        # loop through the patient sequences
        for d in  directoryList:
            if "ADC" in str(d):
                adcDirectory = str(os.path.join(directory,d))
            if "3SCAN_TRACE_P2_0006" in str(d):
                b0Directory = str(os.path.join(directory,d))

        if not adcDirectory is None:
            fileList = self.fileProcess.listFiles(str(adcDirectory))
            destination = str(os.path.abspath(os.path.join(os.getcwd(),"temp","adc")))
            for dicomFile in fileList:
                source = str(os.path.join(adcDirectory,dicomFile))

                # reading dicom file data
                readDicomFile = DicomFile(source)
                currentSliceLocation = readDicomFile.getSliceLocation()
                destinationNew = str(os.path.join(destination,str(currentSliceLocation)))
                self.fileProcess.copyFile(source,destinationNew)
                

        # TODO - edit here
        if not b0Directory is None:
            fileList = self.fileProcess.listFiles(str(b0Directory))
            destinationb0 = str(os.path.abspath(os.path.join(os.getcwd(),"temp","sequence","b0")))
            destinationb1000 = str(os.path.abspath(os.path.join(os.getcwd(),"temp","sequence","b1000")))
            for dicomFile in fileList:
                source = str(os.path.join(b0Directory,dicomFile))
                
                # reading dicom file data
                readDicomFile = DicomFile(source)
                cuurentSquenceName =  readDicomFile.getSequenceName()
                currentSliceLocation = readDicomFile.getSliceLocation()
                # copying files to required folders
                if "b0" in cuurentSquenceName:
                    destination = str(os.path.join(destinationb0,str(currentSliceLocation)))
                    self.fileProcess.copyFile(source,destination)
                elif "b1000" in cuurentSquenceName:
                    destination = str(os.path.join(destinationb1000,str(currentSliceLocation)))
                    self.fileProcess.copyFile(source,destination)


            # create ADC from b0 and b1000
            readAllB0B1000()
            
                    
