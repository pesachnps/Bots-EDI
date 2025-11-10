# Modern EDI Interface - User Guide

Welcome to the Modern EDI Interface! This guide will help you navigate and use all the features available in the new interface.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Navigation](#navigation)
3. [Core Features](#core-features)
4. [Transaction Management](#transaction-management)
5. [Operations](#operations)
6. [Tips & Tricks](#tips--tricks)

---

## Getting Started

### Accessing the Interface

**URL**: http://localhost:3000/admin

**Login**: Use your existing Bots credentials

### Dashboard Overview

After logging in, you'll see the dashboard with:
- Quick access to key features
- Recent activity summary
- System status indicators

---

## Navigation

The sidebar is organized into logical sections that can be expanded or collapsed:

### 📊 Dashboard
- Main overview page
- Quick stats and recent activity

### 👥 Partners
- Manage trading partners
- View partner details and settings

### ⚙️ Configuration
**Collapsible section** containing:
- **Routes** - Define data flow paths
- **Channels** - Configure communication endpoints
- **Translations** - Set up message mappings
- **Confirm Rules** - Manage acknowledgment rules
- **Code Lists** - Maintain code conversion tables
- **Counters** - View/edit system counters

### 📦 Transactions
**Collapsible section** containing:
- **Incoming** - View received transactions
- **Outgoing** - View sent transactions

### 🔧 Operations
**Collapsible section** containing:
- **Engine** - Run the EDI engine
- **Files** - Browse transaction files
- **Logs** - View system logs
- **System** - System information

### 🔐 Administration
**Collapsible section** containing:
- **Users** - Manage user accounts
- **Permissions** - Set user permissions
- **Analytics** - View analytics (future)
- **Activity Logs** - Audit trail (future)

### 📁 Mailbox Folders
- Dynamic list of mailbox folders
- Expandable for each partner

---

## Core Features

### Routes Management

**Path**: Configuration → Routes

#### Viewing Routes
- All routes displayed as cards
- Color-coded by status (active/inactive)
- Filter by channel, editype, partner, etc.
- Search by route ID

#### Creating a Route
1. Click **"Add Route"** button
2. Fill in required fields:
   - Route ID (unique identifier)
   - From Channel (source)
   - From Editype (message standard)
   - Translation Indicator (0=none, 1=translate, 2=passthrough)
   - To Channel (destination)
3. Optional fields:
   - Partners (from/to)
   - Sequence number
   - Description
4. Click **"Save"**

#### Editing a Route
1. Click on a route card
2. Modify fields as needed
3. Click **"Update"**

#### Deleting a Route
1. Click on a route card
2. Click **"Delete"** button
3. Confirm deletion

#### Route Actions
- **Clone**: Duplicate an existing route with a new ID
- **Activate/Deactivate**: Toggle route active status
- **Export**: Export route configuration (API ready)

---

### Channels Management

**Path**: Configuration → Channels

#### Channel Types
Channels are divided into:
- **In Channels** (receive data)
- **Out Channels** (send data)

Use the tabs at the top to switch between them.

#### Supported Channel Types
- `file` - Local file system
- `ftp` / `ftps` - FTP/FTPS
- `sftp` - SSH File Transfer
- `smtp` / `pop3` / `imap4` - Email
- `as2` / `as3` - AS2/AS3 protocol
- `communicationscript` - Custom script
- And more...

#### Creating a Channel
1. Select **In** or **Out** tab
2. Click **"Add Channel"**
3. Fill in:
   - Channel ID
   - Type (select from dropdown)
   - Type-specific fields (dynamically shown)
4. Click **"Save"**

#### Type-Specific Fields

**File Type:**
- Path (directory path)
- Filename pattern

**FTP/SFTP:**
- Host
- Port
- Username
- Password
- Path
- Active/Binary mode (FTP only)

**Email:**
- Host
- Port
- Username
- Password
- TLS settings

#### Testing Connection
- Click **"Test Connection"** button
- See real-time result
- Green check = success, Red X = failure

#### Protection
Channels in use by routes cannot be deleted. You'll see a warning if you try.

---

### Translations Management

**Path**: Configuration → Translations

#### What is a Translation?
A translation maps one message format to another using:
- **From Editype** → **To Editype**
- **Mapping Script** (Python file)
- **Grammars** (message structure definitions)

#### Creating a Translation
1. Click **"Add Translation"**
2. Specify:
   - From editype (e.g., `x12`, `edifact`)
   - From messagetype (e.g., `850`, `ORDERS`)
   - To editype
   - To messagetype
   - Mapping script path
3. Optional:
   - Alternative ID
   - Partner-specific mappings
4. Click **"Save"**

#### Viewing Translations
- Filter by editype
- See partner associations
- View mapping script references

---

### Confirm Rules

**Path**: Configuration → Confirm Rules

#### What are Confirm Rules?
Rules that determine when and how to send acknowledgments (997, CONTRL, etc.)

#### Viewing Rules
- All rules listed with:
  - Rule type
  - ID value
  - Confirm type
  - Negative flag

#### Deleting a Rule
1. Find the rule
2. Click **"Delete"**
3. Confirm deletion

---

### Code Lists

**Path**: Configuration → Code Lists

#### What are Code Lists?
Translation tables for codes (e.g., internal codes → partner codes)

#### Browsing Code Lists
1. See list of all code types
2. Click on a type to view codes
3. Each code has:
   - Left code (input)
   - Right code (output)
   - 8 custom attributes (attr1-attr8)

#### Managing Codes
- View codes in table format
- See counts per code type
- Navigate between types

---

### Counters

**Path**: Configuration → Counters

#### What are Counters?
System counters for:
- Message numbering
- Cleanup tracking
- Custom sequences

#### Viewing/Editing Counters
1. All counters displayed in list
2. Click **"Edit"** to modify value
3. Enter new value
4. Click **"Update"**

**Warning**: Editing counters can affect system behavior. Use caution!

---

## Transaction Management

### Incoming Transactions

**Path**: Transactions → Incoming

#### Viewing Incoming Data
- All received transactions listed
- Paginated (20 per page)
- Status badges (color-coded):
  - 🟢 Green = OK/DONE
  - 🔴 Red = ERROR
  - 🟡 Yellow = OPEN/PROCESS

#### Transaction Information
Each transaction shows:
- ID (idta)
- Status
- From/To channels
- From/To partners
- Editype & messagetype
- Filename
- Timestamp
- File size

#### Filtering Transactions
Use the filter controls to:
- Select date range
- Filter by partner
- Filter by status
- Filter by editype
- Search by filename

#### Actions
- **Resend**: Reprocess a transaction
- **Delete**: Remove transaction (with confirmation)
- **View Details**: See full transaction info

#### Pagination
- Navigate using Previous/Next buttons
- See current page number
- Total count displayed

---

### Outgoing Transactions

**Path**: Transactions → Outgoing

Similar to Incoming, but for sent transactions.

Features:
- Same filtering options
- Same status indicators
- Resend/Delete actions
- Pagination

---

### Transaction Lineage

**API Available**: GET `/api/v1/admin/transactions/<id>/lineage`

View the complete parent/child relationship tree for any transaction. Shows:
- Parent transactions (sources)
- Child transactions (results)
- Full processing chain

---

## Operations

### Engine Control

**Path**: Operations → Engine

#### Running the Engine
1. Click **"Run Engine"** button
2. Watch real-time output in the output box
3. Status updates every 5 seconds
4. See completion message

#### Engine Status
The status indicator shows:
- 🟢 **Running** - Engine is active
- 🔴 **Stopped** - Engine is idle
- 🟡 **Starting** - Engine starting up

#### Output Display
- Real-time command output
- Scrollable text area
- Shows all engine messages
- Errors highlighted

---

### File Browser

**Path**: Operations → Files

#### Browsing Files
1. Enter directory path or use dropdown
2. Click **"Browse"**
3. See list of files with:
   - Filename
   - Size (human-readable: KB, MB, GB)
   - Type indicator

#### Navigation
- Enter full paths (e.g., `data/archive`)
- Browse common locations:
  - data
  - archive
  - infile
  - outfile
  - etc.

#### Actions
- Click filename to download (via API)
- View file sizes
- Navigate directory structure

---

### Log Viewer

**Path**: Operations → Logs

#### Viewing Logs
1. See list of all log files
2. Each log shows:
   - Filename
   - Size
3. Click to download (via API)

#### Log Files
Common logs:
- `engine.log` - Engine run logs
- `webserver.log` - Web server logs
- `errors.log` - Error messages
- Partner-specific logs

---

### System Information

**Path**: Operations → System

#### System Details
View comprehensive system information:

**Python Environment:**
- Python version
- Executable path

**Bots Information:**
- Bots version
- Installation path

**Platform:**
- Operating system
- System architecture

**Database:**
- Database backend type
- Connection details

---

## Tips & Tricks

### Keyboard Shortcuts
- **Esc** - Close modal dialogs
- **Ctrl/Cmd + K** - Quick search (future)

### Navigation Tips
1. **Collapsible Sections**: Click section headers to expand/collapse
2. **Mobile**: Swipe from left to open sidebar
3. **Active Page**: Current page highlighted in blue

### Performance
- **Pagination**: Use pagination for large lists
- **Filtering**: Apply filters before loading data
- **Refresh**: Click refresh icon to reload data

### Best Practices

#### Routes
- Use descriptive route IDs
- Document routes in description field
- Test routes before activating
- Use sequence numbers for order control

#### Channels
- Test connections after creation
- Use meaningful channel IDs
- Document special settings
- Keep credentials secure (passwords masked)

#### Transactions
- Clean up old transactions regularly
- Monitor error status
- Resend failed transactions promptly
- Check logs for errors

#### Engine Runs
- Review output after each run
- Check for errors or warnings
- Run during low-traffic periods
- Monitor engine status

### Troubleshooting

#### Can't Delete Channel
- Check if channel is used in routes
- Remove from routes first
- Then delete channel

#### Route Not Running
- Verify channel configurations
- Check translation mappings
- Ensure route is active
- Review engine logs

#### Transaction Errors
- Check error message
- Review log files
- Verify channel connectivity
- Check mapping scripts

#### Page Not Loading
- Refresh browser
- Check network connection
- Clear browser cache
- Check console for errors (F12)

---

## Mobile Usage

The Modern EDI interface is fully responsive:

### Features
- Touch-friendly buttons
- Responsive tables
- Mobile-optimized forms
- Collapsible navigation

### Tips
- Use hamburger menu (☰) to open sidebar
- Tap sections to expand/collapse
- Swipe tables to scroll horizontally
- Use landscape mode for tables

---

## Support & Feedback

### Getting Help
1. Check this user guide
2. Review error messages
3. Check log files
4. Contact your administrator

### Reporting Issues
When reporting issues, include:
- Page/feature affected
- Steps to reproduce
- Error messages
- Screenshots (if applicable)
- Browser and version

---

## What's New in Modern EDI

### Improvements Over Old Interface
1. ✅ **Better Navigation** - Organized, collapsible sections
2. ✅ **Modern UI** - Clean, card-based design
3. ✅ **Mobile Support** - Works on phones and tablets
4. ✅ **Real-time Updates** - Engine status auto-refreshes
5. ✅ **Better Filtering** - Advanced search and filters
6. ✅ **Confirmation Dialogs** - Prevent accidental deletions
7. ✅ **Status Indicators** - Color-coded visual feedback
8. ✅ **Improved Performance** - Faster page loads

### Preserved Features
- All existing functionality maintained
- Same database and data
- Compatible with existing workflows
- Same user permissions

---

## Glossary

**Route**: Configuration defining data flow from source to destination

**Channel**: Communication endpoint (file, FTP, email, etc.)

**Translation**: Mapping between message formats using scripts

**Editype**: Message standard (x12, edifact, xml, etc.)

**Messagetype**: Specific message within editype (850, ORDERS, etc.)

**Transaction**: Instance of data being processed

**Engine**: Core processing component that runs routes

**Idta**: Transaction ID (unique identifier)

**Status**: Transaction processing state (OK, ERROR, DONE, etc.)

**Lineage**: Parent/child relationship tree for transactions

**Confirm Rules**: Rules for sending acknowledgments

**Code Lists**: Translation tables for code values

**Counters**: System sequence numbers

---

*Last Updated: Phase 11 Complete*
*Version: 1.0*

For additional help, contact your system administrator.
