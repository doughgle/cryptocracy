# Cryptocracy Terraform
---

Terraform code to describe infrastructure as code for Cryptocracy on AWS.

## How to use?

Define your AWS creds. In this example, as environment variables. See AWS docs for alternatives.  
```sh
$ export AWS_ACCESS_KEY_ID="FOO"
$ export AWS_SECRET_ACCESS_KEY="BAR"
$ export AWS_DEFAULT_REGION="ap-southeast-1"
```

To create the nonprod infrastructure (for running tests etc).

```bash
$ terraform init
$ terraform workspace new nonprod
$ terraform apply
```

Initialize and create the infrastructure with Terraform.
```
$ terraform init
$ terraform apply
aws_s3_bucket.proxy_crypt_bucket: Refreshing state... (ID: proxy-crypt-bucket)
aws_dynamodb_table.proxy_key_table: Refreshing state... (ID: proxy-key-table)

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create
-/+ destroy and then create replacement

Terraform will perform the following actions:

-/+ aws_dynamodb_table.proxy_key_table (new resource required)
      id:                               "proxy-key-table" => <computed> (forces new resource)
      arn:                              "arn:aws:dynamodb:ap-southeast-1:409928522412:table/proxy-key-table" => <computed>
      attribute.#:                      "1" => "1"
      attribute.387955424.name:         "user_id" => "user_id"
      attribute.387955424.type:         "S" => "S"
      hash_key:                         "user_id" => "user_id"
      name:                             "proxy-key-table" => "proxy-key-table-default" (forces new resource)
      point_in_time_recovery.#:         "1" => <computed>
      read_capacity:                    "1" => "1"
      server_side_encryption.#:         "1" => "1"
      server_side_encryption.0.enabled: "true" => "true"
      stream_arn:                       "" => <computed>
      stream_label:                     "" => <computed>
      stream_view_type:                 "" => <computed>
      tags.%:                           "2" => "2"
      tags.Environment:                 "Dev" => "default"
      tags.Project:                     "proxy-crypt" => "proxy-crypt"
      write_capacity:                   "1" => "1"

  + aws_s3_bucket.object_cache_bucket
      id:                               <computed>
      acceleration_status:              <computed>
      acl:                              "private"
      arn:                              <computed>
      bucket:                           "object-cache-bucket-default"
      bucket_domain_name:               <computed>
      bucket_regional_domain_name:      <computed>
      force_destroy:                    "false"
      hosted_zone_id:                   <computed>
      region:                           <computed>
      request_payer:                    <computed>
      tags.%:                           "2"
      tags.Environment:                 "default"
      tags.Project:                     "proxy-crypt"
      versioning.#:                     <computed>
      website_domain:                   <computed>
      website_endpoint:                 <computed>

-/+ aws_s3_bucket.proxy_crypt_bucket (new resource required)
      id:                               "proxy-crypt-bucket" => <computed> (forces new resource)
      acceleration_status:              "" => <computed>
      acl:                              "private" => "private"
      arn:                              "arn:aws:s3:::proxy-crypt-bucket" => <computed>
      bucket:                           "proxy-crypt-bucket" => "proxy-crypt-bucket-default" (forces new resource)
      bucket_domain_name:               "proxy-crypt-bucket.s3.amazonaws.com" => <computed>
      bucket_regional_domain_name:      "proxy-crypt-bucket.s3.ap-southeast-1.amazonaws.com" => <computed>
      force_destroy:                    "false" => "false"
      hosted_zone_id:                   "Z3O0J2DXBE1FTB" => <computed>
      region:                           "ap-southeast-1" => <computed>
      request_payer:                    "BucketOwner" => <computed>
      tags.%:                           "2" => "2"
      tags.Environment:                 "Dev" => "default"
      tags.Project:                     "proxy-crypt" => "proxy-crypt"
      versioning.#:                     "1" => <computed>
      website_domain:                   "" => <computed>
      website_endpoint:                 "" => <computed>


Plan: 3 to add, 0 to change, 2 to destroy.
```
