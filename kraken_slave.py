import requests, os, zipfile

jobsURL = 'http://jsonplaceholder.typicode.com/posts'
test_download_url = 'http://www.blog.pythonlibrary.org/wp-content/uploads/2012/06/wxDbViewer.zip'


# job list
def get_jobs(srcpath):
    r = requests.get(srcpath)
    if r is not None:
        return r.json()
    else:
        return None

# first job
def get_open_job():
    jobs = get_jobs(jobsURL)
    if jobs is not None:
        return jobs[0]
    else:
        return None


# file download
def download_file(srcpath, filename, dstpath):
    if not os.path.exists(dstpath):
        os.makedirs(dstpath)

    r = requests.get(srcpath, stream=True)
    with open(dstpath + filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


# file upload
def upload_file(srcpath, filename, dstpath):
    files = {'upload_file': open(srcpath + filename, 'rb')}
    requests.put(dstpath, files=files)
    r.text


# zip extract
def unzip_file(srcpath, zipname, dstpath):
    if not os.path.exists(srcpath):
        os.makedirs(srcpath)

    zfile = zipfile.ZipFile(srcpath + zipname)
    for name in zfile.namelist():
        (dirname, filename) = os.path.split(name)
        print('UNZIP: ' + filename + ' from ' + srcpath + zipname + ' to ' + dstpath)

        zfile.extract(name, dstpath)


# zip create
def zip_file(srcpath, zipname, dstpath):
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


def request_open_job_to_process():
    job = get_open_job()
    if job is not None:
        download_file(test_download_url, str(job['id']) + '.zip', 'data/download/')
        unzip_file('data/download/', str(job['id']) + '.zip', 'data/unzipped/')
        # start external program
        zip_file('data/unzipped/', str(job['id']) + '_result.zip', 'data/zipped/')
    else:
        return 0


request_open_job_to_process()
upload_file('data/zipped/', '1_result.zip', 'http://www.posttestserver.com/post.php')