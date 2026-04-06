# Test Cases
## Test Categories
### Authentication
- no token
### Authorization
- non-owner
- user not me
### Success path
- create ok
- list ok
- patch ok
### Validation / business rule
- missing field
- invalid status
- null field
- duplicate email
- malformed / empty JSON body
### Error handling
- not found
- error response format
- global exception handling

---
## STM-TC-AUTH-01
- Test Item：Authentication
- Scenario：Valid user sends a request to create task without access token.
- Precondition：
Created valid user exist in the system.
The create task endpoint is available and protected by authentication.
No access token is included in request.
- Test step：
1.Create a valid user
2.Prepare request payload
3.Send a post request to /api/v1/users/{user_id}/tasks
4.Make request without access token
5.Get system response and check
- Test data：
User data：valid user
Task payload：valid minimal payload
Access token：not provided
- Expected result：
1.request is rejected 
2.401 Unauthorized 
3.the response should be JSON 
4.the JSON response contain an error object contain code and type 
5.message is str and non-empty
- Priority：High
- Automation status：Automated
- Related pytest file：tests/test_task.py

## STM-TC-AUTH-02
- Test Item：Authentication
- Scenario：Valid user sends a request to patch task without access token.
- Precondition：
Created valid owner user exist in the system.
Valid target task existed in the system.
The patch task endpoint is available and protected by authentication.
No access token is included in request.
- Test step：
1.Create a valid owner user
2.Create a valid target task by owner user
3.Prepare request payload
4.Send a patch request to /api/v1/users/task/{task_id} without access token
5.Get system response and check
- Test data：
User data：valid owner user
Task payload：valid minimal payload
Access token：not provided
- Expected result：
1.request is rejected 
2.401 Unauthorized 
3.the response should be JSON 
4.the JSON response contain an error object contain code and type 
5.message is str and non-empty
- Priority：High
- Automation status：Automated
- Related pytest file：tests/test_task_patch.py

## STM-TC-AUTHZ-01
- Test Item：Authorization
- Scenario：Valid user sends a request to create task using another user_id with own access token.
- Precondition：
Existed a target user in the system.
Created authenticated user exist in the system.
The create task endpoind is available, protected by authentication and also subject to authorization checks.
Access token is belong to the authenticated user.
- Test step：
1.Create a authenticated user
2.Prepare request payload with user_id by target user
3.Send a post request to /api/v1/users/{other_user_id}/tasks with access token.
4.Get system response and check
- Test data：
User data：Authenticated user data.
Target user_id：another user_id.
Task payload：valid task creation payload
Access token：provided for authenticated user
- Expected result：
1.request is rejected 
2.403 Forbidden 
3.the response should be JSON 
4.the JSON response contain an error object contain code and type 
- Priority：High
- Automation status：Automated
- Related pytest file：tests/test_task.py

## STM-TC-AUTHZ-02
- Test Item：Authorization
- Scenario：Non-owner user tries to modify other user's task.
- Precondition：
Owner user exist in the system.
Existed a target task belong to the owner user in the system.
Created non-owner authenticated user exist in the system.
The patch task endpoint is available, protected by authentication and also subject to authorization checks.
The access token belongs to the non-owner authenticated user.
- Test step：
1.Create a owner user
2.Send a post request to /api/v1/users/{owner_id}/tasks with access token to create target task.
3.Create a non-owner authenticated user
4.Prepare request payload by non-owner authenticated user
5.Record the updated_at.
5.Send a patch request to /api/v1/tasks/{task_id} with access token provided by non-owner user.
6.Get system response and check
- Test data：
User data：
owner authenticated user data.
non owner authenticated user data.
Task data：existing task data.
Task payload：valid task patch payload.
Access token：provided for non-owner authenticated user
- Expected result：
1.request is rejected 
2.403 Forbidden 
3.the response should be JSON 
4.the task record remains unchanged. 
- Priority：High
- Automation status：Automated
- Related pytest file：tests/test_task_patch.py

## STM-TC-VL-01
- Test Item：Validation
- Scenario：Authenticated user sends patch request without valid status value.
- Precondition：
The autheticated user exist in the system.
The target task exist in the system and belongs to the  authenticated user.
The patch task endpoint is available, protected by authentication and also subject to authorization checks.
The access token belongs to the authenticated user.
- Test step：
1.Create a authenticated user.
1.Create a target task belongs to the authenticated user.
2.Prepare request payload with invalid status value.
3.Send a patch request to /api/v1/tasks/{task_id} with invalid status value to patch the task.
4.Get system response and check
- Test data：
User data：
The authenticated user data.
Task payload：
The target task payload.
Task patch payload without valid status.
Access token：Provided for authenticated user.
- Expected result：
1.request is rejected 
2.system returns 400 Bad Request
- Priority：Medium
- Automation status：Automated
- Related pytest file：tests/test_task_patch.py

## ID：STM-TC-SC-01
- Test Item：Success
- Scenario：Authenticated user sends post request with valid payload to create a task.
- Precondition：
The autheticated user exist in the system.
The create task endpoint is available, protected by authentication and also subject to authorization checks.
The access token belongs to the authenticated user.
- Test step：
1.Create a authenticated user.
2.Prepare request payload with valid status value.
3.Send a post request to /api/v1/users/{user_id}/tasks with valid status value to create the task.
4.Get system response and check
- Test data：
User data：
The authenticated user data.
Task payload：
The target task payload.
Task task payload with valid status.
Access token：Provided for authenticated user.
- Expected result：
1.request is accepted 
2.system returns 201 Created
3.response contains correct task data(title, status, owner_id)
- Priority：Medium
- Automation status：Automated
- Related pytest file：tests/test_task.py
## STM-TC-SC-02
- Test Item：Success
- Scenario：Authenticated user sends a patch request to update their own task with valid payload.
- Precondition：
The autheticated user exist in the system.
The target task exist in the system and belongs to the  authenticated user.
The patch task endpoint is available, protected by authentication and also subject to authorization checks.
The access token belongs to the authenticated user.
- Test step：
1.Create a authenticated user.
2.Create a target task belongs to the autheticated user.
3.Prepare request payload with valid status value.
4.Send a patch request to /api/v1/tasks/{task_id} with invalid status value to patch the task.
5.Verify the response.
- Test data：
User data：
The authenticated user data.
Task payload：
The target task payload.
Task patch payload with valid status.
Access token：Provided for authenticated user.
- Expected result：
1.request is accepted 
2.system returns 200 
3.the task is update correctly
- Priority：Medium
- Automation status：Automated
- Related pytest file：tests/test_task_patch.py

## STM-TC-EH-01
- Test Item：Error handling
- Scenario：Authenticated user sends patch request with malformed JSON.
- Precondition：
The autheticated user exist in the system.
The target task exist in the system and belongs to the  autheticated user.
The patch task endpoint is available, protected by authentication and also subject to authorization checks.
The access token belongs to the authenticated user.
- Test step：
1.Create a authenticated user.
2.Create a target task belongs to the autheticated user.
3.Prepare request payload with malformed JSON.
4.Send a patch request to /api/v1/tasks/{task_id} with malformed JSON to patch the task.
5.Get system response and check
- Test data：
User data：
The authenticated user data.
Task payload：
The target task payload.
Task patch payload with malformed JSON.
Access token：Provided for authenticated user.
- Expected result：
1.request is rejected 
2.system returns 400 Bad Request
3.error response follows standardized JSON format
- Priority：Medium
- Automation status：Automated
- Related pytest file：tests/test_task_patch.py