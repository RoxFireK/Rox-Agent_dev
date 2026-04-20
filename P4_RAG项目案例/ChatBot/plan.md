学习流程
# 步骤1：快速浏览（5分钟）
# - 看类名、方法名
# - 看import依赖
# - 大概知道有run方法

# 步骤2：仔细阅读原文（20分钟）
# - 理解每一步在做什么
# - 记录关键逻辑（如max_steps检查、工具调用判断）
# - 看不懂的暂时标记

# 步骤3：关掉原文自己写（30分钟）
# - 根据理解重写核心逻辑
# - 不追求完全相同，追求逻辑一致

# 步骤4：对比优化（10分钟）
# - 打开原文对比
# - 发现自己遗漏了什么
# - 理解为什么原文那么写

# 步骤5：跑通测试（15分钟）
# - 写简单测试
# - 确保能运行

DAY1-2
第1个文件：config/schema.py
├── 重要程度：P0
├── 为什么最先：所有模块依赖配置
├── 最小实现：只需要 OPENAI_API_KEY, DATABASE_URL
└── 代码量：~30行

第2个文件：backend/database.py  
├── 重要程度：P0
├── 为什么第二：其他模型依赖数据库连接
├── 最小实现：create_engine, SessionLocal
└── 代码量：~20行

第3个文件：backend/models/__init__.py + session.py
├── 重要程度：P0
├── 最小实现：Session表（id, created_at）
└── 代码量：~40行

第4个文件：app.py
├── 重要程度：P0 ⭐⭐⭐⭐⭐（最核心入口）
├── 最小实现：
│   ├── FastAPI初始化
│   ├── 数据库初始化
│   ├── 挂载路由占位符
│   └── 启动uvicorn
└── 代码量：~50行

第5个文件：backend/api/__init__.py + chat.py
├── 重要程度：P0 ⭐⭐⭐⭐⭐
├── 最小实现：
│   ├── POST /chat 接收消息
│   ├── 直接调用OpenAI（不用Agent Loop）
│   ├── 保存到数据库
│   └── 返回回复
└── 代码量：~60行

【里程碑】此时你有一个能工作的聊天API：curl发消息 → LLM回复

DAY3-4
第6个文件：providers/base.py
├── 重要程度：P1
├── 为什么现在做：隔离LLM实现
├── 最小实现：BaseLLM抽象类，chat方法
└── 代码量：~30行

第7个文件：providers/openai_provider.py  
├── 重要程度：P1 ⭐⭐⭐⭐
├── 依赖：base.py
├── 最小实现：继承BaseLLM，封装OpenAI调用
└── 代码量：~50行

第8个文件：tools/base.py
├── 重要程度：P1
├── 最小实现：BaseTool抽象类，name, description, execute
└── 代码量：~25行

第9个文件：tools/echo_tool.py（先不写registry）
├── 重要程度：P1
├── 目的：测试用工具
├── 实现：接收text返回text
└── 代码量：~15行

第10个文件：modules/agent/loop.py ⭐⭐⭐⭐⭐（最重要）
├── 重要程度：P1
├── 依赖：providers, tools
├── 最小实现：
│   ├── 接收messages和tools
│   ├── 调用LLM判断是否需要工具
│   ├── 执行工具
│   └── 返回最终回复
└── 代码量：~80行

第11个文件：modules/agent/context.py
├── 重要程度：P1
├── 作用：管理消息历史，计算token
├── 最小实现：messages数组 + 简单token估算
└── 代码量：~40行

【里程碑】此时Agent能调用工具：问"1+1等于几" → 调用计算器工具

DAY5-7
第12个文件：backend/models/message.py
├── 重要程度：P2
├── 依赖：session.py
├── 字段：id, session_id, role, content, created_at
└── 代码量：~35行

第13个文件：tools/registry.py
├── 重要程度：P2
├── 作用：集中管理所有工具
├── 实现：字典存储，register和get方法
└── 代码量：~30行

第14个文件：modules/agent/prompts.py
├── 重要程度：P2
├── 作用：系统提示词模板
├── 最小实现：SYSTEM_PROMPT常量 + 变量替换
└── 代码量：~20行

第15个文件：backend/api/chat.py（重构）
├── 重要程度：P2
├── 改动：从直接调LLM → 调Agent Loop
├── 新增：加载tools，创建session
└── 代码量：+30行

第16个文件：config/loader.py
├── 重要程度：P2
├── 作用：加载yaml/env配置
├── 最小实现：读取.env文件
└── 代码量：~20行

第17个文件：backend/models/personality.py
├── 重要程度：P2
├── 作用：人格/系统提示词管理
├── 字段：name, system_prompt
└── 代码量：~30行

第18个文件：modules/agent/memory.py
├── 重要程度：P2
├── 作用：长期记忆（简单版用文件存储）
├── 最小实现：基于文件的key-value存储
└── 代码量：~40行

DAY8-10
第19个文件：modules/channels/base.py
第20个文件：modules/channels/console_channel.py（测试用）
第21个文件：modules/channels/manager.py
第22个文件：cron/scheduler.py
第23个文件：external_agents/adapters/base.py
第24个文件：backend/api/agent_teams.py
