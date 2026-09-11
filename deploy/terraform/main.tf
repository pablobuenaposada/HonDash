data "digitalocean_ssh_key" "keys" {
  for_each = toset(var.ssh_key_names)
  name     = each.value
}

# Keeps the droplet in its own project rather than in the account's default
# one. DigitalOcean creates every droplet in the default project and it is
# moved here afterwards, so it briefly appears there during an apply.
# Firewalls cannot belong to a project, so that one stays outside.
resource "digitalocean_project" "demo" {
  name        = var.project_name
  description = var.project_description
  purpose     = "Web Application"
  environment = var.project_environment

  resources = [
    digitalocean_droplet.demo.urn,
  ]
}

resource "digitalocean_droplet" "demo" {
  name     = var.name
  region   = var.region
  size     = var.droplet_size
  image    = var.droplet_image
  ssh_keys = [for key in data.digitalocean_ssh_key.keys : key.fingerprint]

  # Droplet metadata has a 64KiB limit, the cloud-init below is far smaller.
  user_data = templatefile("${path.module}/cloud-init.yaml.tftpl", {
    repo_url    = var.repo_url
    repo_branch = var.repo_branch
  })

  tags = [var.name]

  lifecycle {
    # user_data only runs on first boot and changing it would replace the
    # droplet, throwing away the running demo. Redeploys go through
    # deploy/deploy.sh over ssh instead, so edits to the cloud-init are
    # deliberately not a reason to rebuild the box.
    ignore_changes = [user_data]
  }
}

resource "digitalocean_firewall" "demo" {
  name        = var.name
  droplet_ids = [digitalocean_droplet.demo.id]

  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = var.ssh_allowed_cidrs
  }

  inbound_rule { # frontend
    protocol         = "tcp"
    port_range       = "80"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule { # backend websocket, the browser connects to it directly
    protocol         = "tcp"
    port_range       = "5678"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "icmp"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}
