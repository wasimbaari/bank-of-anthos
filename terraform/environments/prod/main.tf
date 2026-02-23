module "network" {
  source              = "../../modules/network"
  environment         = var.environment
  vpc_cidr            = var.vpc_cidr
  public_subnet_cidrs = var.public_subnet_cidrs
  availability_zones  = var.availability_zones
}

module "security" {
  source      = "../../modules/security"
  environment = var.environment
  github_repo = var.github_repo
  vpc_id      = module.network.vpc_id
}

module "compute" {
  source      = "../../modules/compute"
  environment = var.environment
  vpc_id      = module.network.vpc_id
  # This must match the output name 'public_subnets' in the network module
  subnet_ids        = module.network.public_subnets
  key_name          = var.key_name
  eks_instance_type = var.eks_instance_type
}