# Workshop on Recommendation Engine using Apache Spark on Amazon Elastic MapReduce (EMR)
This is the detailed description of the initial setup before attending the workshop on building a Recommendation Engine using Apache Spark running on [Amazon EMR](https://aws.amazon.com/emr/). The workshop uses Python 3, [Zeppelin](https://zeppelin.apache.org/) and the [Spark DataFrames API](https://spark.apache.org/docs/2.1.0/sql-programming-guide.html). Amazon EMR comes with python3 installed on all the cluster nodes, we use emr-5.5.0 release for this workshop, and we configure our EMR cluster to have Zeppelin & Spark installed at launch. Refer to the Cloudformation template for more details.

## Pull all the files in this Git repository.
Do not change the names of the files that we will soon be uploading to S3. The Cloudformation template we use will be expecting these exact names.

`bootstrap_EMRCluster.sh` - This file sets up the bootstrap_zeppelin.sh to use later.

`bootstrap_zeppelin.sh` - A misnomer actually, this file changes the interpreter we will use by default in the interpreter.json file

`personalRatings.txt` - This is the file that contains a sample set of movies that user zero(0) has rated. To see which movies these are, you can have a look at the rateMovies script. This file is generated by rateMovies script or you can manually edit the ratigs to eeach of the movies.

`rateMovies` - This is the script that is used to rate movies and generate the `personalRatings.txt` file and uploads it to an S3 bucket of your choice. We run this script without any parameters, if you are not able to run this script, just edit `personalRatings.txt` with the ratings for yoru choice for the movies and upload it to the S3 bucket you will create in the next step.

## Creating a bucket
With a name of your choice in the region of your choice. Note, this will decide in which region your EMR cluster will be launched, it will be the same as the region where the bucket is created. You can [create an Amazon S3 bucket using the AWS Management Console](http://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html) or using the CLI, here is an example of creating the bucket using AWS CLI.

`aws s3 mb s3://your-bucket-name`

## Prepare the scripts for use later
Change the following files to use the name of your new bucket instead of the string __myBucket__.

`bootstrap_EMRCluster.sh` - Replace __myBucket__ with the name of the bucket you just created above.

`rateMovies` - Replace __myBucket__ with the name of the bucket you just created above. If you are going to modify the `personalRatings.txt` file by hand, you don't need to do modify this file.

## Getting the Data
We will be using the [Movielens 100K dataset](https://grouplens.org/datasets/movielens/100k/) for this exercise. Download it, unzip the bundle, and upload all the files to the bucket you just created above.
## Run the Cloudformation template
Now, open the Cloudformation console in the AWS Management Console, and create the stack, the template will ask for some parameters, make sure you already have them, they are,

__EC2 Keypair name__ : Read [here](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) how to create an EC2 key pair. This will be used to set up SSH between your laptop/desktop to the Master node.

__Location of the bootstrap actions script__ : This is the same as `s3://your-bucket-name/bootstrap_EMRCluster.sh`. You will replace __your-bucket-name__ with the name of the S3 bucket you created above.

__Subnet Id__ : This is the id of the subnet where you will launch the EMR cluster EC2 instances. This is of the format `subnet-XXXXXXX`. Ensure that the subnet is a public subnet, to know how to recognise a public subnet [review this documentation](http://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_Scenario1.html).

_A subnet that's associated with a route table that has a route to an Internet gateway is known as a public subnet._ 

__Log URI__ : This is the location where EMR will store the logs, this is useful later for debugging issues you may face.

## After the stack is created
We will need to modify the Security group of the master node in the EMR cluster. You can find the Master node's security group by looking at the Cluster details and identifying the master node's security group. Like so,

![](https://github.com/OmarKhayyam/EC2Collection/blob/master/SGandFQDN.png?raw=true)

Click on the security group and add your custom IP address for SSH into the inbound list of allowed IP addresses and ports, for details have a look at [this](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/authorizing-access-to-an-instance.html).

### Setting the Apache Zeppelin interpreter
Issue the following command from your laptop/machine, note that the key path and name are fictitious and should be replaced with your own key path and name, this is the key pair we generated when we created the EC2 key pair (see above). Also, the EC2 fully qualified name for the master node is also fictitious and should be replaced with your own. Refer screenshot above for details on where you can find this information.

`ssh -i ~/Keys/MyEMRKey.pem hadoop@ec2-11-111-111-11.ap-south-1.compute.amazonaws.com 'sudo /home/hadoop/bootstrap_zeppelin.sh'`

#### Windows Users
Log into the master node with putty. [Read instructions to change the .pem file format to putty compatible format here](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html). 

After you have logged in, issue the above command like so,

`sudo /home/hadoop/bootstrap_zeppelin.sh`

### Setting up the SSH tunnel from your machine/laptop to the Master Node in the EMR cluster
To do this, if you have a Mac or Linux based laptop/machine, issue the following command,

`ssh -f -N -i <full path to the .pem file you got when you generated your EC2 key pair> -L 127.0.0.1:8890:127.0.0.1:8890 hadoop@<Full DNS name of the EMR cluster master node>`

for example, note that all DNS names and key names are fictitious.

`ssh -f -N -i ~/Keys/MyEMRKey.pem -L 127.0.0.1:8890:127.0.0.1:8890 hadoop@ec2-11-111-111-11.ap-south-1.compute.amazonaws.com`

#### Windows Users
To set up an SSH tunnel from your Windows laptop/machine to the Master node in the EMR cluster, [follow these instructions](http://realprogrammers.com/how_to/set_up_an_ssh_tunnel_with_putty.html).

### Accessing the Zeppelin Notebook
All you have to do is open your favourite browser and enter the following in it and hit <ENTER>,

`http://localhost:8890`

This should display a page similar to this,

![]()
