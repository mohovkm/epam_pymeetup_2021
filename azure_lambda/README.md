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

```bash
sls plugin install -n serverless-python-requirements
sls plugin install -n serverless-azure-functions
```

6. Deploy to Azure
```bash
SLS_PROVIDER=azure sls deploy
```

7. Deploy to AWS
```bash
SLS_PROVIDER=aws sls deploy
```
