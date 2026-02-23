$Region = "ap-south-1"
$Timestamp = Get-Date -Format "yyyyMMddHHmmss"
$BucketName = "wasim-anthos-tf-state-prod-$Timestamp"
$DynamoDbTable = "terraform-state-locks"

Write-Host "Starting Terraform Backend Bootstrap in $Region..." -ForegroundColor Cyan

# 1. Create the S3 Bucket
Write-Host "Creating S3 bucket: $BucketName..."
aws s3api create-bucket --bucket $BucketName --region $Region --create-bucket-configuration LocationConstraint=$Region

# 2. Enable Bucket Versioning
Write-Host "Enabling versioning..."
aws s3api put-bucket-versioning --bucket $BucketName --versioning-configuration Status=Enabled

# 3. Create DynamoDB Table
Write-Host "Creating DynamoDB table: $DynamoDbTable..."
aws dynamodb create-table --table-name $DynamoDbTable --attribute-definitions AttributeName=LockID,AttributeType=S --key-schema AttributeName=LockID,KeyType=HASH --billing-mode PAY_PER_REQUEST --region $Region

Write-Host "=================================================" -ForegroundColor Green
Write-Host "✅ Backend Provisioned!" -ForegroundColor Green
Write-Host "Bucket Name: $BucketName" -ForegroundColor Yellow
Write-Host "=================================================" -ForegroundColor Green