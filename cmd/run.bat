@echo off
:: Set code page to UTF-8 to support Vietnamese characters
chcp 65001 >nul

:: Check if a parameter is passed
if "%1"=="" (
    echo Không có đối số nào được cung cấp.
    exit /b 1
)

:: In giá trị của tham số đầu tiên
echo Đối số được cung cấp là: %1

:end
