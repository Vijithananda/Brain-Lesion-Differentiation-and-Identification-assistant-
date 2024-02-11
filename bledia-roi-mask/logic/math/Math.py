
import math

class Math:
    def __init__(self,mask,mat):
        self.mask = mask
        self.mat = mat
        self.pixelCount = self._bCountCoveredPixels()
        self.mean = self._bMean()
        self.std = self._bStandardDeviation()

    def _bMean(self):
        m,n = self.mask.shape[0],self.mask.shape[1]
        sum = 0

        for i in range(m):
            for j in range(n):
                if self.mask[i][j]==1:
                    sum+=self.mat[i][j]

        return float(sum)/self.pixelCount


    def _bStandardDeviation(self):
        m,n = self.mask.shape[0],self.mask.shape[1]
        
        sum = 0

        for i in range(m):
            for j in range(n):
                if self.mask[i][j]==1:
                    val = self.mat[i][j]-self.mean
                    sum += val*val

        return math.sqrt(float(sum)/self.pixelCount)
        


    def _bCountCoveredPixels(self):
        sum = 0
        m,n = self.mask.shape[0],self.mask.shape[1]

        for i in range(m):
            for j in range(n):
                if self.mask[i][j]==1:
                    sum+=1
        print(sum)
        return sum

    def getMean(self):
        return self.mean

    def getStd(self):
        return self.std

    def getSkewness(self):
        sum = 0
        m,n = self.mask.shape[0],self.mask.shape[1]

        for i in range(m):
            for j in range(n):
                if self.mask[i][j]==1:
                    val = self.mat[i][j]-self.mean
                    sum+=math.pow(val,3)

        return float(sum)/((self.pixelCount-1)*math.pow(self.std,3))


    def getKurtosis(self):
        sum = 0
        m,n = self.mask.shape[0],self.mask.shape[1]

        for i in range(m):
            for j in range(n):
                if self.mask[i][j]==1:
                    val = self.mat[i][j]-self.mean
                    sum+=math.pow(val,4)

        return float(sum)/((self.pixelCount-1)*math.pow(self.std,4))