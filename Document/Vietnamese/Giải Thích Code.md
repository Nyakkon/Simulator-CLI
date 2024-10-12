
# **README (Tiếng Việt)**

## **Giới thiệu**
Ứng dụng CLI "QORE" là một ứng dụng dòng lệnh (CLI) giúp quản lý và tự động hóa các tác vụ bằng cách chạy các tệp `.bat` thông qua XML cấu hình. Nó hỗ trợ các lệnh từ các tệp XML và cấu hình từ tệp `cnf.ini`, cung cấp cho người dùng khả năng tạo ra các lệnh tùy chỉnh dựa trên yêu cầu của dự án.

### **Cấu trúc Dự Án**
```
C:\Windows\Software\QORE\
    ├── cmd/               # Chứa các file .bat
    ├── env/               # Chứa file cấu hình cnf.ini
    ├── XML/               # Chứa các file XML định nghĩa lệnh
    └── main.py            # File Python chính để xử lý CLI
```

---

## **Giải thích chi tiết từng phần của code**

### **1. Đọc và tải các mô tả lệnh từ `cnf.ini`**

```python
def load_command_descriptions():
    '''Đọc các định nghĩa lệnh từ tệp C:\Windows\Software\QORE\env\cnf.ini'''
    config = configparser.ConfigParser()
    cnf_path = r'C:\Windows\Software\QORE\env\cnf.ini'
```

- **Mục đích:** Hàm này đọc các định nghĩa lệnh từ tệp `cnf.ini`, được lưu trong thư mục `env`. Hàm này kiểm tra xem tệp `cnf.ini` có tồn tại không, và sau đó lấy các mô tả lệnh từ phần `[commands]` trong tệp.

```python
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
```

- **Hoạt động:** Nếu không tìm thấy tệp `cnf.ini`, hàm này sẽ trả về một thông báo lỗi. Nếu tệp tồn tại, nó sẽ đọc và trả về các lệnh được định nghĩa trong tệp cấu hình.

### **2. Kiểm tra tên lệnh hợp lệ**

```python
def is_valid_name(name):
    '''Kiểm tra tên hợp lệ, chỉ chứa chữ cái, số, và dấu gạch ngang'''
    return re.match(r'^[a-zA-Z0-9-_]+$', name) is not None
```

- **Mục đích:** Hàm này đảm bảo rằng tên lệnh chỉ chứa các ký tự hợp lệ như chữ cái, số và dấu gạch ngang.

### **3. Đọc file XML để lấy lệnh**

```python
def parse_xml(file_path):
    '''Đọc file XML và trả về Name, Description, và đường dẫn file .bat'''
    tree = ET.parse(file_path)
    root = tree.getroot()
    name = root.find('Name').text if root.find('Name') is not None else 'N/A'
    description = root.find('Description').text if root.find('Description') is not None else 'N/A'
    dat_path = root.find('DatFilePath').text if root.find('DatFilePath') is not None else 'N/A'
    dat_path = os.path.join(r'C:\Windows\Software\QORE\cmd', dat_path)
    return name, description, dat_path
```

- **Mục đích:** Hàm này phân tích file XML để lấy thông tin về tên lệnh, mô tả và đường dẫn tới file `.bat` cần thực thi.

### **4. In ra danh sách các lệnh với mô tả từ `cnf.ini` và XML**

```python
def print_command_help(names_from_xml, command_descriptions):
    '''In ra danh sách tất cả các lệnh với mô tả từ tệp cnf.ini'''
    print("Options (and corresponding environment variables):")
    
    for command, description in command_descriptions.items():
        print(f"-{command}      : {description}")
    for name, (description, _) in names_from_xml.items():
        print(f"-{name}      : {description}")
```

- **Mục đích:** Hàm này in ra tất cả các lệnh có sẵn từ cả hai nguồn: tệp cấu hình `cnf.ini` và các file XML.

---

## **5. Tạo thư mục nếu chưa tồn tại**
```python
def fix_problem():
    folders = ['XML', 'cmd']
    for folder in folders:
        if not os.path.exists(folder):
            print(f"Tạo thư mục {folder}...")
            os.makedirs(folder)
        else:
            print(f"Thư mục {folder} đã tồn tại.")
```
- **Mục đích:** Hàm này tạo các thư mục `XML` và `cmd` nếu chúng chưa tồn tại để đảm bảo không xảy ra lỗi khi chương trình chạy.

### **6. Thiết lập biến môi trường hệ thống**

```python
def set_system_environment():
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
```

- **Mục đích:** Hàm này thêm đường dẫn của `QORE` vào biến môi trường `PATH` để có thể chạy ứng dụng từ bất kỳ vị trí nào trong hệ thống.

---

## **7. Làm sạch biến PATH**
```python
def clean_path():
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
            current_path, _ = winreg.QueryValueEx(key, 'Path')
            clean_path = current_path.replace(';;', ';').rstrip(';') + ';'
            winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, clean_path)
    except PermissionError:
        print("Err: Clear Fail (x2010)")
```

- **Mục đích:** Làm sạch biến môi trường PATH để loại bỏ các dấu phân cách thừa và đảm bảo các đường dẫn được cấu hình chính xác.

---

## **8. Hàm chính (main)**
```python
def main():
    command_descriptions = load_command_descriptions()
    names_from_xml = get_names_from_xml_folder()
    parser = argparse.ArgumentParser(description="QORE - Ứng dụng CLI cho quản lý và tự động hóa tác vụ.")
    parser.add_argument('-version', action='version', version='App 1.0')
    parser.add_argument('-list', action='store_true', help="Duyệt và in thông tin từ các file XML")
    parser.add_argument('-fix-problem', action='store_true', help="Kiểm tra và tạo thư mục XML và cmd nếu chưa tồn tại")
    parser.add_argument('-set-env', action='store_true', help="Thiết lập biến môi trường QORE để gọi từ CMD")

    for name in names_from_xml.keys():
        parser.add_argument(f'-{name}', action='store_true', help=f"Chạy file .bat từ {name}")

    args = parser.parse_args()
    if args.fix_problem:
        fix_problem()
    if args.set_env:
        set_system_environment()
        clean_path()
    if args.list:
        print_command_help(names_from_xml, command_descriptions)
    for name, (_, dat_path) in names_from_xml.items():
        if getattr(args, name):
            run_bat_from_name(dat_path)

if __name__ == '__main__':
    main()
```

- **Chức năng:** 
  - **load_command_descriptions:** Tải các mô tả lệnh từ tệp cấu hình.
  - **get_names_from_xml_folder:** Lấy các lệnh từ các file XML.
  - **argparse:** Phân tích và xử lý các đối số dòng lệnh.
  - **run_bat_from_name:** Chạy file `.bat` tương ứng với lệnh đã chọn.

---

