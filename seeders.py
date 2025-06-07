"""
資料填充器 (Seeders) - 用於產生測試資料
"""

import requests
import json
import random
import time
from datetime import datetime

# API 基礎 URL
BASE_URL = "http://localhost:8080"

# 假資料池
TEAM_NAMES = [
    "前端開發團隊",
    "後端開發團隊", 
    "移動應用開發團隊",
    "DevOps 團隊",
    "資料科學團隊",
    "UI/UX 設計團隊",
    "產品管理團隊",
    "品質保證團隊",
    "基礎架構團隊",
    "機器學習團隊",
    "安全團隊",
    "雲端架構團隊",
    "全端開發團隊",
    "商業智能團隊",
    "客戶支援團隊"
]

MEMBER_NAMES = [
    "張三", "李四", "王五", "趙六", "錢七", "孫八", "周九", "吳十",
    "鄭十一", "王十二", "馮十三", "陳十四", "褚十五", "衛十六", "蔣十七",
    "沈十八", "韓十九", "楊二十", "朱二十一", "秦二十二", "尤二十三", "許二十四",
    "何二十五", "呂二十六", "施二十七", "張二十八", "孔二十九", "曹三十",
    "嚴三十一", "華三十二", "金三十三", "魏三十四", "陶三十五", "姜三十六",
    "戚三十七", "謝三十八", "鄒三十九", "喻四十", "柏四十一", "水四十二",
    "竇四十三", "章四十四", "雲四十五", "蘇四十六", "潘四十七", "葛四十八",
    "奚四十九", "范五十", "彭五十一", "郎五十二", "魯五十三", "韋五十四",
    "昌五十五", "馬五十六", "苗五十七", "鳳五十八", "花五十九", "方六十"
]

def check_api_health():
    """檢查 API 服務是否可用"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API 服務正常運行")
            return True
        else:
            print(f"❌ API 服務回應異常: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 無法連接到 API 服務: {e}")
        print("請確保應用程式正在 http://localhost:8080 運行")
        return False

def generate_random_members():
    """產生隨機成員名單"""
    num_members = random.randint(2, 8)  # 每個團隊 2-8 個成員
    return random.sample(MEMBER_NAMES, num_members)

def create_team(name, members):
    """建立單一團隊"""
    try:
        payload = {
            "name": name,
            "members": members
        }
        
        response = requests.post(
            f"{BASE_URL}/api/teams",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            if data.get('result'):
                team_info = data['data']['team']
                print(f"✅ 建立團隊: {team_info['name']} (ID: {team_info['id'][:8]}...) - {len(members)} 名成員")
                return team_info
            else:
                print(f"❌ 建立團隊失敗: {data.get('message', '未知錯誤')}")
                return None
        else:
            print(f"❌ HTTP 錯誤 {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 網路錯誤: {e}")
        return None

def get_all_teams():
    """取得所有團隊"""
    try:
        response = requests.get(f"{BASE_URL}/api/teams", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('result'):
                return data['data']['teams']
        return []
    except requests.exceptions.RequestException:
        return []

def clear_existing_teams():
    """清除現有團隊（可選）"""
    teams = get_all_teams()
    if not teams:
        print("📝 沒有現有團隊需要清除")
        return
    
    print(f"🗑️  發現 {len(teams)} 個現有團隊")
    user_input = input("是否要清除所有現有團隊？ (y/N): ").strip().lower()
    
    if user_input == 'y':
        deleted_count = 0
        for team in teams:
            try:
                response = requests.delete(f"{BASE_URL}/api/teams/{team['id']}", timeout=10)
                if response.status_code == 200:
                    deleted_count += 1
                    print(f"🗑️  已刪除團隊: {team['name']}")
                else:
                    print(f"❌ 刪除團隊失敗: {team['name']}")
            except requests.exceptions.RequestException as e:
                print(f"❌ 刪除團隊時發生錯誤: {e}")
        
        print(f"✅ 成功刪除 {deleted_count} 個團隊")
    else:
        print("📝 保留現有團隊")

def seed_teams(num_teams=10):
    """填充團隊資料"""
    print(f"🌱 開始填充 {num_teams} 個團隊資料...")
    
    # 隨機選擇不重複的團隊名稱
    selected_names = random.sample(TEAM_NAMES, min(num_teams, len(TEAM_NAMES)))
    
    created_teams = []
    success_count = 0
    
    for i, team_name in enumerate(selected_names, 1):
        print(f"\n[{i}/{len(selected_names)}] 建立團隊: {team_name}")
        
        members = generate_random_members()
        team = create_team(team_name, members)
        
        if team:
            created_teams.append(team)
            success_count += 1
        
        # 避免請求過於頻繁
        if i < len(selected_names):
            time.sleep(0.5)
    
    return created_teams, success_count

def display_summary(created_teams):
    """顯示建立結果摘要"""
    print("\n" + "="*60)
    print("📊 資料填充完成摘要")
    print("="*60)
    
    if not created_teams:
        print("❌ 沒有成功建立任何團隊")
        return
    
    print(f"✅ 成功建立 {len(created_teams)} 個團隊:")
    print()
    
    for i, team in enumerate(created_teams, 1):
        print(f"{i:2d}. {team['name']}")
        print(f"    ID: {team['id']}")
        print(f"    成員數量: {len(team['members'])}")
        print(f"    成員: {', '.join(team['members'])}")
        print(f"    建立時間: {team['createdAt']}")
        print()
    
    print(f"📈 總計建立了 {len(created_teams)} 個團隊，共 {sum(len(team['members']) for team in created_teams)} 名成員")

def main():
    """主程式"""
    print("🚀 團隊資料填充器")
    print("="*40)
    
    # 檢查 API 服務
    if not check_api_health():
        print("\n請先啟動 Flask 應用程式:")
        print("docker-compose up --build")
        print("或")
        print("python app.py")
        return
    
    print()
    
    # 詢問是否清除現有資料
    clear_existing_teams()
    
    # 詢問要建立多少團隊
    while True:
        try:
            num_teams = input(f"\n請輸入要建立的團隊數量 (1-{len(TEAM_NAMES)}, 預設 10): ").strip()
            if not num_teams:
                num_teams = 10
            else:
                num_teams = int(num_teams)
            
            if 1 <= num_teams <= len(TEAM_NAMES):
                break
            else:
                print(f"❌ 請輸入 1 到 {len(TEAM_NAMES)} 之間的數字")
        except ValueError:
            print("❌ 請輸入有效的數字")
    
    # 執行資料填充
    created_teams, success_count = seed_teams(num_teams)
    
    # 顯示結果
    display_summary(created_teams)
    
    if success_count > 0:
        print(f"\n🎉 資料填充完成！您可以透過以下指令驗證結果:")
        print(f"curl -X GET http://localhost:8080/api/teams")
    else:
        print(f"\n😞 資料填充失敗，請檢查 API 服務狀態")

if __name__ == "__main__":
    main()