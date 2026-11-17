Lựa chọn GET /books :
- Tần suất gọi cao 
- Ảnh hưởng trực tiếp đến trải nghiệm ( khi người dùng thao tác đến sort, đổi trang v.v.. cùng các query parameters) 

wait time : 1-3s per request.

| Kịch bản | Số Users | Tốc độ tạo  | Thời gian chạy | RPS đo được (`GET /books`) | p95 Response Time | Tỷ lệ lỗi HTTP |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| A | 10 | 2 user/s | 30s | 1.62 req/s | 11 ms | 0.00% |
| B | 50 | 5 user/s | 60s | 8.70 req/s | 15 ms | 0.00% |
| C | 200 | 50 user/s | 30s | 37.11 req/s | 83 ms | 0.00% |

Nhận xét:
- Từ Kịch bản A sang B (10 → 50 users): Hệ thống tăng trưởng thông lượng tốt, độ trễ p95 ổn định  (11 ms → 15 ms), 0% lỗi.
- Từ Kịch bản B sang C (50 → 200 users): Khi tải tăng lên 200 users đồng thời, p95 của `GET /books` tăng vọt từ 15 ms lên 83 ms (gấp ~5.5 lần). Tuy nhiên, 100% request vẫn trả về mã 200 OK. Điều này chứng minh server bắt đầu xuất hiện độ trễ hàng đợi (queueing delay) trên tiến trình xử lý đơn, nhưng chưa chạm tới ngưỡng sụp đổ (crash).


Chỉ số SLI đề xuất  và mục tiêu SLO: 
- Availability: Tỉ lệ thành công nhận được (`GET /books`) ( HTTP 200 )  ≥ 99%
- Latency :
   Bình thường : p95 ≤ 200 ms ; Tail : p99 ≤ 500 ms

Dùng SLO thay avg :  nếu  1 ông xui tự nhiên dính  500ms sẽ kéo tất tần tật các người khác theo. nên để p95 để đại diện đa số trải nghiệm người dùng
Tại sao lại là 200s trong khi đo được 83 : Do đang đo trên máy local , ta tính thêm cả TLS/nginx ( 20ms ) + tốc độ truyền mangj thật ( ~ 70ms) , thêm vào đó là tiêu chuẩn Nielsen Norman  :Từ 100 ms – 300 ms: Người dùng cảm thấy web mượt mà, không bị gián đoạn mạch suy nghĩ.


Kết quả đo trên máy local , chưa thể thực sự ước lượng cho môi trường production , phải đo thực tế .
Nếu ngân sách lỗi 0.1% bị tiêu hao quá 50% trong nửa đầu chu kỳ đánh giá:
- Cần tối ưu lại hiệu năng, cơ sở dữ liệu , query
- Bổ sung caching 
- Nâng cấp runtime 
Nếu vẫn không được thì cần nâng cấp hạ tầng và đàm phán lại SLO