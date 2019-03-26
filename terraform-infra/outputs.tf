output "proxy_key_store_table_name" {
  value = "${aws_dynamodb_table.proxy_key_table.name}"
}

output "object_store_bucket_name" {
  value = "${aws_s3_bucket.proxy_crypt_bucket.bucket}"
}

output "object_cache_bucket_name" {
  value = "${aws_s3_bucket.object_cache_bucket.bucket}"
}