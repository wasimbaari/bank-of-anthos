module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "${var.environment}-bank-cluster"
  cluster_version = "1.31"

  vpc_id                   = var.vpc_id
  subnet_ids               = var.subnet_ids
  control_plane_subnet_ids = var.subnet_ids

  cluster_endpoint_public_access           = true
  enable_cluster_creator_admin_permissions = true

  eks_managed_node_groups = {
    main = {
      # Use the updated variable name here
      instance_types = [var.eks_instance_type]
      min_size       = 1
      max_size       = 3
      desired_size   = 2
      key_name       = var.key_name
    }
  }
}