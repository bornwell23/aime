import subprocess
import logging
import multiprocessing
import os
import difflib
import sys
import io
import re
from pathlib import Path
from typing import List, Tuple, Optional
import autopep8
from datetime import datetime


FIX = False
docker_command = ["docker-compose", "build"] # "--no-cache"
flake8_command = ["flake8", "--ignore=W293,E501,F841,F401"]
pylint_command = ["pylint", "--disable=C,R,W", "--enable=E", "--ignore=tests"]


def setup_logging(base_log_dir: Path, name: str) -> logging.Logger:
    """
    Set up logging for a specific service with file and console handlers.
    
    Args:
        base_log_dir (Path): Base directory for logs
        name (str): Name of the service being logged
    
    Returns:
        logging.Logger: Configured logger for the service
    """
    # Create logger
    logger = logging.getLogger(f"DockerImageFixer.{name}")
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("%(asctime)s - %(processName)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)
    
    # File handler for main log
    main_log_file = Path(base_log_dir, f"{name}.log")
    file_handler = logging.FileHandler(main_log_file, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter("%(asctime)s - %(processName)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    
    # Clear any existing handlers to prevent duplicate logs
    logger.handlers.clear()
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


class DockerImageFixer:
    def __init__(self, base_log_dir: Path, service_name: str):
        self.service_name = service_name
        self.logger = setup_logging(base_log_dir, service_name)
        self.base_log_dir = base_log_dir
    
    def show_diff(self, file_path: str, original: str, fixed: str):
        """Show a unified diff of the changes."""
        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            fixed.splitlines(keepends=True),
            fromfile=f"{file_path} (before)",
            tofile=f"{file_path} (after)"
        )
        diff_text = ''.join(diff)
        if diff_text:
            self.logger.debug(f"Changes in {file_path}:\n{diff_text}")
            
            # Log diff to a separate file
            diff_log_file = Path(self.base_log_dir, f"{self.service_name}_diffs.log")
            with open(diff_log_file, 'a') as f:
                f.write(f"\n--- Diff for {file_path} ---\n{diff_text}\n")

    def fix_python_file(self, file_path: str) -> bool:
        """Fix PEP8 issues in a Python file using autopep8."""
        try:
            with open(file_path, 'r', encoding="utf-8") as f:
                content = f.read()
            
            fixed_content = content
            fixed_content = autopep8.fix_code(
                content,
                options={
                    "aggressive": 1,
                    "ignore": [
                        "W293", "E501", "F841"
                    ],
                    "verbose": 0
                }
            )
            
            if content != fixed_content:
                self.show_diff(file_path, content, fixed_content)

                if FIX:
                    self.logger.info(f"Fixing {file_path}")
                    with open(file_path, 'w', encoding="utf-8") as f:
                        f.write(fixed_content)
                else:
                    self.logger.info(f"{file_path} needs to be fixed")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error fixing {file_path}: {str(e)}")
            return False

    def find_python_files(self) -> List[str]:
        """Find all Python files in the service directory."""
        python_files = []
        for root, _, files in os.walk(self.service_name):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))
        return python_files

    def fix_pep8_issues(self) -> int:
        """Fix PEP8 issues in all Python files in the service directory."""
        python_files = self.find_python_files()
        fixed_count = 0
        if not FIX:
            self.logger.info(f"Found {len(python_files)} {self.service_name} python files to fix but FIX is set to False, view {self.base_log_dir}/{self.service_name}_diffs.log for details, and run with --fix to fix")
        else:
            self.logger.info(f"Found {len(python_files)} {self.service_name} python files to fix")
        for file_path in python_files:
            if self.fix_python_file(file_path):
                fixed_count += 1
        
        return fixed_count

    def build_image(self) -> Tuple[bool, str]:
        """Build the Docker image and return success status and output."""
        try:
            self.logger.info(f"Building {self.service_name} image")           
            proc = subprocess.run(docker_command + [self.service_name], capture_output=True)
            output = proc.stdout.decode("utf-8")
            if proc.returncode != 0 or ("Running pylint" in output and "did not complete successfully" in output):
                self.logger.error(f"{self.service_name} build failed")
                self.logger.debug(f"Build output: {output}")
                return False, output
            
            self.logger.info(f"Successfully built {self.service_name} image")
            return True, output
            
        except Exception as e:
            error_msg = f"Error building {self.service_name}: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg


def check_service_syntax(service):
    proc = subprocess.run(flake8_command + [service], capture_output=True)
    flake_output =  proc.stdout.decode("utf-8")
    re_str = r"[FEW](\d){1,3}"
    errors_found = sum(1 for _ in re.finditer(re_str, flake_output))
    return errors_found


def process_service(base_log_dir: Path, service: str) -> Tuple[str, bool, str, int]:
    """Process a single service in a separate process."""
    fixer = DockerImageFixer(base_log_dir, service)
    
    success = True
    fixed_count = errors_found = 0
    output = ""


    success, output = fixer.build_image()
    if not success:
        errors_found = check_service_syntax(service)
        fixer.logger.info(f"{service} has {errors_found} errors before fixing")

        fixed_count = fixer.fix_pep8_issues()
        success, output = fixer.build_image()
        if not success:
            errors_found = check_service_syntax(service)
            fixer.logger.info(f"{service} has {errors_found} errors after fixing")
            proc = subprocess.run(flake8_command + [service], capture_output=True)
            flake_output =  proc.stdout.decode("utf-8")
            output += f"Flake8 output:\n{flake_output}\n"
            proc = subprocess.run(pylint_command + [service], capture_output=True)
            pylint_output = proc.stdout.decode("utf-8")
            output += f"Pylint output:\n{pylint_output}\n"
           
        build_log_file = Path(base_log_dir, f"{service}.log")
        with open(build_log_file, 'w', encoding="utf-8") as log_file:
            log_file.write(output)
    
    return service, success, output, errors_found, fixed_count


def create_logging():
    # Create timestamped log directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_log_dir = Path("test", "logs", timestamp)
    base_log_dir.mkdir(parents=True, exist_ok=True)
    
    # Global logger
    global_logger = setup_logging(base_log_dir, "main")

    return base_log_dir, global_logger


def main(base_log_dir, global_logger):
    # Define services to build
    services = [
        "ui",
        "server",
        "auth-service"
    ]
    
    # Create a pool of workers
    with multiprocessing.Pool() as pool:
        # Pass the base log directory to each process
        results = pool.starmap(process_service, [(base_log_dir, service) for service in services])
    
    # Process results
    all_successful = True
    for service_name, success, output, errors_found, fixed_count in results:
        if success:
            global_logger.info(f"{service_name} is fixed, {errors_found} errors found, {fixed_count} files fixed")
        else:
            all_successful = False
            global_logger.error(f"{service_name} needs to be fixed, {errors_found} errors found, {fixed_count} files fixed. View {base_log_dir}/{service_name}.log for details. Run {' '.join(flake8_command)} {service_name} to view remaining errors.")
            global_logger.debug(f"Build output: {output}")
    
    return all_successful

if __name__ == "__main__":
    if "--help" in sys.argv:
        print("Usage: python test_docker_builds.py [--fix] [--dontfix] [service_name]. Run without service_name to build/fix all services.")
        sys.exit(0)
    if "--fix" in sys.argv:
        FIX = True
        sys.argv.remove("--fix")
    if "--dontfix" in sys.argv:
        FIX = False
        sys.argv.remove("--dontfix")
    

    # for testing purposes
    # sys.argv.append("server")

    base_log_dir, global_logger = create_logging()

    if len(sys.argv) > 1:
        service_name = sys.argv[1]
        if service_name in ["ui", "server", "auth-service"]:
            service_name, success, output, errors_found, fixed_count = process_service(base_log_dir, service_name)
            if success:
                global_logger.info(f"{service_name} is fixed, {errors_found} errors found, {fixed_count} files fixed")
            else:
                global_logger.error(f"{service_name} needs to be fixed, {errors_found} errors found, {fixed_count} files fixed. View {base_log_dir}/{service_name}.log for details. Run '{' '.join(flake8_command)} {service_name}' to view remaining errors.")
                global_logger.debug(f"Build output: {output}")
        else:
            global_logger.error(f"Unknown service: {service_name}")
            success = False
    else:
        success = main(base_log_dir, global_logger)
    exit(0 if success else 1)
