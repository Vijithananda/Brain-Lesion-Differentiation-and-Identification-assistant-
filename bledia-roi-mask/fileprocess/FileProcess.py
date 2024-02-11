import shutil
import os

class FileProcess:
    def copyFile(self,source,destination):
        '''
            Args:
                source (str) : absolue path of file
                destination (str) : absolute path of destination
        '''
        try:
            shutil.copy2(source,destination)
        except:
            print('Cannot find the source file '+ source)


    def copyRenamedFile(self,source,destination):
        '''
            Args:
                source (str) : absolue path of file
                destination (str) : absolute path of destination
        '''
        try:
            shutil.copy(source,destination)
        except:
            print('Cannot find the source file '+ source)

            

    def moveFile(self,source,destination):
        '''
            Args:
                source (str) : absolue path of file
                destination (str) : absolute path of destination
        '''
        try:
            shutil.move(source,destination)
        except:
            print('Cannot find the source file '+ source)

    def deleteFile(self,path):
        '''
            Args:
                path (str) : absolute path of file
        '''
        try:
            os.remove(path)
        except:
            print('Cannot find a file to delete')

    def listFiles(self,path):
        '''
            List only files in the given directory

            Args:
                path (str) : absolute path of directory

            Returns:
                list : List of file names
        '''
        files = []
        try:
            files = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path,file))]
            return files
        except:
            print('Directory path is incorrect')
        finally:
            return files

    def listDirectories(self, path):
        '''
            List only sub directories in the given directory

            Args:
                path (str) : absolute path of directory

            Returns:
                list : List of sub directory names
        '''
        directories = []
        try:
            directories=[d for d in os.listdir(path) if os.path.isdir(os.path.join(path,d))]
            return directories
        except:
            print('Directory path is incorrect')
        finally:
            return directories




    def createDirectories(self,path):
        '''
            Create needed directories

            Args:
                path (str) : relative directory path
        '''
        currentDir = os.getcwd()
        absolutePath = os.path.join(currentDir,path)
        if not os.path.exists(str(absolutePath)):
            try:
                os.mkdir(str(absolutePath))
            except:
                print('Failed to crete drectory: '+str(path))
