# Maintenance Workflow

1. Start from clean `main` and create a branch.
2. Run `git status`, `git ls-files`, dependency audits, and relevant tests.
3. Make small scoped changes.
4. Update docs beside behavior changes.
5. Run backend, frontend, E2E, Docker, and research checks when touched.
6. Secret-scan staged changes before pushing.
7. Push the branch, open a pull request, wait for CI, then merge without force-pushing.
8. Tag releases only from clean, verified `main`.
