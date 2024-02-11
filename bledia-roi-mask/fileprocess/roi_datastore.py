import os
import numpy as np
from fileprocess.FileProcess import FileProcess


def deleteRoiMaskedImages():
    fileprocess = FileProcess()

    absMergedDirectory =  os.path.abspath(os.path.join(os.getcwd(),"temp","sequence","roi_masked_image"))
    fileList = fileprocess.listFiles(str(absMergedDirectory))
        
    for file in fileList:
        fileName = os.path.join(absMergedDirectory,file)
        fileprocess.deleteFile(str(fileName))

def create_output_mask(mask,mat):
    m,n = mat.shape[0],mat.shape[1]
    output_mat = []

    for i in range(m):
        row = []
        for j in range(n):
            value = mask[i][j]*mat[i][j]
            row.append(value)
        output_mat.append(row)

    return output_mat


def exportMaskedMat(mask, image, name):
    '''
        Write to masked output to a file
    '''
    # create roi masked image

    # output_mat = np.dot(mask,image)
    output_mat = create_output_mask(mask,image)

    absoulutePath = os.path.join(os.getcwd(),"temp","sequence","roi_masked_image",name)
    f= open(str(absoulutePath),"w+")
    m,n = mask.shape[0],mask.shape[1]

    for i in range(m):
        for j in range(n):
            val = output_mat[i][j]
            f.write(str(val))
            if(j<n-1):
                f.write(",")
        if(i<n-1):
            f.write("\n")

    f.close()




