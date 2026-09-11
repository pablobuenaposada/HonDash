output "demo_host" {
  description = "Public IPv4 of the droplet, set this as the DEMO_HOST repository variable in GitHub"
  value       = digitalocean_droplet.demo.ipv4_address
}

output "demo_url" {
  description = "Where the demo is reachable once cloud-init has finished"
  value       = "http://${digitalocean_droplet.demo.ipv4_address}/"
}

output "project_name" {
  description = "DigitalOcean project holding the droplet"
  value       = digitalocean_project.demo.name
}
