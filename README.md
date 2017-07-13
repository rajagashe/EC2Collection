# Workshop on Recommendation Engine using Apache Spark on Amazon Elastic MapReduce (EMR)
This is the detailed description of the initial setup before attending the workshop on building a Recommendation Engine using Apache Spark running on Amazon EMR. The workshop uses Python 3, Zeppelin and the Spark DataFrames API. Amazon EMR comes with python3 installed on all the cluster nodes, we use emr-5.5.0 release for this workshop, and we configure our EMR cluster to have Zeppelin & Spark installed at launch. Refer to the Cloudformation template for more details.

## Pull all the files in this Git repository.
## Creating a bucket
With a name of your choice in the region of your choice. Note, this will decide in which region your EMR cluster will be launched, it will be the same as the region where the bucket is created. You can [create an Amazon S3 bucket using the AWS Management Console](http://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html) or using the CLI, here is an example of creating the bucket using AWS CLI.

`aws s3 mb s3://your-bucket-name`

## Prepare the scripts for use later
Change the following files to use the name of your new bucket instead of the string __myBucket__.

## Getting the Data
We will be using the [Movielens 100K dataset](https://grouplens.org/datasets/movielens/100k/) for this exercise. Download it, unzip the bundle, and upload all the files to the bucket you just created above.
## Run the Cloudformation template
Now, open the Cloudformation console in the AWS Management Console, and create the stack, the template will ask for some parameters, make sure you already have them, they are,

...An EC2 Keypair name

...Location of the bootstrap actions script

...A subnet Id

...Log URI

## After the stack is created
We will need to modify the Security group of the master node in the EMR cluster. You can find the Master node's security group by looking at the cluster details thus,

`aws emr describe-cluster --cluster-id j-xxxxxxxxxxx`
