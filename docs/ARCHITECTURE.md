# 活動報名系統 架構設計文件 (Architecture Document)

## 1. 技術架構說明

本專案採用 **Python + Flask** 搭配 **Jinja2** 模板引擎渲染畫面，並以 **SQLite** 作為資料庫儲存方案。不採用前後端分離，藉此加快 MVP 版本的開發建置速度。

### 選用技術與原因
- **後端框架**：Flask。具備輕量、開發快速的特性，有豐富的擴充套件可以滿足基礎需求。
- **模板引擎**：Jinja2。直接與 Flask 整合，可以在伺服器端渲染 HTML，降低前端狀態管理的複雜度，並且具備優秀的安全性（自動跳脫字元）。
- **資料庫**：SQLite。免安裝伺服器軟體的輕量級資料庫，將資料儲存在單一檔案中，非常適合小到中型規模或 MVP 專案。

### Flask MVC 模式說明
* **Model (資料模型)**：負責定義資料儲存格式（例如：使用者、活動、票券資料表）。透過 Python 的類別與資料表進行對應（ORM）。
* **View (視圖)**：負責呈現結果給使用者。本專案以 Jinja2 的 HTML 等模板來當作視圖。
* **Controller (控制器)**：負責接聽路由（Routing）、處理商業邏輯與對 Models 存取。本專案對應為 Flask 的 Route。

---

## 2. 專案資料夾結構

本專案將採以下結構來組織程式碼：

```text
app/
 ├── models/            # 存放所有資料庫模型定義與操作
 │   ├── user.py        # 會員 Model
 │   ├── event.py       # 活動 Model
 │   └── registration.py# 報名與票券 Model
 ├── routes/            # 存放所有路由控制器 (Controller)
 │   ├── auth.py        # 註冊登入路由
 │   ├── event.py       # 活動顯示與管理路由
 │   └── webhook.py     # 金流或其他自動通知處理路由
 ├── templates/         # 存放所有的 Jinja2 HTML 頁面 (View)
 │   ├── base.html      # 全域通用樣板 (Header / Footer)
 │   ├── home.html      # 首頁
 │   ├── events/        # 相關活動與報名頁面
 │   └── auth/          # 註冊與登入頁面
 ├── static/            # 存放前端靜態資源
 │   ├── css/           # 自訂 CSS 樣式
 │   ├── js/            # 客製化或增強互動的 JS
 │   └── images/        # 圖檔與 Logo
 ├── utils/             # 共用工具函式 (如：寄信、產生 QR Code 程式)
 │   └── qr_gen.py      # QR Code 生成模組
 ├── config.py          # 全域環境與設定檔
instance/
 └── database.db        # SQLite 資料庫實體檔案 (勿推送到 Git)
docs/
 ├── PRD.md             # 產品需求文件
 └── ARCHITECTURE.md    # 系統架構設計 (本文件)
app.py                  # Flask 應用程式啟動入口
requirements.txt        # 紀錄 Python 套件依賴
.gitignore              # 忽略不需要進行版本控制的檔案或是敏感資料
```

---

## 3. 元件關係圖

以下展示使用者從瀏覽器發送請求，如何依序經過 Route、存取 Model、從資料庫取資料再經過 Jinja2 渲染傳回。

```mermaid
graph TD
    Client[使用者的瀏覽器]
    
    subgraph Flask Application
        Router[Flask Route (Controller)]
        Model[Models]
        Jinja[Jinja2 Template (View)]
    end
    
    DB[(SQLite 資料庫)]
    
    Client -- 1. 發出 HTTP 請求 --> Router
    Router -- 2. 讀寫資料、商業邏輯 --> Model
    Model -- 3. SQL 查詢與變更 --> DB
    DB -- 4. 回傳實體資料 --> Model
    Model -- 5. 資料打包傳遞 --> Router
    Router -- 6. 拋送資料進行渲染 --> Jinja
    Jinja -- 7. 產生最終 HTML 回傳 --> Client
```

---

## 4. 關鍵設計決策

1. **傳統伺服器渲染 (SSR) 取代前後端分離**：
   - *原因*：為了最快部署 MVP 並驗證市場，減少前後端 API 介接溝通的成本。同時 Jinja2 亦有利於基礎的 SEO 與靜態內容爬取。

2. **選擇 SQLite 作為主資料庫**：
   - *原因*：減輕運維負擔，開發與部署流程簡化且不需要專門管理 DB 伺服器；未來若有高規模的營運量，也可平順切換至 PostgreSQL。

3. **模組化的路由設計 (Blueprint)**：
   - *原因*：我們將 `routes` 根據業務拆分 (`auth.py`, `event.py`)，並利用 Flask 的 Blueprint 註冊到 `app.py` 中，確保專案結構擴充時不會變得難以維護。

4. **動態表單使用 JSON / 長文字欄位彈性儲存預留**：
   - *原因*：因應 PRD 提到的「動態報名表單編輯器」，活動客製化欄位容易變動，系統結構預計未來可用 JSON 結構或關聯表單設計保留動態擴充彈性，以防頻繁更改資料表。
