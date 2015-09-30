# EC2Collection
This is a Python class that gathers the Amazon Web Services (AWS) EC2(Elastic Compute Cloud) data from your account for a specific region and provides routines to analyse it. This class is iterable.

#Pre-Requisites
This module expects the following other modules to be present before it can be used:
        sys,os,base64,datetime,hashlib,hmac,requests,copy,dateutil.tz and boto3.
This module only supports Python 3 and has been test only with Python 3.4 on RHEL and 
Mac OSX.

#Installation
pip based installation coming soon.

#About the Methods
This class has methods that can help you do many things, here is a brief summary, there is also the __main__ that will help you with examples of how you can use this class, at this point though they are all commented.
The creds file used in the __main__ is expected to be in the following format:

KeyID   XXXXXXXXXXXXXXXXXXXX

SecretKey       yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy

The class can also get Access Key ID and Secret Key from the environment, if none is provided at the time of instantiation.

You are expected to have adequate permissions to perform these operations, at this point I do not have exception handling in place, that will be added later, I wanted to get this out so people can use it.

No optimization has been performed on this code yet.

Methods:
========

drillByMultipleParams(attribvallist) - returns an intersection of a list based
                on a certain criteria, it further gets more subsets from the 
                previously obtained subset, so on and so forth, these subset 
                lists generated are basically as many as there would be 
                parameters.
                attribvallist - list of supported attributes of this collection
                such that the list starts with an attribute followed by its value,
                like so : ['vpcid','vpc-xxxxxx','platform','rhel','virtualizationtype','hvm']
                This list parameter means that you want to find the list of
                EC2 instances that are part of vpc-xxxxxx and have platform set to
                rhel and whose virtualization type is hvm. The list is processed
                from left to right. Always processes the full list of EC2 instances
                in the account.

refresh() - Refresh the EC2 instance list. This call is made if you have
                changed something and want to get an updated list.

launchedBefore(inslist=None,Year=None,Month=None,Day=None) - This is called with a
                list parameter followed by an integer Year, integer Month and an
                integer Day. If the Year, Month or Day is None, today() is taken
                as the day, if inslist is None all the EC2 instances in the collection
                are processed. This returns a list of instances launched before
                the given date.

launchedAfter(inslist=None,Year=None,Month=None,Day=None) - This is same as above, 
                except, it returns a list of instances that were launched after a certain 
                date.

areTaggedWith(inslist=None,TagKey='Name') - Takes an instance list and a tag key and returns 
                all the instances tagged with that key. Processes all instances in the 
                collection if list passed is empty, and default key value parameter is
                'Name'.

areNotTaggedWith(inslist=None,TagKey='Name') - This is the opposite of the above, 
                returns a list of instances that are not tagged with a given key.

getInstanceList(inslist,instanceattr='instanceid',attrval=None) - Returns a list of instances 
                based on an attribute value. The first parameter is a list and if its None, the
                instances in the collection are used, instance attribute, if not provided
                is assumed to be instance identifier and if attrval is None, the whole 
                collection is returned.

showSupportedAttribs() - Displays the supported attributes for the operations
                        listed as part of the EC2Collection class. The list
                        displayed is comma-separated.

showTagValues - Displays the tags on an instance.

removeTagValue - Removes a tag from the instance.

addModifyTagValue - Add or modify a tag value.

showInstances - Display instances on the basis of a certain attribute value
