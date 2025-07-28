import subprocess
import platform
from pathlib import Path
import logging
import os

class OfficeConverterWindows:
    """
    A Windows-compatible utility class for converting Microsoft Office and OpenDocument files to PDF format.
    
    This class provides functionality to convert various office document formats to PDF
    using LibreOffice's command-line interface, with graceful handling for Windows systems.
    
    Features:
        - Single file conversion to PDF
        - Batch conversion of directories
        - Recursive directory processing
        - Custom output naming with prefix/suffix support
        - Comprehensive error handling and logging
        - Windows-compatible LibreOffice detection
    
    Supported Formats:
        - Microsoft Office: .docx, .doc, .ppt, .pptx
        - OpenDocument: .odt
    
    Requirements:
        - LibreOffice must be installed on the system (optional on Windows)
        - System command 'soffice' must be available (Linux/Mac) or LibreOffice in PATH (Windows)
    
    Attributes:
        logger: Configured logging instance for tracking operations
        SUPPORTED_FORMATS (dict): Mapping of file extensions to format descriptions
        libreoffice_available (bool): Whether LibreOffice is available on the system
    """
    
    # Define supported formats as a class attribute with descriptions
    SUPPORTED_FORMATS = {
        # Microsoft Office formats
        '.docx': 'Word Document',
        '.doc': 'Legacy Word Document',
        '.ppt': 'PowerPoint Presentation',
        '.pptx': 'PowerPoint Presentation',
        # OpenDocument formats
        '.odt': 'OpenDocument Text'
    }

    def __init__(self):
        """
        Initialize the OfficeConverter and check LibreOffice installation.
        
        Note:
            On Windows, LibreOffice availability is checked but not required.
            On Linux/Mac, LibreOffice is required for office document conversion.
        """
        self.logger = self._setup_logger()
        self.libreoffice_available = self._check_libreoffice_availability()

    def _setup_logger(self):
        """
        Configure and set up the logger for the OfficeConverter.
        
        Returns:
            logging.Logger: Configured logger instance
        """
        logger = logging.getLogger('OfficeConverterWindows')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _check_libreoffice_availability(self):
        """
        Check if LibreOffice is available on the system.
        
        Returns:
            bool: True if LibreOffice is available, False otherwise
        """
        system = platform.system().lower()
        
        try:
            if system == "windows":
                # Check for LibreOffice in common Windows installation paths
                possible_paths = [
                    r"C:\Program Files\LibreOffice\program\soffice.exe",
                    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
                    "soffice.exe"  # If in PATH
                ]
                
                for path in possible_paths:
                    try:
                        subprocess.run([path, "--version"], 
                                     check=True, capture_output=True, timeout=5)
                        self.logger.info(f"LibreOffice found at: {path}")
                        return True
                    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
                        continue
                
                self.logger.warning("LibreOffice not found on Windows. Office document conversion will be limited.")
                return False
                
            else:
                # Linux/Mac: use 'which' command
                subprocess.run(['which', 'soffice'], check=True, capture_output=True)
                self.logger.info("LibreOffice found on system")
                return True
                
        except subprocess.CalledProcessError:
            self.logger.warning("LibreOffice not found on system. Office document conversion will be limited.")
            return False
        except Exception as e:
            self.logger.warning(f"Error checking LibreOffice availability: {e}")
            return False

    def convert_to_pdf(self, input_file, output_file=None, output_dir=None):
        """
        Convert a single office document to PDF format.
        
        This method handles the conversion of various office document formats to PDF,
        with support for custom output locations and naming.
        
        Args:
            input_file (str): Path to the input document
            output_file (str, optional): Desired name for the output PDF (without extension)
            output_dir (str, optional): Directory for the output PDF
            
        Returns:
            str: Path to the converted PDF file, or None if conversion failed
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If input file format is not supported
        """
        input_path = Path(input_file)
        
        # Check if input file exists
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Check if format is supported
        if input_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file format: {input_path.suffix}")
        
        # Check if LibreOffice is available
        if not self.libreoffice_available:
            self.logger.warning(f"Cannot convert {input_file} to PDF: LibreOffice not available")
            return None
        
        try:
            # Determine output path
            if output_file is None:
                output_file = input_path.stem
            
            if output_dir is None:
                output_dir = input_path.parent
            else:
                output_dir = Path(output_dir)
                output_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = output_dir / f"{output_file}.pdf"
            
            # Convert using LibreOffice
            system = platform.system().lower()
            if system == "windows":
                # Windows: use full path to soffice.exe
                possible_paths = [
                    r"C:\Program Files\LibreOffice\program\soffice.exe",
                    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
                    "soffice.exe"
                ]
                
                soffice_cmd = None
                for path in possible_paths:
                    try:
                        subprocess.run([path, "--version"], 
                                     check=True, capture_output=True, timeout=5)
                        soffice_cmd = path
                        break
                    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
                        continue
                
                if not soffice_cmd:
                    raise RuntimeError("LibreOffice not found on Windows")
                
                cmd = [soffice_cmd, "--headless", "--convert-to", "pdf", 
                       "--outdir", str(output_dir), str(input_path)]
            else:
                # Linux/Mac: use 'soffice' command
                cmd = ["soffice", "--headless", "--convert-to", "pdf", 
                       "--outdir", str(output_dir), str(input_path)]
            
            # Execute conversion
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.logger.info(f"Successfully converted {input_file} to {output_path}")
                return str(output_path)
            else:
                self.logger.error(f"Conversion failed: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            self.logger.error(f"Conversion timed out for {input_file}")
            return None
        except Exception as e:
            self.logger.error(f"Error converting {input_file}: {e}")
            return None

    def batch_convert_to_pdf(self, input_directory, output_dir=None, recursive=False, prefix=None, suffix=None):
        """
        Convert multiple office documents in a directory to PDF format.
        
        Args:
            input_directory (str): Directory containing office documents
            output_dir (str, optional): Directory for output PDFs
            recursive (bool): Whether to process subdirectories
            prefix (str, optional): Prefix for output filenames
            suffix (str, optional): Suffix for output filenames
            
        Returns:
            list: List of successfully converted PDF file paths
        """
        input_dir = Path(input_directory)
        if not input_dir.exists():
            raise FileNotFoundError(f"Input directory not found: {input_directory}")
        
        if output_dir is None:
            output_dir = input_dir
        else:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        
        converted_files = []
        
        # Get all office files
        if recursive:
            office_files = []
            for ext in self.SUPPORTED_FORMATS.keys():
                office_files.extend(input_dir.rglob(f"*{ext}"))
        else:
            office_files = []
            for ext in self.SUPPORTED_FORMATS.keys():
                office_files.extend(input_dir.glob(f"*{ext}"))
        
        self.logger.info(f"Found {len(office_files)} office files to convert")
        
        for file_path in office_files:
            try:
                # Determine output filename
                filename = file_path.stem
                if prefix:
                    filename = f"{prefix}{filename}"
                if suffix:
                    filename = f"{filename}{suffix}"
                
                # Convert file
                pdf_path = self.convert_to_pdf(str(file_path), filename, output_dir)
                if pdf_path:
                    converted_files.append(pdf_path)
                    
            except Exception as e:
                self.logger.error(f"Error converting {file_path}: {e}")
                continue
        
        self.logger.info(f"Successfully converted {len(converted_files)} files")
        return converted_files 