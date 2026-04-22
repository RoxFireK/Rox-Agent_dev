#启动延迟注解评估，可以引用尚未定义的类
from __future__ import annotations
#导入时间日期处理工具
from datetime import datetime, timezone
#导入类型注解相关工具 列表 可选类型 运行时检查标志 文本类型别名
from typing import List, Optional, TYPE_CHECKING, Text
#导入sql工具 布尔类型 日期时间类型 数据库索引 字符串类型 长文本类型
from sqlalchemy import Boolean,DateTime,Index,String,Text
#导入sql组件 类型注解容器 列定义 表关系
from sqlalchemy.orm import Mapped,mapped_column,relationship
#导入数据库基类
from backend.database import Base

def utc_now():
    #返回带时区的UTC时间
    return datetime.now(timezone.utc)

class Session(Base):
    #会话表，继承base
    #表名
    __tablename__ = "session"
    # 类型注解        列定义        数据类型  设为主键
    id:Mapped[str] = mapped_column(String,primary_key = True)
    # nullable 非空限制
    """
    创建表
    CREATE TABLE session (
        id VARCHAR NOT NULL,
        name VARCHAR NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (id)
    );
    """
    name:Mapped[str] = mapped_column(String,nullable=False)
    #传递参数，每次调用时获取当前时间
    # 创建时间
    created_at:Mapped[datetime] = mapped_column(DateTime,default=utc_now)
    # 更新时间
    updated_at:Mapped[datetime] = mapped_column(
        DateTime,
        #插入时的默认值
        default=utc_now,
        #更新时自动更新这个字段
        onupdate=utc_now
    )

    #会话总结
    summary:Mapped[Optional[str]] = mapped_column(String(200),nullable=True)
    summary_updated_at:Mapped[Optional[datetime]] = mapped_column(DateTime,nullable = True)

    #上下文滚动压缩，已总结到的消息ID
    last_summarized_msg_id:Mapped[Optional[int]] = mapped_column(nullable=True)

    #游标标记会话记忆，避免重启后重复总结整段对话
    auto_memory_summary_msg_id:Mapped[Optional[int]] = mapped_column(nullable=True)

    #会话级短期上下文总结缓存
    # 摘要字段
    short_context_summary:Mapped[Optional[str]] = mapped_column(Text,nullable=True)
    # 摘要对应的消息ID
    short_context_summary_msg_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    # 摘要更新时间
    short_context_summary_updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )
    # 摘要窗口大小
    short_context_summary_window_size:Mapped[Optional[int]] = mapped_column(
        nullable=True,
    )

    #会话级配置
    #模型配置
    session_model_config:Mapped[Optional[str]] = mapped_column(Text,nullable=True)
    #人格配置
    session_persona_config: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    #自定义配置开关 默认为false
    use_custom_config: Mapped[bool] = mapped_column(Boolean, default=False)
    #渠道上下文 存储来源渠道的上下文信息
    channel_context:Mapped[Optional[str]] = mapped_column(Text,nullable=True)

    #一对多关系，一个session对应多个message
    messages:Mapped[List["Message"]] = relationship(
        "Message",back_populates = "session",cascade="all, delete-orphan"
        #cascade="all, delete-orphan"：自动删除
    )

    #表级参数         创建索引      索引名称      索引列名 加速查询
    __table_args__ = (Index("idx_sessions_updated","updated_at"),)