# BÁO CÁO BÀI TẬP: AUDIT PUBLIC API

**Đối tượng Audit:** GitHub REST API (v3)  
**Tài nguyên (Resource):** Repository (Kho lưu trữ)  
**Mục tiêu:** Đánh giá tính tuân thủ kiến trúc RESTful thông qua vòng đời CRUD thực tế.

---

## Bảng Tổng hợp 5 Endpoints

| STT | Chức năng | Method | Endpoint | Status Code (Thực tế) | Headers Tiêu Biểu | Có RESTful không? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | Lấy danh sách Repo | `GET` | `/users/{username}/repos` | `200 OK` | `Link`<br>`X-RateLimit-Limit` | **Có** (Chuẩn HATEOAS & Stateless) |
| **2** | Tạo mới Repo | `POST` | `/user/repos` | `201 Created` | `Location`<br>`Authorization` | **Có** (Mã 201 chuẩn cho Create) |
| **3** | Xem chi tiết 1 Repo | `GET` | `/repos/{owner}/{repo}` | `200 OK` | `ETag`<br>`Cache-Control` | **Có** (Dùng Path Variable) |
| **4** | Cập nhật 1 phần | `PATCH` | `/repos/{owner}/{repo}` | `200 OK` | `Content-Type: application/json` | **Có** (Đúng bản chất partial update) |
| **5** | Xóa Repo | `DELETE`| `/repos/{owner}/{repo}` | `204 No Content` / `403 Forbidden` | `X-Accepted-OAuth-Scopes` | **Có** (Không trả về body khi xóa) |

---

## Đánh giá chi tiết tính RESTful dựa trên kết quả Audit

**1. Tuân thủ định dạng Định danh Tài nguyên (Resource URI)**
* Tất cả các endpoint đều sử dụng **danh từ số nhiều** (`/users`, `/repos`) để biểu diễn tài nguyên.
* Tuyệt đối không sử dụng động từ trong URL (ví dụ: không dùng `/deleteRepo` hay `/createRepo`).
* Thể hiện rõ quan hệ phân cấp: `/repos/{owner}/{repo}`.

**2. Sử dụng đúng ngữ nghĩa của HTTP Methods và Status Code**
* **Tạo mới (POST):** GitHub trả về đúng mã `201 Created` chứ không phải `200 OK` chung chung. Đặc biệt, response header có chứa `location: https://api.github.com/repos/...` chỉ điểm chính xác URL của tài nguyên vừa được tạo.
* **Cập nhật (PATCH):** GitHub hỗ trợ `PATCH` cho phép chỉ gửi lên trường dữ liệu cần sửa (ví dụ chỉ đổi `description`), thay vì phải dùng `PUT` và gửi lại toàn bộ JSON object.
* **Xóa (DELETE):** Khi xóa thành công, API trả về `204 No Content` với body hoàn toàn trống. Đây là thiết kế tối ưu băng thông và cực kỳ chuẩn mực của kiến trúc REST.

**3. Kiến trúc Phi trạng thái (Stateless) & Quản lý Rate Limit**
Toàn bộ request đều độc lập và phải mang theo Token xác thực, Server hoàn toàn không lưu Session. Điều này được thể hiện rõ qua các Header đếm ngược giới hạn lượt gọi trả về liên tục ở mọi request:
* `x-ratelimit-limit: 5000` (Tổng số request được phép).
* `x-ratelimit-remaining: 4995` (Số request còn lại).

**4. Dẫn hướng thông minh (HATEOAS - Mức cao nhất của RESTful)**
Khi dùng `GET` lấy danh sách Repo, thay vì bắt client tự tính toán trang tiếp theo, GitHub trả về Header `Link`:
`link: <.../repos?per_page=2&page=2>; rel="next"`
Hệ thống tự động cung cấp sẵn URL để client bấm vào đi tiếp, đáp ứng tiêu chuẩn cao nhất của RESTful.

**5. Cơ chế phân quyền chi tiết (Scopes Authorization)**
Trong quá trình Audit lệnh `DELETE`, API đã trả về mã lỗi **`403 Forbidden`**. Header của API tiết lộ rõ nguyên nhân thông qua:
* `x-oauth-scopes: repo` (Quyền hiện tại của Token)
* `x-accepted-oauth-scopes: delete_repo` (Quyền API yêu cầu để được phép thực thi)
Cách xử lý lỗi này tuân thủ tuyệt đối chuẩn RESTful: Dùng HTTP Status Code để từ chối truy cập ngay lập tức ở tầng giao thức thay vì trả về `200 OK` rồi mới báo lỗi bên trong JSON body.