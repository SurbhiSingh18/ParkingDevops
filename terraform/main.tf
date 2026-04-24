provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_deployment" "parking" {
  metadata {
    name = "parking-app"
    labels = {
      app = "parking-app"
    }
  }

  spec {
    replicas = 2

    selector {
      match_labels = {
        app = "parking-app"
      }
    }

    template {
      metadata {
        labels = {
          app = "parking-app"
        }
      }

      spec {
        container {
          name  = "parking-container"
          image = "shruthikeerthana/parking-flask"

          port {
            container_port = 5000
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "parking" {
  metadata {
    name = "parking-service"
  }

  spec {
    selector = {
      app = "parking-app"
    }

    port {
      port        = 80
      target_port = 5000
      node_port   = 30007
    }

    type = "NodePort"
  }
}