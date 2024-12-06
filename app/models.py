from . import db

# 用户表
class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    registerID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    membership_duration = db.Column(db.Integer, nullable=False)
    nickname = db.Column(db.String(100), db.ForeignKey('players.Nickname'), nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'

# 工会表
class Guild(db.Model):
    __tablename__ = 'guilds'
    GuildID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    GuildName = db.Column(db.String(100), nullable=False)
    Power = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Guild {self.GuildName}>'

# 团队表
class Team(db.Model):
    __tablename__ = 'teams'
    TeamID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TeamName = db.Column(db.String(100), nullable=False)
    GuildID = db.Column(db.Integer, db.ForeignKey('guilds.GuildID'), nullable=False)

    def __repr__(self):
        return f'<Team {self.TeamName}>'

# 玩家表
class Player(db.Model):
    __tablename__ = 'players'
    PlayerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nickname = db.Column(db.String(100), unique=True, nullable=False)
    GuildID = db.Column(db.Integer, db.ForeignKey('guilds.GuildID'), nullable=True)
    TeamID = db.Column(db.Integer, db.ForeignKey('teams.TeamID'), nullable=True)
    Power = db.Column(db.Integer, default=0)
    Merit = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Player {self.Nickname}>'

# 部队配置表
class TroopConfiguration(db.Model):
    __tablename__ = 'troop_configurations'
    ConfigurationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    General1 = db.Column(db.String(100), nullable=False)
    General2 = db.Column(db.String(100), nullable=False)
    General3 = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<TroopConfiguration {self.ConfigurationID}>'

# 玩家与部队关联表
class PlayerTroop(db.Model):
    __tablename__ = 'player_troops'
    PlayerID = db.Column(db.Integer, db.ForeignKey('players.PlayerID'), primary_key=True)
    ConfigurationID = db.Column(db.Integer, db.ForeignKey('troop_configurations.ConfigurationID'), primary_key=True)
    Power = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<PlayerTroop PlayerID={self.PlayerID} ConfigurationID={self.ConfigurationID}>'

# 战斗记录表
class Battle(db.Model):
    __tablename__ = 'battles'
    BattleID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DateTime = db.Column(db.DateTime, nullable=False)
    AttackerPlayerID = db.Column(db.Integer, db.ForeignKey('players.PlayerID'), nullable=False)
    DefenderPlayerID = db.Column(db.Integer, db.ForeignKey('players.PlayerID'), nullable=False)
    AttackerConfigurationID = db.Column(db.Integer, db.ForeignKey('troop_configurations.ConfigurationID'), nullable=False)
    DefenderConfigurationID = db.Column(db.Integer, db.ForeignKey('troop_configurations.ConfigurationID'), nullable=False)
    Result = db.Column(db.String(100), nullable=False)
    BattleLocation = db.Column(db.String(100), nullable=False)
    CasualtyRatio = db.Column(db.Float, nullable=False)
    BuildingsDestroyed = db.Column(db.Boolean, default=False)
    LandOcc = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Battle {self.BattleID}>'

# 部队使用记录表
class TroopUsage(db.Model):
    __tablename__ = 'troop_usage'
    UsageID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    BattleID = db.Column(db.Integer, db.ForeignKey('battles.BattleID'))  # 新增字段
    ConfigurationID = db.Column(db.Integer, db.ForeignKey('troop_configurations.ConfigurationID'), nullable=False)
    DateTime = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<TroopUsage {self.UsageID}>'

# 部队战绩表
class TroopRecord(db.Model):
    __tablename__ = 'troop_records'
    RecordID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ConfigurationID = db.Column(db.Integer, db.ForeignKey('troop_configurations.ConfigurationID'), nullable=False)
    BattleID = db.Column(db.Integer, db.ForeignKey('battles.BattleID'), nullable=False)
    Result = db.Column(db.String(100), nullable=False)
    CasualtyRatio = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<TroopRecord {self.RecordID}>'
