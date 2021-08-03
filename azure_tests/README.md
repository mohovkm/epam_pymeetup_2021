# Serverless project for Azure functions

In this project we can see, how to use Azure Functions:
- AF with HTTP event
- AF to send message to the Queue
- AF to retreive message from the Queue
- AF to send notification (with SendGrid or other provider)

And mostly how to write testable stateless functions and how to test them

Install dependecies locally:
```bash
poetry install
poetry build
poetry install
```

Run tests:
```bash
poetry run pytest
```

Run offline plugin (will fail after GET requested, cause we don't have connection to the queue established):
```bash
sls offline
```

Configure your Azure Credentials step-by-step with [docs](https://www.serverless.com/framework/docs/providers/azure/guide/credentials/) or with running custom script (that do all the same steps):

```bash
.../epam_pymeetup_2021/azure_tests > chmod +x ../export_az_creds.sh 
.../epam_pymeetup_2021/azure_tests > source ../export_az_creds.sh 
```

Deploy functions in your Azure Dev environment
```bash
sls deploy
```
