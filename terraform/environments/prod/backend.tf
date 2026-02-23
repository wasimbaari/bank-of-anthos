terraform {
  backend "s3" {
    bucket         = "wasim-anthos-tf-state-prod-20260223103909"
    key            = "prod/infrastructure/terraform.tfstate"
    region         = "ap-south-1"
    encrypt        = true
    dynamodb_table = "terraform-state-locks"
  }
}