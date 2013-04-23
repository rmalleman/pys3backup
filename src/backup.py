import os
import sys
import tempfile
import boto
import shutil
import tarfile
from datetime import datetime
from argparse import ArgumentParser
from boto.exception import S3ResponseError
from boto.s3.key import Key

from pys3backup import configuration


__author__ = 'matt'

log = configuration.log
log.info("backup module successfully loaded")
class S3Backup:

    """This class handles all the uploading and downloading to and from a specific amazon s3 bucket"""

    def __init__(self, access_key=None,secret_key=None,s3_bucket=None):

        """instantiate the object with an access_key, secret_key, and an s3_bucket.  These should
        all be available in the AWS Management console.  The s3 bucket will be created automatically
        if it doesn't exist"""


        self.access_key = access_key
        self.secret_key = secret_key
        self.s3_bucket = None

        self.conn = boto.connect_s3(self.access_key, self.secret_key)

        try:

            self.s3_bucket = self.conn.get_bucket(s3_bucket)
            log.info("S$ Bucket Load Attempt")

        except (Exception,S3ResponseError), e:
            if e.code == "NoSuchBucket":
                self.s3_bucket = self.conn.create_bucket(s3_bucket)
                log.info("S3 bucket created: %s" % s3_bucket)
            else:
                raise e

    def get(self, key):
        """Get the file associated with key"""

        get_key = Key(self.s3_bucket)
        get_key.key = key
        get_file = tempfile.NamedTemporaryFile(mode='w+t',delete=False)

        #get_file = tempfile.mkstemp()
        get_key.get_contents_to_file(get_file)

        get_file.seek(0)
        return get_file

    def put(self, key, file):
        """Puts the file into the s3 bucket, and associates it with the key"""

        put_key = Key(self.s3_bucket)
        put_key.key = key

        put_key.set_contents_from_file(file)

        put_key.set_acl("private")



    def delete(self, key):
        """deletes the file associated with the key"""

        delete_key = Key(self.s3_bucket)
        delete_key.key = key
        self.s3_bucket.delete_key(delete_key)



    def list(self):

        """returns a list of all the keys available in the s3_bucket"""
        return [key.name for key in self.s3_bucket.get_all_keys()]


def main():

    #arg parser stuff
    parser = ArgumentParser(description='pyS3backup - A program to manage backing up important data '
                                        'to an offsite s3 backup')
    action = parser.add_mutually_exclusive_group(required= True)
    action.add_argument('-l','--list', action='store_true', help='List current offsite backups')
    action.add_argument('-b','--backup', action='store_true', help='run the backup')
    action.add_argument('-r','--restore', help='restore file')
    parser.add_argument('-d','--dest', help='restore destination')

    args = parser.parse_args()

    try:
        cfg = configuration.get()
        ACCESS_KEY = cfg.get('s3_info', 'access_key')
        SECRET_KEY = cfg.get('s3_info', 'secret_key')
        S3_BUCKET = cfg.get('s3_info', 's3_bucket')


    except Exception,e:
        sys.stderr.write("Error parsing configuration file, read the docs")
        log.info(e)
        exit(0)

    try:
        backup = S3Backup(access_key=ACCESS_KEY,secret_key=SECRET_KEY,s3_bucket=S3_BUCKET)
    except Exception,e:
        sys.stderr.write("S3 Bucket info is wrong")
        log.error(e)
        exit(0)

    #restore action
    if args.restore:
        dest = args.dest

        #if user didn't input a destination for the restore file
        if dest is None:
            sys.stderr.write("Please input a path for the destination of the restore file (-d switch)")
            exit(0)
        #if dest directory doesn't exist
        elif not os.path.exists(dest):
            sys.stderr.write("Specified destination directory doesn't exist")
            exit(0)
        else:
            try:
                file = backup.get(args.restore)
                if file is None:
                    log.error("%s doesn't exist in the s3 bucket" % args.restore)
                    exit(0)
                file.seek(0)
                out_file = str(dest + args.restore)
                shutil.move(file.name,dest+os.path.basename(args.restore))
                log.info('%s restored successfully' % file.name)
                exit(0)
            except Exception,e:
                import traceback
                print traceback.format_exc()
                log.error(e)
                exit(-1)
    if args.list:
        for key in backup.list():
            print key

    #backupp
    if args.backup:
        tmp_dir = '/tmp/'
        file_name = datetime.now().strftime('%Y_%m_%d_%H_%M_%S.tar.gz')
        up = '%s%s' % (tmp_dir, file_name)
        data = cfg.get('backup','data').split(',')
        out = tarfile.open(up,mode="w:gz")

        for path in data:
            if not os.path.exists(path):
                log.info('%s does not exist' % path )
                continue
            out.add(path)
        out.close()
        backup.put(file_name,open(up,mode='r'))
        #os.remove(out)

