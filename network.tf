# Main Network
resource "google_compute_network" "vpc" {
  name                    = "chatmap-net"
  auto_create_subnetworks = "false"
  routing_mode            = "GLOBAL"
}


# Firewall
resource "google_compute_firewall" "allow-internal" {
  name    = "chatmap-fw-allow-internal"
  network = "${google_compute_network.vpc.name}"
  allow {
    protocol = "icmp"
  }
  allow {
    protocol = "tcp"
    ports    = ["0-65535"]
  }
  allow {
    protocol = "udp"
    ports    = ["0-65535"]
  }
  source_ranges = [
    "${var.uc1_private_subnet}",
    "${var.ue1_private_subnet}",
    "${var.uc1_public_subnet}",
    "${var.ue1_public_subnet}"
  ]
}

resource "google_compute_firewall" "allow-http" {
  name    = "chatmap-fw-allow-http"
  network = "${google_compute_network.vpc.name}"
  allow {
    protocol = "tcp"
    ports    = ["80"]
  }
  target_tags = ["http"]
  source_ranges = ["0.0.0.0/0"] # Allows HTTP traffic from anywhere
  source_tags = ["web']
}

resource "google_compute_firewall" "allow-bastion" {
  name    = "chatmap-fw-allow-bastion"
  network = "${google_compute_network.vpc.name}"
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
  target_tags = ["ssh"]
  source_ranges = ["81.156.247.86/32"]
}


# Subnetworks
resource "google_compute_subnetwork" "public_subnet" {
  name          = "chatmap-pub-net"
  ip_cidr_range = "${var.uc1_public_subnet}"
  network       = "${google_compute_network.vpc.name}"
  region        = "europe-west2"
}
resource "google_compute_subnetwork" "private_subnet" {
  name          = "chatmap-pri-net"
  ip_cidr_range = "${var.uc1_private_subnet}"
  network       = "${google_compute_network.vpc.name}"
  region        = "europe-west2"
}
