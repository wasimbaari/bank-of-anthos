variable "aws_region" {}
variable "environment" {}
variable "vpc_cidr" {}
variable "public_subnet_cidrs" { type = list(string) }
variable "availability_zones" { type = list(string) }
variable "github_repo" {}
variable "key_name" {}

# Updated naming
variable "eks_instance_type" {
  description = "The EC2 instance type for the EKS managed node group"
  type        = string
  default     = "m7i-flex.large"
}