# UML Module Diagrams

## Overview

This document describes four high-level UML module diagrams for a small
financial system:

1.  **Account Management System** --- management of user accounts and
    currency accounts.
2.  **Withdraw, Deposit and Transfer Currency** --- operations for
    withdrawing, depositing, and transferring currency.
3.  **Logging System** --- collection, processing, storage, and
    monitoring of application logs.
4.  **Exchange Rate System** --- obtaining, processing, storing, and
    providing currency exchange rates.

The diagrams are intentionally high-level. They show the main modules,
components, and dependencies without describing the internal
implementation of each service.

------------------------------------------------------------------------

## 1. Account Management System

### Purpose

The module is responsible for managing the user's account and currency
accounts.

### Main Components

-   **User Interface (Web / App)** --- the main point of interaction
    between the user and the system.
-   **Account Management Module** --- manages the profile, profile
    deletion, adding currency accounts, and updating profile
    information.
-   **Currency Account Creation Module** --- handles currency selection,
    validation, checking for an existing currency account, and account
    creation.
-   **Backend Services** --- contains business logic, validation, and
    operation processing.
-   **Database** --- stores information about users, accounts, and
    transactions.

### Main Flow

``` text
User
  ↓
User Interface
  ↓
Account Management / Currency Account Creation
  ↓
Backend Services
  ↕
Database
```

------------------------------------------------------------------------

## 2. Withdraw, Deposit and Transfer Currency

### Purpose

This diagram combines three main operations with currency accounts:

-   withdrawing currency;
-   depositing currency;
-   transferring currency between accounts.

### Withdraw Currency Module

The module handles withdrawals.

Main components:

-   **Withdraw UI** --- interface for the withdrawal operation.
-   **Currency Account Service** --- works with the currency account.
-   **Balance Validation** --- checks the available balance.
-   **Withdrawal Service** --- processes the withdrawal.
-   **Payout Processing** --- performs the payout.
-   **Transaction Recording** --- records the operation.

Main flow:

``` text
User
  ↓
Withdraw UI
  ↓
Currency Account Service
  ↓
Balance Validation
  ↓
Withdrawal Service
  ↓
Payout Processing
  ↓
Transaction Recording
```

### Deposit Currency Module

The module handles deposits into a currency account.

Main components:

-   **Deposit UI** --- interface for the deposit operation.
-   **Currency Account Service** --- checks the currency account.
-   **Deposit Service** --- manages the deposit operation.
-   **Generate Deposit Credentials** --- prepares deposit credentials.
-   **Payment Monitoring** --- waits for and checks incoming funds.
-   **Timeout Handling** --- handles cases where the payment does not
    arrive in time.
-   **Transaction Recording** --- records the operation.

Main flow:

``` text
User
  ↓
Deposit UI
  ↓
Currency Account Service
  ↓
Deposit Service
  ↓
Deposit Credentials
  ↓
Payment Monitoring
  ↓
Transaction Recording
```

### Transfer Currency Module

The module handles transfers between currency accounts.

Main components:

-   **Transfer UI** --- interface for the transfer operation.
-   **Transfer Service** --- manages the transfer.
-   **Source Account Validation** --- validates the source account.
-   **Destination Account Validation** --- validates the destination
    account.
-   **Transfer Execution** --- executes the transfer.
-   **Transaction Recording** --- records the operation.

Main flow:

``` text
User
  ↓
Transfer UI
  ↓
Transfer Service
  ↓
Source / Destination Account Validation
  ↓
Transfer Execution
  ↓
Transaction Recording
```

### Shared Services

The three operations use shared services:

-   **Currency Account Service**
-   **Account Service**
-   **Notification Service**
-   **Exchange Rate Service**

Operation data is stored in:

-   User / Account Database
-   Currency Account Database
-   Transaction Database

------------------------------------------------------------------------

## 3. Logging System

### Purpose

The Logging System provides centralized collection, processing, storage,
and monitoring of application logs.

### Main Modules

#### Log Collection Module

Collects logs from applications and prepares them for further
processing.

Main components:

-   **Application (Services)**
-   **Log Collector**
-   **Log Parser & Enricher**
-   **Log Validator**

#### Log Processing Module

Processes incoming logs.

Main components:

-   **Log Processor**
-   **Log Level Filter**
-   **Log Router**
-   **Log Aggregator**
-   **Log Buffer (Queue)**

#### Log Storage Module

Stores and indexes logs.

Main components:

-   **Log Storage Service**
-   **Log Indexer**
-   **Log Archiver**

Storage is divided into:

-   **Hot Storage** --- recently created logs;
-   **Warm Storage** --- archived logs;
-   **Cold Storage** --- long-term log storage.

#### Log Monitoring & Management Module

Provides tools for working with logs:

-   **Log Search Service**
-   **Log Viewer (UI)**
-   **Log Alerting Service**
-   **Log Retention Manager**

External integrations include:

-   Notification Service;
-   SIEM / Monitoring Systems.

### Main Flow

``` text
Application
  ↓
Log Collection
  ↓
Log Processing
  ↓
Log Storage
  ↓
Search / Viewer / Alerting
```

------------------------------------------------------------------------

## 4. Exchange Rate System

### Purpose

The Exchange Rate System obtains exchange rates from external providers,
processes them, stores them, and provides them to other parts of the
system.

### Main Modules

#### Rate Source Module

Obtains exchange-rate data from external providers.

Main components:

-   **Source Configuration Manager**
-   **Rate Data Fetcher**
-   **Source Adapter (Provider Connectors)**
-   **External Rate Providers**

#### Rate Processing Module

Processes the received rate values.

Main components:

-   **Data Normalizer**
-   **Rate Validator**
-   **Rate Calculator**
-   **Rate Aggregator**

The module handles normalization, validation, rate calculation, and
selection of an appropriate rate.

#### Rate Storage Module

Stores current and historical exchange rates.

Main components:

-   **Rate Repository**
-   **Historical Rate Repository**
-   **Cache Manager**

Storage includes:

-   **Current Rates DB**
-   **Historical Rates DB**

#### Rate Service Module

Provides exchange rates to other parts of the system.

Main components:

-   **Rate Query API**
-   **Rate Service**
-   **Conversion Service**
-   **Response Formatter**

The module also supports currency conversion operations.

#### Rate Management Module

Provides administrative management of exchange rates.

Main components:

-   **Rate Management API**
-   **Manual Rate Manager**
-   **Rate Override Manager**
-   **Schedule Manager**

### Shared Services

The system uses common services:

-   Authentication Service;
-   Authorization Service;
-   Notification Service;
-   Audit & Log Service;
-   Config Service;
-   Monitoring Service.

External integrations are also provided for notifications and
monitoring.

### Main Flow

``` text
External Rate Providers
  ↓
Rate Source
  ↓
Rate Processing
  ↓
Rate Storage
  ↓
Rate Service
  ↓
Application / Client
```

Administrative changes follow this flow:

``` text
Rate Management
  ↓
Backend / Shared Services
  ↓
Rate Storage
```

------------------------------------------------------------------------

## System-Level Interaction

At a high level, the modules can be connected as follows:

``` text
                    ┌──────────────────────┐
                    │      User / App      │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              ↓                ↓                ↓
       Account Management   Currency Ops    Exchange Rate
              │                │                │
              └────────────────┼────────────────┘
                               ↓
                       Backend Services
                               │
             ┌─────────────────┼─────────────────┐
             ↓                 ↓                 ↓
          Database          Logging        Monitoring
```

**Account Management** manages users and currency accounts.

**Currency Operations** perform financial operations: withdrawals,
deposits, and transfers.

**Exchange Rate System** provides current exchange rates for operations
that require currency conversion or exchange-rate calculations.

**Logging System** provides collection and storage of information about
system activity and operations.

------------------------------------------------------------------------

## Diagram Conventions

All diagrams use a consistent high-level style:

-   **Module / Component** --- an individual software module or
    component.
-   **Solid arrow** --- primary data flow or interaction.
-   **Dashed arrow** --- dependency or external integration.
-   **Database** --- persistent data storage.

The diagrams do not describe classes, methods, API contracts, or
specific implementation technologies. Their purpose is to show the
**architectural separation of the system into major modules and the
relationships between them**.
