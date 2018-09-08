# Use Cases
===

|add user||
|---|---|
|actors|Data Owner, System|
|pre-conditions|one-time setup complete.<br>master key generated.<br>global params generated.<br>Cloud Server's public key known.<br>User's public key known.
|post-conditions|user and proxy key are added in Cloud Server's proxy key store.|
|main course|Data Owner decides attributes for user.<br>Data Owner inputs `userid ` (maybe email address), `user's public key` and associated `attributes`.<br>System generates proxy key for user with decided attibutes.<br>System posts proxy key with username to Cloud Server. (*should this be out of band?*)<br>Cloud Server adds proxy key for user.<br>System responds to Data Owner with result and `user identification ref`.|
|alternate courses|
|exceptional courses|

---

|encrypt file||
|---|---|
|actors|Data Owner|
|pre-conditions|one-time setup complete.<br>master key generated.<br>global params generated.
|post-conditions|ciphertext file produced for given plaintext file.|
|main course|Data Owner submits `file` for encryption together with an `access policy expression`.<br>System responds with a ciphertext representing the file.<br>|
|alternate courses|
|exceptional courses|
