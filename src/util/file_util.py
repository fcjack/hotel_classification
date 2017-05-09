import os


class FileUtil(object):
    @staticmethod
    def get_file_paths_from_directory(directory):
        """ 
            This method will get the real path for all files from directory 
        requested in a relative path.
             
            The logic is simple, receive the relative path for directory requested,
        discover the actual path for this file and join with the relative.
             
            I will list all files and return the list of paths for each file.
         """
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, directory)
        files = os.listdir(path)

        file_paths = [os.path.join(path, file) for file in files]
        return file_paths
