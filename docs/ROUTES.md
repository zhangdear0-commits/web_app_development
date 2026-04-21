# 活動報名系統 路由設計文件 (API & Routes Design)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 (活動列表) | GET | `/` | `templates/home.html` | 顯示目前開放報名的所有活動 |
| 註冊首頁 | GET | `/auth/register` | `templates/auth/register.html` | 顯示註冊表單 |
| 送出註冊 | POST | `/auth/register` | — | 建立帳號並重導向至登入頁 |
| 登入首頁 | GET | `/auth/login` | `templates/auth/login.html` | 顯示登入表單 |
| 送出登入 | POST | `/auth/login` | — | 驗證密碼，成功則重導向首頁或後台 |
| 建立活動頁面 | GET | `/events/create` | `templates/events/create.html` | 顯示建立活動之表單（含動態欄位設定） |
| 寫入新活動 | POST | `/events/create` | — | 存入資料庫，建立活動並重導向活動詳情 |
| 活動詳情 | GET | `/events/<id>` | `templates/events/detail.html` | 顯示單一活動完整資訊與參加按鈕 |
| 報名表單頁面 | GET | `/events/<id>/register` | `templates/events/register.html` | 根據主辦自定義欄位，動態渲染報名表單 |
| 送出報名 | POST | `/events/<id>/register` | — | 處理報名/候補邏輯，寄信並重導向提示頁面 |
| 活動管理儀表板 | GET | `/dashboard/<id>` | `templates/events/dashboard.html` | 顯示該活動的報名統計圖表與名單 |
| 匯出報名名單 | GET | `/events/<id>/export` | — | 下載 Excel 格式之參加者名單 |
| QR Code 現場簽到 | POST | `/events/<id>/check-in` | — | 接收 QR token 並更新簽到狀態回傳成功或失敗 |

## 2. 每個路由的詳細說明

### `GET /` (首頁)
- **處理邏輯**：呼叫 `Event.get_all()` 取得開放中活動列表。
- **輸出**：渲染 `home.html` 帶入 event 列表。

### `GET /auth/login` 與 `POST /auth/login`
- **輸入**：Email, Password
- **處理邏輯**：透過 `User` 模型驗證登入資訊是否吻合，將 User ID 存入 session。
- **錯誤處理**：驗證失敗則 Flash 錯誤訊息並重新渲染登入頁。

### `GET /events/create` 與 `POST /events/create`
- **輸入**：表單包含名稱、時間、名額限制、自訂欄位 Schema 等。
- **處理邏輯**：將這些資料利用 `Event.create()` 存入。
- **輸出**：成功後重導向至 `/events/<id>`。

### `GET /events/<id>/register` 與 `POST /events/<id>/register`
- **輸入**：參加者填寫的動態欄位對應內容。
- **處理邏輯**：開啟資料庫 Transaction 防超賣。建立 `Registration` 紀錄，如名額滿設定為候補。利用 `qr_gen.py` 產生 QR Code Token，並呼叫 Email 模組寄信。
- **輸出**：成功後重導回活動列表或報名成功頁面。

### `POST /events/<id>/check-in`
- **輸入**：QR Code Token 參數。
- **處理邏輯**：搜尋 `Registration` 符合該 token 且未簽到者，更新為 `checked_in` 狀態。
- **輸出**：JSON 格式之成功或失敗狀態，供手機端/前端接收。

## 3. Jinja2 模板清單

- 共用基礎：`templates/base.html` (被其他模板繼承的基底框架，含 Navbar & Footer)
- 首頁：`templates/home.html` (繼承 `base.html`)
- 帳號類：
  - `templates/auth/register.html`
  - `templates/auth/login.html`
- 活動類：
  - `templates/events/create.html` (建立活動表單)
  - `templates/events/detail.html` (活動預覽詳細介紹)
  - `templates/events/register.html` (參加者填寫報名表單介面)
  - `templates/events/dashboard.html` (主辦方管理後台與圖表)

## 4. 路由骨架程式碼
請參考以下專案目錄，我們已經完成了各個 Flask Route (.py 檔) 的骨架建立：
- `app/routes/main.py`
- `app/routes/auth.py`
- `app/routes/event.py`
