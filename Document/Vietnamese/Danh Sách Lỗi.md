# Hướng dẫn kiểm tra Simulator-CLI

## Giới thiệu
Mục đích của hướng dẫn này là hỗ trợ người dùng kiểm tra công cụ Simulator-CLI, xác định các lỗi tiềm ẩn và cung cấp các bước chi tiết về cách khắc phục sự cố. Tài liệu này rất quan trọng để đảm bảo thiết lập và hoạt động trơn tru của công cụ.

## Lỗi thường gặp và khắc phục sự cố

### 1. Lỗi: `Environment Variables Not Set`

**Mô tả:**
Một trong những sự cố phổ biến nhất khi chạy CLI là thiếu biến môi trường. Nếu bạn gặp lỗi cho biết lệnh `QORE` không được nhận dạng hoặc không chạy được, điều này có nghĩa là biến môi trường chưa được định cấu hình đúng.

**Nguyên nhân:**
Hệ thống không thể tìm thấy đường dẫn `C:\Windows\Software\QORE` và do đó, không thể nhận dạng lệnh `QORE`.

**Giải pháp:**
1. Mở **Bảng điều khiển** và điều hướng đến **Hệ thống và bảo mật**.
2. Nhấp vào **Hệ thống**, sau đó chọn **Cài đặt hệ thống nâng cao** trên bảng điều khiển bên trái.
3. Trong cửa sổ **System Properties**, nhấp vào nút **Environment Variables**.
4. Trong **System variables**, cuộn đến **Path** và nhấp vào **Edit**.
5. Thêm `C:\Windows\Software\QORE` vào cuối danh sách.
6. Nhấn **OK** và khởi động lại dấu nhắc lệnh của bạn.
7. Xác minh môi trường bằng cách nhập `QORE -list` trong dấu nhắc lệnh.

**Lưu ý:** Đảm bảo đặt cả **System Variables** và **User Variables** nếu lỗi vẫn tiếp diễn.

### 2. Lỗi: `File Not Found` đối với XML hoặc tệp Batch

**Mô tả:**
Bạn có thể gặp lỗi chỉ ra các tệp `.xml` hoặc `.bat` bị thiếu trong thư mục `QORE` khi chạy các lệnh như `QORE -list`.

**Nguyên nhân:**
Cấu hình XML cần thiết hoặc các tệp tập lệnh `.bat` không có trong thư mục chính xác, thường là `C:\Windows\Software\QORE\XML` hoặc `C:\Windows\Software\QORE\cmd`.

**Giải pháp:**
1. Đảm bảo rằng các tệp `.xml` cần thiết có trong thư mục `C:\Windows\Software\QORE\XML`.
2. Tương tự, các tệp `.bat` phải nằm trong `C:\Windows\Software\QORE\cmd`.
3. Nếu các tệp bị thiếu, hãy tải xuống từ nguồn thích hợp hoặc tạo thủ công cấu trúc bắt buộc.
4. Chạy lại lệnh sau khi xác minh vị trí tệp.

### 3. Lỗi: `Permission Denied` hoặc `Access Denied`

**Mô tả:**
Khi chạy chương trình, đặc biệt là trong quá trình thiết lập biến môi trường, bạn có thể gặp phải lỗi cấp phép ngăn chặn việc thay đổi cài đặt hệ thống.

**Nguyên nhân:**
Điều này thường xảy ra do không có quyền quản trị.

**Giải pháp:**
1. Đóng dấu nhắc lệnh hoặc thiết bị đầu cuối hiện tại.
2. Mở dấu nhắc lệnh hoặc cửa sổ PowerShell mới **với tư cách là quản trị viên**.
- Nhấp chuột phải vào biểu tượng Dấu nhắc lệnh hoặc PowerShell và chọn **Chạy với tư cách quản trị viên**.
3. Chạy lại lệnh gây ra sự cố về quyền.
4. Nếu bạn đang sửa đổi đường dẫn hệ thống hoặc sổ đăng ký, thì cần có quyền quản trị.

### 4. Lỗi: `Không tìm thấy đường dẫn sổ đăng ký`

**Mô tả:**
Khi chạy `set_system_environment`, bạn có thể gặp lỗi cho biết đường dẫn hệ thống không thể cập nhật do thiếu đường dẫn sổ đăng ký.

**Nguyên nhân:**
Lỗi này xảy ra khi khóa sổ đăng ký cho biến môi trường không tồn tại hoặc không thể truy cập được.

**Giải pháp:**
1. Mở **Trình chỉnh sửa sổ đăng ký** bằng cách nhập `regedit` vào thanh tìm kiếm của Windows.
2. Điều hướng đến `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment`.
3. Nhấp chuột phải vào **Environment** và chọn **New** > **String Value**.
4. Đặt tên cho chuỗi mới là `Path` và đặt giá trị của nó thành `C:\Windows\Software\QORE`.
5. Thoát khỏi Registry Editor và thử chạy lại lệnh CLI.

### 5. Lỗi: `Invalid Command in cnf.ini`

**Mô tả:**
Trong khi chạy công cụ, lỗi có thể xảy ra khi đọc lệnh từ tệp `cnf.ini`, đặc biệt là nếu có các mục nhập không hợp lệ hoặc không đúng định dạng.

**Nguyên nhân:**
Lỗi này xảy ra khi tệp `cnf.ini` chứa các ký tự không hợp lệ, định dạng không đúng hoặc thiếu các phần.

**Giải pháp:**
1. Điều hướng đến `C:\Windows\Software\QORE\env\cnf.ini`.
2. Mở tệp `cnf.ini` trong trình soạn thảo văn bản (như Notepad++ hoặc Visual Studio Code).
3. Đảm bảo rằng phần `[commands]` có mặt và mỗi lệnh tuân theo đúng định dạng:
```
[commands]
version = Phiên bản ứng dụng
list = Hiển thị các lệnh khả dụng
fix-problem = Kiểm tra và tạo các thư mục cần thiết
set-env = Đặt biến môi trường hệ thống
```
4. Sửa mọi sự cố định dạng và lưu tệp.
5. Chạy lại công cụ CLI.

### 6. Lỗi: `Lỗi giải mã Unicode trong cnf.ini`

**Mô tả:**
Lỗi này có thể phát sinh khi cố gắng phân tích cú pháp tệp `cnf.ini`, đặc biệt là khi tệp chứa các ký tự không phải ASCII khiến trình phân tích cú pháp không thành công.

**Nguyên nhân:**
Điều này có thể xảy ra nếu tệp `cnf.ini` được lưu ở định dạng không phải UTF-8 hoặc nếu tệp chứa các ký tự không thể giải mã đúng cách.

**Giải pháp:**
1. Mở `cnf.ini` trong trình soạn thảo văn bản.
2. Lưu tệp với mã hóa UTF-8:
- Trong Notepad++, hãy vào **Mã hóa** > **Chuyển đổi sang UTF-8**.
- Lưu và đóng tệp.
3. Thử lại lệnh.

### 7. Lỗi: `Tệp hàng loạt không thực thi`

**Mô tả:**
Khi cố gắng thực thi tệp `.bat` từ CLI, lệnh có thể không thành công và không có gì xảy ra.

**Nguyên nhân:**
Điều này thường xảy ra nếu đường dẫn đến tệp `.bat` không chính xác hoặc nếu bản thân tệp hàng loạt có vấn đề như lệnh không hợp lệ.

**Giải pháp:**
1. Kiểm tra lại đường dẫn đến tệp `.bat` để đảm bảo đường dẫn chính xác.
2. Đảm bảo rằng tệp `.bat` chứa các lệnh hợp lệ bằng cách mở tệp trong trình soạn thảo văn bản.
3. Nếu cần, hãy chạy tệp `.bat` trực tiếp từ dòng lệnh bằng cách sử dụng `call` để kiểm tra xem có lỗi nào không.

### 8. Lỗi: `Lệnh không được nhận dạng`

**Mô tả:**
Khi nhập `QORE -list` hoặc bất kỳ lệnh nào khác, bạn sẽ nhận được lỗi cho biết lệnh không được nhận dạng.

**Nguyên nhân:**
Lỗi này xảy ra khi các biến môi trường chưa được thiết lập đúng cách hoặc công cụ không nằm trong thư mục chính xác.

**Giải pháp:**
1. Đảm bảo rằng công cụ đã được đặt trong thư mục `C:\Windows\Software\QORE`.
2. Làm theo hướng dẫn thiết lập biến môi trường được cung cấp trong hướng dẫn này.
3. Khởi động lại dấu nhắc lệnh và thử lại lệnh.

## Hướng dẫn từng bước để sửa lỗi

### Thiết lập biến môi trường
1. Mở **Bảng điều khiển**.
2. Chọn **Hệ thống và bảo mật** > **Hệ thống** > **Cài đặt hệ thống nâng cao**.
3. Trong **Thuộc tính hệ thống**, nhấp vào **Biến môi trường**.
4. Chỉnh sửa biến **Đường dẫn** trong **Biến hệ thống** và thêm `C:\Windows\Software\QORE`.
5. Khởi động lại dấu nhắc lệnh và nhập `QORE -list` để xác nhận thiết lập.

### Sửa lỗi thủ công các sự cố liên quan đến sổ đăng ký
Nếu bạn gặp sự cố liên quan đến sổ đăng ký hệ thống khi thiết lập môi trường, hãy làm theo các bước sau:
1. Mở **Registry Editor** (`regedit`).
2. Điều hướng đến `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment`.
3. Xác minh rằng `Path` tồn tại và chứa mục nhập chính xác cho `C:\Windows\Software\QORE`.
4. Nếu mục nhập bị thiếu, hãy tạo thủ công và thêm đường dẫn chính xác.

## Liên hệ và hỗ trợ
Để được hỗ trợ thêm, vui lòng liên hệ với nhóm hỗ trợ theo địa chỉ **miko@wibu.me**.

Chúng tôi ở đây để đảm bảo rằng trải nghiệm của bạn với **Simulator-CLI** diễn ra suôn sẻ và không có lỗi!