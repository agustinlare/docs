# AWS Resources and Services List

## AWS Organizations

Lets you create new AWS accounts at no additional charge. With accounts in an organization, you can easily allocate resources, group accounts, and apply governance policies to accounts or groups

## AWS Config

Continually assesses, audits, and evaluates the configurations and relationships of your resources on AWS, on premises, and on other clouds

### Configuration Stream

A configuration stream is an automatically updated list of all configuration items for the resources that AWS Config is recording. Every time a resource is created, modified, or deleted, AWS Config creates a configuration item and adds to the configuration stream. The configuration stream works by using an Amazon Simple Notification Service (Amazon SNS) topic of your choice. The configuration stream is helpful for observing configuration changes as they occur so that you can spot potential problems, generating notifications if certain resources are changed, or updating external systems that need to reflect the configuration of your AWS resources. 

## AWS SSM

AWS Systems Manager is the operations hub for your AWS applications and resources and a secure end-to-end management solution for hybrid cloud environments that enables secure operations at scale

## AWS CloudFormation

Lets you model, provision, and manage AWS and third-party resources by treating infrastructure as code

## Amazon GuardDuty

Amazon GuardDuty is a threat detection service that continuously monitors your AWS accounts and workloads for malicious activity and delivers detailed security findings for visibility and remediation. Looks at CloudTrail logs, VPC Flow logs and DNS Logs.

## Amazon CloudWatch 

Collects and visualizes real-time logs, metrics, and event data in automated dashboards to streamline your infrastructure and application maintenance

## Amazon Inspector 

Amazon Inspector is a vulnerability management service that continuously scans your AWS workloads for software vulnerabilities and unintended network exposure

## Amazon Macie

Amazon Macie is a data security service that uses machine learning (ML) and pattern matching to discover and help protect your sensitive data

## AWS CloudTrail 

Monitors and records account activity across your AWS infrastructure, giving you control over storage, analysis, and remediation actions

## VPC Flow Logs

VPC Flow Logs is a feature that enables you to capture information about the IP traffic going to and from network interfaces in your VPC

## Amazon OpenSearch

Amazon OpenSearch Service makes it easy for you to perform interactive log analytics, real-time application monitoring, website search, and more

## AWS Trusted Advisor

AWS Trusted Advisor provides recommendations that help you follow AWS best practices

## Amazon SES

Lets you reach customers confidently without an on-premises (SMTP) system.

## Amazon SNS

Sends notifications two ways, A2A and A2P. A2A provides high-throughput, push-based, many-to-many messaging between distributed systems, microservices, and event-driven serverless applications

## Amazon Redshift

Uses SQL to analyze structured and semi-structured data across data warehouses, operational databases, and data lakes, using AWS-designed hardware and machine learning to deliver the best price performance at any scale.

## Amazon Athena

Amazon Athena is a serverless, interactive analytics service built on open-source frameworks, supporting open-table and file formats. 

## AWS Glue 

AWS Glue is a serverless data integration service that makes it easier to discover, prepare, move, and integrate data from multiple sources for analytics, machine learning (ML), and application development.

## Amazon Kenesis

Amazon Kinesis makes it easy to collect, process, and analyze real-time, streaming data so you can get timely insights and react quickly to new information. Amazon Kinesis offers key capabilities to cost-effectively process streaming data at any scale, along with the flexibility to choose the tools that best suit the requirements of your application. With Amazon Kinesis, you can ingest real-time data such as video, audio, application logs, website clickstreams, and IoT telemetry data for machine learning, analytics, and other applications.

### Kinesis Data Streams

Amazon Kinesis Data Streams is a scalable and durable real-time data streaming service that can continuously capture gigabytes of data per second from hundreds of thousands of sources. 

### Kinesis Data Firehose

Amazon Kinesis Data Firehose is the easiest way to capture, transform, and load data streams into AWS data stores for near real-time analytics with existing business intelligence tools.

### Kinesis Data Analytics

Amazon Kinesis Data Analytics is the easiest way to process data streams in real time with SQL or Apache Flink without having to learn new programming languages or processing frameworks.

## Amazon EMR 

Amazon EMR is the industry-leading cloud big data solution for petabyte-scale data processing, interactive analytics, and machine learning using open-source frameworks such as Apache Spark, Apache Hive, and Presto. 