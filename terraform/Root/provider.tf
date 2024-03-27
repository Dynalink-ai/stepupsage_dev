terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.11.0"            # means any version equal & above
    }
  }
}

provider "aws" {
  # Configuration options
  region = var.region#"us-east-1"
  profile = "default"
  access_key = "AKIAU6GDVZE3CAEDBJ2D" # Not recommended to hardcode
  secret_key = "cjloRBaI+VUiwR8qLUGC4N6LRMHg0HpEvooDgf8J" # Not recommended to hardcode
}


/*provider "aws" {
  region     = "us-west-2" # Specify your preferred region
  access_key = "your_access_key_here" # Not recommended to hardcode
  secret_key = "your_secret_key_here" # Not recommended to hardcode
}*/

