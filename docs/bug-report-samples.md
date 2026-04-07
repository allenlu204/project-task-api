# Bug Report Samples
## Bug-001
Summary：Unauthorized patch attempt should not modify task metadata
Related Jira Issue：STM-11
Related Test Case：STM-TC-AUTHZ-02
Severity：High
Priority：High
Environment：Secure Task Management API test environment
Preconditions：
Owner user exist in the system.
Existed a target task belong to the owner user in the system.
Created non-owner authenticated user exist in the system.
The patch task endpoint is available, protected by authentication and also subject to authorization checks.
The access token belongs to the non-owner authenticated user.
Steps to Reproduce：
Create a owner user
Create a non-owner authenticated user
Record the updated_at.
Send a patch request to /api/v1/tasks/{task_id} with access token provided by non-owner user.
Expected Result：
request is rejected 
403 Forbidden 
the response should be JSON 
the task record remains unchanged. 
Actual Result：
Unauthorized patch attempts may still modify task metadata or update timestamps if access control is not enforced correctly.
Status：open
Notes：
This bug sample is based on ownership-based authorization testing and is intended to demonstrate defect tracking for protected resource modification.
---
## Bug-002
Summary：Authenticated user sends patch request with malformed JSON.
Related Jira Issue：STM-12
Related Test Case：STM-TC-EH-01
Severity：Medium
Priority：Medium
Environment：Secure Task Management API test environment
Preconditions：
The autheticated user exist in the system.
The target task exist in the system and belongs to the  autheticated user.
The patch task endpoint is available, protected by authentication and also subject to authorization checks.
The access token belongs to the authenticated user.
Steps to Reproduce：
Create a authenticated user.
Create a target task belongs to the autheticated user.
Prepare request payload with malformed JSON.
Send a patch request to /api/v1/tasks/{task_id} with malformed JSON to patch the task.
Get system response and check
Expected Result：
request is rejected 
system returns 400 Bad Request
error response follows standardized JSON format
Actual Result：
 Malformed JSON requests may return inconsistent error messages or a non-standardized error response format.
Status：open
Notes：
This bug sample is based on malformed JSON error-handling testing and is intended to demonstrate error response consistency tracking.