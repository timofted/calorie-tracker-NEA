# Calorie Tracking Application

A desktop calorie-tracking application built with Python. The system
allows users to create an account, sign in, manage their profile, record
food intake, retrieve nutritional information, and review their progress
over time.

> **Project note:** This README and the requirements below are based on
> the coursework structure and functionality previously reviewed. They
> describe the system at a functional level; check each item against the
> final version of the source code before treating it as a verified
> implementation claim.

## Contents

-   [Overview](#overview)
-   [System requirements](#system-requirements)
    -   [Functional requirements](#functional-requirements)
    -   [Non-functional requirements](#non-functional-requirements)
    -   [External interface
        requirements](#external-interface-requirements)
    -   [Data requirements](#data-requirements)
-   [Technology stack](#technology-stack)
-   [Project structure](#project-structure)
-   [Installation](#installation)
-   [Configuration](#configuration)
-   [Running the application](#running-the-application)
-   [Typical workflow](#typical-workflow)
-   [Security and privacy
    considerations](#security-and-privacy-considerations)
-   [Testing checklist](#testing-checklist)
-   [Limitations and future
    improvements](#limitations-and-future-improvements)

## Overview

The application is intended to help an individual monitor food
consumption and personal progress. It provides a graphical interface,
stores user-related information in an SQLite database, and uses the USDA
FoodData Central API to look up nutritional information for food items.
Nutritional totals and historical information can be presented through
graphical visualisations.

## System requirements

The following requirements form a proposed specification for the
application. Requirement IDs are included to make them easier to
reference in coursework documentation and testing.

### Functional requirements

#### Account registration and authentication

-   **FR-01 --- Account registration:** The system shall allow a new
    user to create an account by entering the required registration
    details.
-   **FR-02 --- Unique accounts:** The system shall prevent registration
    where the chosen username or other designated unique identifier is
    already in use.
-   **FR-03 --- Input checking:** The system shall check required
    registration fields and reject missing or invalid values with a
    clear message.
-   **FR-04 --- Sign in:** The system shall allow an existing user to
    sign in using their account credentials.
-   **FR-05 --- Credential verification:** The system shall verify
    submitted credentials against the account information stored in the
    database.
-   **FR-06 --- Failed sign-in feedback:** The system shall inform the
    user when sign-in details are missing or incorrect without exposing
    sensitive account information.
-   **FR-07 --- Sign out:** The system shall allow the current user to
    end their session.
-   **FR-08 --- Session handling:** The system shall keep track of the
    currently authenticated user while the application is in use and
    associate that user's actions with the correct account.

#### User profile and settings

-   **FR-09 --- View account details:** The system shall provide a way
    for a signed-in user to view their stored account or profile
    information.
-   **FR-10 --- Manage account details:** Where supported by the
    interface, the system shall allow a user to update relevant profile
    or account settings.
-   **FR-11 --- Account separation:** The system shall ensure that
    account-specific information is associated with the correct user.

#### Food and nutrition tracking

-   **FR-12 --- Search for food:** The system shall allow a user to
    search for food items using the external food-data service.
-   **FR-13 --- Retrieve nutrition data:** The system shall retrieve
    available nutritional information for a matching food item from the
    USDA FoodData Central API.
-   **FR-14 --- Process API responses:** The system shall process the
    API's JSON response and extract the nutritional values required by
    the application.
-   **FR-15 --- Record food intake:** The system shall allow a user to
    record a food item and its relevant serving or quantity information,
    where supported by the interface.
-   **FR-16 --- Calculate nutritional values:** The system shall
    calculate the nutritional contribution of recorded food using the
    available food data and quantity information.
-   **FR-17 --- Daily totals:** The system shall calculate or display
    the user's recorded calorie intake and relevant macronutrient totals
    for the applicable day, where supported.
-   **FR-18 --- Review food records:** The system shall allow the user
    to view previously recorded food information.
-   **FR-19 --- User-specific records:** Food records shall be
    associated with the user who created them and shall not be presented
    as another user's records.

#### Weight and progress tracking

-   **FR-20 --- Store weight history:** The system shall store weight
    measurements associated with a user and their recording dates.
-   **FR-21 --- Review progress:** The system shall provide a way to
    review stored progress information over time.
-   **FR-22 --- Visualise progress:** The system shall use graphical
    visualisations to present relevant historical data, where the
    required data is available.
-   **FR-23 --- Handle missing history:** The system shall display an
    appropriate message or empty state when there is not enough
    historical data to produce a meaningful graph.

#### Navigation and application feedback

-   **FR-24 --- Graphical interface:** The system shall provide a
    graphical user interface for its main functions.
-   **FR-25 --- Screen navigation:** The system shall provide navigation
    between the available application screens.
-   **FR-26 --- User feedback:** The system shall provide understandable
    feedback after important actions, including successful operations
    and errors.
-   **FR-27 --- Data persistence:** The system shall retain successfully
    saved account, food and progress information when the application is
    closed and reopened.

### Non-functional requirements

-   **NFR-01 --- Usability:** Controls, labels and messages shall be
    understandable to the intended user.
-   **NFR-02 --- Consistency:** The interface shall use consistent
    navigation, layout and terminology across screens.
-   **NFR-03 --- Reliability:** The application shall handle invalid
    input, missing records and failed API requests without terminating
    unexpectedly.
-   **NFR-04 --- Performance:** Common local operations, such as opening
    screens and reading stored records, should complete within a
    reasonable time on a typical desktop computer.
-   **NFR-05 --- Maintainability:** The code should be organised into
    modules with clear responsibilities, making it easier to test and
    modify individual features.
-   **NFR-06 --- Data integrity:** Database operations shall preserve
    relationships between users and their associated records.
-   **NFR-07 --- Security:** Authentication data and user-specific
    records shall be handled carefully, and database queries shall use
    parameterised statements where user input is included.
-   **NFR-08 --- Privacy:** The application shall not expose one user's
    personal records to another user through normal application use.
-   **NFR-09 --- Compatibility:** The application shall run in a
    supported Python environment with its required libraries installed.
-   **NFR-10 --- External-service resilience:** The application shall
    provide suitable feedback when the food-data API is unavailable,
    returns no results, or responds with an error.

### External interface requirements

-   **User interface:** A desktop graphical interface implemented with
    Tkinter.
-   **Database interface:** SQLite is used for local persistent storage.
-   **Food-data interface:** The application communicates with the USDA
    FoodData Central API over HTTP and processes JSON responses.
-   **Graphical output:** Matplotlib is used to display data
    visualisations; NumPy may be used for numerical operations.
-   **Image resources:** Pillow may be used to load or process image
    assets used by the interface.

### Data requirements

The database design reviewed for the project included data relating to:

-   **Users:** account identifiers and authentication-related
    information.
-   **Food records:** food items and nutritional information recorded by
    users.
-   **Weight records:** user-associated weight measurements and
    historical dates.

The exact table names, column names, constraints and relationships
should be taken from the final database schema. User records should be
linked using stable identifiers, and database constraints should be used
where appropriate to protect data consistency.

## Technology stack

  Technology                  Purpose
  --------------------------- -------------------------------------------
  Python                      Main application programming language
  Tkinter                     Desktop graphical user interface
  SQLite                      Local relational database
  SQL                         Database queries and updates
  Requests                    HTTP communication with the food-data API
  JSON                        Processing API responses
  USDA FoodData Central API   External nutritional data source
  Matplotlib                  Graphs and data visualisation
  NumPy                       Numerical calculations or data handling
  Pillow (PIL)                Image loading and processing, where used

## Project structure

The reviewed project included files with responsibilities broadly
corresponding to the following areas. The exact structure may differ in
the final version.

  -----------------------------------------------------------------------
  File or resource                    Apparent responsibility
  ----------------------------------- -----------------------------------
  `menu.py`                           Main menu or application navigation

  `login.py`                          Login interface and authentication
                                      flow

  `loggingfood.py`                    Food search, nutrition retrieval or
                                      food logging

  `datarep.py`                        Data representation and graphs

  `home.png`                          Interface image asset

  `setting.png`                       Interface image asset

  SQLite database file                Persistent application data

  Additional Python modules           Supporting database, registration
                                      or settings functionality
  -----------------------------------------------------------------------

Update this section if files are renamed, added or removed.

## Installation

### Prerequisites

-   Python 3 installed.
-   The project source files.
-   Internet access for food searches that use the USDA API.
-   A USDA FoodData Central API key if the API endpoint used by the
    application requires one.

### Set up a virtual environment

From the project directory, run:

``` bash
python -m venv .venv
```

Activate it:

**Windows (PowerShell):**

``` powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

``` bash
source .venv/bin/activate
```

### Install dependencies

Install the libraries used by the project:

``` bash
python -m pip install requests matplotlib numpy pillow
```

Tkinter is included with many standard Python installations. On some
Linux distributions it must be installed separately through the
operating system's package manager.

If the project contains a `requirements.txt` file, prefer:

``` bash
python -m pip install -r requirements.txt
```

A `requirements.txt` should be created and kept up to date with the
versions actually tested by the project.

## Configuration

The application uses the USDA FoodData Central API for nutritional
lookups.

1.  Obtain an API key from the USDA FoodData Central website if
    required.
2.  Configure the key outside the source code, for example through an
    environment variable.
3.  Ensure the application reads the configured key securely.
4.  Do not commit API keys, passwords, database files containing
    personal information, or other secrets to a public repository.

Example environment-variable setup:

**Windows PowerShell:**

``` powershell
$env:USDA_API_KEY = "your_api_key"
```

**macOS / Linux:**

``` bash
export USDA_API_KEY="your_api_key"
```

The application must be updated to read `USDA_API_KEY` from the
environment for this configuration method to work. Do not assume this is
already implemented.

## Running the application

Run the application's entry-point file from the project directory. If
`menu.py` is the entry point in your copy:

``` bash
python menu.py
```

If the project uses a different entry point, replace `menu.py` with the
correct filename.

## Typical workflow

1.  Launch the application.
2.  Register a new account or sign in with an existing account.
3.  Navigate to the food-tracking area.
4.  Search for a food item using the available food-data lookup.
5.  Review the returned nutritional information.
6.  Record the food and relevant quantity or serving details.
7.  Review daily nutritional totals.
8.  Open the progress or data-representation area to review available
    historical information.
9.  Sign out when finished.

The exact workflow depends on the screens and features present in the
final code.

## Security and privacy considerations

This project is an educational application and should not be presented
as a production-ready health or account-management service without
further security work.

Before publishing the source code:

-   Remove API keys and other credentials from source files and
    repository history. If a real key has already been published, revoke
    it and generate a replacement.
-   Use a password-storage algorithm designed for passwords, such as
    Argon2id, bcrypt or PBKDF2, with an appropriate work factor and
    unique salt. A fast general-purpose hash such as plain SHA-256 is
    not suitable for password storage.
-   Use parameterised SQL statements rather than building SQL commands
    by concatenating user input.
-   Validate user input and handle unexpected values safely.
-   Protect session information against unauthorised modification and
    ensure users can access only their own records.
-   Configure and test SQLite foreign-key enforcement where relational
    constraints are relied upon.
-   Set sensible HTTP timeouts and handle network errors, unsuccessful
    HTTP responses and malformed API data.
-   Avoid committing real user data or a populated personal database to
    version control.

## Testing checklist

Use this checklist when testing the final version. Record the actual
result for each test.

  -----------------------------------------------------------------------
  ID                      Test                    Expected result
  ----------------------- ----------------------- -----------------------
  T-01                    Register with valid     Account is created and
                          details                 stored

  T-02                    Register with missing   Registration is
                          required details        rejected with a useful
                                                  message

  T-03                    Register using an       Duplicate account is
                          existing unique         rejected
                          identifier              

  T-04                    Sign in with correct    User is authenticated
                          credentials             

  T-05                    Sign in with incorrect  Access is denied and an
                          credentials             error message is shown

  T-06                    Sign out                The active session is
                                                  ended

  T-07                    Search for a valid food Nutritional information
                          item                    is returned when the
                                                  API is available

  T-08                    Search for a food item  A suitable no-results
                          with no match           message is shown

  T-09                    Attempt a food lookup   The application handles
                          without network access  the failure without
                                                  crashing

  T-10                    Record a food item      The record is saved
                                                  against the active user

  T-11                    Review daily nutrition  Totals reflect the
                          totals                  user's recorded food

  T-12                    Save and reopen         Previously saved data
                          application data        remains available

  T-13                    View progress with      Relevant graph or
                          historical records      progress view is
                                                  displayed

  T-14                    View progress without   An appropriate empty
                          historical records      state or message is
                                                  displayed

  T-15                    Sign in as a different  The second user cannot
                          user                    see the first user's
                                                  private records
  -----------------------------------------------------------------------

## Limitations and future improvements

Potential improvements include:

-   Add automated unit and integration tests for authentication,
    database operations and nutritional calculations.
-   Improve password storage using a dedicated password-hashing
    algorithm.
-   Move secrets into environment-based configuration and document setup
    using a `.env.example` file without real credentials.
-   Add stronger session management and access-control checks.
-   Improve API error handling, request timeouts and user feedback.
-   Add database migrations and clearer schema documentation.
-   Add options to edit or delete food and weight records, if not
    already supported.
-   Improve accessibility and interface responsiveness.
-   Package the application for easier installation on supported
    operating systems.

## Contributing

For coursework or a personal portfolio, document significant changes and
keep the README aligned with the actual implementation. If using Git,
make small, descriptive commits and do not commit secrets or personal
database contents.

## Disclaimer

This application is intended for educational and personal tracking
purposes. Nutritional information depends on the data returned by the
external food-data provider and may not be suitable for medical or
clinical decisions.
