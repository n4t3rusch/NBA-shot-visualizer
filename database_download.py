import kagglehub

# Download latest version
path = kagglehub.dataset_download("techbaron13/nba-shots-dataset-2001-present")

print("Path to dataset files:", path)