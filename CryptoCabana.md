1. List Containers

az storage container list \
  --account-name cryptocabanaf5scjagc \
  --sas-token "sv=2022-11-02&ss=b&srt=sco&sp=rl&se=2099-12-31T23:59:59Z&st=2024-01-01T00:00:00Z&spr=https&sig=ZAo05W8KXdSLM9afYCNGogNRV2N5a6aB4dQI3LXz%2Fh0%3D" \
  --output table
  
2. List Blobs in a Container

az storage blob list \
  --account-name cryptocabanaf5scjagc \
  --container-name vault \
  --sas-token "sv=2022-11-02&ss=b&srt=sco&sp=rl&se=2099-12-31T23:59:59Z&st=2024-01-01T00:00:00Z&spr=https&sig=ZAo05W8KXdSLM9afYCNGogNRV2N5a6aB4dQI3LXz%2Fh0%3D" \
  --output table
  
3. Download a Blob

az storage blob download \
  --account-name cryptocabanaf5scjagc \
  --container-name vault \
  --name "<blob-name>" \
  --sas-token "sv=2022-11-02&ss=b&srt=sco&sp=rl&se=2099-12-31T23:59:59Z&st=2024-01-01T00:00:00Z&spr=https&sig=ZAo05W8KXdSLM9afYCNGogNRV2N5a6aB4dQI3LXz%2Fh0%3D" \
  --file vaultfile
  
View the downloaded file:
cat vaultfile

1. Authenticate with Service Principal

az login --service-principal \
  --username <client_id> \
  --password '<client_secret>' \
  --tenant 8f8c5f8e-42d3-4ceb-97ad-241bbf446d6c
  
2. List Secrets

az keyvault secret list \
  --vault-name ccabana-kv-f5scjagc \
  --output table
  
3. Read a Secret

az keyvault secret show \
  --vault-name ccabana-kv-f5scjagc \
  --name "<secret-name>" \
  --query value -o tsv
  
4. List Versions of a Secret

az keyvault secret list-versions \
  --vault-name ccabana-kv-f5scjagc \
  --name "key-shard-2" \
  --query "[].id" -o tsv
  
5. Read a Specific Version

az keyvault secret show \
  --vault-name ccabana-kv-f5scjagc \
  --name "key-shard-2" \
  --version "3d6492d2c6f74123bc754a9ded22b2a0" \
  --query value -o tsv
  

