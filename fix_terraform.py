import os

def fix_project():
    # 1. Define Paths
    base_path = "terraform/environments/prod"
    modules_path = "terraform/modules"
    
    # 2. Fix Root main.tf (Ensure it's a clean orchestrator)
    main_tf_path = os.path.join(base_path, "main.tf")
    main_tf_content = """module "network" {
  source              = "../../modules/network"
  environment         = var.environment
  vpc_cidr            = var.vpc_cidr
  public_subnet_cidrs = var.public_subnet_cidrs
  availability_zones  = var.availability_zones
}

module "security" {
  source      = "../../modules/security"
  environment = var.environment
  vpc_id      = module.network.vpc_id
  github_repo = var.github_repo
}

module "compute" {
  source            = "../../modules/compute"
  environment       = var.environment
  vpc_id            = module.network.vpc_id
  subnet_ids        = module.network.public_subnets
  key_name          = var.key_name
  eks_instance_type = var.eks_instance_type
}
"""
    with open(main_tf_path, 'w') as f:
        f.write(main_tf_content)
    print("✅ Rewrote main.tf with valid syntax")

    # 3. Create/Fix alb_controller.tf (Valid HCL format)
    alb_path = os.path.join(modules_path, "compute/alb_controller.tf")
    alb_content = """
module "lb_role" {
  source    = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  role_name = "${var.environment}_eks_lb_controller"

  attach_load_balancer_controller_policy = true

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["kube-system:aws-load-balancer-controller"]
    }
  }
}

resource "helm_release" "alb_controller" {
  name       = "aws-load-balancer-controller"
  repository = "https://aws.github.io/eks-charts"
  chart      = "aws-load-balancer-controller"
  namespace  = "kube-system"

  set {
    name  = "clusterName"
    value = module.eks.cluster_name
  }

  set {
    name  = "serviceAccount.create"
    value = "true"
  }

  set {
    name  = "serviceAccount.name"
    value = "aws-load-balancer-controller"
  }

  set {
    name  = "serviceAccount.annotations.eks\\\\.amazonaws\\\\.com/role-arn"
    value = module.lb_role.iam_role_arn
  }

  set {
    name  = "region"
    value = "ap-south-1"
  }

  set {
    name  = "vpcId"
    value = var.vpc_id
  }
}
"""
    with open(alb_path, 'w') as f:
        f.write(alb_content)
    print("✅ Fixed alb_controller.tf syntax (No more semicolons)")

if __name__ == "__main__":
    fix_project()