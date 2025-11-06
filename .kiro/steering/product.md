# Product Overview

This is a Django-based Electronic Data Interchange (EDI) translation system built on the Bots EDI framework. It provides automated translation between various EDI formats (EDIFACT, X12, TRADACOMS, XML, JSON, CSV) with a comprehensive REST API layer.

## Core Purpose

Enable automated B2B data exchange by translating between different EDI formats through configurable routes and mappings. The system monitors directories for incoming files, processes them through translation routes, and outputs in the target format.

## Key Capabilities

- Multi-format EDI translation with flexible routing
- REST API with token authentication, rate limiting, and granular permissions
- Web-based admin interface for configuration and monitoring
- Automatic file processing via directory monitoring
- Complete audit logging for compliance and troubleshooting

## Target Users

- EDI administrators configuring translation routes
- Developers integrating via REST API
- Trading partners exchanging business documents
