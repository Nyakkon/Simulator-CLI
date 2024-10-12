
# Ứng dụng CLI QORE

## Tổng Quan

Script này là một công cụ giao diện dòng lệnh (CLI) để quản lý và tự động hóa các tác vụ trong hệ thống. Nó sử dụng các tệp cấu hình ở định dạng XML và `.ini`, được đặt trong thư mục `C:\Windows\Software\QORE`. Công cụ cho phép thực thi các tệp `.bat`, thiết lập biến môi trường hệ thống, và cung cấp danh sách các lệnh có sẵn.

### Chi Tiết Mã Lệnh

#### 1. `load_command_descriptions()`
Hàm này tải mô tả lệnh từ tệp `C:\Windows\Software\QORE\env\cnf.ini`.

- **Mục Đích:** Đọc các lệnh được định nghĩa trong tệp `.ini` để mô tả chức năng của mỗi lệnh.
- **Cách Thức:**
    - Đọc tệp `cnf.ini` sử dụng module `configparser`.
    - Trả về danh sách các lệnh tìm thấy trong phần `[commands]`.
    - Xử lý lỗi trong trường hợp tệp `.ini` hoặc phần lệnh không tồn tại.

#### 2. `is_valid_name(name)`
Hàm này kiểm tra xem tên có chứa các ký tự hợp lệ (chữ cái, số, dấu gạch ngang và dấu gạch dưới) hay không.

- **Mục Đích:** Đảm bảo rằng chỉ những tên lệnh hợp lệ mới được sử dụng.
- **Cách Thức:**
    - Sử dụng biểu thức chính quy để kiểm tra các ký tự cho phép.

#### 3. `parse_xml(file_path)`
Hàm này phân tích một tệp XML để lấy ra tên lệnh, mô tả và đường dẫn đến tệp `.bat`.

- **Mục Đích:** Đọc các tệp XML trong thư mục `C:\Windows\Software\QORE\XML`, chứa chi tiết về từng lệnh.
- **Cách Thức:**
    - Lấy ra `Name`, `Description`, và đường dẫn tới tệp `.bat` (`DatFilePath`).
    - Tạo đường dẫn tuyệt đối đến thư mục `cmd` nơi chứa các tệp `.bat`.

#### 4. `get_names_from_xml_folder()`
Hàm này duyệt qua tất cả các tệp XML trong thư mục `C:\Windows\Software\QORE\XML` để tạo danh sách tên lệnh hợp lệ.

- **Mục Đích:** Thu thập các lệnh từ các tệp XML và kiểm tra chúng bằng hàm `is_valid_name()`.
- **Cách Thức:**
    - Đọc tất cả các tệp XML trong thư mục và phân tích nội dung của chúng.
    - Chỉ thêm những lệnh hợp lệ vào danh sách.

#### 5. `run_bat_from_name(dat_file)`
Hàm này thực thi tệp `.bat` tương ứng với lệnh đã chọn.

- **Mục Đích:** Chạy tệp `.bat` cho mỗi lệnh.
- **Cách Thức:**
    - Chuyển đổi đường dẫn tương đối thành tuyệt đối.
    - Sử dụng `os.system()` để gọi tệp `.bat`.

#### 6. `print_command_help(names_from_xml, command_descriptions)`
Hàm này in ra tất cả các lệnh có sẵn kèm theo mô tả từ tệp cnf.ini.

- **Mục Đích:** Cung cấp danh sách các lệnh từ cả tệp `.ini` và các tệp XML.
- **Cách Thức:**
    - In ra các lệnh được định nghĩa trong tệp `cnf.ini`.
    - In ra các lệnh từ thư mục XML.

#### 7. `fix_problem()`
Hàm này đảm bảo rằng các thư mục cần thiết (`XML` và `cmd`) tồn tại.

- **Mục Đích:** Đảm bảo rằng script có thể tạo và lưu trữ tệp trong các thư mục đúng.
- **Cách Thức:**
    - Kiểm tra xem các thư mục có tồn tại không và tạo chúng nếu chưa có.

#### 8. `set_system_environment()`
Hàm này thêm đường dẫn tới thư mục `QORE` vào biến môi trường `PATH` của hệ thống.

- **Mục Đích:** Để cho phép các lệnh `QORE` có thể được gọi từ bất kỳ thư mục nào trên dòng lệnh.
- **Cách Thức:**
    - Mở Windows Registry để thay đổi biến `PATH`.

#### 9. `clean_path()`
Hàm này làm sạch biến `PATH` của hệ thống bằng cách loại bỏ các mục nhập trùng lặp hoặc không hợp lệ.

- **Mục Đích:** Đảm bảo rằng biến `PATH` được định dạng đúng.
