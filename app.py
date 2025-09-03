from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from flasgger import Swagger
from datetime import datetime
import uuid
import os

app = Flask(__name__)

# ✅ 正確配置 Swagger
app.config['SWAGGER'] = {
    'title': 'Team Management API',
    'uiversion': 3
}
swagger = Swagger(app)

# ✅ 啟用跨域 - 允許所有域名訪問
CORS(app, 
     origins='*',
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'])

# ✅ 模擬資料庫
teams_db = {}

class Team:
    def __init__(self, name, members):
        self.id = str(uuid.uuid4())
        self.name = name
        self.members = members
        self.createdAt = datetime.utcnow().isoformat()
        self.updatedAt = datetime.utcnow().isoformat()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'members': self.members,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt
        }

def auto_seed_data():
    if len(teams_db) == 0:
        print("🌱 自動填充初始資料")
        sample_teams = [
            {"name": "前端開發團隊", "members": ["張三", "李四", "王五"]},
            {"name": "後端開發團隊", "members": ["趙六", "錢七", "孫八"]},
            {"name": "UI/UX 設計團隊", "members": ["周九", "吳十"]},
            {"name": "DevOps 團隊", "members": ["鄭十一", "王十二", "馮十三"]},
            {"name": "產品管理團隊", "members": ["陳十四", "褚十五"]}
        ]
        for team_data in sample_teams:
            team = Team(team_data["name"], team_data["members"])
            teams_db[team.id] = team
        print(f"✅ 建立 {len(sample_teams)} 筆資料")

def create_api_response(result=True, error_code="", message="", data=None):
    return {
        'result': result,
        'errorCode': error_code,
        'message': message,
        'data': data
    }

@app.route('/')
def redirect_to_docs():
    return redirect('/apidocs')

@app.route('/health', methods=['GET'])
def health_check():
    """
    健康檢查
    ---
    tags:
      - System
    summary: API 健康檢查
    description: 檢查 API 服務是否正常運行
    responses:
      200:
        description: 服務正常運行
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: true
            errorCode:
              type: string
              example: ""
            message:
              type: string
              example: "Service is healthy"
            data:
              type: "null"
              example: null
    """
    return jsonify(create_api_response(message="Service is healthy"))

@app.route('/api/teams', methods=['GET'])
def get_teams():
    """
    取得所有團隊列表
    ---
    tags:
      - Teams
    summary: 取得所有團隊
    description: 獲取系統中所有團隊的列表，包含每個團隊的詳細資訊
    responses:
      200:
        description: 成功取得團隊列表
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: true
            errorCode:
              type: string
              example: ""
            message:
              type: string
              example: "Teams retrieved successfully"
            data:
              type: object
              properties:
                teams:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: string
                        example: "550e8400-e29b-41d4-a716-446655440000"
                      name:
                        type: string
                        example: "前端開發團隊"
                      members:
                        type: array
                        items:
                          type: string
                        example: ["張三", "李四", "王五"]
                      createdAt:
                        type: string
                        format: date-time
                        example: "2023-12-01T10:30:00.000000"
                      updatedAt:
                        type: string
                        format: date-time
                        example: "2023-12-01T10:30:00.000000"
                total:
                  type: integer
                  example: 5
      500:
        description: 伺服器內部錯誤
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: false
            errorCode:
              type: string
              example: "GET_TEAMS_ERROR"
            message:
              type: string
              example: "Internal server error"
            data:
              type: "null"
              example: null
    """
    try:
        teams_list = [team.to_dict() for team in teams_db.values()]
        data = {
            'teams': teams_list,
            'total': len(teams_list)
        }
        return jsonify(create_api_response(message="Teams retrieved successfully", data=data))
    except Exception as e:
        return jsonify(create_api_response(result=False, error_code="GET_TEAMS_ERROR", message=str(e))), 500

@app.route('/api/teams/<team_id>', methods=['GET'])
def get_team(team_id):
    """
    取得特定團隊詳細資訊
    ---
    tags:
      - Teams
    summary: 根據 ID 取得團隊
    description: 使用團隊 ID 獲取特定團隊的詳細資訊
    parameters:
      - name: team_id
        in: path
        type: string
        required: true
        description: 團隊的唯一識別碼
        example: "550e8400-e29b-41d4-a716-446655440000"
    responses:
      200:
        description: 成功取得團隊資訊
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: true
            errorCode:
              type: string
              example: ""
            message:
              type: string
              example: "Team retrieved successfully"
            data:
              type: object
              properties:
                team:
                  type: object
                  properties:
                    id:
                      type: string
                      example: "550e8400-e29b-41d4-a716-446655440000"
                    name:
                      type: string
                      example: "前端開發團隊"
                    members:
                      type: array
                      items:
                        type: string
                      example: ["張三", "李四", "王五"]
                    createdAt:
                      type: string
                      format: date-time
                      example: "2023-12-01T10:30:00.000000"
                    updatedAt:
                      type: string
                      format: date-time
                      example: "2023-12-01T10:30:00.000000"
      404:
        description: 找不到指定的團隊
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: false
            errorCode:
              type: string
              example: "TEAM_NOT_FOUND"
            message:
              type: string
              example: "Team not found"
            data:
              type: "null"
              example: null
      500:
        description: 伺服器內部錯誤
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: false
            errorCode:
              type: string
              example: "GET_TEAM_ERROR"
            message:
              type: string
              example: "Internal server error"
            data:
              type: "null"
              example: null
    """
    try:
        if team_id not in teams_db:
            return jsonify(create_api_response(result=False, error_code="TEAM_NOT_FOUND", message="Team not found")), 404
        team = teams_db[team_id]
        return jsonify(create_api_response(message="Team retrieved successfully", data={'team': team.to_dict()}))
    except Exception as e:
        return jsonify(create_api_response(result=False, error_code="GET_TEAM_ERROR", message=str(e))), 500

@app.route('/api/teams', methods=['POST'])
def create_team():
    """
    新增團隊
    ---
    tags:
      - Teams
    summary: 建立新團隊
    description: 建立一個新的團隊，需要提供團隊名稱和成員列表
    parameters:
      - name: body
        in: body
        required: true
        description: 團隊資料
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              description: 團隊名稱
              example: "新產品開發團隊"
              minLength: 1
            members:
              type: array
              description: 團隊成員列表
              items:
                type: string
              example: ["小明", "小華", "小美", "小強"]
          example:
            name: "新產品開發團隊"
            members: ["小明", "小華", "小美", "小強"]
    responses:
      201:
        description: 團隊建立成功
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: true
            errorCode:
              type: string
              example: ""
            message:
              type: string
              example: "Team created successfully"
            data:
              type: object
              properties:
                team:
                  type: object
                  properties:
                    id:
                      type: string
                      example: "550e8400-e29b-41d4-a716-446655440001"
                    name:
                      type: string
                      example: "新產品開發團隊"
                    members:
                      type: array
                      items:
                        type: string
                      example: ["小明", "小華", "小美", "小強"]
                    createdAt:
                      type: string
                      format: date-time
                      example: "2023-12-01T15:30:00.000000"
                    updatedAt:
                      type: string
                      format: date-time
                      example: "2023-12-01T15:30:00.000000"
      400:
        description: 請求格式錯誤或必要欄位缺失
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: false
            errorCode:
              type: string
              enum: ["INVALID_REQUEST_FORMAT", "INVALID_TEAM_NAME", "INVALID_MEMBERS_FORMAT"]
              example: "INVALID_TEAM_NAME"
            message:
              type: string
              example: "Team name cannot be empty"
            data:
              type: "null"
              example: null
      500:
        description: 伺服器內部錯誤
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: false
            errorCode:
              type: string
              example: "CREATE_TEAM_ERROR"
            message:
              type: string
              example: "Internal server error"
            data:
              type: "null"
              example: null
    """
    try:
        if not request.is_json:
            return jsonify(create_api_response(result=False, error_code="INVALID_REQUEST_FORMAT", message="Request must be JSON")), 400

        data = request.get_json()
        name = data.get("name", "").strip()
        members = data.get("members", [])

        if not name:
            return jsonify(create_api_response(result=False, error_code="INVALID_TEAM_NAME", message="Team name cannot be empty")), 400

        if not isinstance(members, list):
            return jsonify(create_api_response(result=False, error_code="INVALID_MEMBERS_FORMAT", message="Members must be a list")), 400

        new_team = Team(name, members)
        teams_db[new_team.id] = new_team

        return jsonify(create_api_response(message="Team created successfully", data={'team': new_team.to_dict()})), 201
    except Exception as e:
        return jsonify(create_api_response(result=False, error_code="CREATE_TEAM_ERROR", message=str(e))), 500

@app.route('/api/teams/<team_id>', methods=['PUT'])
def update_team(team_id):
    """
    更新團隊資訊
    ---
    tags:
      - Teams
    summary: 更新現有團隊
    description: 更新指定團隊的名稱和成員列表，可以只更新部分欄位
    parameters:
      - name: team_id
        in: path
        type: string
        required: true
        description: 要更新的團隊 ID
        example: "550e8400-e29b-41d4-a716-446655440000"
      - name: body
        in: body
        required: true
        description: 要更新的團隊資料
        schema:
          type: object
          properties:
            name:
              type: string
              description: 新的團隊名稱（選填）
              example: "更新後的團隊名稱"
            members:
              type: array
              description: 新的團隊成員列表（選填）
              items:
                type: string
              example: ["新成員A", "新成員B", "新成員C"]
          example:
            name: "更新後的前端開發團隊"
            members: ["張三", "李四", "王五", "新成員趙六"]
    responses:
      200:
        description: 團隊更新成功
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: true
            errorCode:
              type: string
              example: ""
            message:
              type: string
              example: "Team updated successfully"
            data:
              type: object
              properties:
                team:
                  type: object
                  properties:
                    id:
                      type: string
                      example: "550e8400-e29b-41d4-a716-446655440000"
                    name:
                      type: string
                      example: "更新後的前端開發團隊"
                    members:
                      type: array
                      items:
                        type: string
                      example: ["張三", "李四", "王五", "新成員趙六"]
                    createdAt:
                      type: string
                      format: date-time
                      example: "2023-12-01T10:30:00.000000"
                    updatedAt:
                      type: string
                      format: date-time
                      example: "2023-12-01T16:45:00.000000"
      400:
        description: 請求格式錯誤
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: false
            errorCode:
              type: string
              example: "INVALID_REQUEST_FORMAT"
            message:
              type: string
              example: "Request must be JSON"
            data:
              type: "null"
              example: null
      404:
        description: 找不到指定的團隊
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: false
            errorCode:
              type: string
              example: "TEAM_NOT_FOUND"
            message:
              type: string
              example: "Team not found"
            data:
              type: "null"
              example: null
      500:
        description: 伺服器內部錯誤
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: false
            errorCode:
              type: string
              example: "UPDATE_TEAM_ERROR"
            message:
              type: string
              example: "Internal server error"
            data:
              type: "null"
              example: null
    """
    try:
        if team_id not in teams_db:
            return jsonify(create_api_response(result=False, error_code="TEAM_NOT_FOUND", message="Team not found")), 404

        if not request.is_json:
            return jsonify(create_api_response(result=False, error_code="INVALID_REQUEST_FORMAT", message="Request must be JSON")), 400

        data = request.get_json()
        team = teams_db[team_id]

        name = data.get("name", "").strip()
        if name:
            team.name = name

        members = data.get("members")
        if isinstance(members, list):
            team.members = members

        team.updatedAt = datetime.utcnow().isoformat()

        return jsonify(create_api_response(message="Team updated successfully", data={'team': team.to_dict()}))
    except Exception as e:
        return jsonify(create_api_response(result=False, error_code="UPDATE_TEAM_ERROR", message=str(e))), 500

@app.route('/api/teams/<team_id>', methods=['DELETE'])
def delete_team(team_id):
    """
    刪除團隊
    ---
    tags:
      - Teams
    summary: 刪除指定團隊
    description: 永久刪除指定的團隊，此操作無法復原
    parameters:
      - name: team_id
        in: path
        type: string
        required: true
        description: 要刪除的團隊 ID
        example: "550e8400-e29b-41d4-a716-446655440000"
    responses:
      200:
        description: 團隊刪除成功
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: true
            errorCode:
              type: string
              example: ""
            message:
              type: string
              example: "Team deleted successfully"
            data:
              type: object
              properties:
                deletedTeamId:
                  type: string
                  example: "550e8400-e29b-41d4-a716-446655440000"
      404:
        description: 找不到指定的團隊
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: false
            errorCode:
              type: string
              example: "TEAM_NOT_FOUND"
            message:
              type: string
              example: "Team not found"
            data:
              type: "null"
              example: null
      500:
        description: 伺服器內部錯誤
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: false
            errorCode:
              type: string
              example: "DELETE_TEAM_ERROR"
            message:
              type: string
              example: "Internal server error"
            data:
              type: "null"
              example: null
    """
    try:
        if team_id not in teams_db:
            return jsonify(create_api_response(result=False, error_code="TEAM_NOT_FOUND", message="Team not found")), 404

        del teams_db[team_id]
        return jsonify(create_api_response(message="Team deleted successfully", data={'deletedTeamId': team_id}))
    except Exception as e:
        return jsonify(create_api_response(result=False, error_code="DELETE_TEAM_ERROR", message=str(e))), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify(create_api_response(result=False, error_code="ENDPOINT_NOT_FOUND", message="API endpoint not found")), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify(create_api_response(result=False, error_code="INTERNAL_SERVER_ERROR", message="Internal server error")), 500

if __name__ == '__main__':
    auto_seed_data()
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
