#!/bin/bash
sudo sed -i -e '/\"zeppelin.pyspark.python\":/ s/: .*/: \"python3\"/' /etc/zeppelin/conf/interpreter.json
