# 构建阶段：使用 uv 安装依赖
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

# 安装依赖
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# 安装应用代码和最终依赖
COPY app ./app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


# 运行阶段：生产镜像
FROM python:3.12-slim-bookworm
ENV PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    FLASK_APP=app

# 复制虚拟环境和应用代码
COPY --from=builder --chown=app:app /app /app

# 创建非 root 用户
RUN addgroup --system app && adduser --system --no-create-home --ingroup app app
USER app

# 配置路径和环境
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"

# 使用 Gunicorn 作为 WSGI 服务器
CMD ["gunicorn", \
    "--bind", "0.0.0.0:8000", \
    "--workers", "4", \
    "--timeout", "30", \
    "app:create_app()"]