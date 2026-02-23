aws_region          = "ap-south-1"
environment         = "prod"
vpc_cidr            = "10.0.0.0/16"
public_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
availability_zones  = ["ap-south-1a", "ap-south-1b"]
eks_instance_type   = "m7i-flex.large"
key_name            = "wasim-key pair"
github_repo         = "wasimbaari/bank-of-anthos"