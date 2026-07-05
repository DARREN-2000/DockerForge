# Deployment

DockerForge is primarily a CLI tool meant to run locally or inside CI/CD pipelines to assist in preparing your codebase for deployment.

Once DockerForge generates your Dockerfile and verifies the build succeeds via the `build` or `remediate` commands, the resulting Docker image is standard and can be pushed to any registry (e.g., Docker Hub, AWS ECR, GCP GCR) and deployed to any container orchestration platform (e.g., Kubernetes, ECS, Cloud Run).
