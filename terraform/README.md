# Terraform Configuration

This directory contains Terraform configuration for deploying the Task Manager application to AWS.

## Important Note

**This is a demo configuration for Carbonara analysis purposes.** The infrastructure is intentionally configured to deploy to a high-carbon region (us-east-1) so that the Carbonara tool can detect and recommend optimization opportunities.

## Carbon Impact

- **Current Region**: `us-east-1` (Virginia, USA)
- **Carbon Intensity**: ~400 gCO2/kWh
- **Recommended Region**: `eu-north-1` (Stockholm, Sweden)
- **Recommended Carbon Intensity**: ~45 gCO2/kWh
- **Potential Reduction**: ~89%

## Resources Defined

1. **VPC** - Virtual Private Cloud for network isolation
2. **Lambda Function** - Python 3.11 runtime for the FastAPI application
3. **RDS PostgreSQL** - Database instance (db.t3.micro)
4. **API Gateway** - HTTP API for Lambda access
5. **Security Groups** - Network security rules
6. **IAM Roles** - Permissions for Lambda execution

## Note on lambda_function.zip

The `lambda_function.zip` file referenced in this configuration is a placeholder. In a real deployment, you would:

1. Package your FastAPI application
2. Include all dependencies
3. Create a Lambda handler
4. Upload to S3 or provide the zip file

For this demo, the Terraform file structure is what matters for Carbonara analysis, not the actual deployment.

## Running Carbonara Analysis

To analyze this infrastructure with Carbonara:

1. Open this project in VSCode with the Carbonara extension installed
2. Run the deployment analysis feature
3. Carbonara will detect the high-carbon region and suggest alternatives

## If You Want to Actually Deploy

**Warning**: This will create real AWS resources and incur costs!

```bash
# Create a dummy lambda package (for terraform validation only)
cd terraform
echo '{}' > handler.py
zip lambda_function.zip handler.py

# Initialize Terraform
terraform init

# Plan the deployment
terraform plan

# Apply (creates real resources - costs money!)
terraform apply
```

## Cleanup

```bash
terraform destroy
```

## Carbon-Optimized Alternative

To deploy to a low-carbon region, change line 22 in `main.tf`:

```hcl
# Change from:
provider "aws" {
  region = "us-east-1"
}

# To:
provider "aws" {
  region = "eu-north-1"  # Stockholm, Sweden - low carbon
}
```
