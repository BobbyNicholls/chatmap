resource "google_compute_instance" "app" {
  name         = "app"
  machine_type = "e2-medium"
  zone         = "europe-west2"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.app-subnet.name
    access_config { }  
  }

  metadata = {
    ssh-keys = "webadmin:${file("~/.ssh/id_rsa.pub")}"
  } 
}

resource "google_compute_address" "app-ip" {
  name   = "app-internal-ip"
}
