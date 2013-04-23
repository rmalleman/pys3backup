__author__ = 'matt'
import tempfile
import unittest

from scripts.pys3backup import configuration, backup

cfg = configuration.get()
ACCESS_KEY = cfg.get('s3_info', 'access_key')
SECRET_KEY = cfg.get('s3_info', 'secret_key')
S3_BUCKET = cfg.get('s3_info', 's3_bucket')

print ACCESS_KEY
print SECRET_KEY
print S3_BUCKET

class PyS3BackupTestCases(unittest.TestCase):

    def setUp(self):

        self.sample_file = tempfile.NamedTemporaryFile()
        self.sample_file.write("Sample file for unittests")
        self.sample_file.seek(0)
        print self.sample_file.name
        self.backup = backup.S3Backup(access_key=ACCESS_KEY,secret_key=SECRET_KEY,s3_bucket=S3_BUCKET)

    def testS3Backup(self):
        self.assertIsNotNone(self.backup)
        self.backup.put("buh",self.sample_file)
        self.assertIsNotNone(self.backup.list())
        self.assertIsNotNone(self.backup.get("buh"))
        self.backup.delete("buh")

if __name__ == '__main__':
    unittest.main()

