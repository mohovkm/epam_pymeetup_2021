# Multicloud development. Azure functions / AWS lamda

### Steps to deploy:

1. Install NodeJS and NPM
2. Install [Serverless framework](https://www.serverless.com/)
```bash
npm install -g serverless
```
3. Setup AWS credentials [Link](https://www.serverless.com/framework/docs/providers/aws/guide/credentials/)
4. Setup Azure credentials [Link](https://www.serverless.com/framework/docs/providers/azure/guide/credentials/)
5. Install serverless plugins:
    - (Python requirements)[https://www.serverless.com/plugins/serverless-python-requirements]
    - (Azure functions)[https://www.serverless.com/plugins/serverless-azure-functions]

Due to bug in serverless framework installation with templated serverless.yml will not work, so we 
need to swap it with simple yml file, install requirements and swap back:
```bash
mv serverless.yml serverless.yml.bak
mv serverless_to_install_plugins.yml serverless.yml

sls plugin install -n serverless-python-requirements
sls plugin install -n serverless-azure-functions

mv serverless.yml serverless_to_install_plugins.yml
mv serverless.yml.bak serverless.yml
```

6. Deploy to Azure
```bash
SLS_PROVIDER=azure sls deploy
```

7. Deploy to AWS
```bash
SLS_PROVIDER=aws sls deploy
```
