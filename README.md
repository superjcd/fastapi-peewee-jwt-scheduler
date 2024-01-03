这是一个开箱即用的FastAPI脚手架，集成了ORM模型、JWT认证、日志系统、异常处理、路由注册、系统配置、调度任务等常用的模块。


## 项目结构
```

```

## 集成的模块

- 日志系统

集成 `loguru`，一个优雅、简洁的日志库

- 异常处理

定义认证异常类，注册 `Exception Handler`

- 路由注册

路由集中注册，按模块划分为不同的文件，代码层次结构清晰

- 系统配置

基于 `pydantic.BaseSettings`，使用 `.env` 文件设置环境变量。配置文件按功能模块划分，默认定义了app基础配置、数据库配置(mysql+redis)、日志配置、认证配置

- 数据库 ORM模型

基于 `peewee`，一个轻量级的Python ORM框架

- 中间件

默认注册了全局CORS中间件

- JWT认证

默认提供了账号密码和手机号验证码两种认证方式。框架易于扩展新的认证方式。

测试登录认证请先执行初始化的SQL：`fastapi-skeleton/database/migrations/*.sql`

注：验证码的存储依赖redis

- 调度任务

基于 `APScheduler` 调度任务框架

注：定时任务与api是分开启动的

## 运行

1. 执行初始化SQL：`/database/migrations/2022_09_07_create_users_table.sql`

2. API

```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

3. 调度器

```bash
python scheduler.py 
```

关于部署部分，参见我的另一篇文章 [fastapi部署](https://www.kxler.com/2022/10/21/fastapi-deployment-venv-gunicorn-service/)

## 参考

[FastAPI官方中文文档](https://fastapi.tiangolo.com/zh/)

FastAPI作者的全栈项目脚手架 [full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql)

代码结构组织风格参考 [Laravel框架](https://github.com/laravel/laravel)
