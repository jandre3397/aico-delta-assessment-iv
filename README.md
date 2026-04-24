
# Assessment IV – Internal ML Platform Delivery

## Scenario

This project follows Scenario 1: ML Platform. The platform supports three internal business units:

- Fraud Detection Team
- Recommendations Team
- Forecasting Team

Each team has its own FastAPI service deployed to Amazon EKS. Each service exposes `/health`, `/ready`, and `/predict` endpoints and routes to a SageMaker endpoint through Kubernetes environment variables.

## Architecture

```text
Streamlit Dashboard
        |
        v
Amazon EKS Cluster
 ├── fraud namespace
 │    └── fraud-api -> SageMaker endpoint
 ├── recommendations namespace
 │    └── recommendations-api -> recommendations-endpoint-v1
 └── forecasting namespace
      └── forecasting-api -> forecasting-endpoint-v1
````

## Technologies

* AWS SageMaker
* FastAPI
* Docker
* Amazon ECR
* Amazon EKS
* Kubernetes
* Terraform
* GitHub Actions
* Streamlit Dashboard

## Project Structure

```text
assessment-iv-ml-platform/
├── services/
│   ├── fraud-detection/
│   ├── recommendations/
│   └── forecasting/
├── k8s/
│   ├── fraud/
│   ├── recommendations/
│   └── forecasting/
├── dashboard/
├── terraform/
├── .github/workflows/
└── README.md
```

## Kubernetes Namespaces

* `fraud`
* `recommendations`
* `forecasting`

## Deployment Verification

```bash
kubectl get pods -n fraud
kubectl get pods -n recommendations
kubectl get pods -n forecasting
```

## Service Verification

```bash
kubectl get svc -n fraud
kubectl get svc -n recommendations
kubectl get svc -n forecasting
```

## Endpoint Routing Verification

```bash
kubectl exec -n recommendations deployment/recommendations-api -- printenv ENDPOINT_NAME
kubectl exec -n forecasting deployment/forecasting-api -- printenv ENDPOINT_NAME
```

## Dashboard

Run port-forwarding in three terminals:

```bash
kubectl port-forward -n fraud svc/fraud-service 8001:80
kubectl port-forward -n recommendations svc/recommendations-service 8002:80
kubectl port-forward -n forecasting svc/forecasting-service 8003:80
```

Then run:

```bash
streamlit run dashboard/app.py
```

## Terraform Lifecycle

```bash
cd terraform
terraform init
terraform plan
terraform apply
terraform destroy
```

This project uses the existing class EKS cluster named `k8s-training-cluster`.

## CI/CD

The GitHub Actions workflow in `.github/workflows/deploy.yml` connects to EKS, applies Kubernetes manifests, and verifies pod status.

## Teardown

```bash
kubectl delete namespace fraud
kubectl delete namespace recommendations
kubectl delete namespace forecasting
```

