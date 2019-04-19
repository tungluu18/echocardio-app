# Echo_cardiography RESTful API

#### Yêu cầu môi trường
* mysql (hoặc docker)
* python3
#### Cài đặt

> git clone https://github.com/tungluu18/echocardio-app.git
> cd ./echocardio-app
> python3 -m venv venv
> pip3 install -r requirements.txt
### Nếu sử dụng mysql server trên máy
#### Cấu hình app: tạo file .env trong trong folder root của project, định nghĩa các giá trị sau
##### Cấu hình database trong .env
    DB_USER={Tên một người dùng trên database}
    DB_PWD={Mật khẩu của người dùng đó}
    DB_HOST={Địa chỉ host của database}
    DB_PORT={Cổng kết nối tới database trên host}
    DB_NAME={Tên của database}
Các giá trị mặc địhn (được dùng nếu không có file .env) ở trong file config.py

### Nếu sử dụng docker để host mysql
Build image cho database từ dockerfile, từ folder root của project
> docker build -t database-echo-app .
Start container mysql từ image vừa build
> docker container run --publish 3307:3306 --name echo-app-sql-service --detach database-echo-app

Trường hợp chạy app bị lỗi liên quan đến khóa sha256:
> docker container exec -it database-echo-app /bin/bash
> mysql -u tungluu18 -p
> Nhập mật khẩu 'tungluu18'

#### Khởi tạo database
> python3 init_db.py

#### Seed dữ liệu người dùng (test only)
> python3 seed_db.py
(Mật khẩu mặc định là 123456

### Chạy app
> ./start.sh
hoặc
>./start_wsgi.sh

#### Kiểm tra
> http://127.0.0.1:5000/api/v1

#### Trang quản lý của admin
> http://127.0.0.1:5000/website/admin/homepage
