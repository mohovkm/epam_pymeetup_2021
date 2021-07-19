echo "ATTENTION! Run this script with \"source\" command!!!"
echo "Be shure, that you have installed Azure CLI framework"
echo "You will be asked to login into your azure account in browser"

login_result=$(az login)

echo "Type email with Azure subscription: "

read az_subscription_email

if [ -z "$az_subscription_email" ]
then 
    echo "You entered wrong email. Do all these steps manually."
    echo "https://www.serverless.com/framework/docs/providers/azure/guide/credentials/"
    exit
fi

subscription_list=$(az account list)

if [ -z "$subscription_list" ]
then 
    echo "Can't find any subscriptions. Do all these steps manually."
    echo "https://www.serverless.com/framework/docs/providers/azure/guide/credentials/"
    exit
fi

subscription_id=$(az account list | jq --arg azemail "$az_subscription_email" '.[] | select(.user.name==$azemail)' | jq -r '.id')

if [ -z "$subscription_id" ]
then 
    echo "Can't find subscription id. Do all these steps manually."
    echo "https://www.serverless.com/framework/docs/providers/azure/guide/credentials/"
    exit
fi

az account set -s $subscription_id

service_principal=$(az ad sp create-for-rbac)

if [ -z "$service_principal" ]
then 
    echo "Can't create service principal. Do all these steps manually."
    echo "https://www.serverless.com/framework/docs/providers/azure/guide/credentials/"
    exit
fi

tenant_id=$(echo $service_principal | jq -r '.tenant' )
name=$(echo $service_principal | jq -r '.name' )
password=$(echo $service_principal | jq -r '.password' )

export AZURE_SUBSCRIPTION_ID=$subscription_id
export AZURE_TENANT_ID=$tenant_id
export AZURE_CLIENT_ID=$name
export AZURE_CLIENT_SECRET=$password

echo "All fine. You can use Serverless framework with Azure now"
