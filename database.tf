resource "google_sql_database_instance" "main-db" {
  name             = "main-db"
  database_version = "POSTGRES_13"
  region           = "europe-west2"

  settings {
    tier = "db-f1-micro" 
  }
}

resource "google_sql_database" "app-data" {
  name     = "app-data"
  instance = google_sql_database_instance.main-db.name
}
