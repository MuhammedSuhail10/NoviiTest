# User and Task API Documentation

## Table of Contents

1. [Overview](#overview)
2. [Authentication API](#authentication-api)
   - [Create Superuser](#create-superuser)
   - [User Login](#user-login)
3. [Task Management API](#task-management-api)
   - [Get Tasks](#get-tasks)
   - [Edit Task](#edit-task)
   - [Get Report](#get-report)
4. [Error Handling](#error-handling)

## Overview

This document describes the API for user authentication and task management functionalities in a task management system. It supports:

- Token-based authentication
- Superuser creation and login
- Task fetching, editing, and reporting for authenticated users

All endpoints (except `create_superuser` and `login`) require token authentication:

```
Authorization: Token <your_token>
```

---

## Authentication API

### Create Superuser

- **Endpoint:** `POST /api/create_superuser`
- **Description:** Registers a new superuser with a token.

**Request Body:**

```json
{
    "username": "admin@example.com",
    "password": "adminpassword"
}
```

**Success Response:**

```json
{
    "status": true,
    "token": "<generated_token>"
}
```

**Failure Response:**

```json
{
    "status": false,
    "message": "username already exists"
}
```

### User Login

- **Endpoint:** `POST /api/login`
- **Description:** Authenticates user and returns a token.

**Request Body:**

```json
{
    "username": "user@example.com",
    "password": "userpassword"
}
```

**Success Response:**

```json
{
    "status": true,
    "token": "<your_token>"
}
```

**Failure Response:**

```json
{
    "status": false,
    "message": "Invalid credentials"
}
```

---

## Task Management API

### Get Tasks

- **Endpoint:** `GET /api/get_tasks`
- **Permission:** Authenticated users only
- **Description:** Returns all tasks assigned to the authenticated user that are due today or earlier.

**Success Response:**

```json
[
    {
        "id": 1,
        "title": "Design Homepage",
        "due_date": "2025-04-08",
        "status": "pending"
    },
    ...
]
```

### Edit Task

- **Endpoint:** `PUT /api/edit_task/<id>`
- **Description:** Updates task status. If completing, requires completion report and worked hours.

**Request Body (completing):**

```json
{
    "status": "completed",
    "completion_report": "Task finished successfully.",
    "worked_hours": 4
}
```

**Request Body (other status):**

```json
{
    "status": "in_progress"
}
```

**Response:**

```json
{
    "message": "Task updated succesfully"
}
```

**Failure Response:**

```json
{
    "message": "Completion report and working hours is mandatory to complete a task"
}
```

### Get Report

- **Endpoint:** `GET /api/get_report/<id>`
- **Permission:** Authenticated users with `superuser` or `admin` role
- **Description:** Retrieves a report for a completed task.

**Success Response:**

```json
{
    "task_title": "Design Homepage",
    "status": "completed",
    "completion_report": "Successfully implemented UI",
    "worked_hours": 5
}
```

**Failure Response:**

```json
{
    "message": "Unauthorized"
}
```

---

## Error Handling

All endpoints return consistent error structures:

```json
{
    "status": false,
    "message": "Descriptive error message"
}
```

### Common Errors

- Missing required fields
- Invalid credentials
- Unauthorized access
- Invalid task update parameters

