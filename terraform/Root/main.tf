terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.45.0"            # means any version equal & above
    }
  }
}

provider "aws" {
  # Configuration options
  region = var.region#"us-east-1"
  profile = "default"
  access_key = "" # Not recommended to hardcode
  secret_key = "" # Not recommended to hardcode
}

#Creation Deatils of VPC
#new commit
module "vpc" {
    source = "../modules/VPC"
    # region = var.region
    # vpc_name= var.vpc.name  #not sure of the variable mentioned here , Double check
    vpc_cidr   = var.vpc_cidr
    project_name = var.project_name
    pub_sub_1a_cidr = var.pub_sub_1a_cidr
    pub_sub_1b_cidr = var.pub_sub_1b_cidr
    pri_sub_1st = var.pri_sub_1st
    pri_sub_2nd = var.pri_sub_2nd 
  
}


#Here module.vpc.<variable> = mean, we are taking vlaues from the output of VPC module & using thoes in NAT-GATEWAY module as input.
# in this module.vpc.<variable> = .<variable> , is the variable declared also in ./Nat-Gateway/variable.tf

# #Create NAT-Gateway
module "Nat_Gateway" {
    source = "../modules/Nat-Gateway"


    vpc_id = module.vpc.vpc_id
    internet_gateway = module.vpc.internet_gateway
    pub_sub_1a_id = module.vpc.pub_sub_1a_id
    pub_sub_1b_id = module.vpc.pub_sub_1b_id
    pri_sub_1st_id = module.vpc.pri_sub_1st_id
    pri_sub_2nd_id = module.vpc.pri_sub_2nd_id
    
}

module "security-group" {
    source = "../modules/security-group"
    vpc_id = module.vpc.vpc_id
    project_name = var.project_name
}

module "EC2-Keypair" {
  
    source = "../modules/EC2-Keypair"
    project_name = var.project_name
}





/*module "ASG_fe" {
    source = "../modules/ASG_fe"
    project_name = module.vpc.project_name
    pub_sub_1a_id = module.vpc.pub_sub_1a_id
    pub_sub_1b_id = module.vpc.pub_sub_1b_id
    ec2_public_sg_id = module.security-group.ec2_public_sg_id
    alb_tg_arn_fe =  module.ALB_fe.alb_tg_arn_fe
    key_name = module.EC2-Keypair.key_name
    desired_cap = var.desired_cap
    min_size = var.min_size
    max_size = var.max_size
    instance_type = var.instance_type
    ami = var.ami
    asg_health_check_type = var.asg_health_check_type

}*/

# module "ASG_be" {
#     source = "../ASG_be"
#     project_name = module.vpc.project_name
#     pub_sub_1a_id = module.vpc.pub_sub_1a_id
#     pub_sub_1b_id = module.vpc.pub_sub_1b_id
#     ec2_public_sg_id = module.security-group.ec2_public_sg_id
#     alb_tg_arn_be = module.ALB_be.alb_tg_arn_be
#     desired_cap = var.desired_cap
#     min_size = var.min_size
#     max_size = var.max_size
#     instance_type = var.instance_type
#     ami = var.ami
#     asg_health_check_type = var.asg_health_check_type
  
# }

module "iam_user" {
    source = "../modules/1IAM-User-access-PublicEC2"
    project_name = module.vpc.project_name
    iam_user1 = var.iam_user_name
}

#will install DB on these EC2 using Ansible
/*module "ec2_instance_in_private_subnet" {
    source = ".."
    instance_type = var.instance_type
    key_name = module.EC2-Keypair.key_name
    ami = var.ami
    pri_sub_1st_id = module.vpc.pri_sub_1st_id
    pri_sub_2nd_id = module.vpc.pri_sub_2nd_id
    ec2_private_sg_id = module.security-group.ec2_private_sg_id
    project_name = var.project_name
    pub_sub_1a_id = module.vpc.pub_sub_1a_id
    ec2_public_sg_id = module.security-group.ec2_public_sg_id
  
}*/

module "EC2_Instances" {
    source = "../modules/EC2-Instance"
    key_name = module.EC2-Keypair.key_name
    ami = var.ami
    instance_type = var.instance_type
    ec2_public_sg_id = module.security-group.ec2_public_sg_id
    project_name = var.project_name
    pub_sub_1a_id = module.vpc.pub_sub_1a_id
    pub_sub_1b_id = module.vpc.pub_sub_1b_id
  
}

module "ALB_fe" {
    source = "../modules/ALB_fe"
    project_name      = module.vpc.project_name
    pub_sub_1a_id     = module.vpc.pub_sub_1a_id
    pub_sub_1b_id     = module.vpc.pub_sub_1b_id
    ec2_public_sg_id  = module.security-group.ec2_public_sg_id
    vpc_id            = module.vpc.vpc_id
    webserver_fe_AZ1_id = module.EC2_Instances.webserver_fe_AZ1_id
    webserver_fe_AZ2_id = module.EC2_Instances.webserver_fe_AZ2_id
}

module "ALB_be" {
    source = "../modules/ALB_be"
    project_name = module.vpc.project_name
    pub_sub_1a_id     = module.vpc.pub_sub_1a_id
    pub_sub_1b_id     = module.vpc.pub_sub_1b_id
    ec2_public_sg_id  = module.security-group.ec2_public_sg_id
    vpc_id            = module.vpc.vpc_id
    webserver_be_AZ1_id = module.EC2_Instances.webserver_be_AZ1_id
    webserver_be_AZ2_id = module.EC2_Instances.webserver_be_AZ2_id
}
