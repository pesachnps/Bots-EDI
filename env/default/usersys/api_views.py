"""
Bots EDI API Views
REST API endpoints for EDI operations
"""

import os
import json
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .api_auth import api_authenticate
import bots.botsinit
import bots.botslib
import bots.botsglobal


# Initialize Bots
try:
    bots.botsinit.generalinit()
except:
    pass  # May already be initialized


@csrf_exempt
@require_http_methods(["POST"])
@api_authenticate(['file_upload'])
def upload_file(request):
    """
    Upload an EDI file for processing
    
    POST /api/v1/files/upload
    Headers: X-API-Key: your-api-key
    Body: multipart/form-data with 'file' field
    Optional params: route, partner, messagetype
    """
    try:
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)
        
        uploaded_file = request.FILES['file']
        route = request.POST.get('route', '')
        partner = request.POST.get('partner', '')
        messagetype = request.POST.get('messagetype', '')
        
        # Save file to infile directory
        botssys_dir = bots.botsglobal.ini.get('directories', 'botssys')
        infile_dir = os.path.join(botssys_dir, 'infile')
        
        # Create route-specific directory if specified
        if route:
            infile_dir = os.path.join(infile_dir, route)
        
        os.makedirs(infile_dir, exist_ok=True)
        
        # Save file
        file_path = os.path.join(infile_dir, uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        return JsonResponse({
            'success': True,
            'message': 'File uploaded successfully',
            'file': {
                'name': uploaded_file.name,
                'size': uploaded_file.size,
                'path': file_path,
                'route': route,
                'partner': partner,
                'messagetype': messagetype
            }
        }, status=201)
        
    except Exception as e:
        return JsonResponse({
            'error': 'Upload failed',
            'message': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
@api_authenticate(['file_download'])
def download_file(request, file_id):
    """
    Download a processed EDI file
    
    GET /api/v1/files/download/<file_id>
    Headers: X-API-Key: your-api-key
    """
    try:
        botssys_dir = bots.botsglobal.ini.get('directories', 'botssys')
        outfile_dir = os.path.join(botssys_dir, 'outfile')
        
        # Find file
        file_path = os.path.join(outfile_dir, file_id)
        
        if not os.path.exists(file_path):
            return JsonResponse({'error': 'File not found'}, status=404)
        
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
        
    except Exception as e:
        return JsonResponse({
            'error': 'Download failed',
            'message': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
@api_authenticate(['file_list'])
def list_files(request):
    """
    List available files
    
    GET /api/v1/files/list?type=infile|outfile
    Headers: X-API-Key: your-api-key
    """
    try:
        file_type = request.GET.get('type', 'outfile')
        
        botssys_dir = bots.botsglobal.ini.get('directories', 'botssys')
        target_dir = os.path.join(botssys_dir, file_type)
        
        files = []
        for root, dirs, filenames in os.walk(target_dir):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, target_dir)
                files.append({
                    'name': filename,
                    'path': rel_path,
                    'size': os.path.getsize(filepath),
                    'modified': os.path.getmtime(filepath)
                })
        
        return JsonResponse({
            'success': True,
            'type': file_type,
            'count': len(files),
            'files': files
        })
        
    except Exception as e:
        return JsonResponse({
            'error': 'List failed',
            'message': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@api_authenticate(['route_execute'])
def execute_route(request):
    """
    Execute a Bots route
    
    POST /api/v1/routes/execute
    Headers: X-API-Key: your-api-key
    Body: {"route": "route_name"}
    """
    try:
        data = json.loads(request.body)
        route = data.get('route', '')
        
        if not route:
            return JsonResponse({'error': 'Route name required'}, status=400)
        
        # Execute route using Bots engine
        import subprocess
        result = subprocess.run(
            ['bots-engine', route],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        return JsonResponse({
            'success': result.returncode == 0,
            'route': route,
            'output': result.stdout,
            'errors': result.stderr if result.returncode != 0 else None
        })
        
    except subprocess.TimeoutExpired:
        return JsonResponse({
            'error': 'Route execution timeout',
            'route': route
        }, status=504)
    except Exception as e:
        return JsonResponse({
            'error': 'Execution failed',
            'message': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
@api_authenticate(['report_view'])
def get_reports(request):
    """
    Get translation reports
    
    GET /api/v1/reports?limit=100&status=success|error
    Headers: X-API-Key: your-api-key
    """
    try:
        limit = int(request.GET.get('limit', 100))
        status_filter = request.GET.get('status', '')
        
        from bots.models import report
        
        reports_query = report.objects.all().order_by('-ts')[:limit]
        
        if status_filter:
            reports_query = reports_query.filter(statust=status_filter)
        
        report_data = []
        for r in reports_query:
            report_data.append({
                'id': r.idta,
                'timestamp': r.ts.isoformat() if r.ts else None,
                'status': r.statust,
                'type': r.messagetype,
                'partner': r.frompartner,
                'filename': r.filename
            })
        
        return JsonResponse({
            'success': True,
            'count': len(report_data),
            'reports': report_data
        })
        
    except Exception as e:
        return JsonResponse({
            'error': 'Report retrieval failed',
            'message': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
@api_authenticate([])
def api_status(request):
    """
    Get API status and usage information
    
    GET /api/v1/status
    Headers: X-API-Key: your-api-key
    """
    api_key = request.api_key
    
    return JsonResponse({
        'success': True,
        'api_key': {
            'name': api_key.name,
            'user': api_key.user.username,
            'is_active': api_key.is_active,
            'rate_limit': api_key.rate_limit,
            'current_usage': api_key.current_usage,
            'usage_reset_time': api_key.usage_reset_time.isoformat(),
            'last_used': api_key.last_used.isoformat() if api_key.last_used else None,
            'created_at': api_key.created_at.isoformat(),
            'permissions': [p.code for p in api_key.permissions.all()]
        }
    })
