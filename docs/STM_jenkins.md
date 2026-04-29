# STM Jenkins Demo Notes

## Goal:Build a minimal Jenkins demo that can fetch the repository, execute shell commands, run pytest, and show logs for troubleshooting.
## Minimum Success Criteria
Jenkins can fetch the github responsurtory successfully. 
Jenkins can execute the shell commands in the workspace.
Jenkins can trigger pytest.
Console logs are visible.
A short demo note is completed.

## Trigger
Manual run whe demo purpose.
Future extension:push/pull request style CI trigger.

## Pipeline Overview
This pipeline demonstrates a minimal CI flow from source to enviroment setup,enviroment validation,test execution,failure log collection.

## Stages
Checkout 
Setup Environment 
Install Dependencies 
Prepare Database 
Run Tests 
Failure Handling 

### Checkout
- Purpose:GitHub 抓取 repo，確認 Jenkins 能取得專案內容
- Success Criteria:
jenkins 成功從 GitHub 抓取 repo 
Jenkins workspace 中可看到正確的專案檔案結構

### Setup Environment
- Purpose:準備 Python 執行環境、依賴套件與必要環境變數
- Success Criteria:
Required system dependencies are available. 
Required environment variables are set. 
Python dependencies are installed successfully.

### Env Check
- Purpose:在執行測試前，確認 shell、Python、必要環境與基本服務可用，降低後續返工成本
- Success Criteria:
Shell commands can be executed successfully. 
Python can be called successfully. 
The database service is reachable and responds to ping.

### Run Tests
- Purpose:執行最小可行的自動化測試流程，確認 Jenkins 能成功觸發 pytest 並產生結果
- Success Criteria:
pytest is triggered successfully. 
Test output is visible in the console log.

### Dump Logs On Failure
- Purpose:在失敗時收集最小且關鍵的錯誤資訊，協助快速定位問題
- Success Criteria:
Failure logs are generated when the pipeline fails. 
The logs contain enough information to identify the main cause of failure.

## Current Progress
## Current Blockers
## Next Step