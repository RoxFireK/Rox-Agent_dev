"""数据库"""
from dataclasses import dataclass
#装饰器，方便进行数据库对齐
from pathlib import Path
#面向对象处理文件系统路径
from typing import Tuple
#提供带有类型注释的元组

from loguru import logger
#一个很好用的日志记录器
from sqlalchemy import create_engine,inspect
#创建数据库连接引擎 inspect内省工具
from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker,create_async_engine
#sessionmaker创建会话工厂，生成会话对象
#AsyncSession异步对话
# 同步:队列，干完一件再干下一件
# 异步:不等待事件结束，继续派发新任务，适用于多项任务交替运行
from sqlalchemy.orm import DeclarativeBase,sessionmaker
from sqlalchemy.testing import future

#DeclarativeBase:所有模型的基础类

from backend.utils.paths import DATA_DIR

#数据库文件路径
DATABASE_PATH = DATA_DIR / "chatbot.db"
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"
SYNC_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

class Base(DeclarativeBase):
    #数据库模型基类
    pass

@dataclass(frozen=True)
class CompatibilityColumnMigration:
    #单列兼容迁移：对数据库的一个列进行修改且不中断服务
    #ddl：创建该列时完整的sql ddl语句片段 使用时直接拼接到增删减改语句中
    name:str
    ddl:str

@dataclass(frozen=True)
class CompatibilityTableMigration:
    #单表兼容迁移:修改表且不中断服务
    table_name:str
    columns:Tuple[CompatibilityColumnMigration,...]



_SCHEMA_COMPATIBILITY_MIGRATION = (
    #会话管理系统
    CompatibilityTableMigration(
        table_name="sessions",
        columns = (
            #模型配置
            CompatibilityColumnMigration(
                name = "session_model_config",
                ddl = "session_model_config TEXT",
            ),
            #人格配置
            CompatibilityColumnMigration(
                name = "session_persona_config",
                ddl = "session_persona_config TEXT",
            ),
            #是否使用自定义
            CompatibilityColumnMigration(
                name = "use_custom_config",
                ddl = "use_custum_config BOOLEAN DEFAULT 0",
            ),
            #多渠道上下文管理，支持跨渠道的对话连续性
            CompatibilityColumnMigration(
                name="channel_context",
                ddl="channel_context TEXT",
            ),
            #===========短上下文摘要=============
            #实现对话摘要压缩机制，解决长对话的token问题
            #短上下文摘要内容
            CompatibilityColumnMigration(
                name="short_context_summary",
                ddl="short_context_summary TEXT",
            ),
            #摘要信息对应id
            CompatibilityColumnMigration(
                name="short_context_summary_msg_id",
                ddl="short_context_summary_msg_id INTEGER ",
            ),
            #摘要更新时间
            CompatibilityColumnMigration(
                name="short_context_summary_updated_at",
                ddl="hort_context_summary_updated_at DATETIME",
            ),
            #摘要窗口大小
            CompatibilityColumnMigration(
                name="short_context_summary_window_size",
                ddl="short_context_summary_window_size INTEGER",
            ),
            #自动记忆机制，实现长期记忆，自动提取和保存重要信息
            CompatibilityColumnMigration(
                name="auto_memory_summary_msg_id",
                ddl="auto_memory_summary_msg_id INTEGER",
            ),
        ),
    ),
    #agent团队管理系统
    CompatibilityTableMigration(
        table_name = "agent_teams",
        columns = (
            #团队模型配置
            CompatibilityColumnMigration(
                name = "team_model_config",
                ddl = "team_model_config TEXT",
            ),
            #是否使用自定义模型
            CompatibilityColumnMigration(
            name = "use_custom_model",
            ddl = "use_custom_model BOOLEAN DEFAULT 0",
            ),
        ),
    ),
    #消息存储(用户发送的消息)
    CompatibilityTableMigration(
        table_name="messages",
        columns=(
            CompatibilityColumnMigration(
                name="message_context",
                ddl="message_context TEXT",
            ),
        ),
    ),
    #存储某个账号的定时任务配置
    CompatibilityTableMigration(
        table_name="cron_jobs",
        columns=(
            CompatibilityColumnMigration(
                name="account_id",
                ddl="account_id VARCHAR",
            ),
        ),
    ),
)


#异步引擎 从引擎获取数据库链接
engine = create_async_engine(
    #数据库链接地址
    DATABASE_URL,
    #SQL日志输出控制，是否在控制台打印所有执行的SQL语句
    echo = False,
    #使用SQL新特性api
    future = True,
)

#同步引擎，用于非异步上下文
sync_engine = create_engine(
    SYNC_DATABASE_URL,
    echo = False,
    future = True,
)

#会话工厂 async异步
AsyncSessionLocal = async_sessionmaker(
    #获取数据库引擎
    engine,
    #会话类类型，async_sessionmaker默认就是AsyncSession
    class_ = AsyncSession,
    #提交后是否过期对象，避免额外查询
    expire_on_commit = False,
)

#同步会话工厂
SessionLocal = sessionmaker(
    sync_engine,
    expire_on_commit = False,
)

async def get_db() -> AsyncSession:
    #获取数据库会话
    async with AsyncSessionLocal() as session:
        #yield:每个请求获得独立的数据库会话，使用完自动关闭
        yield session

def get_db_session_factory():
    #获取数据库会话工厂
    #用于需要创建多个独立会话的场景
    return AsyncSessionLocal

#数据库兼容性迁移函数,用于为旧版本表添加缺失列
def _apply_schema_compatibility_migrations(
        #同步数据库连接对象
        sync_conn,
        #迁移配置元组
        migrations: Tuple[CompatibilityTableMigration,...] = _SCHEMA_COMPATIBILITY_MIGRATION,
        #->None函数没有返回值
) -> None:
    #对旧版本数据库执行最小 schema 兼容迁移
    #创建一个检查器对象，用于获取数据库的元数据信息(有哪些表和列)
    inspector = inspect(sync_conn)
    #获取现有表名
    table_names = set(inspector.get_table_names())
    #循环处理每个需要迁移的表
    for table_migration in migrations:
        #如果要迁移的表在数据库中不存在，就跳过
        if table_migration.table_name not in table_names:
            continue
        #获取当前表已经存在的所有列名，存入集合
        existing_columns = {
            column["name"]
            for column in inspector.get_columns(table_migration.table_name)
        }
        #遍历需要添加的列
        for column_migration in table_migration.columns:
            #检查点
            if column_migration.name in existing_columns:
                continue
            #执行sql添加列
            sync_conn.exec_driver_sql(
                f"ALTER TABLE {table_migration.table_name} ADD COLUMN {column_migration.ddl}"
            )
            #记录日志,添加了某个列 warning级别引起注意
            logger.warning(
                "Applied compatibility migration for"
                f"{table_migration.table_name}.{column_migration.name} "
            )
            #更新已存在列集合
            existing_columns.add(column_migration.name)

async def init_db() -> None:
    #初始化数据库
    #导入所有模型以确保表被创建
    from backend.models import agentTeam,cronJob,message,personality,session,setting,task,toolConversation
    #创建异步数据库事务上下文，自动管理事务提交和回滚
    async with engine.begin() as conn:
        #创建所有数据库表
        await conn.run_sync(Base.metadata.create_all)
        #调用迁移函数
        await conn.run_sync(_apply_schema_compatibility_migrations)
    #初始化人格配置
    await init_personalities()

async def init_personalities() -> None:
    #初始化内置性格数据
    from backend.models.personality import Personality
    from sqlalchemy import select

    #创建异步对话上下文，自动管理会话的生命周期
    async with AsyncSessionLocal() as session:
        #进行异常处理
        try:
            #执行查询，获取personality表中的记录
            result = await session.execute(select(Personality))
            #从查询中获取第一条记录
            existing = result.scalars().first()
            if existing:
                #已有数据则跳过初始化
                return

            #从personalities.py导入内置数据
            from backend.modules.agent.personalities import PERSONALITY_PRESETS
            # 为不同人格设置对应图标,以字典格式
            icon_map = {
                "grumpy": "CloudLightning",
                "roast": "Frown",
                "gentle": "Heart",
                "blunt": "Target",
                "toxic": "Snowflake",
                "chatty": "MessageSquare",
                "philosopher": "BookOpen",
                "cute": "Smile",
                "humorous": "Laugh",
                "hyper": "TrendingUp",
                "chuuni": "Gamepad2",
                "zen": "Clock",
            }

            #插入内置性格
            for pid,data in PERSONALITY_PRESETS.items():
                #参数来源于models.personality的personality类
                personality = Personality(
                    id = pid,
                    name = data["name"],
                    description = data["description"],
                    traits = data["traits"],
                    speaking_style = data["speaking_style"],
                    icon = icon_map.get(pid,"Smile"),
                    is_builtin = True,
                    is_active = True,
                )
                session.add(personality)

            #将当前事务中的所有更改永远保存到数据库中
            await session.commit()

        #捕获任何类型的异常
        except Exception:
            #发现异常时回滚
            await session.rollback()
            #发现错误静默处理
            pass
