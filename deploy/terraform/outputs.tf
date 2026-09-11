output "demo_host" {
  description = "Stable address of the demo, use this for DNS and the DEMO_HOST repository variable in GitHub"
  value       = digitalocean_reserved_ip.demo.ip_address
}

output "demo_url" {
  description = "Where the demo is reachable once cloud-init has finished"
  value       = "http://${digitalocean_reserved_ip.demo.ip_address}/"
}

output "droplet_ip" {
  description = "The droplet's own address, changes if it is ever rebuilt"
  value       = digitalocean_droplet.demo.ipv4_address
}

output "project_name" {
  description = "DigitalOcean project holding the demo resources"
  value       = digitalocean_project.demo.name
}
