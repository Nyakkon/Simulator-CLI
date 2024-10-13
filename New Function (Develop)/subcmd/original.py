import argparse
import os
import xml.etree.ElementTree as ET
import winreg
import re
import configparser

# Đường dẫn tới tệp cmd.ini và show.ini
CMD_INI_PATH = r'C:\Windows\Software\QORE\env\cmd.ini'
SHOW_INI_PATH = r'C:\Windows\Software\QORE\env\show.ini'

# Đường dẫn tới thư mục cmd
CMD_FOLDER_PATH = r'C:\Windows\Software\QORE\cmd'

def load_command_descriptions():
    """Đọc các định nghĩa lệnh từ tệp cnf.ini"""
    config = configparser.ConfigParser()
    cnf_path = r'C:\Windows\Software\QORE\env\cnf.ini'

    if os.path.exists(cnf_path):
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

def run_bat_from_name(bat_file, arg=None):
    """Thực thi file .bat tương ứng với subcommand đã chọn"""
    full_path = os.path.abspath(os.path.join(CMD_FOLDER_PATH, bat_file))

    if os.path.exists(full_path):
        if arg:
            os.system(f'call {full_path} {arg}')
        else:
            os.system(f'call {full_path}')
    else:
        print(f"Err: File .bat {full_path} không tồn tại")

def save_command_to_show_ini(command_name, command_subs, description, bat_files):
    """Lưu lệnh và mô tả vào tệp show.ini với mã hóa UTF-8"""
    config = configparser.ConfigParser()
    if os.path.exists(SHOW_INI_PATH):
        config.read(SHOW_INI_PATH)
    else:
        with open(SHOW_INI_PATH, 'w', encoding='utf-8') as configfile:  # Đảm bảo mã hóa UTF-8 khi tạo tệp
            config.write(configfile)

    if not config.has_section('commands'):
        config.add_section('commands')

    # Lưu subcommands và file bat tương ứng
    for sub, bat in zip(command_subs, bat_files):
        config.set('commands', f'{command_name}_{sub}', f'{description} | Bat file: {bat}')

    with open(SHOW_INI_PATH, 'w', encoding='utf-8') as configfile:  # Ghi vào tệp với mã hóa UTF-8
        config.write(configfile)
    print(f"Đã lưu lệnh '{command_name}' với subcommands {command_subs} và các file bat '{bat_files}' vào show.ini")

def is_valid_name(name):
    """Kiểm tra tên hợp lệ, chỉ chứa chữ cái, số, và dấu gạch ngang"""
    return re.match(r'^[a-zA-Z0-9\-_]+$', name) is not None

def parse_xml(file_path):
    """Đọc file XML và trả về Name, Description, và đường dẫn file .bat"""
    tree = ET.parse(file_path)
    root = tree.getroot()

    name = root.find('Name').text if root.find('Name') is not None else 'N/A'
    description = root.find('Description').text if root.find('Description') is not None else 'N/A'
    dat_path = root.find('DatFilePath').text if root.find('DatFilePath') is not None else 'N/A'

    dat_path = os.path.join(CMD_FOLDER_PATH, dat_path)
    
    return name, description, dat_path

def get_names_from_xml_folder():
    """Duyệt qua các file XML trong thư mục 'XML' và trả về danh sách các tên từ thẻ 'Name'"""
    xml_folder = r'C:\Windows\Software\QORE\XML'
    names = {}

    if not os.path.exists(xml_folder):
        print(f"Err: Thư mục {xml_folder} không tồn tại.")
        return names

    for xml_file in os.listdir(xml_folder):
        if xml_file.endswith('.xml'):
            file_path = os.path.join(xml_folder, xml_file)
            try:
                name, description, dat_path = parse_xml(file_path)
                if is_valid_name(name):
                    valid_name = name.lower().replace('-', '_')
                    names[valid_name] = (description, dat_path)
                else:
                    print(f"Err: Tham số '{name}' không hợp lệ, bỏ qua file {xml_file}.")
            except Exception as e:
                print(f"Err: Không thể xử lý tệp XML.")
    return names

def print_command_help():
    """In ra danh sách tất cả các lệnh từ tệp show.ini"""
    config = configparser.ConfigParser()
    if os.path.exists(SHOW_INI_PATH):
        config.read(SHOW_INI_PATH)
        if config.has_section('commands'):
            print("Danh sách các lệnh:")
            for command, description in config.items('commands'):
                print(f"-{command}: {description}")
        else:
            print("Không tìm thấy phần 'commands' trong show.ini")
    else:
        print(f"Không tìm thấy tệp {SHOW_INI_PATH}")

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
        print("Err: Clear Fail")

def main():
    parser = argparse.ArgumentParser(description="QORE - Ứng dụng CLI cho quản lý và tự động hóa tác vụ.")

    # Thêm tùy chọn cho add_command
    parser.add_argument('-add_command', action='store_true', help="Thêm lệnh và mô tả vào show.ini")
    parser.add_argument('-command_name', type=str, help="Tên lệnh cần thêm")
    parser.add_argument('-command_sub', type=str, nargs='+', help="Danh sách subcommand cho lệnh chính")
    parser.add_argument('-description', type=str, help="Mô tả cho lệnh cần thêm")
    parser.add_argument('-bat', type=str, nargs='+', help="Danh sách file bat tương ứng với mỗi subcommand")

    # Các lệnh động (dynamic commands)
    args, unknown = parser.parse_known_args()

    # Xử lý các lệnh động từ subcommand đã lưu
    config = configparser.ConfigParser()
    if os.path.exists(SHOW_INI_PATH):
        config.read(SHOW_INI_PATH)
        if config.has_section('commands'):
            for key, value in config.items('commands'):
                command, sub = key.split('_', 1)
                if f'-{command}' in unknown and f'-{sub}' in unknown:
                    bat_file = value.split('|')[-1].strip().replace('Bat file: ', '')
                    sub_arg = unknown[unknown.index(f'-{sub}') + 1]
                    run_bat_from_name(bat_file, sub_arg)

    # Xử lý việc lưu lệnh vào show.ini
    if args.add_command and args.command_name and args.command_sub and args.description and args.bat:
        if len(args.command_sub) == len(args.bat):
            save_command_to_show_ini(args.command_name, args.command_sub, args.description, args.bat)
        else:
            print("Số lượng subcommands và file bat phải khớp nhau")

if __name__ == '__main__':
    main()
