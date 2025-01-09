resource "google_compute_instance" "app" {
  name         = "app"
  machine_type = "e2-medium"
  zone         = "europe-west2-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.public_subnet.name
    access_config { }  
  }

  tags = ["ssh", "http-server", "https-server", "web"]

#  metadata = {
#    ssh-keys = "webadmin:${file("~/.ssh/id_rsa.pub")}"
#  } 
}

resource "google_compute_address" "app-ip" {
  name   = "app-internal-ip"
}
