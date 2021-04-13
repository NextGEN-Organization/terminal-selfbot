from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)

def searchForSubfolders(id):
    folders = []
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(id)}).GetList()
    for file in file_list:
        if ("folder" in file['mimeType']):
            folders.append((file['title'], file['id']))
    return folders


def searchForFilesInFolder(id):
    files = []
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(id)}).GetList()
    for file in file_list:
        if not ("folder" in file['mimeType']):
            files.append((file['title'], file['id']))
    return files


def searchForAllInFolder(id):
    files = []
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(id)}).GetList()
    for file in file_list:
        files.append((file['title'], file['mimeType'], file['id']))
    return files


def searchForFileAnywhere(name):
    file_list = drive.ListFile({'q': "trashed=false".format(id)}).GetList()
    for file in file_list:
        if (''.join(name) == file['title']):
            return file


def searchForTrashedFiles(name):
    file_list = drive.ListFile({'q': "trashed=false".format(id)}).GetList()
    for file in file_list:
        if (''.join(name) == file['title']):
            return file


def allFiles():
    files = []
    file_list = drive.ListFile({'q': "trashed=false".format(id)}).GetList()
    for file in file_list:
        if not ("folder" in file['mimeType']):
            files.append((file['title'], file['id']))
    return files


def allFolders():
    folders = []
    file_list = drive.ListFile({'q': "trashed=false".format(id)}).GetList()
    for file in file_list:
        if ("folder" in file['mimeType']):
            folders.append((file['title'], file['id']))
    return folders
