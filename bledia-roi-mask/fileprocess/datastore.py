import csv
import os
from numpy import genfromtxt

def writeToCSV(imageData,roi,basicFeatures, glcmFeatures):
    collection = os.path.abspath(os.path.join(os.getcwd(),"collection","data.csv"))
    with open(str(collection), mode='a') as dataFile:
        dicomFile = imageData.getDicomFile()
        dicomFile.getPersonId()
        dataWriter = csv.writer(dataFile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)

        row = []
        row.append(dicomFile.getPersonId())
        row.append(dicomFile.getSliceLocation())
        row.append(basicFeatures.mean)
        row.append(basicFeatures.getKurtosis())
        row.append(basicFeatures.getSkewness())
        row.append(str(glcmFeatures.mean))
        row.append(str(glcmFeatures.variance))
        row.append(glcmFeatures.energy)
        row.append(glcmFeatures.entrophy)
        row.append(glcmFeatures.contrast)
        row.append(glcmFeatures.homogenity)
        row.append(glcmFeatures.correlation)
        row.append(glcmFeatures.shade)
        row.append(glcmFeatures.prominence)
        row.append(str(roi).strip("[]"))

        dataWriter.writerow(row)



def writeMatToFile(mat,name):
    '''
        Write mat to file for view

        Args:
            mat (np.array) : matrix
            name (str) : filename
    '''
    m,n = mat.shape[0],mat.shape[1]
    absoulutePath = os.path.join(os.getcwd(),"test",name)
    f= open(str(absoulutePath),"w+")


    for i in range(m):
        for j in range(n):
            f.write("%f, " %float(mat[i][j]))
        f.write("\n")

    f.close()


def writeADCMatFile(absoulutePath, mat):
    '''
        Write mat to file for view

        Args:
            mat (np.array) : matrix
            name (str) : filename
    '''
    m,n = mat.shape[0],mat.shape[1]
    f= open(str(absoulutePath),"w+")


    for i in range(m):
        for j in range(n):
            f.write("%f " %float(mat[i][j]))
            if(j<n-1):
                f.write(",")
        if(i<n-1):
            f.write("\n")

    f.close()
    

def readADCMatFromFile(absoulutePath):
    data = genfromtxt(absoulutePath, delimiter=',')
    return data