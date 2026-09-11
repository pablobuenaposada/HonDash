terraform {
  required_version = "~> 1.5"

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.34"
    }
  }

  # State is kept locally, in deploy/terraform/terraform.tfstate (gitignored).
  # The droplet is created once from your machine and then never touched by CI,
  # which only ever redeploys onto the existing box, so there is nothing to
  # share and no object storage to pay for. Back the state file up; see
  # ../README.md.
}

provider "digitalocean" {
  token = var.do_token
}
