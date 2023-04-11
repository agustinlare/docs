resource "onepassword_item" "test" {
  vault    = "devops"
  category = "document"
  title    = "1p-test"
}

terraform {
  required_providers {
    onepassword = {
      source  = "1Password/onepassword"
      version = "~> 1.0.1"
    }
  }
}

provider "onepassword" {
  url = "https://clavellc.1password.com"
  token = file("api-token.secret")
}