Yes. Do these in order.

## 1. Show your frontend/dashboard

From project root:

```bash
cd ~/assessment-iv-ml-platform
streamlit run dashboard/app.py
```

If that file does not exist yet:

```bash
touch dashboard/app.py
```

Paste this:

```python
import streamlit as st
import requests

st.set_page_config(page_title="Internal ML Platform Dashboard", layout="wide")

st.title("Internal ML Platform Dashboard")
st.write("Operational visibility for Fraud Detection, Recommendations, and Forecasting services.")

services = {
    "Fraud Detection": "http://localhost:8001/health",
    "Recommendations": "http://localhost:8002/health",
    "Forecasting": "http://localhost:8003/health",
}

cols = st.columns(3)

for col, (name, url) in zip(cols, services.items()):
    with col:
        st.subheader(name)
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                st.success("Healthy")
                st.json(response.json())
            else:
                st.error(f"Error: {response.status_code}")
        except Exception as e:
            st.warning(f"Unreachable: {e}")
```

Before running Streamlit, make sure your 3 port-forwards are open:

```bash
kubectl port-forward -n fraud svc/fraud-service 8001:80
kubectl port-forward -n recommendations svc/recommendations-service 8002:80
kubectl port-forward -n forecasting svc/forecasting-service 8003:80
```

Open each in a separate terminal.

---

## 2. Read-and-click presentation script

Say this while clicking:

“First, this is my internal ML platform dashboard. It is designed for a platform engineering team supporting three internal business units: fraud detection, recommendations, and forecasting. Each card shows the service health, team name, model version, and request count.”

Click/point to each card.

“For the backend, each business unit has its own FastAPI service deployed in EKS. Each service exposes `/health`, `/ready`, and `/predict`, which satisfies the platform health and inference requirements.”

Switch to terminal.

“Here I’m showing the Kubernetes namespaces and pods.”

Run:

```bash
kubectl get pods -n fraud
kubectl get pods -n recommendations
kubectl get pods -n forecasting
```

Say:

“All three services are running successfully in separate namespaces.”

Run:

```bash
kubectl exec -n recommendations deployment/recommendations-api -- printenv ENDPOINT_NAME
kubectl exec -n forecasting deployment/forecasting-api -- printenv ENDPOINT_NAME
```

Say:

“This shows explicit routing. Recommendations routes to `recommendations-endpoint-v1`, and forecasting routes to `forecasting-endpoint-v1`.”

Run your prediction commands if needed.

Say:

“The prediction response confirms the FastAPI service is invoking SageMaker and returning a model prediction.”

Then show:

```bash
terraform output
```

Say:

“Terraform documents the shared infrastructure values, including the class EKS cluster.”

Then show GitHub Actions file.

Say:

“The GitHub Actions workflow connects to EKS, applies Kubernetes manifests, and verifies the deployments.”

---

## 3. Create README.md now

From project root:

```bash
cd ~/assessment-iv-ml-platform
touch README.md
```

Paste this:

````md
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

