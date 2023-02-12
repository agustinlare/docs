# AWS Security Specialty

# Incident Reponse

The incident response cycle is a structured process organizations follow to respond to security incidents, and continuously improve their incident management process. 

## Main Points

1. Given an AWS abuse notice, evaluate the suspected compromise instance or expose access Keys
2. Verify that the incident response plan includes relevant AWS services
3. Evaluate the configuration of automated alerting and execute possible remediation of security-related incidents and emerging issues

### Case of Compromised Instance

- Amazon GuardDuty is a threat detection service that continuously monitors your AWS accounts and workloads for malicious activity and delivers detailed security findings for visibility and remediation.
- VPC Flow Logs is a feature that enables you to capture information about the IP traffic going to and from network interfaces in your VPC. Flow log data can be published to the following locations: Amazon CloudWatch Logs, Amazon S3. After you create a flow log, you can retrieve and view the flow log records in the log group, bucket, or delivery stream that you configured.
- Isolate instances from network using security group
- Launch a replacement from AMI

### Case of Exposed access keys

- Access Advisor report to determine which services were accessed using that key and at what time.
- GuardDuty
- CloudTrail Logs
- Disable Keys, create new keys

## Incident Reponse Plan

![cyberincidentresponsecycle_axa-xl_graphic2.png](_resources/cyberincidentresponsecycle_axa-xl_graphic2.png)

### Preparation

Invariably, there will come a time where a risk will materialize, and a cyber incident will occur. Preparation is where the foundations of any future response process lie. In this phase, you should adopt a risk-based approach to cybersecurity, by taking the time to understand your organization’s technological and business environment, identify and track threats and document risks to your organization. Once you define your risk and identify your critical assents, you'll need an actionable plan that empowers your teams to response indicendets.

- Limit the blast radious
    - Deploy Accounts using AWS Organization
    - Using multiple VPC to restrict access
    - Self documented infraestructure (AWS Config, AWS CloudFormation, AWS SSM)
- Procedures and Run Playbooks
    - Store this files in diffrente accounts with high avaialability with soft copies in offline storage
- Normal Behavior Baseline
    - Amazon CloudWatch
    - Amazon GuardDuty
- Clean image for DRP
    - Create clean EC2 AMI 
    - EBS Snapshots
    - Backup stored in S3
    - Save configuration files in S3
- Risk assessment
    - Amazon Inspector, EC2 perspective
    - Amazon GuardDuty
    - Amazon Macie, S3 perspective
- Network security
    - VPC NACL
    - Security Groups
    - VPC Flow Logs
    - AWS WAF
- Store Relevant Event Information
    - Amazon CloudWatch Logs
    - Configuration stream (Snapshot of config)
    - Amazon CloudWatch Events
    - Access logs stored in S3
    - CloudTrail Logs

### Detection and Analysis

The detection phase uses technical or administrative security controls to detect malicious activity in the environment.

- Recognizing sings of an intrusion attempt
    - Amazon CloudWatch
    - Amazon CloudTrail (audit log)
    - Amazon GuardDuty
    - VPC Flow Logs
- Incident Analysis
    - Visualize performance baseline with CloudWatch dashboards, SSM Insights dashboards
    - Understand normal behavior with GuardDuty dashboard
    - Implement log retention policies, CloudWatch log expiration, S3 life cycle policies and glacier vault lock policy
    - Corralate events between logs and metrics with Amazon OpenSearch & Kibana and CloudWatch logs insights
- Incident Notification
    - Amazon SNS
    - Amazon SES
    - AWS Trusted Advisor
- Use all help Available
    - Open a support case
    - Search the AWS Forums
    - Great justification for premium support

### Contaiment Eradication & Recovery

Detection flows into containment, eradication, and recovery, with the implication that each may be repeated multiple times during a given incident. This is intended to acknowledge the reality that, as the response process unfolds, new issues will likely be detected and addressed.

#### Steps

- Containment strategy
    - Security Group rules
    - Revoke IAM sessions
    - WAF ACL rules
    - IAM policies
    - Access key rotation
    - KMS CMK rotation
- Evidence gathering and handling
    - CloudTrail log
    - CloudWatch log
    - VPC Flow Logs
    - IAM Access Advisor
- Identify the attacking Entity 
    - DNS Lookup
    - GuardDuty Finding
- EC2 Instance termination
- Disable compromised keys
- Separate compromised data for analysis
- Recovery
    - Know your RTO (recovery time objective) and RPO (recovery point objective)
    - Ability to recognize resources that needed to be repair and those that need replacement
    - Automate task to help a faster recovery
- Clean Up
    - Remove temporary resources
    - KMS key audit
    - Full IAM audit
    - Review further fidings

### Post-Incident Activity

When recovery has been completed across the organization, it can be tempting to simply put the incident behind you. However, doing so will be detrimental to your organization’s growth, as well as your preparedness to tackle similar incidents in the future. Understanding the cause of the incident, reviewing how your program can be improved, and implementing the improvements constitute an essential feedback loop. This feedback loop should be formalized in your incident response plan.

You'll need:

- Evidence retation
    - S3
    - Glacier
    - AMI of compromised instances
    - Snapshots of compromised volumes
- Proposals for improvment
    - Least privilage
        - Access control
        - Network permissions
    - Monitoring
        - Better dashboards
        - Active response

## Case Study: Compromised EC2 Instance

Scenario: One of your EC2 instances has been compromised by an unknown actor
How can you:

1.  identify compromised resources
2.  identify blast radius
3.  mitigate the event
4.  recover safely

### identify compromised resources

Option 1: AWS abuse notice via email

> No context, few data points = Sub-optimal

Option 2: Identify through existing instrumentation using services CloudWatch, VPC Flow logs, EC2 OS Firewall

> Allow us to gather data points on the security performance and by doing this we start to correlate our viewed behavior with actions that are been taken potentially by an outside source and that allow us to make informed decisions on how to move ahead.

### identify Blast Radios

Use AWS ecosystem to determine inventory relationships and which resources are associated with the compromised instance. AWS Config continually assesses, audits, and evaluates the configurations and relationships of your resources like to which subnet is associated, NACL, security group or volumes has attached. By learning all this information can actually change the scoop of our suspected compromised.

#### mitigate the Event

Given this configuration (fig 1.) we create a different SG and detachment the previous one to add a new one completely isolated from the network in place for analysis (fig 2).

![Fig1](_resources/aws-migrate-the-events.drawio.png)


#### recovery safely

Assuming that we've created our backups we can then launch another resource from it with the correct application security group. Also we need to retain our data and one way to do it is to persist all logs and data points in durable storage for post mortem analysis. Once we have the data it's important to analyse it to make recommendations and we can do it with some of this applications: 

- RedShift queries, feature RedShift: We can use it to create query S3 data like if it was part of PostgreSQL database.
- Athena: Analyze data or build application from an Amazon Simple Storage Service (S3)
- Glub Job: Execution of Code
- QuickSight dashboard

## Question Breakdown

Your security team has been informed that one of your IAM username/password pairs
has been published to social media and has been used several times by unauthorized
sources. How can the security team stop the unauthorized access, and determine what
actions were taken with the compromised account, with minimal impact on existing
account resources?

- [ ] Immediately change the IAM user password, ask the user what actions they normally take, then compare with current AWS inventory

> Stops the usage of the IAM account, but does not really address action taken with the compromised credentials

- [ ] Delete the IAM user account, remove all resources created by the user, and analyze CloudTrail logs for unauthorized actions

> Stops the usage of the IAM account, analyzes unauthorized usage, but impacts exisiting resources

- [ ] Immediately change the IAM user password, and remove all resources created by the user

> Stops the usage of the IAM account, but impacts existing resources

- [x] Immediately change the IAM user password, and analyze CloudTrail logs for unauthorized actions

# Logging and Monitoring

## Securit Monitoring

### Infraestructure Monitoring Services

- VPC Flow Logs
- Amazon GuardDuty
- Athernas queries
- AWS Config configuration stream, apply logic to that stream to determine if a change matches a rule. It watches security group changes, new instances launch, changes or additions in route tables.
- Amazon inspector 

### Application Monitoring Service

- CloudWatch logs
- CloudTrail, Cognito user authentication, step functions logs, deployments via AWS CodeDeploy
- S3, ALB Access Logs, CloudFront access logs, Redshift audit logs.

### Accounts Monitoring Services

- CloudWatch Events: Activity can be publish and create rule to match specific events and take action accordingly. GuardDuty, CloudTrail Events, AWS Organization events, can push events to this service.
- AWS Config: Include a predefined rules to get advantage of once enabled for accounts monitoring. [List of AWS Config Managed Rules](https://docs.aws.amazon.com/config/latest/developerguide/managed-rules-by-aws-config.html)

## Troubleshooting tools

### Tools

- Amazon Inspector findings
- CloudWatch alarms and metrics
- CloudTrail Logs
- CloudWatch Logs Insights

### Root causes

- Unclear requirements for security monitoring
- Poorly implemented CloudWatch Alarms
- Gaps in OS update procedures and compliance checking

## Case Study: Broken Monitoring

Scenario: Recent security event never generated notifications.
How can you:

1.  trace why notification have not received
2.  implement missing monitoring
3.  ensure compliance going forward

Given this pipeline

![aws-broken-monitoring-pipeline.png](_resources/aws-broken-monitoring-pipeline.drawio.png)

### trace why notification have not received

Possible Root Causes

- CloudTrail has been disabled
- CloudWatch alarm deleted or modified
- SNS topic or subscription deleted
- Email distribution subscription deleted or changed or blocked, individual email goes to ex-employee inbox.

### implement missing monitoring

- Enable CloudTrail
- Document all alarms and re-create
- Recreate topic or subscription
- Re-create distribution list

### ensure compliance

- Config Rule + Lambda function to ensure CloudTrail is enable
- Schedule lambda function that evaluates alarms and recreates as needed
- Prevent topic or subscription deletes via Organization SCP

## Question Breakdown

An application running in EC2 has a requirement for independent, periodic security checks against the application code. These checks can send notifications upon warning, but for critical alerts they must shut down the application on the instance. How can your security team perform these checks without injecting code into the application, while meeting the notification and active response requirement?

- [ ] Install the AWS Inspector agent on the instance, and schedule regular audit jobs. Send the findings to an SNS topic with a Lambda function subscribed that parses the findings and responds appropriately.
> AWS Inspector cannot audit your custom application code, but sending findings to Lambda is a good option
- [x] Deploy a second application on the EC2 instance with the security audit code. Send security audit results to CloudWatch Events, and create a rule to send warning events to SNS, and critical events to SSM Run Command to stop the application
- [ ] Install CloudWatch Logs agent on the instance, streaming all application logs. Create a CloudWatch Logs metric filter with alarms for notifications and a Lambda function to stop the application
> This does not act as an independent audit, relying on application logs
- [ ] Install the AWS Inspector agent on the instance, and schedule regular audit jobs. Send the findings to Cloud Watch Events, and create a rule to send warning events to SNS, and critical events to SSM Run Command to stop the application
> Inspector cannot audit custom code. Te passive/active response mechanism is appropriate.

## Logging Solutions

### Access logs

*API Gateway*: CloudWatch Logs, using IAM Role
*CloudFront*: S3 Bucket
*ELB*: S3 Bucket*
*S3*: S3 Bucket*

> * Best effort delivery, AWS does not grantee that every single log entry would actually make it into the S3 Bucket

### Execution logs

*API Gateway*: CloudWatch Logs, using IAM Role
*Lambda Functions*: CloudWatch Logs, using IAM Role
*Custom EC2*: S3 Bucket o CloudWatch Logs, using IAM Role

### Security Log

*Inspector*: With the possibility to use notification to SNS using an IAM Role
*GuardDuty*: You can send your findings to CloudWatch Events using IAM Role and take actions.
*CloudTrail*: CloudWatch Logs, using an IAM Role. By default uses S3 Bucket
*VPC Flow Logs*: CloudWatch Logs, using an IAM Role

## Log processing

- Amazon Kinesis Data Stream
- Amazon Kinesis Firehose (you can place them into S3, Redshift, Amazon ES, 3rd party applications)
- Amazon Athenas
- Amazon Redshift
- AWS Glue
- Amazon Elastic MapReduce
- Amazon Elasticsearch and Kibana
- Amazon CloudWatch logs Insights
- AWS Lambda (enables you to perform custom analytics from already easy to integrate services)

## Case Study: Automated Log Management

Scenario: New monitoring requirements to persist all logs in S3 and expire all entries in
CloudWatch log groups after 365 days

How can you:

1.  transfer logs from CloudWatch Logs to S3?
2.  implement automated log expiration across all log groups?

### transfer logs from CloudWatch Logs to S3

Using Kinesis Firehose placing the logs entry into the S3 Bucket. It require permissions and configuration into the following steps:

1.  Create IAM Role with trust policy allowing use by Kinesis Firehose
2.  Associate another IAM Role with permissions policy allowing write access to S3 bucket.
3.  Create Firehose delivery stream using IAM Role and ARN from previous steps and S3 bucket ARN
4.  Create IAM Role with trust policy allowing use by CloudWatch Logs
5.  Associate IAM Role with permissions policy allowing access to Kinesis Firehose
6.  Create a subscription filter using IAM role ARN created in previous step and delivery stream ARN *(requires CLI)*

### implement automated log expiration across all log groups

Creating IAM role with trust policy allowing to assume by Lambda function. The permissions policy will allow us to modify the configuration of a CloudWatch Group after this we create our lambda function that set the expiration days on CloudWatch Logs groups passed as parameter. After that we need to create a CloudWatch Event Rule that matches new CloudWatch Logs group creation and add the lambda function as target for this rule.

## Question Breakdown

You've been asked to stream application logs from CloudWatch Logs to Splunk.
There is an existing subscription filter on the log group, set up for Kinesis Firehose to S3. What is the most appropriate way to ingest the logs in near real-time for Splunk analysis?

- [ ] Create a Lambda function subscribed to the CloudWatch log group that streams entries to the Splunk endpoint
> CloudWatch log groups only support one subscription filter at a time
- [ ] Create a Splunk connector to the S3 bucket destination for the Kinesis Firehose
> S3 ingestion will not be near real-time, because Firehoes uses a buffer and batch mechanism
- [x] Enable Source record transformation on the Kinesis Firehose. Create a Lambda function using the Splunk blueprints which decompresses the log entries and pushes to Splunk
- [ ] Write a shell script that uses the AWS CLl to export logs from the CloudWatch log group and ingest into Splunk
> May be functional but not reliable or near real-time

# Infrastructure Security 

## Edge Security, ingress points

- CloudFront
- S3
- API Gateway
- ELB
- AWS Service API endpoints
- VPC Ingress

### VPC Security

**Subnets** can be used to isolate workloads, you can apply NACL and route tables and it gives you finer granularity cidr-related security features and you have the option to monitor using VPC Flow Log feature.

**Network ACL** stateless firewall with order rule sets for both inbound and outbound traffic that is going to be apply at the subnet level. You can use them to enforce compliance for application tier traffic and rejection inbound traffic to database from non-application sources and prevent compromised instances from exploring the network.

**Route Table** can be use to enable internet accessibility, limit outbound access to a specific cidr range -- even /32 and allow least privilege access to on-premises networks down to a single IP or enable traffic flow to authorized endpoints.

**Security Groups** is a stateful firewall. It also allows for inbound and outbound rules and since its stateful only requires to create rules in one direction. Its easier to apply least privilege because by default traffic is block so you can whitelist the appropriate external sources for access. You can create inbound rules to allow traffic only from specific upstream sources (like ALB). It can be apply to other features like lambda functions and endpoints.

## VPC Egress

**Internet Gateway** enables internet access with no blacklist capability so you may want to use more specific route tables entries to limit outbound access.

**Virtual Private Gateway** is used by both VPN and Direct Connect it can be used to route traffic to and between multiple customer networks (VPN CloudHub) and it has no native features for blacklisting traffic.

**VPC Peering Connection** this give you the ability to connect two VPCs and treat them as part of the same network. Requires route table entries, use specific cidr for least privilege. Restrict traffic with security groups and NACL.

**Gateway Endpoint** only used for access to DynamoDB and S3. VPC + DynamoDB or S3 must be present in the same region.Keep traffic private by avoiding public AWS network and allows you to apply resource-level permissions on all requests.

**Interface endpoint** access service API, API Gateway and Marketplace products keeps traffic private by avoiding public AWS network and does not require public IP addresses.

**NAT Gateway** actually exist inside of the VPC rather than attached to the VPC. Managed services that its deploy on a availability zone scope that only allows outbound access to the internet. They cannot be associated with security groups but with NACL that is part of the subnet they are launched into. Apply specific route table entries for least privilege.

**DIY** use fro inline IDS/IPS and DLP. This give you full control over the resource. With this approach can act as router, proxy or security appliance and by disable the source destination checking on the network interface it too becomes a target of round tables entries so you can enforce your traffic directly through this DIY endpoint.

## Multiple VPC Strategies

AWS customers often rely on hundreds of accounts and virtual private clouds (VPCs) to segment their workloads and expand their footprint.This level of scale often creates challenges around resource sharing, inter-VPC connectivity, and on-premises facilities to VPC connectivity.

### Same regions

![aws-vpc-strategies-sameregion.drawio.png](_resources/aws-vpc-strategies-sameregion.drawio.png)

### Different regions

![aws-vpc-strategies-diffregion.drawio.png](_resources/aws-vpc-strategies-diffregion.drawio.png)

### Different account

![aws-vpc-strategies-diffaccs.drawio.png](_resources/aws-vpc-strategies-diffaccs.drawio.png)

## Connect multiple VPC - Transit Gateway

You can deploy a transit gateway to create assosiations with other vpcs and manage the interconectivity between this vpcs attaching to the transit gateway itself and route tables. This gives your even more flexibility like VPC Peering connections.

## Consideration

The biggest arguments against using multiple accounts on AWS include the complexity of managing and maintaining global visibility of resources, it may require a greater amount of time and effort to establish security policies and control access to resources, which can increase the possibility of bugs and security vulnerabilities. It can also be more difficult to audit and track activities and resource usage across multiple accounts, which can make it difficult to make informed decisions about cost optimization and efficiency.

- More Security Groups
- More NACL
- More route tables (use Transit Gateway)
- More routes
- More egress points
- Higher operation overhead

## Case Study: Multi-Scope Infraestructure Design

Scenario: Design a secure infraestructure with multiple networks for hosting and operations

How can you:

1.  design an application/network infrastructure for HIPAA compliant workloads
2.  design a devops infrastructure for shared use
3.  utilize AWS services to eliminate traffic between the two networks

### design an application/network infrastructure for HIPAA compliant workloads

|  | Internet Accesibility  | Route Tables | NACLs | Services/Apps | SG Config |
|---|---|---|---|---|---|
| Subnet A | Direct access | 0.0.0.0/0 route to IGW | Reject outobund to VPC-only subnets | Managed services in public subnets with ALB with WAF | Inbound 443 / Outbound 8080 to app |
| Subnet B | Indirect internet access | 0.0.0.0/0 routed to NAT GW | Reject all non-application traffic in/out | Resources for application hosting (ECS/Fargate) | Inbound 8080 from LB / Outbound 3306 to DB |
| Subnet C | No internet access | No route for 0.0.0.0/0 | Accept inbound to DB from app only | Data presisted using synchronous replication (RDS/Aurora) | Inbound 3306 / No outbound |

### design a devops infrastructure for shared use

VPC deployed into multiple AZ with public and private subnets and EC2 instances running the CI in a private subnet. We are some workloads we are going to need configure to allow our devops pipeline to work specific for access to the CI and for our CI have access to our source code.

Force all traffice to VPN. This will allow our CI have access to our private data center network that has our source code. Also allow access to our CI through CLI or web browser from our internal company network. Then use a NAT Gateway for outbound acces to AWS API endpoints allowing push container image to ECR, create task definitions in ECS and deploying new services, and finally create new listle new rules to ABL to pint traffic to new ECS service.

## Question Breakdown

Your R&D team is designing a new application which will consist of multiple tiers as follows:

- Customer-facing: Web front end accessible by browser (ports 80/443)
- REST API: Application front end available to client apps and partners (port 443)
- Application: Business logic implementation (port 8080)
- Database: Relational data (port 3306)

Both the customer-facing and REST API tiers need access to the application tier, and only the application tier needs access to the database. Each tier is launched into dedicated subnets.

Which combination of security group and NACL rules would be part of a least-privilege network security configuration? (pick four)

- [x] NACL: deny ALL outbound from Customer-facing to Database subnets
- [ ] SG: allow ALL tcp inbound from REST API SG to Application SG
> Any time you're allowing ALL inbound, you should look for ways to restrict to a range or single port
- [x] SG: allow inbound 3306 from Application subnets to DB subnets
- [x] NACL: deny ALL inbound from REST API to Database
- [x] SG: remove default outbound rule from all SG
- [ ] NACL: allow ALL tcp inbound and outbound to Customer-facing subnets
> This is the default configuration. If the web tier only allows 80/443, it would be good to restrict this NACL to match