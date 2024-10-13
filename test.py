import argparse
import os
import xml.etree.ElementTree as ET
import winreg
import re
import configparser

def load_command_descriptions():
    """Đọc các định nghĩa lệnh từ tệp C:\Windows\Software\QORE\env\cnf.ini"""
    config = configparser.ConfigParser()
    cnf_path = r'C:\Windows\Software\QORE\env\cnf.ini'

    if os.path.exists(cnf_path):
        # Đọc tệp với mã hóa utf-8
        with open(cnf_path, 'r', encoding='utf-8') as configfile:
            config.read_file(configfile)
        
        if 'commands' in config:
            return config['commands']
        else:
            print("Err: Không tìm thấy phần 'commands' trong tệp cnf.ini")
            return {}
    else:
        print(f"Err: Không tìm thấy tệp cnf.ini tại {cnf_path}")
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
    dat_path = os.path.join(r'C:\Windows\Software\QORE\cmd', dat_path)  # Đường dẫn tuyệt đối tới 'cmd'
    
    return name, description, dat_path

def get_names_from_xml_folder():
    """Duyệt qua các file XML trong thư mục 'XML' và trả về danh sách các tên từ thẻ 'Name'"""
    xml_folder = r'C:\Windows\Software\QORE\XML'
    names = {}

    if not os.path.exists(xml_folder):
        print(f"Err: Thư mục {xml_folder} không tồn tại. (x2910)")
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
                    print(f"Err: Tham số '{name}' không hợp lệ, bỏ qua file {xml_file} với tham số là '{name}'. Mã: [x3902]")
            except Exception as e:
                print(f"Err: Không thể xử lý tệp XML. Lỗi: [x9320]")
    return names

def run_bat_from_name(dat_file):
    """Thực thi file .bat tương ứng với tên đã chọn"""
    full_path = os.path.abspath(dat_file)  # Lấy đường dẫn tuyệt đối
    
    if os.path.exists(full_path):
        os.system(f'call {full_path}')
    else:
        print(f"Err: File .bat {full_path} không tồn tại (x9338)")

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
        print("Lỗi: Bạn cần quyền quản trị để thay đổi biến môi trường hệ thống.")

def clean_path():
    """Làm sạch biến PATH trong Registry"""
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
            current_path, _ = winreg.QueryValueEx(key, 'Path')
            clean_path = current_path.replace(';;', ';').rstrip(';') + ';'
            winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, clean_path)
    except PermissionError:
        print("Err: Clear Fail (x2010)")

def main():
    # Lấy mô tả các lệnh từ tệp cnf.ini
    command_descriptions = load_command_descriptions()

    # Lấy các tên từ file XML
    names_from_xml = get_names_from_xml_folder()

    # Tạo đối tượng ArgumentParser
    parser = argparse.ArgumentParser(description="QORE - Ứng dụng CLI cho quản lý và tự động hóa tác vụ.")
    
    # Thêm tùy chọn -version để hiển thị phiên bản ứng dụng
    parser.add_argument('-version', action='version', version='App 1.0')
    
    # Thêm tùy chọn -list để in ra danh sách Name và Description
    parser.add_argument('-list', action='store_true', help="Duyệt và in thông tin từ các file XML")

    # Thêm tùy chọn -fix-problem để tạo thư mục nếu cần
    parser.add_argument('-fix-problem', action='store_true', help="Kiểm tra và tạo thư mục XML và cmd nếu chưa tồn tại")

    # Thêm tùy chọn -set-env để thiết lập biến môi trường hệ thống
    parser.add_argument('-set-env', action='store_true', help="Thiết lập biến môi trường QORE để gọi từ CMD")

    # Thêm tùy chọn để cho phép các đối số CLI tùy chỉnh
    parser.add_argument('-custom_cli_in_xml', type=str, help="Thực thi lệnh tùy chỉnh CLI với chuỗi người dùng truyền vào.")

    # Parse các tham số dòng lệnh
    args = parser.parse_args()

    # Nếu -fix-problem được cung cấp, kiểm tra và tạo thư mục XML và cmd nếu chưa tồn tại
    if args.fix_problem:
        fix_problem()

    # Nếu -set-env được cung cấp, thiết lập biến môi trường
    if args.set_env:
        set_system_environment()
        clean_path()

    # Nếu -list được cung cấp, in ra danh sách Name và Description từ XML
    if args.list:
        print_command_help(names_from_xml, command_descriptions)
    
    # Kiểm tra và chạy lệnh tùy chỉnh CLI nếu tham số được cung cấp
    if args.custom_cli_in_xml:
        print(f"Executing custom CLI command with argument: {args.custom_cli_in_xml}")
        # Run any custom logic or process here based on args.custom_cli_in_xml

    # Kiểm tra và chạy file .bat tương ứng nếu tham số được cung cấp
    for name, (_, dat_path) in names_from_xml.items():
        if getattr(args, name):
            run_bat_from_name(dat_path)

if __name__ == '__main__':
    main()
