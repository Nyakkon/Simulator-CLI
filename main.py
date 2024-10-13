import os
import datetime
import argparse
import xml.etree.ElementTree as ET
import winreg
import re
import configparser
import requests

# Error codes mapping (fixed codes for documentation purposes)
ERROR_CODES = {
    "MISSING_XML_FOLDER": "x2910",
    "INVALID_PARAM": "x3902",
    "BATCH_FILE_MISSING": "x9338",
    "CNF_FILE_MISSING": "x1010",
    "COMMANDS_SECTION_MISSING": "x2020",
    "PERMISSION_ERROR": "x4030",
    "PATH_CLEAN_FAIL": "x2010"
}

def log_error(error_message, error_code):
    """Log error messages to both the console and a file using UTF-8 encoding"""
    log_directory = r"C:\Windows\Software\QORE\log"
    os.makedirs(log_directory, exist_ok=True)  # Ensure the log directory exists
    log_file = os.path.join(log_directory, "error_log.txt")

    timestamp = datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] ERROR {error_code}: {error_message}"
    
    # Print the error message to the console
    print(f"Err: Không khả dụng, kiểm tra mã lỗi - {error_code}")

    # Write the error message to the log file using UTF-8 encoding
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(log_message + "\n")

def load_command_descriptions():
    r"""Đọc các định nghĩa lệnh từ tệp C:\Windows\Software\QORE\env\cnf.ini"""
    config = configparser.ConfigParser()
    cnf_path = r'C:\Windows\Software\QORE\env\cnf.ini'

    if os.path.exists(cnf_path):
        with open(cnf_path, 'r', encoding='utf-8') as configfile:
            config.read_file(configfile)
        
        if 'commands' in config:
            return config['commands']
        else:
            log_error("Không tìm thấy phần 'commands' trong tệp cnf.ini", ERROR_CODES["COMMANDS_SECTION_MISSING"])
            return {}
    else:
        log_error(f"Không tìm thấy tệp cnf.ini tại {cnf_path}", ERROR_CODES["CNF_FILE_MISSING"])
        return {}

def is_valid_name(name):
    """Kiểm tra tên hợp lệ, chỉ chứa chữ cái, số, và dấu gạch ngang"""
    return re.match(r'^[a-zA-Z0-9\-_]+$', name) is not None

def parse_xml(file_path):
    """Đọc file XML và trả về Name, Description, và đường dẫn file .bat"""
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Tìm các thẻ trong XML
    name = root.find('Name').text if root.find('Name') is not None else 'N/A'
    description = root.find('Description').text if root.find('Description') is not None else 'N/A'
    dat_path = root.find('DatFilePath').text if root.find('DatFilePath') is not None else 'N/A'

    # Tạo đường dẫn tới file .bat trong thư mục 'cmd'
    dat_path = os.path.join(r'C:\Windows\Software\QORE\cmd', os.path.basename(dat_path))  # Raw string to avoid warnings
    
    return name, description, dat_path

def get_names_from_xml_folder():
    """Duyệt qua các file XML trong thư mục 'XML' và trả về danh sách các tên từ thẻ 'Name'"""
    xml_folder = r'C:\Windows\Software\QORE\XML'
    names = {}

    if not os.path.exists(xml_folder):
        log_error(f"Thư mục {xml_folder} không tồn tại.", ERROR_CODES["MISSING_XML_FOLDER"])
        return names

    # In ra danh sách các tệp XML được tìm thấy trong thư mục
    for xml_file in os.listdir(xml_folder):
        if xml_file.endswith('.xml'):
            file_path = os.path.join(xml_folder, xml_file)
            try:
                name, description, dat_path = parse_xml(file_path)
                
                # Kiểm tra nếu tên hợp lệ, chỉ thêm vào nếu hợp lệ
                if is_valid_name(name):
                    valid_name = name.lower().replace('-', '_')
                    names[valid_name] = (description, dat_path)  # Lưu Name, Description và đường dẫn file .bat tương ứng
                else:
                    log_error(f"Tham số '{name}' không hợp lệ, bỏ qua file {xml_file}.", ERROR_CODES["INVALID_PARAM"])
            except Exception as e:
                log_error(f"Không thể xử lý tệp XML {xml_file}. Lỗi: {e}", ERROR_CODES["INVALID_PARAM"])
    return names

def run_bat_from_name(dat_file, custom_string=None):
    r"""Thực thi file .bat từ thư mục C:\Windows\Software\QORE\cmd với chuỗi tùy chỉnh"""
    full_path = os.path.abspath(dat_file)  # Lấy đường dẫn tuyệt đối
    
    if os.path.exists(full_path):
        # Chạy file .bat kèm theo custom string của người dùng nếu có
        if custom_string:
            os.system(f'call "{full_path}" {custom_string}')
        else:
            os.system(f'call "{full_path}"')
    else:
        log_error(f"File .bat {full_path} không tồn tại", ERROR_CODES["BATCH_FILE_MISSING"])

def print_command_help(names_from_xml, command_descriptions):
    """In ra danh sách tất cả các lệnh với mô tả từ tệp cnf.ini"""
    print("Options (and corresponding environment variables):")
    
    # In các lệnh được định nghĩa trong cnf.ini
    for command, description in command_descriptions.items():
        print(f"-{command}      : {description}")

    # In các lệnh từ XML sau
    for name, (description, _) in names_from_xml.items():
        print(f"-{name}      : {description}")

def fix_problem():
    """Kiểm tra xem thư mục XML và cmd có tồn tại không, nếu không thì tạo"""
    folders = ['XML', 'cmd']
    for folder in folders:
        if not os.path.exists(folder):
            print(f"Tạo thư mục {folder}...")
            os.makedirs(folder)
        else:
            print(f"Thư mục {folder} đã tồn tại.")

def set_system_environment():
    """Thiết lập biến môi trường hệ thống để có thể gọi QORE từ CMD"""
    QORE_path = r'C:\Windows\Software\QORE'
    
    try:
        # Mở khóa registry của hệ thống để chỉnh sửa biến PATH
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
            current_path, _ = winreg.QueryValueEx(key, 'Path')

            if QORE_path not in current_path:
                new_path = current_path + ";" + QORE_path
                winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)
                print(f"Đã thêm QORE vào biến môi trường PATH (Registry).")
            else:
                print(f"QORE đã tồn tại trong PATH")
    except PermissionError:
        log_error("Bạn cần quyền quản trị để thay đổi biến môi trường hệ thống.", ERROR_CODES["PERMISSION_ERROR"])

def clean_path():
    """Làm sạch biến PATH trong Registry"""
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
            current_path, _ = winreg.QueryValueEx(key, 'Path')
            clean_path = current_path.replace(';;', ';').rstrip(';') + ';'
            winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, clean_path)
    except PermissionError:
        log_error("Clear Fail.", ERROR_CODES["PATH_CLEAN_FAIL"])

def main():
    # Lấy mô tả các lệnh từ tệp cnf.ini
    command_descriptions = load_command_descriptions()

    # Lấy các tên từ file XML
    names_from_xml = get_names_from_xml_folder()

    # Tạo đối tượng ArgumentParser
    parser = argparse.ArgumentParser(description=r"QORE - Ứng dụng CLI cho quản lý và tự động hóa tác vụ.")
    
    # Thêm tùy chọn -version để hiển thị phiên bản ứng dụng
    parser.add_argument('-version', action='version', version='QORE 1.0.1 Updated (GMT +7) 11:40 13/10/2024')
    
    # Thêm tùy chọn -list để in ra danh sách Name và Description
    parser.add_argument('-list', action='store_true', help="Duyệt và in thông tin từ các file XML")

    # Thêm tùy chọn -fix-problem để tạo thư mục nếu cần
    parser.add_argument('-fix-problem', action='store_true', help="Kiểm tra và tạo thư mục XML và cmd nếu chưa tồn tại")

    # Thêm tùy chọn -set-env để thiết lập biến môi trường hệ thống
    parser.add_argument('-set-env', action='store_true', help="Thiết lập biến môi trường QORE để gọi từ CMD")
    
    parser.add_argument('-notification', action='store_true', help="Thông Báo")
    
    parser.add_argument('-error', action='store_true', help="lỗi từ local")
    parser.add_argument('-error-log-from-public-source', action='store_true', help="lỗi từ nguồn tổng")
    
    # Thêm tùy chọn -log-update để thiết lập biến môi trường hệ thống
    parser.add_argument('-changelog', action='store_true', help="Thông tin cập nhật")
    
    # Thêm tùy chọn tự động dựa trên thẻ 'Name' từ XML
    for name in names_from_xml.keys():
        parser.add_argument(f'-{name}', type=str, nargs='?', help=f"Chạy file .bat từ {name} với một chuỗi tùy chỉnh")

    # Parse các tham số dòng lệnh
    args = parser.parse_args()

    # Nếu -fix-problem được cung cấp, kiểm tra và tạo thư mục XML và cmd nếu chưa tồn tại
    if args.fix_problem:
        fix_problem()

    # Nếu -set-env được cung cấp, thiết lập biến môi trường
    if args.set_env:
        set_system_environment()
        clean_path()
    
    
    if args.changelog:
        url = "https://raw.githubusercontent.com/Nyakkon/Simulator-CLI/main/changelog.txt"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for request errors

            # Print the content of the changelog
            print(response.text)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the changelog: {e}")
            

    
    if args.error_log_from_public_source:
        url = "https://github.com/Nyakkon/Simulator-CLI/blob/main/Document/Log_error/log.txt"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for request errors

            # Print the content of the changelog
            print(response.text)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the changelog: {e}")

    # Nếu -list được cung cấp, in ra danh sách Name và Description từ XML
    if args.error:
        log_file_path = r"C:\Windows\Software\QORE\log\error_log.txt"
        try:
            # Open and read the log file
            with open(log_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                print(content)  # Print the content to the console
        except FileNotFoundError:
            print(f"File {log_file_path} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
    if args.list:
        print_command_help(names_from_xml, command_descriptions)
    
    # Kiểm tra và chạy file .bat tương ứng nếu tham số được cung cấp, kèm theo custom string nếu có
    for name, (_, dat_path) in names_from_xml.items():
        if getattr(args, name):
            custom_string = getattr(args, name)
            run_bat_from_name(dat_path, custom_string)

if __name__ == '__main__':
    main()
