# Echo_cardiography RESTful API

#### Yêu cầu môi trường
* mysql
* python3
* python3 virtualenv
#### Cài đặt

> git clone https://github.com/tungluu18/echocardio-app.git

> cd ./echocardio-app

> python3 -m venv venv

> source ./venv/bin/activate

> pip install -r requirement.txt

Cấu hình database trong file **config.py**
* _DB_HOST và _DB_PORT: mặc định là localhost và 3306 cho mysql cài đặt trên local
* _DB_USER tài khoản mysql
* _DB_PWD mật khẩu cho tài khoản mysql _DB_USER
* _DB_NAME tên của database tạo tên mysql (phải khởi tạo trước  database trên mysql )

#### Khởi tạo database
> python3 init_db.py

### Chạy app
> ./start.sh
hoặc
>./start_wsgi.sh

#### Kiểm tra
> http://127.0.0.1:5000/api/v1
