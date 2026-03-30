# ============================================================
# TÍNH NĂNG 7: PHÂN TRANG (PAGINATION)
# ============================================================
# Sửa file: backend/main.py - hàm list_photos

@app.get("/api/photos", response_model=dict)
def list_photos(
    search: Optional[str] = None,
    sort_by: Optional[str] = "date_desc",
    # ✅ THÊM MỚI: tham số phân trang
    page: int = 1,        # Trang hiện tại (bắt đầu từ 1)
    limit: int = 12,      # Số ảnh mỗi trang
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Photo).filter(Photo.user_id == current_user.id)

    if search:
        query = query.filter(Photo.title.ilike(f"%{search}%"))

    # Sắp xếp
    if sort_by == "date_asc":
        query = query.order_by(Photo.uploaded_at.asc())
    elif sort_by == "name_asc":
        query = query.order_by(Photo.title.asc())
    elif sort_by == "name_desc":
        query = query.order_by(Photo.title.desc())
    else:
        query = query.order_by(Photo.uploaded_at.desc())

    # ✅ Đếm tổng số ảnh (để tính tổng số trang)
    total = query.count()

    # ✅ Tính offset: trang 1 bắt đầu từ 0, trang 2 từ 12, trang 3 từ 24...
    offset = (page - 1) * limit
    photos = query.offset(offset).limit(limit).all()

    # ✅ Trả về kèm thông tin phân trang
    return {
        "photos": photos,
        "total": total,                                    # Tổng số ảnh
        "page": page,                                      # Trang hiện tại
        "limit": limit,                                    # Số ảnh/trang
        "total_pages": (total + limit - 1) // limit,      # Tổng số trang
        "has_next": page * limit < total,                  # Còn trang tiếp không
        "has_prev": page > 1,                              # Có trang trước không
    }

# Sửa file: frontend/src/pages/GalleryPage.jsx
# Thêm state và UI phân trang:
"""
const [page, setPage] = useState(1)
const [totalPages, setTotalPages] = useState(1)

// Cập nhật fetchPhotos để nhận page:
const fetchPhotos = async (q = '', p = 1) => {
  const { data } = await photoAPI.list(q, p)
  setPhotos(data.photos)
  setTotalPages(data.total_pages)
}

// UI phân trang ở cuối trang:
<div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'center', marginTop: '2rem' }}>
  <button disabled={page === 1} onClick={() => setPage(p => p - 1)}>← Trước</button>
  <span>{page} / {totalPages}</span>
  <button disabled={page === totalPages} onClick={() => setPage(p => p + 1)}>Sau →</button>
</div>
"""


# ============================================================
# TÍNH NĂNG 8: LỌC ẢNH THEO CATEGORY
# ============================================================
# Sửa file: backend/main.py - hàm list_photos
# Thêm tham số category vào sau sort_by:

@app.get("/api/photos")
def list_photos(
    search: Optional[str] = None,
    sort_by: Optional[str] = "date_desc",
    # ✅ THÊM MỚI: lọc theo category
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Photo).filter(Photo.user_id == current_user.id)

    if search:
        query = query.filter(Photo.title.ilike(f"%{search}%"))

    # ✅ Nếu có category thì lọc thêm
    if category and category != "Tất cả":
        query = query.filter(Photo.category == category)

    # ... (sắp xếp như cũ) ...
    return query.all()

# Sửa file: frontend/src/pages/GalleryPage.jsx
# Thêm bộ lọc category dạng tab/button:
"""
const [activeCategory, setActiveCategory] = useState('Tất cả')
const CATEGORIES = ['Tất cả', 'Phong cảnh', 'Chân dung', 'Ẩm thực', 'Du lịch', 'Khác']

// UI tabs lọc:
<div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
  {CATEGORIES.map(cat => (
    <button
      key={cat}
      onClick={() => { setActiveCategory(cat); fetchPhotos(searchInput, cat) }}
      style={{
        background: activeCategory === cat ? 'var(--accent)' : 'var(--surface)',
        color: activeCategory === cat ? '#000' : 'var(--text-muted)',
        border: '1px solid var(--border)',
        padding: '0.4rem 1rem',
        borderRadius: '20px',
        cursor: 'pointer',
      }}
    >
      {cat}
    </button>
  ))}
</div>
"""


# ============================================================
# TÍNH NĂNG 9: ĐỔI MẬT KHẨU
# ============================================================
# Sửa file: backend/main.py - thêm endpoint mới

from pydantic import BaseModel

class ChangePasswordRequest(BaseModel):
    current_password: str    # Mật khẩu hiện tại để xác thực
    new_password: str        # Mật khẩu mới muốn đổi

@app.post("/api/auth/change-password")
def change_password(
    data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ✅ Kiểm tra mật khẩu hiện tại có đúng không
    if not verify_password(data.current_password, current_user.password):
        raise HTTPException(status_code=400, detail="Mật khẩu hiện tại không đúng")

    # ✅ Kiểm tra mật khẩu mới đủ độ dài
    if len(data.new_password) < 6:
        raise HTTPException(status_code=400, detail="Mật khẩu mới phải có ít nhất 6 ký tự")

    # ✅ Mã hóa mật khẩu mới và lưu vào database
    current_user.password = hash_password(data.new_password)
    db.commit()

    return {"message": "Đổi mật khẩu thành công"}

# Sửa file: frontend/src/api.js - thêm:
# changePassword: (data) => api.post('/auth/change-password', data),

# Tạo file mới hoặc thêm vào ProfilePage.jsx:
"""
// Form đổi mật khẩu
const [pwForm, setPwForm] = useState({ current_password: '', new_password: '', confirm: '' })

const handleChangePassword = async () => {
  if (pwForm.new_password !== pwForm.confirm) {
    setError('Mật khẩu xác nhận không khớp')
    return
  }
  await authAPI.changePassword({
    current_password: pwForm.current_password,
    new_password: pwForm.new_password,
  })
  alert('Đổi mật khẩu thành công!')
}
"""


# ============================================================
# TÍNH NĂNG 10: ĐỔI USERNAME / EMAIL
# ============================================================
# Sửa file: backend/main.py - thêm endpoint mới

class UpdateProfileRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

@app.patch("/api/auth/profile", response_model=UserOut)
def update_profile(
    data: UpdateProfileRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ✅ Kiểm tra username mới có bị trùng không
    if data.username and data.username != current_user.username:
        existing = db.query(User).filter(User.username == data.username).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username đã được sử dụng")
        current_user.username = data.username

    # ✅ Kiểm tra email mới có bị trùng không
    if data.email and data.email != current_user.email:
        existing = db.query(User).filter(User.email == data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email đã được sử dụng")
        current_user.email = data.email

    db.commit()
    db.refresh(current_user)
    return current_user


# ============================================================
# TÍNH NĂNG 11: GIỚI HẠN DUNG LƯỢNG UPLOAD MỖI USER
# ============================================================
# Sửa file: backend/main.py - hàm upload_photo
# Thêm kiểm tra trước khi lưu file

MAX_STORAGE_PER_USER = 100 * 1024 * 1024  # 100MB mỗi user

@app.post("/api/photos", response_model=PhotoOut, status_code=201)
async def upload_photo(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contents = await file.read()

    # ✅ THÊM MỚI: kiểm tra tổng dung lượng đã dùng
    # Lấy tất cả ảnh của user và tính tổng kích thước file
    user_photos = db.query(Photo).filter(Photo.user_id == current_user.id).all()
    total_used = 0
    for p in user_photos:
        filepath = "." + p.image_url
        if os.path.exists(filepath):
            total_used += os.path.getsize(filepath)

    # ✅ Nếu vượt giới hạn thì báo lỗi
    if total_used + len(contents) > MAX_STORAGE_PER_USER:
        used_mb = total_used / (1024 * 1024)
        raise HTTPException(
            status_code=400,
            detail=f"Vượt giới hạn lưu trữ. Đã dùng {used_mb:.1f}MB / 100MB"
        )

    # ... (tiếp tục code upload như cũ) ...


# ============================================================
# TÍNH NĂNG 12: HIỂN THỊ KÍCH THƯỚC FILE VÀ ĐỘ PHÂN GIẢI
# ============================================================
# Sửa file: backend/models.py - thêm 2 cột mới

class Photo(Base):
    # ... (các field cũ) ...
    # ✅ THÊM MỚI: kích thước file (bytes)
    file_size = Column(Integer, nullable=True)
    # ✅ THÊM MỚI: độ phân giải ảnh: "1920x1080"
    resolution = Column(String, nullable=True)

# Sửa file: backend/main.py - hàm upload_photo
# Thêm đọc thông tin ảnh sau khi validate:
"""
# Đọc kích thước file
file_size = len(contents)

# Đọc độ phân giải ảnh bằng Pillow
img = Image.open(io.BytesIO(contents))
width, height = img.size
resolution = f"{width}x{height}"

photo = Photo(
    title=title,
    description=description,
    image_url=f"/uploads/{filename}",
    user_id=current_user.id,
    file_size=file_size,        # ✅ Lưu kích thước file
    resolution=resolution,      # ✅ Lưu độ phân giải
)
"""

# Sửa file: frontend/src/pages/PhotoDetailPage.jsx
# Hiển thị thêm thông tin trong phần meta:
"""
<div style={styles.metaItem}>
  <span style={styles.metaLabel}>Kích thước</span>
  <span style={styles.metaValue}>
    {photo.file_size ? (photo.file_size / 1024).toFixed(1) + ' KB' : 'N/A'}
  </span>
</div>
<div style={styles.metaItem}>
  <span style={styles.metaLabel}>Độ phân giải</span>
  <span style={styles.metaValue}>{photo.resolution || 'N/A'}</span>
</div>
"""


# ============================================================
# TÍNH NĂNG 13: NÚT TẢI ẢNH VỀ (DOWNLOAD)
# ============================================================
# Sửa file: frontend/src/pages/PhotoDetailPage.jsx
# Thêm nút download - KHÔNG cần sửa backend

"""
// Hàm xử lý download ảnh
const handleDownload = () => {
  // Tạo thẻ <a> ẩn để trigger download
  const link = document.createElement('a')
  link.href = photo.image_url          // URL ảnh
  link.download = photo.title + '.jpg' // Tên file khi tải về
  document.body.appendChild(link)
  link.click()                         // Kích hoạt click
  document.body.removeChild(link)      // Xóa thẻ sau khi dùng
}

// Thêm nút vào header của trang detail (cạnh nút Edit và Delete):
<button className="btn-ghost" onClick={handleDownload}>
  ⬇ Tải về
</button>
"""


# ============================================================
# TÍNH NĂNG 14: XEM ẢNH DẠNG SLIDESHOW
# ============================================================
# Tạo file mới: frontend/src/components/Slideshow.jsx

"""
import { useState, useEffect, useCallback } from 'react'

// Props:
// photos: danh sách ảnh
// initialIndex: index ảnh bắt đầu
// onClose: hàm đóng slideshow

export default function Slideshow({ photos, initialIndex = 0, onClose }) {
  const [current, setCurrent] = useState(initialIndex)

  // Di chuyển sang ảnh tiếp theo
  const next = useCallback(() => {
    setCurrent(i => (i + 1) % photos.length)
  }, [photos.length])

  // Di chuyển về ảnh trước
  const prev = useCallback(() => {
    setCurrent(i => (i - 1 + photos.length) % photos.length)
  }, [photos.length])

  // Lắng nghe phím mũi tên và ESC
  useEffect(() => {
    const handleKey = (e) => {
      if (e.key === 'ArrowRight') next()
      if (e.key === 'ArrowLeft') prev()
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [next, prev, onClose])

  const photo = photos[current]

  return (
    <div style={{
      position: 'fixed', inset: 0,
      background: 'rgba(0,0,0,0.95)',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      zIndex: 200,
    }}>
      {/* Nút đóng */}
      <button onClick={onClose} style={{ position: 'absolute', top: '1rem', right: '1rem', ... }}>✕</button>

      {/* Nút previous */}
      <button onClick={prev} style={{ position: 'absolute', left: '1rem', ... }}>←</button>

      {/* Ảnh hiện tại */}
      <img src={photo.image_url} alt={photo.title} style={{ maxHeight: '90vh', maxWidth: '90vw' }} />

      {/* Tiêu đề và số thứ tự */}
      <div style={{ position: 'absolute', bottom: '2rem', textAlign: 'center', color: '#fff' }}>
        <div>{photo.title}</div>
        <div>{current + 1} / {photos.length}</div>
      </div>

      {/* Nút next */}
      <button onClick={next} style={{ position: 'absolute', right: '1rem', ... }}>→</button>
    </div>
  )
}
"""

# Sửa file: frontend/src/pages/GalleryPage.jsx
# Thêm state và nút mở slideshow:
"""
const [slideshow, setSlideshow] = useState({ open: false, index: 0 })

// Thay vì navigate khi click ảnh, mở slideshow:
// Trong PhotoCard hoặc GalleryPage thêm:
<button onClick={() => setSlideshow({ open: true, index: i })}>
  Slideshow
</button>

// Render Slideshow component:
{slideshow.open && (
  <Slideshow
    photos={photos}
    initialIndex={slideshow.index}
    onClose={() => setSlideshow({ open: false, index: 0 })}
  />
)}
"""
