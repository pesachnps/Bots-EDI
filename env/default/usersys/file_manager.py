"""
File Manager Service
Handle file system operations for EDI transactions
"""

import os
import shutil
import hashlib
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError


class FileManager:
    """Service class for managing EDI files on the file system"""
    
    def __init__(self):
        """Initialize the file manager"""
        self.botssys_dir = getattr(settings, 'BOTSSYS', 'botssys')
        self.modern_edi_base = os.path.join(self.botssys_dir, 'modern-edi')
        self.valid_folders = ['inbox', 'received', 'outbox', 'sent', 'deleted']
    
    def _get_folder_path(self, folder):
        """Get the absolute path for a folder"""
        if folder not in self.valid_folders:
            raise ValidationError(f"Invalid folder: {folder}")
        return os.path.join(self.modern_edi_base, folder)
    
    def _ensure_folder_exists(self, folder):
        """Ensure folder exists, create if necessary"""
        folder_path = self._get_folder_path(folder)
        os.makedirs(folder_path, exist_ok=True)
        return folder_path
    
    def save_file(self, content, folder, filename):
        """
        Save EDI file to appropriate folder
        
        Args:
            content: File content (string or bytes)
            folder: Target folder name
            filename: Name of the file
        
        Returns:
            Dictionary with file information
        """
        # Ensure folder exists
        folder_path = self._ensure_folder_exists(folder)
        
        # Construct full file path
        file_path = os.path.join(folder_path, filename)
        
        # Check if file already exists
        if os.path.exists(file_path):
            raise ValidationError(f"File already exists: {filename}")
        
        # Write content to file
        mode = 'wb' if isinstance(content, bytes) else 'w'
        try:
            with open(file_path, mode) as f:
                f.write(content)
        except Exception as e:
            raise ValidationError(f"Failed to save file: {str(e)}")
        
        # Get file information
        file_info = {
            'path': file_path,
            'filename': filename,
            'size': os.path.getsize(file_path),
            'hash': self.get_file_hash(file_path),
            'created_at': datetime.now().isoformat()
        }
        
        return file_info
    
    def move_file(self, from_path, to_folder):
        """
        Move file between folders
        
        Args:
            from_path: Current file path
            to_folder: Destination folder name
        
        Returns:
            New file path
        """
        # Validate source file exists
        if not os.path.exists(from_path):
            raise ValidationError(f"Source file not found: {from_path}")
        
        # Ensure destination folder exists
        dest_folder_path = self._ensure_folder_exists(to_folder)
        
        # Get filename from source path
        filename = os.path.basename(from_path)
        
        # Construct destination path
        dest_path = os.path.join(dest_folder_path, filename)
        
        # Check if destination file already exists
        if os.path.exists(dest_path):
            raise ValidationError(f"Destination file already exists: {dest_path}")
        
        # Move the file
        try:
            shutil.move(from_path, dest_path)
        except Exception as e:
            raise ValidationError(f"Failed to move file: {str(e)}")
        
        return dest_path
    
    def copy_file(self, from_path, to_folder, new_filename=None):
        """
        Copy file to another folder
        
        Args:
            from_path: Source file path
            to_folder: Destination folder name
            new_filename: Optional new filename (uses original if not provided)
        
        Returns:
            New file path
        """
        # Validate source file exists
        if not os.path.exists(from_path):
            raise ValidationError(f"Source file not found: {from_path}")
        
        # Ensure destination folder exists
        dest_folder_path = self._ensure_folder_exists(to_folder)
        
        # Get filename
        filename = new_filename or os.path.basename(from_path)
        
        # Construct destination path
        dest_path = os.path.join(dest_folder_path, filename)
        
        # Check if destination file already exists
        if os.path.exists(dest_path):
            raise ValidationError(f"Destination file already exists: {dest_path}")
        
        # Copy the file
        try:
            shutil.copy2(from_path, dest_path)
        except Exception as e:
            raise ValidationError(f"Failed to copy file: {str(e)}")
        
        return dest_path
    
    def delete_file(self, file_path, permanent=False):
        """
        Delete or archive file
        
        Args:
            file_path: Path to file
            permanent: If True, permanently delete; if False, move to deleted folder
        
        Returns:
            New path if moved to deleted, None if permanently deleted
        """
        # Validate file exists
        if not os.path.exists(file_path):
            raise ValidationError(f"File not found: {file_path}")
        
        if permanent:
            # Permanently delete the file
            try:
                os.remove(file_path)
                return None
            except Exception as e:
                raise ValidationError(f"Failed to delete file: {str(e)}")
        else:
            # Move to deleted folder
            try:
                return self.move_file(file_path, 'deleted')
            except Exception as e:
                raise ValidationError(f"Failed to move file to deleted folder: {str(e)}")
    
    def read_file(self, file_path, mode='r'):
        """
        Read EDI file content
        
        Args:
            file_path: Path to file
            mode: Read mode ('r' for text, 'rb' for binary)
        
        Returns:
            File content
        """
        # Validate file exists
        if not os.path.exists(file_path):
            raise ValidationError(f"File not found: {file_path}")
        
        # Read file content
        try:
            with open(file_path, mode) as f:
                content = f.read()
            return content
        except Exception as e:
            raise ValidationError(f"Failed to read file: {str(e)}")
    
    def write_file(self, file_path, content, mode='w'):
        """
        Write content to file
        
        Args:
            file_path: Path to file
            content: Content to write
            mode: Write mode ('w' for text, 'wb' for binary)
        
        Returns:
            File size
        """
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write content
        try:
            with open(file_path, mode) as f:
                f.write(content)
            return os.path.getsize(file_path)
        except Exception as e:
            raise ValidationError(f"Failed to write file: {str(e)}")
    
    def get_file_hash(self, file_path, algorithm='sha256'):
        """
        Calculate hash of file
        
        Args:
            file_path: Path to file
            algorithm: Hash algorithm ('sha256', 'md5', etc.)
        
        Returns:
            Hexadecimal hash string
        """
        # Validate file exists
        if not os.path.exists(file_path):
            raise ValidationError(f"File not found: {file_path}")
        
        # Calculate hash
        try:
            hash_obj = hashlib.new(algorithm)
            with open(file_path, 'rb') as f:
                # Read file in chunks to handle large files
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except Exception as e:
            raise ValidationError(f"Failed to calculate file hash: {str(e)}")
    
    def get_file_info(self, file_path):
        """
        Get detailed file information
        
        Args:
            file_path: Path to file
        
        Returns:
            Dictionary with file information
        """
        # Validate file exists
        if not os.path.exists(file_path):
            raise ValidationError(f"File not found: {file_path}")
        
        # Get file stats
        try:
            stat = os.stat(file_path)
            
            info = {
                'path': file_path,
                'filename': os.path.basename(file_path),
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'hash': self.get_file_hash(file_path),
                'exists': True
            }
            
            return info
        except Exception as e:
            raise ValidationError(f"Failed to get file info: {str(e)}")
    
    def list_files(self, folder):
        """
        List all files in a folder
        
        Args:
            folder: Folder name
        
        Returns:
            List of file information dictionaries
        """
        folder_path = self._get_folder_path(folder)
        
        # Check if folder exists
        if not os.path.exists(folder_path):
            return []
        
        files = []
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                
                # Skip directories and hidden files
                if os.path.isfile(file_path) and not filename.startswith('.'):
                    try:
                        info = self.get_file_info(file_path)
                        files.append(info)
                    except Exception:
                        # Skip files that can't be read
                        continue
            
            # Sort by modified time (newest first)
            files.sort(key=lambda x: x['modified'], reverse=True)
            
            return files
        except Exception as e:
            raise ValidationError(f"Failed to list files: {str(e)}")
    
    def get_folder_size(self, folder):
        """
        Calculate total size of all files in a folder
        
        Args:
            folder: Folder name
        
        Returns:
            Total size in bytes
        """
        folder_path = self._get_folder_path(folder)
        
        if not os.path.exists(folder_path):
            return 0
        
        total_size = 0
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    total_size += os.path.getsize(file_path)
            return total_size
        except Exception as e:
            raise ValidationError(f"Failed to calculate folder size: {str(e)}")
    
    def cleanup_old_files(self, folder, days_old=30):
        """
        Remove files older than specified days
        
        Args:
            folder: Folder name
            days_old: Age threshold in days
        
        Returns:
            Number of files deleted
        """
        folder_path = self._get_folder_path(folder)
        
        if not os.path.exists(folder_path):
            return 0
        
        from datetime import timedelta
        threshold = datetime.now() - timedelta(days=days_old)
        deleted_count = 0
        
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                
                if os.path.isfile(file_path):
                    # Get file modification time
                    mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    # Delete if older than threshold
                    if mtime < threshold:
                        os.remove(file_path)
                        deleted_count += 1
            
            return deleted_count
        except Exception as e:
            raise ValidationError(f"Failed to cleanup old files: {str(e)}")
    
    def validate_file_content(self, file_path, max_size_mb=10):
        """
        Validate file content and size
        
        Args:
            file_path: Path to file
            max_size_mb: Maximum file size in MB
        
        Returns:
            True if valid, raises ValidationError otherwise
        """
        # Check if file exists
        if not os.path.exists(file_path):
            raise ValidationError(f"File not found: {file_path}")
        
        # Check file size
        file_size = os.path.getsize(file_path)
        max_size_bytes = max_size_mb * 1024 * 1024
        
        if file_size > max_size_bytes:
            raise ValidationError(f"File too large: {file_size} bytes (max: {max_size_bytes} bytes)")
        
        if file_size == 0:
            raise ValidationError("File is empty")
        
        # Check if file is readable
        try:
            with open(file_path, 'r') as f:
                f.read(1)  # Try to read first byte
        except UnicodeDecodeError:
            # File might be binary, try binary mode
            try:
                with open(file_path, 'rb') as f:
                    f.read(1)
            except Exception as e:
                raise ValidationError(f"File is not readable: {str(e)}")
        except Exception as e:
            raise ValidationError(f"File validation failed: {str(e)}")
        
        return True
