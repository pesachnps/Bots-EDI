# Bots EDI Installation

This directory contains a complete Bots EDI (Electronic Data Interchange) installation with comprehensive plugin support.

## 🚀 Quick Start

### Web Interface
Access the Bots web interface at: **http://localhost:8080**

**Default Login Credentials:**
- **Username**: `edi_admin`
- **Password**: `Bots@2025!EDI`

*Note: The default account has superuser privileges. Please change the password after first login for security.*

**Alternative Account** (for development/testing):
- **Username**: `bots`
- **Password**: `bots`

### System Status
- ✅ Bots EDI Engine: Installed and running
- ✅ Web Server: Running on port 8080
- ✅ Database: SQLite configured and operational
- ✅ Plugins: 20 plugins installed (516 files)

## 📦 Installed Plugins

### EDI Standards Support
- **EDIFACT**: Complete D96A support (ORDERS, DESADV, INVOIC, PRICAT, SLSRPT, APERAK)
- **X12/ANSI**: Full 4010/5010 support (850, 810, 837, 835, 856, 997)
- **Tradacoms**: Version 9 support (ORDERS)
- **XML**: Bidirectional XML conversions
- **JSON**: JSON to EDIFACT invoice conversion
- **CSV**: CSV import/export capabilities
- **Fixed Format**: Fixed-width file support

### Business Document Types
- **Purchase Orders** (850, ORDERS)
- **Invoices** (810, INVOIC)
- **Shipping Notices** (856, DESADV)
- **Functional Acknowledgments** (997, APERAK)
- **Healthcare Claims** (837)
- **Remittance Advice** (835)
- **Price Catalogs** (PRICAT)
- **Sales Reports** (SLSRPT)
- **Vendor Consignment**

### Plugin Details
1. **837_4010_to_837_5010** - Healthcare claim version upgrade
2. **fixed_to_810** - Fixed format to X12 810 invoice
3. **to_xml_850-856-810-997** - XML conversions for major documents
4. **x12_850tofixed** - X12 850 to fixed format
5. **x12toxml_one-on-one_835-837** - Healthcare to XML
6. **x12toxml_retailer_version_850-856-810-997** - Retailer-focused XML
7. **x12toxml_supplier_version850-856-810-997** - Supplier-focused XML
8. **xml_to_850** - XML to X12 850 purchase order
9. **edifact2xml_orders-desadv-invoice** - EDIFACT to XML
10. **json_to_invoice** - JSON to EDIFACT invoice
11. **order_to_print** - Order to printable format
12. **orders_desadv_invoice** - Complete order workflow
13. **orders_to_csv** - Orders to CSV export
14. **orders_to_csv_and_vv** - CSV with validation
15. **pricat_slsrpt** - Price catalog and sales reports
16. **to_fixed_orders_desadv_invoice_aperak** - Fixed format conversions
17. **to_json_invoice** - EDIFACT to JSON
18. **vendor_consignment** - Vendor consignment processing
19. **tradacoms_to_xml_orders** - Tradacoms to XML
20. **communication_script** - Custom communication handlers

## 🛠️ Configuration

### Directory Structure
```
C:\Users\USER\.bots\env\default\
├── config/
│   ├── bots.ini          # Main configuration
│   └── settings.py       # Django settings
├── usersys/              # User plugins and scripts
│   ├── grammars/         # EDI format definitions
│   ├── mappings/         # Translation scripts
│   ├── routescripts/     # Route configurations
│   ├── partners/         # Trading partner info
│   └── communicationscripts/  # Communication handlers
├── botssys/              # System files
│   ├── infile/           # Input files
│   ├── outfile/          # Output files
│   └── sqlitedb/        # Database
└── static/               # Web interface assets
```

### Starting/Stopping Services
```bash
# Start Bots web server
cd C:\Users\USER\.bots\env\default
python -c "import bots.botsinit; bots.botsinit.generalinit(); from bots import webserver; webserver.run()"

# The web server runs automatically on http://localhost:8080
```

## 🧪 Testing

### Sample Files
Test files are available in `botssys/infile/` for various EDI formats.

### JSON to EDIFACT Example
```json
{
  "invoice_number": "INV-2025-001",
  "invoice_date": "20251105",
  "buyer": {
    "name": "Customer Company",
    "tax_id": "US123456789"
  },
  "seller": {
    "name": "Supplier Company", 
    "tax_id": "US987654321"
  },
  "line_items": [...],
  "totals": {
    "subtotal": 333.75,
    "tax_amount": 26.70,
    "total_amount": 360.45
  },
  "currency": "USD"
}
```

## 📚 Documentation

- **Official Bots Documentation**: https://bots.sourceforge.io/
- **Current Development**: https://gitlab.com/bots-ediint/bots
- **Plugin Repository**: https://gitlab.com/bots-ediint/bots-plugins
- **EDI Standards**: 
  - EDIFACT: https://www.unece.org/cefact/untdid/d99a.htm
  - X12: https://www.x12.org/
- **Plugin Development**: See installed plugin examples in `usersys/`

## 🔧 Maintenance

### Logs
- Application logs: `botssys/logs/`
- Web server logs: Console output

### Database
- SQLite database: `botssys/sqlitedb/botsdb`
- Backup regularly recommended

### Updates
- Check for core updates at: https://gitlab.com/bots-ediint/bots
- Check for plugin updates at: https://gitlab.com/bots-ediint/bots-plugins

## 🔌 **REST API** (NEW!)

Bots EDI now includes a secure REST API for programmatic access without needing to log in to the web interface.

### **Quick API Start**

```bash
# Initialize API permissions
cd C:\Users\USER\.bots\env\default
python usersys\api_management.py init_permissions

# Create your first API key
python usersys\api_management.py create "My API Key" edi_admin

# Test the API
curl -H "X-API-Key: YOUR_API_KEY" http://localhost:8080/api/v1/status
```

### **API Features**

- 🔐 **Secure Authentication** - Token-based API keys
- 🎯 **Permission Control** - Granular access permissions managed by admin
- ⚡ **Rate Limiting** - Configurable request limits (default: 1000/hour)
- 📊 **Audit Logging** - Complete request history and monitoring
- 🌐 **IP Whitelisting** - Restrict access by IP address
- 📁 **File Operations** - Upload, download, and list EDI files
- 🚀 **Route Execution** - Trigger EDI translations programmatically
- 📈 **Reporting** - Retrieve translation reports via API

### **API Endpoints**

- `POST /api/v1/files/upload` - Upload EDI files
- `GET /api/v1/files/download/<file_id>` - Download files
- `GET /api/v1/files/list` - List available files
- `POST /api/v1/routes/execute` - Execute translation routes
- `GET /api/v1/reports` - Get translation reports
- `GET /api/v1/status` - Check API status and usage

### **API Documentation**

- **Complete Guide:** `API_DOCUMENTATION.md`
- **Setup Instructions:** `API_SETUP_GUIDE.md`
- **Testing Tool:** `test_api.py`
- **Management CLI:** `usersys\api_management.py`

### **Example Usage**

```python
import requests

API_KEY = "your-api-key-here"
headers = {"X-API-Key": API_KEY}

# Upload a file
with open("invoice.edi", "rb") as f:
    files = {"file": f}
    response = requests.post(
        "http://localhost:8080/api/v1/files/upload",
        headers=headers,
        files=files
    )
print(response.json())
```

## 🐳 Docker Support

Full containerized deployment is available with Docker and Docker Compose.

### Quick Start
```bash
# Using Docker Compose (recommended)
docker-compose up -d

# Access at http://localhost:8080
```

### Documentation
See `DOCKER.md` for complete Docker deployment guide, including:
- Production deployment
- Database options (SQLite/PostgreSQL)
- Security configuration
- Monitoring and troubleshooting
- Backup and recovery

### Container Features
- ✅ All 20 plugins pre-installed (516 files)
- ✅ Health checks and monitoring
- ✅ Volume mounts for data persistence
- ✅ Environment-based configuration
- ✅ Production-ready security settings

## 📞 Support

### Web Interface Access
- **URL**: http://localhost:8080
- **Default Username**: `edi_admin`
- **Default Password**: `Bots@2025!EDI`
- **User Management**: Use `python manage_users.py` in the Bots directory

**Alternative Account** (development):
- **Username**: `bots`
- **Password**: `bots`

### Configuration Files
- **Main Config**: `config/bots.ini`
- **Django Settings**: `config/settings.py`
- **Plugin Directory**: `usersys/`
- **User Management Script**: `manage_users.py`

## 🙏 Credits & Acknowledgments

### Bots EDI Project
This installation is made possible by the incredible work of the **Bots EDI** project and its dedicated community of developers, maintainers, and contributors.

### Special Thanks To

#### 🏗️ Core Project Team
- **Original Creator**: **Henk-Jan Ebbers** - The visionary founder and original developer who created Bots EDI as an open-source solution for electronic data interchange. His dedication and technical expertise laid the foundation for the entire Bots EDI ecosystem.
- **Current Maintainers**: The dedicated team that continues to develop, maintain, and support the Bots EDI platform, building upon Henk-Jan's original vision
- **Plugin Developers**: Contributors who have created and maintained the extensive plugin ecosystem

#### 🌐 Community Contributors
- **SourceForge Community**: Long-time contributors and users who have helped shape Bots EDI through feedback, bug reports, and feature requests
- **GitLab Contributors**: The modern development community maintaining plugins and core functionality
- **Documentation Writers**: Those who have created comprehensive guides and tutorials
- **Support Community**: Helpful members who assist others in forums and discussion boards

#### 📚 EDI Standards Organizations
- **UNECE/CEFACT**: For the EDIFACT standards that form the backbone of international EDI
- **X12 Organization**: For developing and maintaining the ANSI X12 standards
- **GS1**: For global standards that enable seamless business communication

### Project Resources
- **Official Website**: [bots-edi.org](https://bots-edi.org)
- **Documentation**: [bots.sourceforge.io](https://bots.sourceforge.io/)
- **Primary Source Code**: [GitLab](https://gitlab.com/bots-ediint/bots) - Current development and releases
- **Legacy Source**: [SourceForge](https://sourceforge.net/projects/bots/) - Historical repository
- **Plugin Repository**: [GitLab](https://gitlab.com/bots-ediint/bots-plugins)
- **Community Support**: Active forums and discussion boards

### Open Source Philosophy
Bots EDI embodies the true spirit of open-source software:
- **Free for Everyone**: No licensing fees or commercial restrictions
- **Community Driven**: Developed and maintained by volunteers and contributors worldwide
- **Enterprise Ready**: Production-grade software used by companies globally
- **Educational Resource**: Learning platform for EDI standards and implementation

### 🌟 Impact
The Bots EDI project has enabled:
- Small businesses to participate in global EDI networks
- Educational institutions to teach EDI concepts
- Developers to learn and contribute to enterprise software
- Organizations to reduce costs through open-source solutions

---

**A special thank you to Henk-Jan Ebbers, the original creator of Bots EDI, whose vision and technical leadership made this incredible open-source EDI solution possible. His dedication to creating a free, enterprise-grade EDI platform has benefited countless organizations worldwide.**

**A heartfelt thank you to everyone who has contributed to making Bots EDI the powerful, flexible, and accessible EDI solution it is today. Your dedication to open-source values and business automation has made electronic data interchange available to organizations worldwide.**

---

**Installation Date**: 2025-11-05  
**Version**: Bots EDI with 20 plugins  
**Total Files**: 516 plugin components
