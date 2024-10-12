
# Hướng Dẫn Sử Dụng Simulator-CLI

## Bước 1: Giải Nén Tệp
- Giải nén file **Simulator-CLI ver 1.0.0.zip**.
- Tạo thư mục mới tại đường dẫn **C:\Windows\Software\QORE**.
- Sau khi giải nén xong, dán toàn bộ nội dung đã giải nén vào thư mục **C:\Windows\Software\QORE**.

## Bước 2: Thiết Lập Biến Môi Trường

### Thiết Lập System Variable
1. Mở **Control Panel** và chọn **System and Security**.
2. Chọn **System**, sau đó nhấn vào **Advanced system settings** ở góc trái.
3. Trong hộp thoại **System Properties**, nhấn vào nút **Environment Variables**.
4. Trong phần **System Variables**, tìm mục **Path** và nhấn **Edit**.
5. Thêm **C:\Windows\Software\QORE** vào cuối danh sách.

   **Hình ảnh minh họa:**

   ![Thiết lập System Variable](image_path_system_variable.png)

### Thiết Lập User Variable
1. Tương tự như trên, trong hộp thoại **Environment Variables**, cuộn xuống **User Variables**.
2. Tìm hoặc thêm **Path** nếu chưa có, sau đó nhấn **Edit**.
3. Thêm **C:\Windows\Software\QORE** vào danh sách.

   **Hình ảnh minh họa:**

   ![Thiết lập User Variable](image_path_user_variable.png)

## Bước 3: Kiểm Tra

- Mở Command Prompt (CMD) và nhập lệnh `QORE -list` để kiểm tra xem công cụ đã được cài đặt thành công.
