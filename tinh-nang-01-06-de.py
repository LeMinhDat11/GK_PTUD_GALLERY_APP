# ============================================================
# TÍNH NĂNG 1: THÊM TRƯỜNG CATEGORY CHO ẢNH
# ============================================================
# Sửa file: backend/models.py
# Thêm cột category vào bảng Photo

from sqlalchemy import Column, String

class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # ✅ THÊM MỚI: trường category để phân loại ảnh
    # nullable=True nghĩa là không bắt buộc phải điền
    category = Column(String, nullable=True, default="Khác")

    owner = relationship("User", back_populates="photos")


# ============================================================
# TÍNH NĂNG 1: THÊM CATEGORY - SCHEMAS
# ============================================================
# Sửa file: backend/schemas.py

from typing import Optional

class PhotoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    # ✅ THÊM MỚI: category trong schema tạo ảnh
    category: Optional[str] = "Khác"

class PhotoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    # ✅ THÊM MỚI: cho phép cập nhật category
    category: Optional[str] = None

class PhotoOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    image_url: str
    uploaded_at: datetime
    user_id: int
    # ✅ THÊM MỚI: trả về category trong response
    category: Optional[str]

    class Config:
        from_attributes = True


# ============================================================
# TÍNH NĂNG 1: THÊM CATEGORY - ENDPOINT UPLOAD
# ============================================================
# Sửa file: backend/main.py - hàm upload_photo

@app.post("/api/photos", response_model=PhotoOut, status_code=201)
async def upload_photo(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    # ✅ THÊM MỚI: nhận category từ form
    category: Optional[str] = Form("Khác"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ... (giữ nguyên code validate file) ...

    photo = Photo(
        title=title,
        description=description,
        image_url=f"/uploads/{filename}",
        user_id=current_user.id,
        # ✅ THÊM MỚI: lưu category vào database
        category=category,
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo


# ============================================================
# TÍNH NĂNG 1: THÊM CATEGORY - FRONTEND UploadModal.jsx
# ============================================================
# Sửa file: frontend/src/components/UploadModal.jsx
# Thêm dropdown chọn category

# Danh sách các category có sẵn
CATEGORIES = ["Phong cảnh", "Chân dung", "Ẩm thực", "Du lịch", "Động vật", "Kiến trúc", "Khác"]

# Thêm state cho category
# const [category, setCategory] = useState('Khác')

# Thêm JSX dropdown vào form (sau phần description):
"""
<div className="form-group">
  <label className="form-label">Danh mục</label>
  <select
    value={category}
    onChange={e => setCategory(e.target.value)}
    style={{ ...styles của input... }}
  >
    {CATEGORIES.map(cat => (
      <option key={cat} value={cat}>{cat}</option>
    ))}
  </select>
</div>
"""

# Thêm category vào FormData khi submit:
# fd.append('category', category)


# ============================================================
# TÍNH NĂNG 2: THÊM TRƯỜNG TAGS
# ============================================================
# Sửa file: backend/models.py
# Tags lưu dạng chuỗi, phân cách bằng dấu phẩy: "biển,hè,2024"

class Photo(Base):
    # ... (các field cũ) ...
    # ✅ THÊM MỚI: tags lưu dạng "tag1,tag2,tag3"
    tags = Column(String, nullable=True, default="")

# Sửa file: backend/schemas.py
class PhotoOut(BaseModel):
    # ... (các field cũ) ...
    # ✅ THÊM MỚI: tags trả về dạng list
    tags: Optional[str] = ""

    # Thêm property để convert string -> list khi cần
    @property
    def tags_list(self):
        if self.tags:
            return [t.strip() for t in self.tags.split(",") if t.strip()]
        return []


# ============================================================
# TÍNH NĂNG 3: SẮP XẾP ẢNH
# ============================================================
# Sửa file: backend/main.py - hàm list_photos

@app.get("/api/photos", response_model=List[PhotoOut])
def list_photos(
    search: Optional[str] = None,
    # ✅ THÊM MỚI: tham số sắp xếp
    # sort_by: "date_desc" | "date_asc" | "name_asc" | "name_desc"
    sort_by: Optional[str] = "date_desc",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Photo).filter(Photo.user_id == current_user.id)

    # Lọc theo tên nếu có search
    if search:
        query = query.filter(Photo.title.ilike(f"%{search}%"))

    # ✅ THÊM MỚI: xử lý sắp xếp theo tham số sort_by
    if sort_by == "date_desc":
        query = query.order_by(Photo.uploaded_at.desc())   # Mới nhất trước
    elif sort_by == "date_asc":
        query = query.order_by(Photo.uploaded_at.asc())    # Cũ nhất trước
    elif sort_by == "name_asc":
        query = query.order_by(Photo.title.asc())          # Tên A-Z
    elif sort_by == "name_desc":
        query = query.order_by(Photo.title.desc())         # Tên Z-A
    else:
        query = query.order_by(Photo.uploaded_at.desc())   # Mặc định: mới nhất

    return query.all()

# Sửa file: frontend/src/api.js
# Sửa hàm list để truyền thêm sort_by:
"""
list: (search, sortBy = 'date_desc') =>
  api.get('/photos', { params: { search: search || undefined, sort_by: sortBy } }),
"""

# Sửa file: frontend/src/pages/GalleryPage.jsx
# Thêm state và dropdown sắp xếp:
"""
const [sortBy, setSortBy] = useState('date_desc')

// Dropdown sắp xếp trong UI:
<select value={sortBy} onChange={e => { setSortBy(e.target.value); fetchPhotos(searchInput, e.target.value) }}>
  <option value="date_desc">Mới nhất</option>
  <option value="date_asc">Cũ nhất</option>
  <option value="name_asc">Tên A-Z</option>
  <option value="name_desc">Tên Z-A</option>
</select>
"""


# ============================================================
# TÍNH NĂNG 4: HIỂN THỊ SỐ LƯỢNG ẢNH
# ============================================================
# Sửa file: backend/main.py - thêm endpoint mới

@app.get("/api/photos/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ✅ THÊM MỚI: đếm tổng số ảnh của user
    total = db.query(Photo).filter(Photo.user_id == current_user.id).count()

    # Đếm theo category (nếu đã thêm tính năng 1)
    # from sqlalchemy import func
    # by_category = db.query(Photo.category, func.count(Photo.id))\
    #     .filter(Photo.user_id == current_user.id)\
    #     .group_by(Photo.category).all()

    return {
        "total_photos": total,
        # "by_category": {cat: count for cat, count in by_category}
    }

# Sửa file: frontend/src/api.js - thêm:
# stats: () => api.get('/photos/stats'),

# Sửa file: frontend/src/pages/GalleryPage.jsx
# Gọi API stats và hiển thị số lượng ảnh trong phần statsBar


# ============================================================
# TÍNH NĂNG 5: ĐỔI THEME SÁNG / TỐI
# ============================================================
# Sửa file: frontend/src/index.css
# Thêm CSS variables cho light theme

"""
/* THEME TỐI (mặc định) */
:root {
  --bg: #0a0a0a;
  --surface: #111111;
  --text: #e8e4dc;
  /* ... */
}

/* ✅ THÊM MỚI: THEME SÁNG */
[data-theme="light"] {
  --bg: #f5f5f0;
  --surface: #ffffff;
  --surface2: #f0ede8;
  --border: #e0ddd8;
  --border-light: #d0cdc8;
  --text: #1a1a1a;
  --text-muted: #6a6660;
  --text-dim: #9a9690;
  --accent: #b8860b;
}
"""

# Sửa file: frontend/src/context/AuthContext.jsx hoặc tạo ThemeContext.jsx mới:
"""
// ThemeContext.jsx
import { createContext, useContext, useState, useEffect } from 'react'

const ThemeContext = createContext(null)

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(
    () => localStorage.getItem('theme') || 'dark'
  )

  useEffect(() => {
    // Áp dụng theme lên thẻ <html>
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('theme', theme)
  }, [theme])

  const toggle = () => setTheme(t => t === 'dark' ? 'light' : 'dark')

  return (
    <ThemeContext.Provider value={{ theme, toggle }}>
      {children}
    </ThemeContext.Provider>
  )
}

export const useTheme = () => useContext(ThemeContext)
"""

# Sửa file: frontend/src/components/Navbar.jsx
# Thêm nút toggle theme:
"""
const { theme, toggle } = useTheme()

<button onClick={toggle} className="btn-icon" title="Đổi theme">
  {theme === 'dark' ? '☀️' : '🌙'}
</button>
"""


# ============================================================
# TÍNH NĂNG 6: TRANG PROFILE
# ============================================================
# Tạo file mới: frontend/src/pages/ProfilePage.jsx

"""
import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { authAPI } from '../api'

export default function ProfilePage() {
  const { user } = useAuth()
  const [stats, setStats] = useState(null)

  // Lấy thống kê ảnh khi load trang
  useEffect(() => {
    api.get('/photos/stats').then(r => setStats(r.data))
  }, [])

  return (
    <div>
      <h1>Hồ sơ của {user.username}</h1>
      <p>Email: {user.email}</p>
      <p>Tổng số ảnh: {stats?.total_photos ?? '...'}</p>
    </div>
  )
}
"""

# Sửa file: frontend/src/App.jsx
# Thêm route mới:
"""
import ProfilePage from './pages/ProfilePage'

// Thêm vào trong <Routes>:
<Route path="/profile" element={<PrivateRoute><ProfilePage /></PrivateRoute>} />
"""

# Sửa file: frontend/src/components/Navbar.jsx
# Thêm link đến trang profile trong dropdown menu
