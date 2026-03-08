$ErrorActionPreference = "Stop"

Write-Host "==> docker compose up -d" -ForegroundColor Cyan
docker compose up -d

Write-Host "==> wait for db healthy" -ForegroundColor Cyan
$tries = 60
for ($i=1; $i -le $tries; $i++) {
  $status = (docker inspect -f "{{.State.Health.Status}}" project-db-1 2>$null)
  if ($status -eq "healthy") { break }
  Start-Sleep -Seconds 1
}
$status = (docker inspect -f "{{.State.Health.Status}}" project-db-1 2>$null)
if ($status -ne "healthy") {
  docker compose ps
  docker logs project-db-1 --tail 200
  throw "DB not healthy (status=$status)"
}

Write-Host "==> run pytest" -ForegroundColor Cyan
$env:PYTHONPATH="."
pytest -q tests/test_task.py tests/test_task_patch.py

Write-Host ""
Write-Host "Swagger UI: http://127.0.0.1:5000/docs" -ForegroundColor Green