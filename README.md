# Project Description — AI Email Prioritization & Response Assistant

## Overview

Develop a desktop-based AI email assistant that automatically reviews incoming emails from a Gmail account every day at 8:00 AM, analyzes the previous 24 hours of messages, identifies emails requiring attention or response, and sends the user a summarized report.

The application will be built as a local-first Flask web application running on the user’s desktop, with a Python backend powered by LangChain and configurable LLM providers.

The system should function as a lightweight personal executive assistant focused on:

- Email triage
- Priority detection
- Response urgency analysis
- Daily summaries
- Configurable AI behavior

---

# Core Features

## 1. Automated Daily Email Review

The system must:

- Connect securely to Gmail using OAuth2 or Gmail API credentials
- Fetch emails received within the last 24 hours
- Run automatically every day at 8:00 AM
- Process unread and optionally read emails
- Ignore spam/promotions unless configured otherwise

### Analysis Tasks

The AI agent should:

- Determine which emails are important
- Identify which emails likely require replies
- Detect urgency and deadlines
- Summarize conversations
- Extract action items
- Flag follow-up tasks

---

## 2. Daily Summary Report

After processing emails, the system will generate and send a structured report to the user.

### Report Contents

The report should include:

- High-priority emails
- Emails requiring responses
- Suggested urgency level
- Brief AI-generated summaries
- Suggested next actions
- Optional draft replies

### Delivery Options

The report may be delivered through:

- Email
- Flask dashboard
- Desktop notification
- Exportable HTML/Markdown report

---

# Desktop Flask Application

## Frontend Requirements

The application should include a desktop-accessible Flask UI with multiple configuration pages.

### Main Dashboard

Displays:

- Last scan time
- Number of important emails found
- Current AI provider/model
- System status
- Upcoming scheduled run
- Recent summaries

---

# Settings Windows / Configuration Panels

## 1. Gmail Integration Settings

A dedicated configuration page for:

- Gmail login
- OAuth credentials
- Gmail API setup
- Token management
- Connected account status

### Features

- Secure credential storage
- OAuth authentication flow
- Token refresh handling
- “Test Connection” button

---

## 2. LLM Settings Panel

A configurable interface for AI settings.

### User-Configurable Options

- LLM provider
- API endpoint
- API key
- Model selection
- Temperature
- Context window size
- Token limits

### Supported Providers

Examples:

- OpenAI
- Ollama
- Anthropic
- Local LLM endpoints
- OpenRouter-compatible APIs

---

## 3. Importance Classification Settings

A rule + AI hybrid configuration system.

### User-Defined Rules

The user should be able to configure:

- Keywords indicating importance
- Keywords indicating low priority
- VIP senders
- Ignore senders
- Priority scoring thresholds
- Categories of emails to always flag

### AI Classification Controls

Adjust:

- Aggressiveness of prioritization
- Sensitivity to deadlines
- Personal vs business weighting
- Reply urgency detection

---

# AI Agent Architecture

## Backend Stack

### Core Technologies

- Python
- Flask
- LangChain
- Gmail API
- APScheduler or Celery for scheduled tasks

### Optional Enhancements

- SQLite/PostgreSQL for storage
- Redis task queue
- Vector memory for email history
- LangGraph workflows

---

# LangChain Agent Responsibilities

The LangChain-powered agent should:

1. Retrieve emails
2. Chunk and preprocess content
3. Analyze importance
4. Score reply urgency
5. Summarize conversations
6. Generate actionable reports
7. Optionally generate reply drafts

---

# Suggested System Architecture

## Components

### Flask Frontend

Handles:

- Dashboard
- Settings UI
- Authentication
- Report viewing

### Background Scheduler

Handles:

- Daily 8AM execution
- Retry logic
- Scheduled scans

### Email Processing Service

Handles:

- Gmail API communication
- Email parsing
- Attachment metadata extraction

### AI Processing Pipeline

Handles:

- Summarization
- Classification
- Priority scoring
- Response recommendation

---

# Security Requirements

The application should:

- Store credentials securely
- Encrypt API keys locally
- Use OAuth2 best practices
- Never expose tokens in logs
- Run entirely locally unless external LLM APIs are configured

---

# Future Expansion Possibilities

Potential future features:

- Multi-account support
- Outlook integration
- Slack/Discord notifications
- Auto-generated replies
- Calendar integration
- Smart follow-up reminders
- Mobile companion app
- RAG memory for long-term email context

---

# Development Goals

The final product should be:

- Modular
- Extensible
- Local-first
- Easy to configure
- Efficient with token usage
- Compatible with local or cloud-hosted LLMs
- Suitable for daily personal productivity workflows
