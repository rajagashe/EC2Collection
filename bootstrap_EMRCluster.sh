#!/bin/bash

aws s3 cp s3://myBucket/bootstrap_zeppelin.sh .
cp ./bootstrap_zeppelin.sh /home/hadoop/
chmod u+x /home/hadoop/bootstrap_zeppelin.sh
