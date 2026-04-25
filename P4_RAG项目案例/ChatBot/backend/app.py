"""FastAPI应用接口"""
#异步处理库，能够进行时间循环管理，协程管理(对可暂停函数进行调度)，并发执行，创建任务与超时控制
import asyncio
#修饰器 异步上下文管理器
from contextlib import asynccontextmanager
#面向对象处理文件系统
from pathlib import Path
#fastapi:前端库
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
#日志记录库
from loguru import logger

#导入后端功能
from backend.utils.logger import setup_logger
from backend.utils.runtime_env import resolve_bind_host
from backend.database import get_db_session_factory
from backend.version import APP_VERSION

setup_logger()

def _create_shared_components(config,config_loader=None):
    from loguru import logger
    from backend.modules.prividers import create_provider
    from backend.modules.prividers.runtime import (
        find_first_selectable_provider,
        get_provider_runtime_state,
    )
    from backend.modules.agent.context import ContextBuilder
    from backend.modules.tools.setup import register_all_tools
    from backend.modules.workspace import (
        seed_bundled_workspace_resources,
        workspace_manager
    )

    logger.info("Getting provider metadata...")
    provider_id = config.model.privider
    runtime_state = get_provider_runtime_state(config,provider_id)
    if not runtime_state.selectable:
        fallback_state = find_first_selectable_provider(config)
        if fallback_state and fallback_state.provider_id!=provider_id:
            logger.warning(
                f"共享组件默认 provider '{provider_id} 不可用({runtime_state.reason}),"
                f"已回退到'{fallback_state.provider_id}'"
            )
