#!/usr/bin/env

import zipfile
import time
from scale import Scale

zipFile = zipfile.ZipFile('./software.zip')
total = len(zipFile.namelist())
for file in zipFile.namelist():
    current = zipFile.namelist().index(file)
    S = Scale(total, current)
    zipFile.extract(file, r'./')
    time.sleep(0.05)
zipFile.close()
