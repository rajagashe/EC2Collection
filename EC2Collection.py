import sys, os, base64, datetime, hashlib, hmac, requests, copy
from dateutil.tz import tzlocal
from boto3.session import Session

"""
The E2Collection class is meant to be used to collect
and then process this EC2 data to gain insights into the
various aspects of cloud resources that are EC2 instances.
This will make no distinction between running and stopped
instances.
Author : Rahul Shringarpure
"""

class EC2Collection:
	"""Collection of EC2 instance pulled from AWS"""
	regionEpMap = {'us-east-1': 'ec2.us-east-1.amazonaws.com',
			'us-west-2': 'ec2.us-west-2.amazonaws.com',
			'us-west-1': 'ec2.us-west-1.amazonaws.com',
			'eu-west-1': 'ec2.eu-west-1.amazonaws.com',
			'eu-central-1': 'ec2.eu-central-1.amazonaws.com',
			'ap-southeast-1': 'ec2.ap-southeast-1.amazonaws.com',
			'ap-southeast-2': 'ec2.ap-southeast-2.amazonaws.com',
			'ap-northeast-1': 'ec2.ap-northeast-1.amazonaws.com',
			'sa-east-1': 'ec2.sa-east-1.amazonaws.com'}

	def __init__(self,access_key_id=None,secret_key=None,regioncode='us-east-1'):
		if access_key_id == None and secret_key == None:
			self.access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
			self.secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
			self.session = Session(self.access_key_id,self.secret_key,None,regioncode)
		else:
			self.access_key_id = access_key_id
			self.secret_key = secret_key
			self.session = Session(access_key_id,secret_key,None,regioncode)
		self.client = self.session.client('ec2')
		self.res = self.session.resource('ec2')
		self.region = regioncode
		self.ec2collectionobj = self.client.describe_instances()
		self.inslist = [ins for indx in self.ec2collectionobj['Reservations'] for ins in indx['Instances']]
		self.size = len(self.inslist)
		self.supportedattribs = []
		self.index = -1

	def __getListByAttr(self,attrlist,inslist):
		attrlistlen = len(attrlist)
		lis1 = copy.deepcopy(inslist)
		attrcount = 0
		while True:
			lis2 = self.getInstanceList(inslist=lis1,instanceattr=attrlist[attrcount],attrval=attrlist[attrcount+1])
			lis1.clear()
			lis1 = copy.deepcopy(lis2)
			attrcount += 2
			if attrcount >= attrlistlen:
				break
			lis2.clear()
		return lis1

	def drillByMultipleParams(self,attribvallist):
		"""attribvallist == ['vpcid','vpc-xxxxxx','platform','rhel','virtualizationtype','hvm']"""
		if not attribvallist:
			return None
		else:
			finallist = self.getListByAttr(attribvallist,self.inslist)
		return finallist

	def refresh(self):
		self.ec2collectionobj = self.client.describe_instances()
		self.inslist = [ins for indx in self.ec2collectionobj['Reservations'] for ins in indx['Instances']]
		self.size = len(self.inslist)
		self.index = -1

	def launchedBefore(self,inslist=None,Year=None,Month=None,Day=None):
		if not inslist:
			inslist = self.inslist
		if not Year or Month or Day:
			timenow = datetime.today(tzlocal())
		else:
			timenow = datetime.datetime(Year,Month,Day,0,0,0,0,tzlocal())
		return [ instance for instance in inslist if instance['LaunchTime'] <= timenow]

	def launchedAfter(self,inslist=None,Year=None,Month=None,Day=None):
		if not inslist:
			inslist = self.inslist
		if not Year or Month or Day:
			timenow = datetime.today(tzlocal())
		else:
			timenow = datetime.datetime(Year,Month,Day,0,0,0,0,tzlocal())
		return [ instance for instance in inslist if instance['LaunchTime'] >= timenow]

	def areTaggedWith(self,inslist=None,TagKey='Name'):
		if not inslist:
			inslist = self.inslist
		return [ instance for instance in inslist if list(filter(lambda x: x['Key'] == TagKey, instance['Tags']))]

	def __isNotInTagList(self,dictkey,dictlist):
		for dic in dictlist:
			if dic['Key'] == dictkey:
				return False
		return True

	def areNotTaggedWith(self,inslist=None,TagKey='Name'):
		if not inslist:
			inslist = self.inslist
		temp = []
		for instance in inslist:
			if self.isNotInTagList(TagKey,instance['Tags']):
				temp.append(instance)
		return(temp)

	def __getitem__(self,index):
		if 0 <= index < self.size:
			return self.inslist[index]
		raise IndexError()

	def __len__(self):
		return len(self.inslist)

	def __iter__(self):
		return (inst for inst in self.inslist)

	def __contains__(self,item): #item == instance id
		return [ instance for instance in self.inslist if self.yesItDoes(instance,item)]

	def __yesItDoes(self,instance,item):
		for ki,val in instance.items():
			if val == item:
				return True
		else:
			return False

	def getInstanceList(self,inslist,instanceattr='instanceid',attrval=None):
		if inslist == None:
			inslist = self.inslist
		if not self.supportedattribs:
			self.supportedattribs = [key for key in self.inslist[0] if not isinstance(self.inslist[0][key],list) and not isinstance(self.inslist[0][key],dict) and key != 'LaunchTime']
		attrib = [key for key in self.supportedattribs if instanceattr.lower() == key.lower()][0]
		if not attrib:
			print("Unsupported attribute. Please use showSupportedAttribs() to get a list of supported attributes.")
		if not attrval:
			return inslist
		else:
			filteredlist = [instance for instance in inslist if instance[attrib] == attrval]
			return filteredlist

	def showSupportedAttribs(self):
		if not self.supportedattribs:
			self.supportedattribs = [key for key in self.inslist[0] if not isinstance(self.inslist[0][key],list) and not isinstance(self.inslist[0][key],dict) and key != 'LaunchTime']
		print(",".join(self.supportedattribs))

	def showTagValues(self,instanceid):
		inslist = self.inslist
		theone = [instance for instance in inslist if instance['InstanceId'] == instanceid][0]
		for tags in theone['Tags']:
			print("{0} - {1}".format(tags['Key'],tags['Value']))

	def removeTagValue(self,instanceid,key):
		inslist = self.inslist
		theone = [instance for instance in inslist if instance['InstanceId'] == instanceid][0]
		val = [value['Value'] for value in theone['Tags'] if value['Key'] == key][0]
		ec2 = self.res
		tg = ec2.Tag(instanceid,key,val)
		tg.delete(DryRun=False)

	def __sign(self,key,msg):
		return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()
	def __getSignatureKey(self,key,date_stamp, regionName, serviceName):
		kDate = self.sign(('AWS4' + key).encode('utf-8'), date_stamp)
		kRegion = self.sign(kDate, regionName)
		kService = self.sign(kRegion, serviceName)
		kSigning = self.sign(kService, 'aws4_request')
		return kSigning

	def addModifyTagValue(self,instanceid,key,value):
		method = 'GET'
		service = 'ec2'
		host = EC2Collection.regionEpMap[self.region]
		region = self.region
		endpoint = 'https://'+host+'/'
		request_parameters = 'Action=CreateTags&ResourceId.1='+ instanceid +'&Tag.1.Key='+key+'&Tag.1.Value='+value+'&Version=2015-04-15'
		t = datetime.datetime.utcnow()
		amzdate = t.strftime('%Y%m%dT%H%M%SZ')
		datestamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope
		canonical_uri = '/'
		canonical_querystring = request_parameters
		canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n'
		signed_headers = 'host;x-amz-date'
		payload_hash = hashlib.sha256(''.encode('utf-8')).hexdigest()
		canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
		algorithm = 'AWS4-HMAC-SHA256'
		credential_scope = datestamp + '/' + region + '/' + service + '/' + 'aws4_request'
		string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
		signing_key = self.getSignatureKey(self.secret_key, datestamp, region, service)
		signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
		authorization_header = algorithm + ' ' + 'Credential=' + self.access_key_id + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
		headers = {'x-amz-date': amzdate, 'Authorization': authorization_header}
		request_url = endpoint + '?' + canonical_querystring
		r = requests.get(request_url, headers=headers)
		if str(r.status_code) == str(200):
			return True
		return False

	def showInstances(self,inslist=None,instanceattr='instanceid',attrval=None):
		if not inslist:
			inslist = self.inslist
		if not self.supportedattribs:
			self.supportedattribs = [key for key in self.inslist[0] if not isinstance(self.inslist[0][key],list) and not isinstance(self.inslist[0][key],dict) and key != 'LaunchTime']
		attrib = [key for key in self.supportedattribs if instanceattr == key.lower()][0]
		if not attrib:
			print("Sorry, unsupported attribute. Use showSupportedAttribs() to find ou supported attributes.")
		if not attrval:
			for instance in inslist:
				print("{0} - {1}".format(instance[attrib],[x for x in instance['Tags'] if x['Key'] == 'Name'][0]['Value']))
		else:
			filteredlist = [instance for instance in inslist if instance[attrib] == attrval]
			for ins in filteredlist:
				print("{0} - {1}".format(ins[attrib],[x for x in ins['Tags'] if x['Key'] == 'Name'][0]['Value']))

if __name__ == "__main__":
	CREDSFILE = '/Users/rahul/credentials.my'
	with open(CREDSFILE, encoding='utf-8') as keydata:
		accninfo = dict([(x.rstrip()).split() for x in keydata])
	ec2collection = EC2Collection(access_key_id = accninfo['KeyID'],secret_key = accninfo['SecretKey'])
	#ec2collection.showSupportedAttribs()
	#ec2collection.showInstances(instanceattr='ebsoptimized',attrval=False)
	#print(ec2collection.getInstanceList(None,instanceattr='virtualizationtype',attrval = 'hvm'))
	#print([ instid['InstanceId'] for instid in ec2collection.launchedAfter(Year=2014,Month=1,Day=1)])
	#print([ instid['InstanceId'] for instid in ec2collection.launchedBefore(Year=2014,Month=1,Day=1)])
	#print([ instid['InstanceId'] for instid in ec2collection.areTaggedWith() ])
	#print("###################################")
	#print("###!!!Got the Drill down list!!!###")
	#print("###################################")
	#print(ec2collection.drillByMultipleParams(['virtualizationtype','hvm','VpcId','vpc-52b1713d','instanceid','i-xyxyxyxy']))
