import os

def fix_project():
    # 1. Define Paths
    base_path = "terraform/environments/prod"
    modules_path = "terraform/modules"
    
    # 2. Fix Root main.tf (Remove duplicate providers)
    main_tf_path = os.path.join(base_path, "main.tf")
    if os.path.exists(main_tf_path):
        with open(main_tf_path, 'r') as f:
            lines = f.readlines()
        
        # Keep only the module calls, strip provider blocks
        new_lines = []
        skip = False
        for line in lines:
            if 'provider "kubernetes"' in line or 'provider "helm"' in line:
                skip = True
            if skip and '}' in line:
                skip = False
                continue
            if not skip:
                new_lines.append(line)
        
        with open(main_tf_path, 'w') as f:
            f.writelines(new_lines)
        print("✅ Cleaned main.tf (Removed duplicate providers)")

    # 3. Create/Fix alb_controller.tf in compute module
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
  set { name = "clusterName"; value = module.eks.cluster_name }
  set { name = "serviceAccount.create"; value = "true" }
  set { name = "serviceAccount.name"; value = "aws-load-balancer-controller" }
  set { name = "serviceAccount.annotations.eks\\\\.amazonaws\\\\.com/role-arn"; value = module.lb_role.iam_role_arn }
  set { name = "region"; value = "ap-south-1" }
  set { name = "vpcId"; value = var.vpc_id }
}
"""
    with open(alb_path, 'w') as f:
        f.write(alb_content)
    print("✅ Created/Updated alb_controller.tf")

    # 4. Fix Security variables (Add missing vpc_id)
    sec_vars_path = os.path.join(modules_path, "security/variables.tf")
    sec_vars_content = """variable "environment" { type = string }
variable "github_repo" { type = string }
variable "vpc_id" { type = string }
"""
    with open(sec_vars_path, 'w') as f:
        f.write(sec_vars_content)
    print("✅ Fixed security/variables.tf")

if __name__ == "__main__":
    fix_project()