# ============================================================
# HƯỚNG DẪN SỬ DỤNG TÀI LIỆU NÀY
# ============================================================
#
# Có 4 file trong thư mục này:
#
# 📄 tinh-nang-01-06-de.py        - Tính năng 1-6 (Dễ)
# 📄 tinh-nang-07-14-trung-binh.py - Tính năng 7-14 (Trung bình)
# 📄 tinh-nang-15-20-kho.py       - Tính năng 15-20 (Khó)
# 📄 cau-hoi-ly-thuyet.py         - Câu hỏi lý thuyết
#
# ============================================================
# DANH SÁCH 20 TÍNH NĂNG
# ============================================================
#
# 🟢 DỄ (01-06)
#   01. Thêm trường CATEGORY cho ảnh
#       → Sửa: models.py, schemas.py, main.py, UploadModal.jsx
#
#   02. Thêm trường TAGS cho ảnh
#       → Sửa: models.py, schemas.py, main.py, UploadModal.jsx
#
#   03. SẮP XẾP ảnh (mới nhất, cũ nhất, A-Z, Z-A)
#       → Sửa: main.py, api.js, GalleryPage.jsx
#
#   04. Hiển thị SỐ LƯỢNG ẢNH của user
#       → Sửa: main.py (thêm endpoint /stats), GalleryPage.jsx
#
#   05. Đổi THEME SÁNG / TỐI
#       → Sửa: index.css, tạo ThemeContext.jsx, Navbar.jsx
#
#   06. Trang PROFILE user
#       → Tạo: ProfilePage.jsx | Sửa: App.jsx, Navbar.jsx
#
# 🟡 TRUNG BÌNH (07-14)
#   07. PHÂN TRANG (Pagination)
#       → Sửa: main.py, api.js, GalleryPage.jsx
#
#   08. LỌC ẢNH theo category (tabs)
#       → Sửa: main.py, GalleryPage.jsx
#
#   09. ĐỔI MẬT KHẨU
#       → Sửa: main.py (thêm endpoint), api.js, ProfilePage.jsx
#
#   10. ĐỔI USERNAME / EMAIL
#       → Sửa: main.py (thêm endpoint), api.js, ProfilePage.jsx
#
#   11. Giới hạn DUNG LƯỢNG UPLOAD mỗi user (100MB)
#       → Sửa: main.py (hàm upload_photo)
#
#   12. Hiển thị KÍCH THƯỚC FILE và ĐỘ PHÂN GIẢI ảnh
#       → Sửa: models.py, main.py, schemas.py, PhotoDetailPage.jsx
#
#   13. Nút TẢI ẢNH VỀ (Download)
#       → Sửa: PhotoDetailPage.jsx (chỉ cần frontend)
#
#   14. Xem ảnh dạng SLIDESHOW
#       → Tạo: Slideshow.jsx | Sửa: GalleryPage.jsx
#
# 🔴 KHÓ (15-20)
#   15. CHIA SẺ ẢNH công khai qua link
#       → Sửa: models.py, main.py, api.js, PhotoDetailPage.jsx
#
#   16. ALBUM / FOLDER nhóm ảnh
#       → Sửa: models.py (thêm model Album, PhotoAlbum)
#       → Sửa: main.py (CRUD album), tạo AlbumPage.jsx
#
#   17. YÊU THÍCH ảnh (Like/Bookmark)
#       → Sửa: models.py, main.py, api.js, PhotoCard.jsx
#
#   18. THỐNG KÊ biểu đồ số ảnh theo tháng
#       → Sửa: main.py (thêm /api/stats)
#       → Tạo: StatsPage.jsx (dùng recharts)
#
#   19. Tự động tạo THUMBNAIL khi upload
#       → Sửa: models.py, main.py (Pillow resize), PhotoCard.jsx
#
#   20. XÓA TÀI KHOẢN (kèm xóa toàn bộ ảnh)
#       → Sửa: main.py (thêm endpoint), api.js, ProfilePage.jsx
#
# ============================================================
# CẤU TRÚC FILE CẦN SỬA NHANH
# ============================================================
#
# backend/
#   main.py     ← Thêm/sửa API endpoints
#   models.py   ← Thêm cột, bảng database
#   schemas.py  ← Thêm field request/response
#   auth.py     ← Liên quan đến bảo mật, token
#
# frontend/src/
#   api.js                    ← Thêm hàm gọi API mới
#   index.css                 ← Sửa màu sắc, font, style
#   App.jsx                   ← Thêm route mới
#   context/AuthContext.jsx   ← Liên quan đến đăng nhập
#   pages/
#     GalleryPage.jsx         ← Trang chính (danh sách ảnh)
#     PhotoDetailPage.jsx     ← Trang chi tiết ảnh
#     LoginPage.jsx           ← Trang đăng nhập
#     RegisterPage.jsx        ← Trang đăng ký
#   components/
#     Navbar.jsx              ← Thanh điều hướng
#     PhotoCard.jsx           ← Thẻ ảnh trong grid
#     UploadModal.jsx         ← Popup upload ảnh
