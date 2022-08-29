# GCP deploy infra as code
This is sample code to deploy infrastructure as code with terraform. In this case the test is with Airflow and GCP-Bigquery to check both enviroments are 

## Setup GCP
### Get keys
The keys are needed to validate your user and it's permissions. To connecto your local instance to the GCP account you can create a service user with basic permissions, BigQuery Data Editor, Storage Admin and Storage Object Admin. Bear in mind this are not the best settings for a real production setup. You can download the keys from the IAM/Service Account section into **~/.google/credentials/** with **google_credentials.json** name and export this variable as  **GOOGLE_APPLICATION_CREDENTIALS**
### Connect to GCP
Install the Google CLI to connect your device with the account, you can find instructions in: https://cloud.google.com/sdk/docs/install 
After installation you can validate your device with: `gcloud auth application-default login`  and enable the APIs following the two below links:
1. https://console.cloud.google.com/apis/library/iam.googleapis.com
2. https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com

After enabling the keys you already have access to the cloud account.

### Deploy Infrastructure as code
Installing Terraform will allow to deploy the Google storage and Google Bigquery services as code. Terraforme can be installed from: https://learn.hashicorp.com/tutorials/terraform/install-cli 
To deploy a services a `.terraform-version`, `main.tf` and `variables.tf` are needed and don't forget to update the `variables.tf` with your own settings.
In the `main.tf` you will list your cloud provider and the services.

### Running local Airflow ETL to access cloud service.
 



