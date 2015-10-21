import requests, os, zipfile

jobsURL = 'https://github.com/timeline.json'
downloadURL = 'http://www.blog.pythonlibrary.org/wp-content/uploads/2012/06/wxDbViewer.zip'
uploadURL = 'http://www.blog.pythonlibrary.org/wp-content/uploads/2012/06/wxDbViewer.zip'
id = 0
status = 'open'


def get_jobs(url):
    j = requests.get(url)
    # status = blocked
    jobList = j.json()
    return jobList


# file downloaden
def download_file(srcpath, filename, dstpath):
    if not os.path.exists(dstpath):
        os.makedirs(dstpath)

    r = requests.get(srcpath, stream=True)
    with open(dstpath + '/' + filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


# file uploaden
def upload_file(srcpath, filename, dstpath):
    files = {'upload_file': open(srcpath + '/' + filename, 'rb')}
    values = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}

    r = requests.post(dstpath, files=files, data=values)


# zip Archiv entpacken
def unzip(srcpath, zipname, dstpath):
    if not os.path.exists(srcpath):
        os.makedirs(srcpath)

    zfile = zipfile.ZipFile(srcpath + zipname)
    for name in zfile.namelist():
        (dirname, filename) = os.path.split(name)
        print('UNZIP: ' + filename + ' from ' + srcpath + zipname + ' to ' + dstpath)

        zfile.extract(name, dstpath)


# zip Archiv erstellen
def zip(srcpath, zipname, dstpath):
    if not os.path.exists(dstpath):
        os.makedirs(dstpath)

    zfile = zipfile.ZipFile(dstpath + zipname, 'w', zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(srcpath)
    for dirname, subdirs, files in os.walk(srcpath):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print('ZIP: ' + srcpath + filename + ' to ' + dstpath + zipname)
            zfile.write(absname, arcname)
    zfile.close()
