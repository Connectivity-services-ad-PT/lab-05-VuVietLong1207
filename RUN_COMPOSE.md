# RUN_COMPOSE.md – Hướng dẫn chạy Lab 05

Tài liệu này hướng dẫn người khác clone repo sạch và chạy lại stack Compose của Lab 05.

---

## 1. Clone repo

```bash
git clone <repo-url>
cd FIT4110_lab05_docker_compose_readiness
```

---

## 2. Cài dependencies cho Newman/Prism/Spectral (tuỳ chọn)

```bash
npm install
```

---

## 3. Build & chạy stack Docker Compose

```bash
# Copy .env.example sang .env và chỉnh sửa nếu cần
cp .env.example .env

# Build images (nếu chưa có) và khởi động các container trong nền
docker compose up -d --build
```

Lệnh trên sẽ tạo các container:

- `fit4110-db-lab05` (PostgreSQL database service chạy trên port 5432)
- `fit4110-worker-lab05` (Notification worker service chạy trên port 9000)
- `fit4110-api-lab05` (Notification API service chạy trên port 8000)

Theo dõi log:

```bash
docker compose logs -f
```

Sau vài giây, kiểm tra health của mỗi service:

```bash
# API (Kiểm tra xem API hoạt động và DB đã connected chưa)
curl http://localhost:8000/health

# Notification Worker
curl http://localhost:9000/health

# DB readiness
docker exec -it fit4110-db-lab05 pg_isready -U lab05
```

Bạn có thể gửi thử thông báo khẩn cấp đến API để kiểm tra luồng hoạt động end-to-end:

```bash
# Gửi alert đến API (Sử dụng PowerShell hoặc curl)
curl -X POST http://localhost:8000/api/v1/alerts \
  -H "Authorization: Bearer local-dev-token" \
  -H "Content-Type: application/json" \
  -d '{"location": "Building B7", "type": "fire_alarm", "details": "Test alert via terminal"}'
```

---

## 4. Chạy Newman test trên stack Compose (tuỳ chọn)

```bash
npm run test:compose
```

Report sinh tại:

```text
reports/newman-lab05-compose.xml
reports/newman-lab05-compose.html
```

---

## 5. Dừng stack

Khi không cần nữa, dừng và xoá các container bằng:

```bash
docker compose down
```

Nếu muốn xoá volume dữ liệu của DB, thêm tuỳ chọn `-v`:

```bash
docker compose down -v
```

---

## 6. Lệnh nhanh

Bạn có thể dùng Makefile:

```bash
make compose-up
make compose-down
make logs
```

---

## 7. Mẹo gỡ lỗi

- Sử dụng `docker compose ps` để xem trạng thái container.
- Nếu API trả lỗi kết nối DB, hãy kiểm tra biến môi trường `POSTGRES_*` trong `.env` và đảm bảo DB đã sẵn sàng (`pg_isready`).
- Nếu AI service cần tải mô hình lớn, tăng `start_period` của healthcheck trong `docker-compose.yml`.