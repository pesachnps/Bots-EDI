# Requirements Document

## Introduction

This document specifies the requirements for a modern web interface for the Bots EDI system that provides folder-based file management for EDI transactions. The new interface will operate independently from the existing Django admin interface, providing users with an intuitive way to manage incoming and outgoing EDI files through a folder structure (Inbox, Received, Outbox, Sent, Deleted). The system will support creating, viewing, editing, moving, and tracking EDI transactions with acknowledgment status.

## Glossary

- **EDI_System**: The Bots Electronic Data Interchange translation system
- **Transaction_File**: An EDI file containing business transaction data (e.g., purchase orders, invoices)
- **Modern_Interface**: The new web-based user interface being developed
- **Folder_View**: A visual representation of one of the five file management folders
- **Transaction_Card**: A visual summary display of a Transaction_File showing key metadata
- **Detail_View**: A comprehensive display of all data within a Transaction_File
- **Acknowledgment_Status**: A flag indicating whether a sent EDI file was successfully acknowledged by the recipient
- **File_Movement**: The action of transferring a Transaction_File from one Folder_View to another

## Requirements

### Requirement 1

**User Story:** As an EDI operator, I want to access a modern web interface separate from the existing admin interface, so that I can manage EDI files without affecting the legacy system.

#### Acceptance Criteria

1. THE Modern_Interface SHALL be accessible via a distinct URL path that does not conflict with existing Django admin routes
2. THE Modern_Interface SHALL operate independently without modifying existing Django admin functionality
3. THE Modern_Interface SHALL use the same authentication system as the existing EDI_System
4. THE Modern_Interface SHALL provide a responsive design that works on desktop and tablet devices
5. WHEN a user navigates to the Modern_Interface, THE EDI_System SHALL display a dashboard with access to all five Folder_Views

### Requirement 2

**User Story:** As an EDI operator, I want to view EDI files organized in an Inbox folder, so that I can create and manage new incoming transactions before they are processed.

#### Acceptance Criteria

1. THE Modern_Interface SHALL provide an Inbox Folder_View for staging new incoming Transaction_Files
2. WHEN viewing the Inbox, THE Modern_Interface SHALL display each Transaction_File as a Transaction_Card showing partner name, document type, and creation date
3. THE Modern_Interface SHALL provide a button to create a new incoming Transaction_File in the Inbox
4. WHEN a user clicks on a Transaction_Card in the Inbox, THE Modern_Interface SHALL display the Detail_View with all transaction data
5. THE Modern_Interface SHALL allow users to edit Transaction_File content while in the Inbox

### Requirement 3

**User Story:** As an EDI operator, I want to view all received EDI files in a Received folder, so that I can review processed incoming transactions and their details.

#### Acceptance Criteria

1. THE Modern_Interface SHALL provide a Received Folder_View for displaying processed incoming Transaction_Files
2. WHEN viewing the Received folder, THE Modern_Interface SHALL display each Transaction_File as a Transaction_Card showing partner name, purchase order number, and received date
3. WHEN a user clicks on a Transaction_Card in the Received folder, THE Modern_Interface SHALL display the Detail_View with all parsed transaction data
4. THE Modern_Interface SHALL display Transaction_Files in the Received folder in reverse chronological order by default
5. THE Modern_Interface SHALL provide search and filter capabilities for Transaction_Files in the Received folder

### Requirement 4

**User Story:** As an EDI operator, I want to create and manage outgoing EDI files in an Outbox folder, so that I can prepare transactions for sending and review scheduled transmissions.

#### Acceptance Criteria

1. THE Modern_Interface SHALL provide an Outbox Folder_View for staging outgoing Transaction_Files
2. THE Modern_Interface SHALL provide a button to create a new outgoing Transaction_File in the Outbox
3. WHEN viewing the Outbox, THE Modern_Interface SHALL display each Transaction_File as a Transaction_Card showing partner name, document type, and scheduled send date
4. THE Modern_Interface SHALL allow users to edit Transaction_File content while in the Outbox
5. THE Modern_Interface SHALL provide a send action button on each Transaction_Card in the Outbox to trigger immediate transmission

### Requirement 5

**User Story:** As an EDI operator, I want to view all sent EDI files in a Sent folder with acknowledgment status, so that I can verify successful transmission and identify failed deliveries.

#### Acceptance Criteria

1. THE Modern_Interface SHALL provide a Sent Folder_View for displaying transmitted Transaction_Files
2. WHEN viewing the Sent folder, THE Modern_Interface SHALL display each Transaction_File as a Transaction_Card showing partner name, document type, sent date, and Acknowledgment_Status
3. THE Modern_Interface SHALL visually distinguish Transaction_Files with successful acknowledgment from those without acknowledgment
4. WHEN a user clicks on a Transaction_Card in the Sent folder, THE Modern_Interface SHALL display the Detail_View including transmission details and Acknowledgment_Status
5. THE Modern_Interface SHALL update Acknowledgment_Status automatically when acknowledgment messages are received

### Requirement 6

**User Story:** As an EDI operator, I want to move EDI files between any folders, so that I can reprocess failed transactions or correct misplaced files.

#### Acceptance Criteria

1. THE Modern_Interface SHALL provide a move action on each Transaction_Card in all Folder_Views
2. WHEN a user initiates File_Movement, THE Modern_Interface SHALL display a folder selection dialog showing all available destination folders
3. WHEN a user confirms File_Movement, THE EDI_System SHALL transfer the Transaction_File to the selected Folder_View
4. THE Modern_Interface SHALL allow File_Movement from the Sent folder to the Outbox folder for retransmission
5. WHEN a Transaction_File is moved to the Outbox from another folder, THE Modern_Interface SHALL allow editing before retransmission

### Requirement 7

**User Story:** As an EDI operator, I want to move EDI files to a Deleted folder instead of permanently deleting them, so that I can recover accidentally deleted files if needed.

#### Acceptance Criteria

1. THE Modern_Interface SHALL provide a Deleted Folder_View for storing removed Transaction_Files
2. THE Modern_Interface SHALL provide a delete action on each Transaction_Card that moves the file to the Deleted folder
3. WHEN viewing the Deleted folder, THE Modern_Interface SHALL display each Transaction_File as a Transaction_Card with deletion date
4. THE Modern_Interface SHALL allow File_Movement from the Deleted folder to any other Folder_View for recovery
5. THE Modern_Interface SHALL provide a permanent delete action in the Deleted folder that removes Transaction_Files from the EDI_System

### Requirement 8

**User Story:** As an EDI operator, I want to view detailed information about any EDI file, so that I can review all transaction data and metadata.

#### Acceptance Criteria

1. WHEN a user clicks on any Transaction_Card, THE Modern_Interface SHALL display a Detail_View in a modal or dedicated page
2. THE Detail_View SHALL display all parsed EDI data fields in a structured, readable format
3. THE Detail_View SHALL display metadata including file name, size, creation date, modification date, and current folder location
4. WHERE the Transaction_File is in the Sent folder, THE Detail_View SHALL display transmission timestamp and Acknowledgment_Status
5. THE Detail_View SHALL provide a close action that returns the user to the Folder_View

### Requirement 9

**User Story:** As an EDI operator, I want to create new EDI transaction files through a form interface, so that I can manually generate transactions when needed.

#### Acceptance Criteria

1. WHEN a user clicks the create button in the Inbox or Outbox, THE Modern_Interface SHALL display a transaction creation form
2. THE transaction creation form SHALL include fields for partner selection, document type, and all required transaction data
3. WHEN a user submits the creation form with valid data, THE EDI_System SHALL generate a new Transaction_File in the selected folder
4. THE Modern_Interface SHALL validate all required fields before allowing form submission
5. WHEN form submission fails validation, THE Modern_Interface SHALL display specific error messages for each invalid field

### Requirement 10

**User Story:** As an EDI operator, I want to edit EDI transaction files in the Inbox and Outbox folders, so that I can correct errors before processing or transmission.

#### Acceptance Criteria

1. WHEN a Transaction_File is in the Inbox or Outbox, THE Modern_Interface SHALL provide an edit action on the Transaction_Card
2. WHEN a user clicks the edit action, THE Modern_Interface SHALL display an editing form pre-populated with current transaction data
3. THE Modern_Interface SHALL allow modification of all editable transaction fields
4. WHEN a user saves edits with valid data, THE EDI_System SHALL update the Transaction_File with the modified data
5. THE Modern_Interface SHALL prevent editing of Transaction_Files in the Received, Sent, and Deleted folders

### Requirement 11

**User Story:** As an EDI operator, I want to send outgoing EDI files from the Outbox, so that I can transmit transactions to trading partners.

#### Acceptance Criteria

1. WHEN a Transaction_File is in the Outbox, THE Modern_Interface SHALL display a send action button on the Transaction_Card
2. WHEN a user clicks the send action, THE EDI_System SHALL initiate transmission of the Transaction_File to the designated partner
3. WHEN transmission is initiated, THE EDI_System SHALL move the Transaction_File from the Outbox to the Sent folder
4. THE EDI_System SHALL record the transmission timestamp when moving the file to the Sent folder
5. IF transmission fails, THE EDI_System SHALL return the Transaction_File to the Outbox and display an error message

### Requirement 12

**User Story:** As an EDI operator, I want to search and filter EDI files across all folders, so that I can quickly locate specific transactions.

#### Acceptance Criteria

1. THE Modern_Interface SHALL provide a search input field accessible from all Folder_Views
2. WHEN a user enters search criteria, THE Modern_Interface SHALL filter displayed Transaction_Cards to match the search terms
3. THE Modern_Interface SHALL support searching by partner name, purchase order number, document type, and date range
4. THE Modern_Interface SHALL provide filter options for document type, partner, and date range
5. WHEN filters are applied, THE Modern_Interface SHALL display only Transaction_Cards matching all active filter criteria
