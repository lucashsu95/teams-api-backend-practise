# 團隊管理 API 應用程式

這是一個使用 Python Flask 開發的簡單團隊管理 API 應用程式，支援 Docker 容器化部署。

## 功能特色

- 完整的團隊 CRUD 操作（新增、查詢、更新、刪除）
- 標準化的 API 回應格式
- 錯誤處理和驗證
- Docker 容器化支援
- RESTful API 設計

## API 端點

### 1. 健康檢查
```
GET /health
```

### 2. 取得所有團隊
```
GET /api/teams
```

### 3. 取得特定團隊
```
GET /api/teams/{team_id}
```

### 4. 新增團隊
```
POST /api/teams
Content-Type: application/json

{
  "name": "團隊名稱",
  "members": ["成員1", "成員2"]
}
```

### 5. 更新團隊
```
PUT /api/teams/{team_id}
Content-Type: application/json

{
  "name": "新團隊名稱",
  "members": ["新成員1", "新成員2"]
}
```

### 6. 刪除團隊
```
DELETE /api/teams/{team_id}
```

## API 回應格式

所有 API 都遵循統一的回應格式：

```json
{
  "result": true,
  "errorCode": "",
  "message": "成功訊息",
  "data": {
    // 實際資料
  }
}
```

## 安裝與執行

### 方法一：使用 Docker（推薦）

1. **複製專案檔案**
   ```bash
   # 確保所有檔案都在同一個目錄中：
   # - app.py
   # - Dockerfile
   # - requirements.txt
   # - docker-compose.yml
   # - README.md
   ```

2. **建立並啟動容器**
   ```bash
   docker-compose up --build
   ```

3. **背景執行**
   ```bash
   docker-compose up -d --build
   ```

4. **停止服務**
   ```bash
   docker-compose down
   ```

5. **填充測式資料**
   ```bash
   docker-compose exec flask-app python seeders.py
   ```
  

### 方法二：本地執行

1. **安裝依賴套件**
   ```bash
   pip install -r requirements.txt
   ```

2. **執行應用程式**
   ```bash
   python app.py
   ```
3. **填充測式資料**
   ```bash
   docker-compose exec flask-app python seeders.py
   ```

4. **應用程式將在 http://localhost:8080 啟動**

## 手動測試指南

### 1. 健康檢查測試
```bash
curl -X GET http://localhost:8080/health
```

**預期回應：**
```json
{
  "result": true,
  "errorCode": "",
  "message": "Service is healthy",
  "data": null
}
```

### 2. 新增團隊測試
```bash
curl -X POST http://localhost:8080/api/teams \
  -H "Content-Type: application/json" \
  -d '{
    "name": "開發團隊",
    "members": ["張三", "李四", "王五"]
  }'
```

**預期回應：**
```json
{
  "result": true,
  "errorCode": "",
  "message": "Team created successfully",
  "data": {
    "team": {
      "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "name": "開發團隊",
      "members": ["張三", "李四", "王五"],
      "createdAt": "2025-06-07T10:30:00.000000",
      "updatedAt": "2025-06-07T10:30:00.000000"
    }
  }
}
```

### 3. 取得所有團隊測試
```bash
curl -X GET http://localhost:8080/api/teams
```

**預期回應：**
```json
{
  "result": true,
  "errorCode": "",
  "message": "Teams retrieved successfully",
  "data": {
    "teams": [
      {
        "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "name": "開發團隊",
        "members": ["張三", "李四", "王五"],
        "createdAt": "2025-06-07T10:30:00.000000",
        "updatedAt": "2025-06-07T10:30:00.000000"
      }
    ],
    "total": 1
  }
}
```

### 4. 取得特定團隊測試
```bash
# 使用上述回應中的 team_id
curl -X GET http://localhost:8080/api/teams/{team_id}
```

### 5. 更新團隊測試
```bash
curl -X PUT http://localhost:8080/api/teams/{team_id} \
  -H "Content-Type: application/json" \
  -d '{
    "name": "後端開發團隊",
    "members": ["張三", "李四", "王五", "趙六"]
  }'
```

### 6. 刪除團隊測試
```bash
curl -X DELETE http://localhost:8080/api/teams/{team_id}
```

**預期回應：**
```json
{
  "result": true,
  "errorCode": "",
  "message": "Team deleted successfully",
  "data": {
    "deletedTeamId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  }
}
```

## 錯誤處理測試

### 1. 測試新增空名稱團隊
```bash
curl -X POST http://localhost:8080/api/teams \
  -H "Content-Type: application/json" \
  -d '{
    "name": "",
    "members": []
  }'
```

**預期回應：**
```json
{
  "result": false,
  "errorCode": "INVALID_TEAM_NAME",
  "message": "Team name cannot be empty",
  "data": null
}
```

### 2. 測試查詢不存在的團隊
```bash
curl -X GET http://localhost:8080/api/teams/non-existent-id
```

**預期回應：**
```json
{
  "result": false,
  "errorCode": "TEAM_NOT_FOUND",
  "message": "Team not found",
  "data": null
}
```

## 專案結構

```
.
├── app.py              # 主要應用程式檔案
├── Dockerfile          # Docker 映像建構檔案
├── docker-compose.yml  # Docker Compose 設定檔
├── requirements.txt    # Python 依賴套件清單
└── README.md          # 專案說明文件
```

## 注意事項

1. **資料持久化**：目前使用記憶體儲存資料，重啟服務後資料會消失。實際應用建議整合真實資料庫（如 PostgreSQL 或 MongoDB）。

2. **安全性**：這是基礎範例，實際應用需要加入身份驗證、授權和輸入驗證等安全機制。

3. **擴展性**：可以加入分頁、搜尋、排序等功能來增強 API 的實用性。

4. **監控與日誌**：建議加入日誌記錄和監控機制以便於維護和除錯。

## 開發環境

- Python 3.11
- Flask 2.3.3
- Docker & Docker Compose