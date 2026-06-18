# Readiness Checklist – Lab 05

Đây là danh sách kiểm tra (checklist) để đảm bảo stack Docker Compose của bạn đã sẵn sàng trước khi gửi bài. Hãy tick vào mỗi mục sau khi hoàn thành.

- [x] **Database ready:** container DB đã chạy và phản hồi `pg_isready`. Kiểm tra bằng `docker exec -it fit4110-db-lab05 pg_isready -U lab05`.
- [x] **Worker/AI service ready:** container `notification-worker` trả về `200` cho endpoint `/health` và `/predict`, `/notify` hoạt động hoàn hảo.
- [x] **API ready:** container API trả `200` cho `/health` (kiểm tra kết nối DB thật) và có thể tạo/lấy readings khi token hợp lệ.
- [x] **Environment variables:** `.env` đã được thiết lập đúng (`APP_PORT`, `POSTGRES_USER`, `AUTH_TOKEN`, `WORKER_URL`,...). Đã commit `.env.example` và không có secret thực tế nào bị rò rỉ.
- [x] **Network & Ports:** mạng `team-internal` hoạt động ổn định; API gọi được worker qua hostname `notification-worker` và DB qua hostname `db`; các cổng `8000` (API) và `9000` (Worker) được ánh xạ chính xác.
- [x] **Image tags:** image API được build thành công với tag `v0.1.0-notify` (`fit4110/notification-service:v0.1.0-notify`).

Ghi chú thêm những vấn đề gặp phải hoặc điều chỉnh tại đây:

```text
1. Thay thế service mẫu ai-service bằng service notification-worker chạy bằng pure Python HTTP server để giảm thiểu dung lượng image và loại bỏ hoàn toàn các lỗi thiếu thư viện phụ thuộc (FastAPI/Uvicorn) trong container slim.
2. Kết nối API trực tiếp với PostgreSQL để thực hiện các câu lệnh kiểm tra sức khỏe (/health) thực tế và lưu trữ lâu dài (persist) dữ liệu telemetry và các alert.
3. Kịch bản kiểm thử Newman được cập nhật từ Lab 4 và chạy thành công 100% (19/19 assertions đạt).
```