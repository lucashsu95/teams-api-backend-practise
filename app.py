from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid
import os

app = Flask(__name__)

# 配置 CORS - 允許來自前端的跨域請求
CORS(app, origins=['http://localhost:3000'], 
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'])

# 模擬資料庫 - 在實際應用中應該使用真實資料庫
teams_db = {}

class Team:
    def __init__(self, name, members):
        self.id = str(uuid.uuid4())
        self.name = name
        self.members = members
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'members': self.members,
            'createdAt': self.created_at,
            'updatedAt': self.updated_at
        }
def auto_seed_data():
    """啟動時自動填充初始資料"""
    if len(teams_db) == 0:
        print("🌱 檢測到空資料庫，自動填充初始測試資料...")
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
        
        print(f"✅ 已自動建立 {len(sample_teams)} 個初始團隊")

def create_api_response(result=True, error_code="", message="", data=None):
    """建立標準 API 回應格式"""
    return {
        'result': result,
        'errorCode': error_code,
        'message': message,
        'data': data
    }

@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    return create_api_response(message="Service is healthy")

@app.route('/api/teams', methods=['GET'])
def get_teams():
    """取得所有團隊列表"""
    try:
        teams_list = [team.to_dict() for team in teams_db.values()]
        data = {
            'teams': teams_list,
            'total': len(teams_list)
        }
        return jsonify(create_api_response(
            message="Teams retrieved successfully",
            data=data
        ))
    except Exception as e:
        return jsonify(create_api_response(
            result=False,
            error_code="GET_TEAMS_ERROR",
            message=str(e)
        )), 500

@app.route('/api/teams/<team_id>', methods=['GET'])
def get_team(team_id):
    """取得特定團隊詳細資訊"""
    try:
        if team_id not in teams_db:
            return jsonify(create_api_response(
                result=False,
                error_code="TEAM_NOT_FOUND",
                message="Team not found"
            )), 404
        
        team = teams_db[team_id]
        data = {'team': team.to_dict()}
        return jsonify(create_api_response(
            message="Team retrieved successfully",
            data=data
        ))
    except Exception as e:
        return jsonify(create_api_response(
            result=False,
            error_code="GET_TEAM_ERROR",
            message=str(e)
        )), 500

@app.route('/api/teams', methods=['POST'])
def create_team():
    """新增團隊"""
    try:
        # 檢查請求格式
        if not request.is_json:
            return jsonify(create_api_response(
                result=False,
                error_code="INVALID_REQUEST_FORMAT",
                message="Request must be JSON"
            )), 400
        
        data = request.get_json()
        
        # 驗證必要欄位
        if 'name' not in data:
            return jsonify(create_api_response(
                result=False,
                error_code="MISSING_REQUIRED_FIELD",
                message="Team name is required"
            )), 400
        
        if not data['name'].strip():
            return jsonify(create_api_response(
                result=False,
                error_code="INVALID_TEAM_NAME",
                message="Team name cannot be empty"
            )), 400
        
        # 建立新團隊
        team_name = data['name'].strip()
        members = data.get('members', [])
        
        # 驗證 members 是列表
        if not isinstance(members, list):
            return jsonify(create_api_response(
                result=False,
                error_code="INVALID_MEMBERS_FORMAT",
                message="Members must be a list"
            )), 400
        
        new_team = Team(team_name, members)
        teams_db[new_team.id] = new_team
        
        response_data = {'team': new_team.to_dict()}
        return jsonify(create_api_response(
            message="Team created successfully",
            data=response_data
        )), 201
        
    except Exception as e:
        return jsonify(create_api_response(
            result=False,
            error_code="CREATE_TEAM_ERROR",
            message=str(e)
        )), 500

@app.route('/api/teams/<team_id>', methods=['PUT'])
def update_team(team_id):
    """更新團隊資訊"""
    try:
        if team_id not in teams_db:
            return jsonify(create_api_response(
                result=False,
                error_code="TEAM_NOT_FOUND",
                message="Team not found"
            )), 404
        
        if not request.is_json:
            return jsonify(create_api_response(
                result=False,
                error_code="INVALID_REQUEST_FORMAT",
                message="Request must be JSON"
            )), 400
        
        data = request.get_json()
        team = teams_db[team_id]
        
        # 更新團隊資訊
        if 'name' in data and data['name'].strip():
            team.name = data['name'].strip()
        
        if 'members' in data and isinstance(data['members'], list):
            team.members = data['members']
        
        team.updated_at = datetime.utcnow().isoformat()
        
        response_data = {'team': team.to_dict()}
        return jsonify(create_api_response(
            message="Team updated successfully",
            data=response_data
        ))
        
    except Exception as e:
        return jsonify(create_api_response(
            result=False,
            error_code="UPDATE_TEAM_ERROR",
            message=str(e)
        )), 500

@app.route('/api/teams/<team_id>', methods=['DELETE'])
def delete_team(team_id):
    """刪除團隊"""
    try:
        if team_id not in teams_db:
            return jsonify(create_api_response(
                result=False,
                error_code="TEAM_NOT_FOUND",
                message="Team not found"
            )), 404
        
        del teams_db[team_id]
        
        response_data = {'deletedTeamId': team_id}
        return jsonify(create_api_response(
            message="Team deleted successfully",
            data=response_data
        ))
        
    except Exception as e:
        return jsonify(create_api_response(
            result=False,
            error_code="DELETE_TEAM_ERROR",
            message=str(e)
        )), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify(create_api_response(
        result=False,
        error_code="ENDPOINT_NOT_FOUND", 
        message="API endpoint not found"
    )), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify(create_api_response(
        result=False,
        error_code="INTERNAL_SERVER_ERROR",
        message="Internal server error"
    )), 500

if __name__ == '__main__':
    auto_seed_data()
    
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)