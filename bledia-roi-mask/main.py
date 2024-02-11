
from screens.Bledia import Bledia
from dicom.DicomFile import DicomFile
from dicom.DicomFileProcess import DicomFileProcess
from fileprocess.FileProcess import FileProcess
import cv2

# create directories
fileProcess = FileProcess()
fileProcess.createDirectories('temp')
fileProcess.createDirectories('temp/adc')
fileProcess.createDirectories('temp/sequence')
fileProcess.createDirectories('temp/sequence/b0')
fileProcess.createDirectories('temp/sequence/b1000')
fileProcess.createDirectories('temp/sequence/adc')
fileProcess.createDirectories('temp/sequence/adc_mat')
fileProcess.createDirectories('temp/sequence/roi_masked_image')
fileProcess.createDirectories('test')
fileProcess.createDirectories('collection')






window = Bledia()
window.start()

# dicom = DicomFile('/home/deshan/projects/bledia/test/TEST.IMA')
# array = dicom.getImageArray()
# out = cv2.addWeighted(array,10,array,0,0)

# cv2.imshow('img',out)
# cv2.waitKey(0)
# cv2.closeAllWindows()

# p = DicomFileProcess()
# p.sortB0B1000Files('/home/deshan/ABEYGUNAWARDANA_G_MRS_64971_180847_WD_10/NTC_HEAD_GENERAL_20191009_000003_000000')