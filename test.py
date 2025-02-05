import zipfile

whl_file_path = 'C:/Users/user/channels-4.2.0-py3-none-any.whl'

with zipfile.ZipFile(whl_file_path, 'r') as z:
    for filename in z.namelist():
        if filename.endswith('METADATA'):
            with z.open(filename) as metadata_file:
                metadata_content = metadata_file.read().decode('utf-8')
                print(metadata_content)