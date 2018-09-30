Use Cases
===

|Add user||
|---|---|
|actors|Data Owner, System|
|pre-conditions|one-time setup complete.<br>master key pair generated.<br>global params generated.<br>Cloud Server's public key known.<br>User's public key known.
|post-conditions|user and proxy key are added in Cloud Server's proxy key store.|
|main course|Data Owner decides attributes for user.<br>Data Owner inputs `userid ` (maybe email address), `user's public key` and associated `attributes`.<br>System generates proxy key for user with decided attibutes.<br>System posts proxy key with username to Cloud Server. (*should this be out of band?*)<br>Cloud Server adds proxy key for user.<br>System responds to Data Owner with result and `user identification ref`.|
|alternate courses|
|exceptional courses|
|example|`$ aws dynamodb scan --table-name proxy-key-table`<br>`$ aws dynamodb put-item --table-name proxy-key-table --item "{\"user_id\":{\"S\":\"alice@dev.net\"}, \"proxy_key\":{\"S\":\"$PROXY_KEY\"}}"`|

---

|Encrypt file||
|---|---|
|actors|Data Owner|
|pre-conditions|one-time setup complete.<br>master key pair generated.<br>global params generated.
|post-conditions|ciphertext file produced for given plaintext file.|
|main course|Data Owner submits `file` for encryption together with an `access policy expression`.<br>System responds with an encrypted file representing the plaintext file.<br>|
|alternate courses|
|exceptional courses|
|example| `$ oabe_enc -v -s CP -e '(A or B) and C' -i data.png -o encrypted.png.cpabe -p gov.sg`|

---

|Upload file||
|---|---|
|example|```$ source /media/dough/Storage/repos//exercises/ABE/proxy-crypt-infra/.mycreds; aws s3 cp encrypted.png.cpabe s3://proxy-crypt-bucket/encrypted.png.cpabe```|

---

|Download file||
|---|---|
|actors|User|
|pre-conditions|File exists in Cloud Server.<br>User's proxy key exists in Proxy Key Store.|
|post-conditions|User has partially decrypted file.|
|main course|<ol><li>User requests `file`.<li>System partially decrypts `file` using User's proxy key.<li>System returns partially decrypted file to User.</ol>|
|alternate courses|
|exceptional courses|
|example|```$ source /media/dough/Storage/repos//exercises/ABE/proxy-crypt-infra/.mycreds; aws s3 cp s3://proxy-crypt-bucket/encrypted.png.cpabe encrypted.png.cpabe```|

---
### Upload Download Worflow
![alt text](diagrams/Upload-Download%20Workflow.png)
---
### Revoke User Workflow
![alt text](diagrams/Revoke%20User%20Workflow.png)