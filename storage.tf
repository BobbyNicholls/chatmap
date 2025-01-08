resource "google_storage_bucket" "app-assets" {
  name          = "app-assets"
  location      = "europe-west2"

  website {
    main_page_suffix = "chat.html"
  }
}
