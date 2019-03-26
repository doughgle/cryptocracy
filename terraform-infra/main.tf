provider "aws" {
  region = "ap-southeast-1"
}

resource "random_uuid" "instance_uuid" {}

resource "aws_s3_bucket" "proxy_crypt_bucket" {
  bucket = "proxy-crypt-bucket-${terraform.workspace}-${random_uuid.instance_uuid.result}"
  acl    = "private"

  tags = "${merge(var.default_tags,map("Environment", terraform.workspace))}"
}

resource "aws_s3_bucket" "object_cache_bucket" {
  bucket = "object-cache-bucket-${terraform.workspace}-${random_uuid.instance_uuid.result}"
  acl    = "private"

  tags = "${merge(var.default_tags,map("Environment", terraform.workspace))}"
}

resource "aws_dynamodb_table" "proxy_key_table" {
  hash_key       = "user_id" # this should be a secure one-way hash of the user id
  name           = "proxy-key-table-${terraform.workspace}"
  read_capacity  = 1
  write_capacity = 1

  "attribute" {
    name = "user_id"
    type = "S"
  }

  server_side_encryption {
    enabled = true
  }

  tags = "${merge(var.default_tags,map("Environment", terraform.workspace))}"
}