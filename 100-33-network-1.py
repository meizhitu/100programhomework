__author__ = 'rui'
#coding=utf-8
import sys
from ftplib import FTP

ftp = FTP()
'''
ref http://pypix.com/python/create-python-library/
'''


class FtpClient():
    message_array = []

    def __init__(self):
        """
        """
        pass

    def log_message(self, message, clear=True):
        """
        Logs the message to the message_array, from where it is retrieved to display in the console.
        :param message: The message string.
        :param clear: Buffer Clearance.
        """
        if clear:
            self.message_array = message

    def get_message(self):
        """
        Returns the logged message to the console.
        :return: Returns the message.
        """
        return self.message_array

    def connect(self, server, ftp_user, ftp_password, port):
        """
        Connects the remote host to the server from the information provided to the connect method.
        If the connection is successful, the messaged will logged and displayed in the console, otherwise
        Exception is raised with the error displayed to the console and program execution halts.
        :param server: The address of the server
        :param ftp_user: The FTP user id.
        :param ftp_password: The FTP password.
        :param port: The port number.
        """
        try:
            ftp.connect(server, port)
            ftp.login(user=ftp_user, passwd=ftp_password)
            self.log_message("Connected to {0} for {1} on port {2}".format(server, ftp_user, port))
        except Exception as e:
            print(e)
            sys.exit(1)

    def make_directory(self, directory):
        """
        Creates the new directory in the connected server in the root or in the directory specified via the parameter.
        :param directory: Directory name to create.
        """
        try:
            ftp.mkd(directory)
            self.log_message("Directory {0} created successfully".format(directory))
        except Exception as e:
            print(e)
            sys.exit(1)

    def change_directory(self, directory):
        """
        CD's into the directory of our wish by providing the directory name as the parameter to it.
        :param directory: Directory name to change to it.
        """
        try:
            ftp.cwd(directory)
            self.log_message("Current Directory is now {0}".format(ftp.pwd()))
        except Exception as e:
            print(e)
            sys.exit(1)

    def directory_exists(self, directory_name):
        """
        Checks if the directory you are trying to upload the files is already present or not and if
        its already present CD's into the directory and if not, creates the directory and CD's into the
        newly created directory.
        :param directory_name: Directory name to check its existence.
        """
        try:
            new_dir_name = directory_name.strip("/")
            if new_dir_name in ftp.nlst():
                self.change_directory(directory_name)
            else:
                self.make_directory(directory_name)
                self.change_directory(directory_name)
        except Exception as e:
            print(e)
            sys.exit(1)

    def get_directory_listing(self,depth=0):
        """
        return a recursive listing of an ftp server contents (starting
        from the current directory)

        listing is returned as a recursive dictionary, where each key
        contains a contents of the subdirectory or None if it corresponds
        to a file.

        @param ftp: ftplib.FTP object
        """
        if depth > 10:
            return ['depth > 10']
        level = {}
        for entry in (path for path in ftp.nlst() if path not in ('.', '..')):
            try:
                ftp.cwd(entry)
                level[entry] = get_directory_listing(ftp, depth + 1)
                ftp.cwd('..')
            except ftplib.error_perm:
                level[entry] = None
        return level

    def upload_file(self, filename):
        """
        The file provided with filename will be uploaded to the server in the recommended
        format automatically to the desired directory.

        :param filename: Name of the file to upload.
        """
        try:
            if filename.lower().endswith(('.*')):
                with open(filename, 'r') as f:
                    ftp.storlines('STOR {}'.format(filename), f)
            else:
                with open(filename, 'rb') as f:
                    ftp.storbinary('STOR {}'.format(filename), f)
            self.log_message("Uploaded {0} in {1}".format(filename, ftp.pwd()))
        except Exception as e:
            print(e)
            sys.exit(1)

    def download_file(self, filename):
        """
        Downloads the file from the connected server, provided the name is passes as the parameter.

        :param filename: Name of the file to download.
        """
        try:
            ftp.retrbinary("RETR " + filename, open(filename, 'wb').write)
            self.log_message("Downloaded {0}".format(filename))
        except Exception as e:
            print(e)
            sys.exit(1)

    def __del__(self):
        """
        Closes the FTP connection.
        """
        ftp.close()


def config():
    ftp_obj = FtpClient()
    FTP_HOST = "ftp.opera.com"
    FTP_USER = ""
    FTP_PASS = ""
    FTP_PORT = 21

    ftp_obj.connect(FTP_HOST, FTP_USER, FTP_PASS, FTP_PORT)
    print(ftp_obj.get_message())
    #direcotry = "/test"
    #ftp_obj.make_directory(direcotry)
    #print(ftp_obj.get_message())
    #app_root = os.path.dirname(os.path.abspath(__file__))
    # Add the file name you want to upload
    #file_path = os.path.join(app_root, 'test.txt')
    #strip_path = file_path.rstrip(os.sep)
    #fp_path = os.path.basename(strip_path)
    # Upload command
    #ftp_obj.upload_file(fp_path)
    #print(ftp_obj.get_message())
    print(ftp_obj.get_directory_listing())
    #print(ftp_obj.get_message())


if __name__ == '__main__':
    config()
