# ============================================================
# TÍNH NĂNG 15: CHIA SẺ ẢNH CÔNG KHAI (PUBLIC LINK)
# ============================================================
# Sửa file: backend/models.py - thêm trường is_public và share_token

import secrets  # Thư viện tạo token ngẫu nhiên

class Photo(Base):
    # ... (các field cũ) ...
    # ✅ THÊM MỚI: ảnh có công khai không (mặc định là riêng tư)
    is_public = Column(Boolean, default=False, nullable=False)
    # ✅ THÊM MỚI: token duy nhất để share (vd: "abc123xyz")
    share_token = Column(String, unique=True, nullable=True)

# Sửa file: backend/main.py - thêm 2 endpoint mới

@app.post("/api/photos/{photo_id}/share")
def toggle_share(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    photo = db.query(Photo).filter(
        Photo.id == photo_id, Photo.user_id == current_user.id
    ).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Không tìm thấy ảnh")

    if photo.is_public:
        # ✅ Nếu đang public -> chuyển thành private, xóa token
        photo.is_public = False
        photo.share_token = None
        message = "Đã đặt ảnh thành riêng tư"
    else:
        # ✅ Nếu đang private -> chuyển thành public, tạo token mới
        photo.is_public = True
        photo.share_token = secrets.token_urlsafe(16)  # Tạo token 16 ký tự ngẫu nhiên
        message = "Đã tạo link chia sẻ"

    db.commit()
    db.refresh(photo)
    return {"message": message, "share_token": photo.share_token, "is_public": photo.is_public}


@app.get("/api/shared/{share_token}")
def view_shared_photo(share_token: str, db: Session = Depends(get_db)):
    # ✅ Endpoint công khai - không cần đăng nhập
    # Ai có link đều xem được
    photo = db.query(Photo).filter(
        Photo.share_token == share_token,
        Photo.is_public == True
    ).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Link không hợp lệ hoặc đã bị thu hồi")
    return photo

# Sửa file: frontend/src/pages/PhotoDetailPage.jsx
# Thêm nút Share:
"""
const handleShare = async () => {
  const { data } = await photoAPI.toggleShare(photo.id)
  if (data.share_token) {
    const shareUrl = `${window.location.origin}/shared/${data.share_token}`
    navigator.clipboard.writeText(shareUrl)
    alert('Đã copy link chia sẻ!')
  } else {
    alert('Đã đặt ảnh thành riêng tư')
  }
}

<button className="btn-ghost" onClick={handleShare}>
  {photo.is_public ? '🔒 Thu hồi link' : '🔗 Tạo link chia sẻ'}
</button>
"""


# ============================================================
# TÍNH NĂNG 16: ALBUM / FOLDER
# ============================================================
# Sửa file: backend/models.py - thêm model Album mới

class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)           # Tên album
    description = Column(Text, nullable=True)       # Mô tả album
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Quan hệ với User
    owner = relationship("User", back_populates="albums")
    # Quan hệ với Photo (1 album có nhiều ảnh)
    photos = relationship("PhotoAlbum", back_populates="album", cascade="all, delete")

# ✅ THÊM MỚI: bảng trung gian Album-Photo (quan hệ nhiều-nhiều)
# 1 ảnh có thể thuộc nhiều album, 1 album chứa nhiều ảnh
class PhotoAlbum(Base):
    __tablename__ = "photo_albums"

    id = Column(Integer, primary_key=True, index=True)
    photo_id = Column(Integer, ForeignKey("photos.id"), nullable=False)
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False)

    photo = relationship("Photo", back_populates="albums")
    album = relationship("Album", back_populates="photos")

# Sửa model Photo: thêm relationship
# albums = relationship("PhotoAlbum", back_populates="photo")

# Sửa model User: thêm relationship
# albums = relationship("Album", back_populates="owner", cascade="all, delete")

# Sửa file: backend/main.py - thêm CRUD endpoints cho Album

@app.get("/api/albums")
def list_albums(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # ✅ Lấy tất cả album của user
    return db.query(Album).filter(Album.user_id == current_user.id).all()

@app.post("/api/albums", status_code=201)
def create_album(name: str, description: Optional[str] = None,
                 db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # ✅ Tạo album mới
    album = Album(name=name, description=description, user_id=current_user.id)
    db.add(album)
    db.commit()
    db.refresh(album)
    return album

@app.post("/api/albums/{album_id}/photos/{photo_id}")
def add_photo_to_album(album_id: int, photo_id: int,
                       db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # ✅ Thêm ảnh vào album
    # Kiểm tra album và ảnh thuộc về user hiện tại
    album = db.query(Album).filter(Album.id == album_id, Album.user_id == current_user.id).first()
    photo = db.query(Photo).filter(Photo.id == photo_id, Photo.user_id == current_user.id).first()
    if not album or not photo:
        raise HTTPException(status_code=404, detail="Album hoặc ảnh không tồn tại")

    # Kiểm tra ảnh chưa có trong album
    existing = db.query(PhotoAlbum).filter(
        PhotoAlbum.album_id == album_id, PhotoAlbum.photo_id == photo_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ảnh đã có trong album")

    photo_album = PhotoAlbum(photo_id=photo_id, album_id=album_id)
    db.add(photo_album)
    db.commit()
    return {"message": "Đã thêm ảnh vào album"}


# ============================================================
# TÍNH NĂNG 17: YÊU THÍCH ẢNH (LIKE / BOOKMARK)
# ============================================================
# Sửa file: backend/models.py - thêm trường is_favorite

class Photo(Base):
    # ... (các field cũ) ...
    # ✅ THÊM MỚI: đánh dấu ảnh yêu thích
    is_favorite = Column(Boolean, default=False, nullable=False)

# Sửa file: backend/main.py - thêm endpoint toggle favorite

@app.post("/api/photos/{photo_id}/favorite")
def toggle_favorite(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    photo = db.query(Photo).filter(
        Photo.id == photo_id, Photo.user_id == current_user.id
    ).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Không tìm thấy ảnh")

    # ✅ Toggle: nếu đang yêu thích thì bỏ, nếu chưa thì thêm
    photo.is_favorite = not photo.is_favorite
    db.commit()
    db.refresh(photo)

    return {
        "is_favorite": photo.is_favorite,
        "message": "Đã thêm vào yêu thích" if photo.is_favorite else "Đã xóa khỏi yêu thích"
    }

# Sửa file: frontend/src/components/PhotoCard.jsx
# Thêm nút tim yêu thích trên ảnh:
"""
const handleFavorite = async (e) => {
  e.stopPropagation()  // Không navigate vào detail khi click tim
  const { data } = await photoAPI.toggleFavorite(photo.id)
  onUpdate({ ...photo, is_favorite: data.is_favorite })
}

// Thêm vào phần overlay của card:
<button
  style={{
    background: photo.is_favorite ? 'rgba(220,50,50,0.85)' : 'rgba(0,0,0,0.5)',
    ...
  }}
  onClick={handleFavorite}
>
  {photo.is_favorite ? '♥' : '♡'}
</button>
"""

# Sửa file: frontend/src/pages/GalleryPage.jsx
# Thêm tab lọc "Yêu thích":
"""
// Thêm vào phần filter:
<button onClick={() => fetchPhotos('', 'date_desc', true)}>
  ♥ Yêu thích
</button>
"""


# ============================================================
# TÍNH NĂNG 18: THỐNG KÊ - BIỂU ĐỒ SỐ ẢNH THEO THÁNG
# ============================================================
# Sửa file: backend/main.py - thêm endpoint thống kê

from sqlalchemy import func, extract

@app.get("/api/stats")
def get_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ✅ Đếm số ảnh upload theo từng tháng trong năm hiện tại
    from datetime import datetime as dt
    current_year = dt.now().year

    monthly = db.query(
        extract('month', Photo.uploaded_at).label('month'),  # Lấy tháng
        func.count(Photo.id).label('count')                  # Đếm số ảnh
    ).filter(
        Photo.user_id == current_user.id,
        extract('year', Photo.uploaded_at) == current_year   # Chỉ lấy năm hiện tại
    ).group_by('month').all()

    # Tạo dict với đủ 12 tháng (tháng nào không có ảnh thì count = 0)
    monthly_data = {i: 0 for i in range(1, 13)}
    for month, count in monthly:
        monthly_data[int(month)] = count

    # ✅ Thống kê tổng quan
    total_photos = db.query(func.count(Photo.id)).filter(Photo.user_id == current_user.id).scalar()

    return {
        "total_photos": total_photos,
        "monthly_uploads": [
            {"month": m, "count": c} for m, c in monthly_data.items()
        ],
        "year": current_year,
    }

# Tạo file mới: frontend/src/pages/StatsPage.jsx
# Dùng thư viện recharts để vẽ biểu đồ (cài: npm install recharts):
"""
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

const MONTH_NAMES = ['T1','T2','T3','T4','T5','T6','T7','T8','T9','T10','T11','T12']

export default function StatsPage() {
  const [stats, setStats] = useState(null)

  useEffect(() => {
    api.get('/stats').then(r => setStats(r.data))
  }, [])

  if (!stats) return <div>Đang tải...</div>

  const chartData = stats.monthly_uploads.map(item => ({
    name: MONTH_NAMES[item.month - 1],
    'Số ảnh': item.count,
  }))

  return (
    <div>
      <h1>Thống kê</h1>
      <p>Tổng số ảnh: {stats.total_photos}</p>

      <h2>Ảnh upload theo tháng ({stats.year})</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="Số ảnh" fill="#c9a84c" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
"""


# ============================================================
# TÍNH NĂNG 19: TỰ ĐỘNG TẠO THUMBNAIL KHI UPLOAD
# ============================================================
# Sửa file: backend/models.py - thêm trường thumbnail_url

class Photo(Base):
    # ... (các field cũ) ...
    # ✅ THÊM MỚI: URL của ảnh thumbnail (nhỏ hơn để load nhanh)
    thumbnail_url = Column(String, nullable=True)

# Sửa file: backend/main.py - hàm upload_photo
# Thêm code tạo thumbnail sau khi lưu ảnh gốc:

THUMBNAIL_SIZE = (400, 400)  # Kích thước thumbnail tối đa

async def create_thumbnail(contents: bytes, original_filename: str) -> str:
    """Tạo ảnh thumbnail nhỏ hơn từ ảnh gốc"""
    # Mở ảnh gốc
    img = Image.open(io.BytesIO(contents))

    # Chuyển sang RGB nếu là PNG có alpha channel (RGBA)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    # ✅ thumbnail() tự resize giữ nguyên tỉ lệ, không vượt THUMBNAIL_SIZE
    img.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)

    # Lưu thumbnail với tên khác
    thumb_filename = f"thumb_{original_filename}"
    thumb_path = os.path.join(UPLOAD_DIR, thumb_filename)

    img.save(thumb_path, "JPEG", quality=85, optimize=True)
    return f"/uploads/{thumb_filename}"

# Trong hàm upload_photo, sau khi lưu file gốc, thêm:
"""
# ✅ Tạo thumbnail
thumbnail_url = await create_thumbnail(contents, filename)

photo = Photo(
    title=title,
    description=description,
    image_url=f"/uploads/{filename}",      # Ảnh gốc
    thumbnail_url=thumbnail_url,            # Ảnh thumbnail
    user_id=current_user.id,
)
"""

# Sửa file: frontend/src/components/PhotoCard.jsx
# Dùng thumbnail thay vì ảnh gốc để load nhanh hơn:
"""
<img
  // ✅ Dùng thumbnail cho gallery (load nhanh)
  // Fallback về ảnh gốc nếu không có thumbnail
  src={photo.thumbnail_url || photo.image_url}
  alt={photo.title}
  style={styles.img}
  loading="lazy"
/>
"""


# ============================================================
# TÍNH NĂNG 20: XÓA TÀI KHOẢN
# ============================================================
# Sửa file: backend/main.py - thêm endpoint xóa tài khoản

@app.delete("/api/auth/account", status_code=204)
def delete_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ✅ Lấy tất cả ảnh của user
    photos = db.query(Photo).filter(Photo.user_id == current_user.id).all()

    # ✅ Xóa từng file ảnh khỏi ổ đĩa
    for photo in photos:
        # Xóa ảnh gốc
        filepath = "." + photo.image_url
        if os.path.exists(filepath):
            os.remove(filepath)

        # Xóa thumbnail nếu có (tính năng 19)
        if hasattr(photo, 'thumbnail_url') and photo.thumbnail_url:
            thumb_path = "." + photo.thumbnail_url
            if os.path.exists(thumb_path):
                os.remove(thumb_path)

    # ✅ Xóa user khỏi database
    # Cascade sẽ tự xóa tất cả Photo liên quan (đã cấu hình trong models.py)
    db.delete(current_user)
    db.commit()

    # Trả về 204 No Content (không có body)

# Sửa file: frontend/src/pages/ProfilePage.jsx
# Thêm nút xóa tài khoản với xác nhận:
"""
const handleDeleteAccount = async () => {
  // Yêu cầu user gõ lại username để xác nhận
  const confirm = window.prompt(
    `Nhập username "${user.username}" để xác nhận xóa tài khoản. Hành động này KHÔNG THỂ hoàn tác!`
  )

  if (confirm !== user.username) {
    alert('Username không khớp, đã hủy xóa tài khoản')
    return
  }

  try {
    await authAPI.deleteAccount()
    logout()              // Xóa token và user khỏi localStorage
    navigate('/login')    // Chuyển về trang đăng nhập
    alert('Tài khoản đã được xóa')
  } catch (err) {
    alert('Xóa tài khoản thất bại: ' + err.response?.data?.detail)
  }
}

// Nút xóa tài khoản - đặt ở cuối trang Profile, màu đỏ rõ ràng
<div style={{ marginTop: '3rem', borderTop: '1px solid var(--border)', paddingTop: '1.5rem' }}>
  <h3 style={{ color: 'var(--danger)', marginBottom: '0.5rem' }}>Vùng nguy hiểm</h3>
  <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '1rem' }}>
    Xóa tài khoản sẽ xóa vĩnh viễn tất cả ảnh và dữ liệu. Không thể khôi phục.
  </p>
  <button className="btn-danger" onClick={handleDeleteAccount}>
    🗑 Xóa tài khoản vĩnh viễn
  </button>
</div>
"""

# Sửa file: frontend/src/api.js - thêm:
# deleteAccount: () => api.delete('/auth/account'),
