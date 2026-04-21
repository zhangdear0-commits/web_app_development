# 活動報名系統 流程圖 (Flowcharts)

本文件基於 PRD 與 ARCHITECTURE 設計，將系統的操作路徑與資料流視覺化。包含使用者流程圖、註冊報名流程的系統序列圖，以及系統功能對應的 URL 路徑清單。

## 1. 使用者流程圖 (User Flow)

展示「活動主辦者」與「一般參加者」在系統中的主要操作路線。

### 1-1. 一般參加者流程
```mermaid
flowchart LR
    A([進入網站首頁]) --> B[瀏覽活動列表]
    B --> C[點擊進入活動詳情]
    C --> D{點擊前往報名}
    
    D -->|尚未登入| E[註冊 / 登入]
    E --> F[填寫動態報名表單]
    D -->|已登入| F
    
    F --> G{報名名額判斷}
    G -->|額滿| H[自動轉入候補名單]
    H --> I[當有人取消，收到遞補通知]
    I --> F
    
    G -->|有餘裕| J[報名成功，產生 QR Code 票券]
    J --> K[發送 Email 通知]
    
    K --> L[活動當天出示 QR Code 簽到]
```

### 1-2. 活動主辦者流程
```mermaid
flowchart LR
    A([登入主辦者後台]) --> B[後台管理 Dashboard]
    B --> C{選擇管理操作}
    
    C -->|建立新活動| D[填寫活動資訊 & 設定動態表單]
    D --> E[發布活動，開放報名]
    
    C -->|管理現有活動| F[查看名單與候補狀態]
    F --> G[編輯表單或處理取消報名]
    
    C -->|分析報名狀況| H[查看圖表趨勢與分析]
    H --> I[匯出 Excel 名單]
    
    C -->|現場簽到作業| J[打開手機鏡頭掃描 QR Code]
    J --> K[自動更新參加者為「已報到」]
```

---

## 2. 系統序列圖 (Sequence Diagram)

此序列圖展示一般參加者「送出報名表單」到「產生票券」之間，系統前後端的資料流運作過程。其中包含了高併發情況下的簡單鎖定機制確保名額不超賣。

```mermaid
sequenceDiagram
    actor User as 一般參加者
    participant Browser as 瀏覽器 (Frontend)
    participant Flask as Flask Route (Controller)
    participant DB as SQLite (Models)
    participant Email as Email 發布模組

    User->>Browser: 填寫資料並點擊「送出報名」
    Browser->>Flask: POST /event/<id>/register (攜帶表單資料)
    
    Flask->>Flask: 資料格式驗證防呆
    Flask->>DB: 開啟資料庫交易 (Transaction)
    DB-->>Flask: Lock Event Row (避免同時超賣)
    
    Flask->>DB: 檢查 Event 剩餘名額
    alt 尚有名額
        Flask->>DB: INSERT INTO Registrations (狀態: 成功)
        Flask->>DB: UPDATE Event (減少 1 名額)
        DB-->>Flask: 交易 Commit 成功
        Flask->>Flask: 呼叫 QR Gen 產生票券圖片
        Flask->>Email: 背景觸發系統發送 "報名成功" 信件
        Flask-->>Browser: HTTP 302 重導向到報名成功頁
        Browser-->>User: 顯示報名成功 & QRCode
    else 名額已滿
        Flask->>DB: INSERT INTO Registrations (狀態: 候補)
        DB-->>Flask: 交易 Commit 成功
        Flask-->>Browser: HTTP 302 重導向到候補成功頁
        Browser-->>User: 顯示目前候補順位
    end
```

---

## 3. 功能清單對照表

列出系統主要功能及其對應的 URL 路徑與 HTTP 操作方法（路由規劃）。

| 功能描述 | HTTP 方法 | URL 路徑 (Endpoint) | 負責元件 / 對應的操作 |
| --- | --- | --- | --- |
| 瀏覽首頁活動列表 | `GET` | `/` | 顯示所有開放中活動 |
| 註冊會員 | `GET` / `POST`| `/auth/register` | 會員註冊頁面 / 送出註冊資料 |
| 會員登入 | `GET` / `POST`| `/auth/login` | 會員登入頁面 / 送出登入驗證 |
| 建立新活動 (主辦方) | `GET` / `POST`| `/events/create` | 新增活動表單頁 / 寫入新活動 |
| 檢視活動詳情 | `GET` | `/events/<event_id>` | 取得該活動的詳細資訊介紹 |
| 報名活動 (參加方) | `GET` / `POST`| `/events/<event_id>/register` | 選填動態欄位表單 / 送出報名或候補 |
| 活動管理儀表板 | `GET` | `/dashboard/<event_id>` | 分頁呈現名單總覽與視覺化圖表 |
| 匯出報名名單 | `GET` | `/events/<event_id>/export` | 使用者下載 Excel 格式檔案 |
| QR Code 現場簽到 | `POST` | `/events/<event_id>/check-in` | 掃描後送出請求更改用戶為「已簽到」 |
