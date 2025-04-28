#!/bin/bash

# Configura as credenciais da AWS
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1

# Cria o bucket no LocalStack
aws --endpoint-url=http://localstack:4566 s3 mb s3://produtos-imagens

echo "Bucket 'produtos-imagens' criado com sucesso!" 