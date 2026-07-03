from os import path

class EmptyFilenameException(Exception):
    pass

class UnableToReadFileException(Exception):
    pass

class UnableToSaveFileException(Exception):
    pass

class FileHandler:

    def __init__(self):
        self.files_received = 0

    def increment_file_counter(self):
        self.files_received += 1

    def read_file(self, filename: str):
        """ Reads and returns the given filename 
        
        Parameters:
         - filename (str): the name of the file to read

        Returns the content of the file

        Throws UnableToReadFileException if unable to read file
        """
        try:
            with open(filename, "rb") as file:
                return file.read()
        except (FileNotFoundError, PermissionError):
            raise UnableToReadFileException()
            
    def save_file(self, file_content, saved_as_name):
        """ Save the given file_content to the given name of the file
        in the form of N_filename, where N is the number of files received
        and filename is saved_as_name

        Parameters:
         - file_content: the content of the file to save
         - saved_as_name (str): the name of the file to save to

         Throws:
          - EmptyFilenameException if an empty saved_as_name string is given
          - UnableToSaveFileException if the given file content cannot be saved
        """
        if saved_as_name == "":
            raise EmptyFilenameException()

        try:
            filename = f"{self.files_received}_{saved_as_name}"
            with open(filename, "wb") as file:
                file.write(file_content)
        except (FileNotFoundError, IsADirectoryError, PermissionError):
            raise UnableToSaveFileException()

    def extract_file_name_from_path(self, filepath: str) -> str:
        return path.basename(filepath)
