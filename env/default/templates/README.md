# Template Overrides

This directory contains custom templates that override the default Bots EDI templates.

## How It Works

Django will search for templates in this order:
1. `env/default/templates/` (this directory) - Your custom templates
2. `site-packages/bots/templates/` - Default Bots templates

## Modified Templates

### bots/about.html
- Removed external links to bots.readthedocs.io, bots-edi.org, and edi-intelligentsia.com
- Location: `templates/bots/about.html`

### bots/menu.html
- Removed Help link to bots.readthedocs.io
- Location: `templates/bots/menu.html`

## Adding New Overrides

To override any Bots template:
1. Copy the template from `C:\Users\USER\AppData\Roaming\Python\Python313\site-packages\bots\templates\`
2. Paste it into this directory maintaining the same folder structure
3. Modify as needed
4. Restart the backend server

## Benefits

- Your customizations survive Bots package updates
- All customizations are in your project directory
- Easy to version control with git
- Clear separation between core package and customizations
