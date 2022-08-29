# GCP deploy infra as code
This is a project deploying infrastructure as code with terraform. Airflow and GCP-Bigquery are used to check that both local and cloud environments are connected and working.
## Setup GCP
### Get keys
The keys are needed to validate your user and its permissions. To connect your local instance to the GCP account you need to create a service user with basic permissions and BigQuery Data Editor, Storage Admin and Storage Object Admin. Keep in mind these are not the best settings for a real production setup but are quick enough to deploy this test. You can download the keys from the IAM/Service Account section into **~/.google/credentials/** with **google_credentials.json** name and export this variable as  **GOOGLE_APPLICATION_CREDENTIALS**
### Connect to GCP
Install the Google CLI to connect your device with the GCP account. You can find instructions in: https://cloud.google.com/sdk/docs/install
After installation you can validate your device with: `gcloud auth application-default login`  and enable the APIs using the following two links:
1. https://console.cloud.google.com/apis/library/iam.googleapis.com
2. https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com
 
After enabling the keys you already have access to the GCP account.
 
### Deploy Infrastructure as code
Installing Terraform will allow the deployment of the Google Storage and Google Bigquery services as code. Terraform can be installed from: https://learn.hashicorp.com/tutorials/terraform/install-cli
To deploy the services a `.terraform-version`, `main.tf` and `variables.tf` files are needed. Don't forget to update the `variables.tf` with your own settings.
The `main.tf` will list your cloud provider and the services.
Commands to deploy:
1. `terraform init`: Initialise configuration.
2. `terraform plan`: Shows configuration.
3. `terraform apply`: Deploy Infrastructure.
4. `terraform destroy`: Delete Infrastructure.
 
## Test
### Running local Airflow ETL to access cloud service.
To test the permissions a file will be downloaded from Github and exported into BigQuery. Airflow will be deployed with the official Docker image from `'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'` You will need to add the environmental settings matching your own account.
Image deployment:
* docker-compose build
* docker-compose up
Once the containers are up and running, last one to depoy is: `airflow-webserver_1`, you can log in to http://localhost:8080/ with the username and password `airflow`. Once logged in you can execute the dag `etl_git_bigquery` to do the ETL. After the ETL is finished you will see the data in the Bigquery.
 
## Known Issues
Showing login details in plain text is bad practice.
 
 
 


