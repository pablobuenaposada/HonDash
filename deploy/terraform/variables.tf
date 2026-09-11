variable "do_token" {
  description = "DigitalOcean personal access token with read/write scope"
  type        = string
  sensitive   = true
}

variable "ssh_key_names" {
  description = "Names of SSH keys already uploaded to the DigitalOcean account that may log into the droplet"
  type        = list(string)
}

variable "region" {
  description = "DigitalOcean region slug, e.g. fra1, ams3, nyc3"
  type        = string
  default     = "fra1"
}

variable "droplet_size" {
  description = "Droplet size slug. The stack only needs about 100MB of RAM, so the 512mb box would also fit; 1gb is chosen for headroom during the frontend build, since these droplets have no swap"
  type        = string
  default     = "s-1vcpu-1gb"
}

variable "droplet_image" {
  description = "Droplet base image slug"
  type        = string
  default     = "ubuntu-24-04-x64"
}

variable "name" {
  description = "Name used for the droplet and its related resources"
  type        = string
  default     = "hondash-demo"
}

variable "repo_url" {
  description = "Repository cloned onto the droplet to get the compose file, nginx config and json schema"
  type        = string
  default     = "https://github.com/pablobuenaposada/HonDash.git"
}

variable "repo_branch" {
  description = "Branch of repo_url to deploy"
  type        = string
  default     = "master"
}

variable "ssh_allowed_cidrs" {
  description = "Who may reach port 22. Defaults to the whole internet; narrow it to your own address if you can"
  type        = list(string)
  default     = ["0.0.0.0/0", "::/0"]
}

variable "project_name" {
  description = "Name of the DigitalOcean project terraform creates to hold the demo resources. Terraform always creates this, it does not adopt a project you made by hand"
  type        = string
  default     = "HonDash demo"
}

variable "project_description" {
  description = "Description shown on the DigitalOcean project"
  type        = string
  default     = "Public HonDash dashboard demo running on fake ECU data"
}

variable "project_environment" {
  description = "One of Development, Staging or Production"
  type        = string
  default     = "Production"

  validation {
    condition     = contains(["Development", "Staging", "Production"], var.project_environment)
    error_message = "project_environment must be Development, Staging or Production."
  }
}
