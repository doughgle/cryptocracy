# Boundaries

Boundaries represent the interfaces with other systems.

+ Object Store - stores encrypted binary objects in the cloud.
+ Proxy Key Store - key-value store of user identities to user proxy keys.
+ Key Authority Service - an HTTP service for user registration and issuing user proxy keys.

#### AWS Boundaries

Object Store and Proxy Key Store are hosted on AWS Cloud. To use them, setup AWS credentials as environment variables or user dot config files.

You can create the credential file yourself. By default, its location is at `~/.aws/credentials`:

```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

You may also want to set a default region. This can be done in the configuration file. By default, its location is at `~/.aws/config`:

```
[default]
region=us-east-1
```