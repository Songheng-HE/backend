from flask import Blueprint, jsonify
from sqlalchemy import func, case
from app.models import db, TroopRecord, TroopConfiguration

# 创建蓝图
troop_usage_routes = Blueprint('troop_usage', __name__)

# 胜率排行榜
@troop_usage_routes.route('/api/troop-win-rate-rankings', methods=['GET'])
def get_troop_win_rate():
    query = (
        db.session.query(
            TroopConfiguration.General1,
            TroopConfiguration.General2,
            TroopConfiguration.General3,
            func.count(TroopRecord.RecordID).label('TotalBattles'),
            func.sum(case((TroopRecord.Result == 'Win', 1), else_=0)).label('Wins'),
            (func.sum(case((TroopRecord.Result == 'Win', 1), else_=0)) / func.count(TroopRecord.RecordID)).label('WinRate')
        )
        .join(TroopRecord, TroopConfiguration.ConfigurationID == TroopRecord.ConfigurationID)
        .group_by(TroopConfiguration.ConfigurationID)
        .order_by((func.sum(case((TroopRecord.Result == 'Win', 1), else_=0)) / func.count(TroopRecord.RecordID)).desc())
        .limit(10)
    )

    results = query.all()
    response_data = [
        {
            "general1": result.General1,
            "general2": result.General2,
            "general3": result.General3,
            "winRate": round(result.WinRate * 100, 2) if result.WinRate else 0  # 胜率转化为百分比
        }
        for result in results
    ]

    # 打印结果到后端控制台
#    print("Troop Win Rate Rankings Query Results:")
#    for result in response_data:
#        print(result)

    return jsonify({"rankings": response_data}), 200


# 战损比排行榜
@troop_usage_routes.route('/api/troop-casualty-rankings', methods=['GET'])
def get_troop_casualty_ratio():
    query = (
        db.session.query(
            TroopConfiguration.General1,
            TroopConfiguration.General2,
            TroopConfiguration.General3,
            func.avg(TroopRecord.CasualtyRatio).label('AverageCasualtyRatio')
        )
        .join(TroopRecord, TroopConfiguration.ConfigurationID == TroopRecord.ConfigurationID)
        .group_by(TroopConfiguration.ConfigurationID)
        .order_by(func.avg(TroopRecord.CasualtyRatio).desc())
        .limit(10)
    )

    results = query.all()
    response_data = [
        {
            "general1": result.General1,
            "general2": result.General2,
            "general3": result.General3,
            "casualtyRatio": round(result.AverageCasualtyRatio, 2) if result.AverageCasualtyRatio else 0
        }
        for result in results
    ]

    print("Troop Win Rate Rankings Query Results:")
    for result in response_data:
        print(result)

    return jsonify({'rankings': response_data}), 200

# 出战次数排行榜
@troop_usage_routes.route('/api/troop-usage-rankings', methods=['GET'])
def get_troop_usage_count():
    query = (
        db.session.query(
            TroopConfiguration.General1,
            TroopConfiguration.General2,
            TroopConfiguration.General3,
            func.count(TroopRecord.RecordID).label('TotalBattles')
        )
        .join(TroopRecord, TroopConfiguration.ConfigurationID == TroopRecord.ConfigurationID)
        .group_by(TroopConfiguration.ConfigurationID)
        .order_by(func.count(TroopRecord.RecordID).desc())
        .limit(10)
    )

    results = query.all()
    response_data = [
        {
            "general1": result.General1,
            "general2": result.General2,
            "general3": result.General3,
            "usageCount": result.TotalBattles
        }
        for result in results
    ]

    return jsonify({'rankings': response_data}), 200
