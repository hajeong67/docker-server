import os

from email.parser import Parser
from zipfile import ZipFile

class WheelFileNotFoundError(Exception):
    msg = 'This file is not a wheel file.'

    def __init__(self, path):
        full_msg = f'{self.msg} Path: {path}'
        super().__init__(full_msg)


class MetadataNotFoundError(Exception):
    msg = 'This file does not contain a wheel file.'

    def __init__(self, path):
        str_path = '\n'.join(path)
        full_msg = f'{self.msg}\nFile List: {str_path}'
        super().__init__(full_msg)

class WheelMetadata:

    METADATA_FILE_NAME = 'METADATA'
    WHEEL_FILE_EXTENSION = '.whl'

    def __init__(self, file_path):
        if not os.path.isfile(file_path): raise FileNotFoundError(file_path)
        self.wheel_file_path = os.fspath(file_path)

        if not self.is_wheel_file(): raise WheelFileNotFoundError(self.wheel_file_path)
        self.wheel_file = ZipFile(self.wheel_file_path)

        exists_metadata, self.metadata_path = self.exists_metadata()
        if not exists_metadata: raise MetadataNotFoundError(self.wheel_file_path)

        self.metadata = self.extract_metadata()
        self.wheel_file.close()

    def is_wheel_file(self):
        return self.wheel_file_path.endswith(WheelMetadata.WHEEL_FILE_EXTENSION)

    def exists_metadata(self):
        for file_path in self.wheel_file.namelist():
            if file_path.endswith(WheelMetadata.METADATA_FILE_NAME):
                return True, file_path
        return False, None

    def extract_metadata(self):
        return Parser().parsestr(self.wheel_file.read(self.metadata_path).decode('utf-8'))

    def get_metadata(self):
        return self.metadata

    def get_name(self):
        return self.metadata.get('Name')

    def get_version(self):
        return self.metadata.get('Version')

    def get_summary(self):
        return self.metadata.get('Summary')

    def get_license(self):
        return self.metadata.get('License')

    def get_keywords(self):
        keywords = self.metadata.get('Keywords', '')
        seps = [', ', ',', ' ']
        for sep in seps:
            if sep in keywords:
                return keywords.split(sep)
        return keywords

    def get_author(self):
        return self.metadata.get('Author')

    def get_author_email(self):
        return self.metadata.get('Author-email')

    # def to_dict(self):
    #     return {
    #         'name': self.get_name(),
    #         'version': self.get_version(),
    #         'summary': self.get_summary(),
    #         'author': self.metadata.get('Author', 'Unknown'),
    #         'license': self.get_license(),
    #         'keywords': ", ".join(self.get_keywords()) if self.get_keywords() else '',
    #     }