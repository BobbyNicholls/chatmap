resource "google_compute_instance" "app" {
  name         = "app"
  machine_type = "e2-highmem-4"
  zone         = "europe-west2-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
      size  = 50
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.public_subnet.name
    access_config { }  
  }

  tags = ["ssh", "http-server", "https-server", "web", "http"]

#  metadata = {
#    ssh-keys = "webadmin:${file("~/.ssh/id_rsa.pub")}"
#  } 
}

resource "google_compute_address" "app-ip" {
  name   = "app-internal-ip"
}
