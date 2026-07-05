# Troubleshooting

## Dependencies Not Found

If `dockerforge analyze` misclassifies a third-party dependency as a local dependency, ensure that your virtual environment is active. DockerForge uses `importlib.util.find_spec` to verify the origin of packages. If the package isn't installed in the environment where DockerForge is running, it may misclassify it.

## Build Remediation Fails

If `dockerforge remediate` states "No remediation needed" but your build failed, it means the failure signature is not yet present in `src/dockerforge/remediation/patterns.py`. Please [open an issue](../.github/ISSUE_TEMPLATE/bug_report.md) with the build logs so we can add the pattern!
