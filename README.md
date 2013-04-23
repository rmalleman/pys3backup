## Synopsis

pys3backup is a utility written for an independent study course at Weber State University to explore the boto s3 python
library.  The utiltiy uses a simple configuration file containing a comma delimited list of folders and files, and then
tars and compresses the file and then puts it into an amazon s3 bucket.  The utility also can list previous backups, and
restore them back to disk

## Installation

To install on a *nix system:

<pre><code>$ python setup.py install</code></pre>

## Usage

To use this utility, you must place a configuration file called .pys3backup in your home folder.  The configuration
file must contain the two sections listed in the sampleconfig.ini.  You can sign up to use an Amazon Web Services account
at http://aws.amazon.com/.  Once you sign up, put your access key, secret key, and s3 bucket in the appropriate section
of the configuration file.  In the backup portion of the configuration file, the only thing needed is a comma delmited list
of files that need to be backed up.

### Backup

The following will back up the specified data and put it into the s3 bucket

<pre><code>$ pys3backup -b</code></pre>

Putting this command on a regular cron job will keep your data backed up.

### List

THis will list all backups in the S3 bucket
<pre><code>$ pys3backup -l</code></pre>

### Restore

For the restore command, you must specify the backup you want to restore, and also the destination

<pre><code>$ pys3backup -r backup.tar.gz -d ~/ </code></pre>

Note, after you restore the backup you will have to untar and uncompress it.

### Delete

THis command will delete your offsite backup permanently.  Proceed with caution

<pre><code>$ pys3backup -x backup.tar.gz</code></pre>

## Tests

All unit tests are in pysbackup_test.py

## Contributors

Software is provided as is, feel free to do whatever non-evil things you want with it

<pre>email:rmalleman AT gmail</pre>
<pre>twitter: @mattinsaltlake</pre>


## License

The MIT License (MIT)

Copyright (c) 2013

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

