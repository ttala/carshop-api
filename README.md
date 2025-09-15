# Carshop API with Kubernetes

In this project, I built a lightweight CI/CD pipeline to deploy a FastAPI application on Kubernetes, with automated delivery managed by ArgoCD.
The application ingests a store.csv file into a PostgreSQL database, which then serves as the sample dataset for API queries.

## Prerequisites
- kubectl installed and configured
- Helm installed

## Install ArgoCD

```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
kubectl create namespace argocd
helm install argocd argo/argo-cd --namespace argocd
```

## Access ArgoCD UI

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:80
```

## Retrieve argocd Credentials

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

## ArgoCD Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: carshop-api
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/ttala/carshop-api.git
    targetRevision: main
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: carshop
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

# Create a Docker registry secret in Kubernetes
To allow Kubernetes to pull images from GitHub Container Registry.

```yaml
kubectl create secret docker-registry ghcr-secret \\
  --docker-server=ghcr.io \\
  --docker-username=YOUR_USERNAME \\
  --docker-password=YOUR_PAT \\
  --namespace=carshop
```
