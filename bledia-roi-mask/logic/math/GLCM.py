import math

import numpy as np

from fileprocess.datastore import writeMatToFile


class GLCM:
    def __init__(self,image,mask,levels=256, maxValue=20000):
        self.maskPixelCount = 0
        self.levels = levels
        self.maxValue = maxValue
        self.orignalGLCM = self._createGLCM(image,mask)
        self.mat = self._getNormalizedGLCM(self.orignalGLCM)
        

        # TODO - remove line
        writeMatToFile(self.orignalGLCM,'glcm')

        self.mean = self._glcmMean() 
        self.variance = self._glcmVariance()
        self._featuresSetOne()
        self._featureSetTwo()

    def _createGLCM(self,image,mask):
        # get image dimensions
        m,n = image.shape[0],image.shape[1]

        # get glcm levels defined by the user
        levels = self.levels
        # create empty 2D array for store GLCM
        glcm = np.zeros((self.levels, self.levels), dtype=int)

        # get the level size to sample the image values
        levelSize = self.maxValue/self.levels

        # generate image with within the 0 - levels
        copiedMat = self._copyMatrix(image)
        copiedMat = copiedMat/levelSize

        # TODO - remove line
        # writeMatToFile(copiedMat,'descreteMat')

        for i in range(m):
            for j in range(n):
                if mask[i][j]==1:
                    posValue = copiedMat[i][j]

                    # Angle 0 
                    if j+1<levels:
                        adjValue = copiedMat[i][j+1]
                        glcm[int(posValue)][int(adjValue)]=glcm[int(posValue)][int(adjValue)]+1
                        self.maskPixelCount+=1


                    # Angle 45 
                    if j+1<levels and i-1>=0:
                        adjValue = copiedMat[i-1][j+1]
                        glcm[int(posValue)][int(adjValue)]=glcm[int(posValue)][int(adjValue)]+1
                        self.maskPixelCount+=1


                    # Angle 90
                    if i-1>=0:
                        adjValue = copiedMat[i-1][j]
                        glcm[int(posValue)][int(adjValue)]=glcm[int(posValue)][int(adjValue)]+1
                        self.maskPixelCount+=1


                    # Angle 135 
                    if j-1>=0 and i-1>=0:
                        adjValue = copiedMat[i-1][j-1]
                        glcm[int(posValue)][int(adjValue)]=glcm[int(posValue)][int(adjValue)]+1
                        self.maskPixelCount+=1



        return np.array(glcm)
                    
    def _getNormalizedGLCM(self,mat):
        return mat/self.maskPixelCount


    def _copyMatrix(self,image):
        m,n = image.shape[0],image.shape[1]
        newImage = np.zeros(image.shape)

        for i in range(m):
            for j in range(n):
                newImage[i][j]=image[i][j]

        return newImage


    def _glcmMean(self):
        m,n = self.mat.shape[0],self.mat.shape[1]
        mat = self.mat
        sumI = 0
        sumJ = 0

        for i in range(m):
            for j in range(n):
                sumI+=i*mat[i][j]
                sumJ+=j*mat[i][j]

        return (sumI,sumJ)


    def _glcmVariance(self):
        m,n = self.mat.shape[0],self.mat.shape[1]

        sumI = 0
        sumJ = 0

        for i in range(m):
            for j in range(n):
                sumI+=self.mat[i][j]*math.pow(i-self.mean[0],2)
                sumJ+=self.mat[i][j]*math.pow(j-self.mean[1],2)


        return (sumI,sumJ)

    def _featuresSetOne(self):
        m,n = self.mat.shape[0],self.mat.shape[1]
        mat = self.mat

        energy = 0
        entrophy = 0
        contrast = 0
        homogenity = 0
        correlation = 0

        for i in range(m):
            for j in range(n):
                energy+= math.pow(mat[i][j],2)

                if mat[i][j]!=0:
                    entrophy+=(-1*math.log(mat[i][j])*mat[i][j])
                
                contrast+=mat[i][j]*math.pow(i-j,2)
                homogenity+= float(mat[i][j])/(1+math.pow(i-j,2))
                correlation+=float(mat[i][j])*(i-self.mean[0])*(j-self.mean[1])/(math.sqrt(self.variance[0])*math.sqrt(self.variance[1]))
        
        self.energy = energy
        self.entrophy = entrophy
        self.contrast = contrast
        self.homogenity = homogenity
        self.correlation = correlation

    def _featureSetTwo(self):
        m,n = self.mat.shape[0],self.mat.shape[1]
        mat = self.mat

        shadeTemp = 0
        promTemp = 0

        for i in range(m):
            for j in range(n):
                shadeTemp += math.pow(i+j-2*self.mean[0],3)*float(mat[i][j])/(math.pow(math.sqrt(self.variance[0]),3)*math.pow(math.sqrt(2*(1+self.correlation)),3))
                promTemp +=  math.pow(i+j-2*self.mean[0],4)*float(mat[i][j])/ (4*math.pow(self.variance[0],2)*math.pow(1+self.correlation,2))

        self.shade = self._sign(shadeTemp)*math.pow(abs(shadeTemp),1.0/3)
        self.prominence = self._sign(shadeTemp)*math.pow(abs(promTemp),1.0/4)

    def _sign(self,number):
        if number==0:
            return 0
        return int(number/abs(number))
    


    