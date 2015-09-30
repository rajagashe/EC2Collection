# EC2Collection
This is a Python class that gathers the Amazon Web Services (AWS) EC2(Elastic Compute Cloud) data from your account for a specific region and provides routines to analyse it.

#Pre-Requisites
This module expects the following other modules to be present before it can be used:
        sys,os,base64,datetime,hashlib,hmac,requests,copy,dateutil.tz and boto3.
This module only supports Python 3 and has been test only with Python 3.4.

#Installation
pip based installation Coming soon.

#About the Methods
This class has methods that can help you do many things, here is a brief summary, there is also the __main__ that will help you with examples of how you can use this class, at this point though they are all commented.
The creds file used in the __main__ is expected to be in the following format:

KeyID   XXXXXXXXXXXXXXXXXXXX
SecretKey       yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy

The class can also get Access Key ID and Secret Key from the environment, if none is provided at the time of instantiation.

You are expected to have adequate permissions to perform these operations, at this point I do not have exception handling in place, that will be added later, I wanted to get this out so people can use it.

No optimization has been performed on this code yet.

***This calss is iterable.

Methods:
getListByAttr - returns a subset of a list based on a certain criteria,
                it further, gets more subsets from the previously obtained
                subset, so on and so forth, these subset lists generated
                are basically as many as there would be parameters.
drillByMultipleParams - returns a subset of a list based on a certain criteria,
                it further, gets more subsets from the previously obtained
                subset, so on and so forth, these subset lists generated
                are basically as many as there would be parameters.
refresh - Refresh the EC2 instance list. This call is made if you have
                changed something.
launchedBefore - This is called with date parameters and an instance list, the
                other parameters are year, month, day, all integer values,
                this will return the list of instances that were launched
                before a given date.
launchedAfter - This is same as above, except, it returns a list of instances
                that were launched after a certain date.
areTaggedWith - Takes an instance list and a tag key and returns all the
                instances tagged with that key.
areNotTaggedWith - This is the opposite of the above, returns a list of
                        instances that are not tagged with given key.
getInstanceList - Returns a list of instaces based on an attribute value.
showSupportedAttribs - Displays the supported attributes for the operations
                        listed herewith.
showTagValues - Displays the tags on an instance.
removeTagValue - Removes a tag from the instance.
addModifyTagValue - Add or modify a tag value.
showInstances - Display instances on the basis of a certain attribute value
