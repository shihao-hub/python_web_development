from nicegui import ui
from datetime import datetime, timedelta
import random
import time

# 维护信息配置
MAINTENANCE_INFO = {
    "title": "系统维护中",
    "subtitle": "我们正在进行系统升级，以提供更好的服务体验",
    "expected_duration": "预计维护时间: 2小时",
    "start_time": datetime.now(),
    "end_time": datetime.now() + timedelta(hours=2),
    "contact": "如有紧急问题，请联系: support@example.com"
}


# 创建维护中页面
def create_maintenance_page():
    # 页面样式
    ui.add_head_html('''
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
                background-size: 400% 400%;
                animation: gradientBG 15s ease infinite;
                height: 100vh;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                overflow: hidden;
            }

            @keyframes gradientBG {
                0% { background-position: 0% 50% }
                50% { background-position: 100% 50% }
                100% { background-position: 0% 50% }
            }

            .maintenance-card {
                background: rgba(255, 255, 255, 0.9);
                border-radius: 16px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                padding: 40px;
                max-width: 700px;
                width: 90%;
                text-align: center;
                position: relative;
                z-index: 10;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.3);
                transform: translateY(0);
                transition: transform 0.3s ease;
            }

            .maintenance-card:hover {
                transform: translateY(-5px);
            }

            .construction-icon {
                font-size: 6rem;
                color: #ff6b6b;
                margin-bottom: 20px;
                animation: pulse 2s infinite;
            }

            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }

            .title {
                font-size: 3.5rem;
                font-weight: 800;
                color: #2c3e50;
                margin-bottom: 15px;
                letter-spacing: 1px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            }

            .subtitle {
                font-size: 1.5rem;
                color: #34495e;
                margin-bottom: 30px;
                line-height: 1.6;
            }

            .info-box {
                background: rgba(236, 240, 241, 0.7);
                border-radius: 12px;
                padding: 25px;
                margin: 25px 0;
                text-align: left;
                border-left: 4px solid #3498db;
            }

            .info-item {
                display: flex;
                align-items: center;
                margin-bottom: 15px;
                font-size: 1.2rem;
            }

            .info-item i {
                margin-right: 15px;
                font-size: 1.5rem;
                width: 30px;
                color: #3498db;
            }

            .timer {
                font-size: 2.5rem;
                font-weight: bold;
                color: #e74c3c;
                margin: 20px 0;
                padding: 15px;
                background: rgba(231, 76, 60, 0.1);
                border-radius: 10px;
                font-family: 'Courier New', monospace;
            }

            .progress-container {
                height: 12px;
                background: #ecf0f1;
                border-radius: 10px;
                margin: 30px 0;
                overflow: hidden;
                box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
            }

            .progress-bar {
                height: 100%;
                background: linear-gradient(90deg, #3498db, #2ecc71);
                border-radius: 10px;
                width: 30%;
                transition: width 0.5s ease;
            }

            .contact {
                margin-top: 30px;
                font-size: 1.2rem;
                color: #7f8c8d;
                padding: 15px;
                background: rgba(236, 240, 241, 0.7);
                border-radius: 10px;
            }

            .particles {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 1;
                pointer-events: none;
            }

            .particle {
                position: absolute;
                background: rgba(255, 255, 255, 0.7);
                border-radius: 50%;
                animation: float 15s infinite linear;
            }

            @keyframes float {
                0% { transform: translateY(100vh) rotate(0deg); }
                100% { transform: translateY(-100px) rotate(360deg); }
            }

            @media (max-width: 768px) {
                .maintenance-card {
                    padding: 25px;
                }

                .title {
                    font-size: 2.5rem;
                }

                .subtitle {
                    font-size: 1.2rem;
                }

                .timer {
                    font-size: 2rem;
                }
            }
        </style>
    ''')

    # 创建背景粒子效果
    with ui.element('div').classes('particles') as particles:
        for _ in range(30):
            size = random.randint(5, 20)
            left = random.randint(0, 95)
            delay = random.uniform(0, 15)
            particle = ui.element('div').classes('particle').style(f'''
                width: {size}px;
                height: {size}px;
                left: {left}%;
                animation-delay: {delay}s;
                opacity: {random.uniform(0.3, 0.8)};
            ''')

    # 创建维护卡片
    with ui.element('div').classes('maintenance-card'):
        # 维护图标
        ui.icon('construction').classes('construction-icon')

        # 标题
        ui.label(MAINTENANCE_INFO['title']).classes('title')

        # 副标题
        ui.label(MAINTENANCE_INFO['subtitle']).classes('subtitle')

        # 进度条
        with ui.element('div').classes('progress-container'):
            progress_bar = ui.element('div').classes('progress-bar')

        # 倒计时计时器
        timer = ui.element('div').classes('timer')

        # 信息框
        with ui.element('div').classes('info-box'):
            with ui.element('div').classes('info-item'):
                ui.icon('schedule')
                ui.label(f'开始时间: {MAINTENANCE_INFO["start_time"].strftime("%Y-%m-%d %H:%M:%S")}')

            with ui.element('div').classes('info-item'):
                ui.icon('update')
                ui.label(f'预计结束: {MAINTENANCE_INFO["end_time"].strftime("%Y-%m-%d %H:%M:%S")}')

            with ui.element('div').classes('info-item'):
                ui.icon('timer')
                ui.label(MAINTENANCE_INFO['expected_duration'])

        # 联系信息
        with ui.element('div').classes('contact'):
            ui.icon('support_agent')
            ui.label(MAINTENANCE_INFO['contact'])

    # 更新倒计时和进度条
    def update_timer():
        total_seconds = (MAINTENANCE_INFO['end_time'] - MAINTENANCE_INFO['start_time']).total_seconds()
        elapsed_seconds = (datetime.now() - MAINTENANCE_INFO['start_time']).total_seconds()

        # 计算剩余时间
        remaining = MAINTENANCE_INFO['end_time'] - datetime.now()
        if remaining.total_seconds() <= 0:
            timer.text = "维护已完成！"
            progress_bar.style('width: 100%')
            return

        # 格式化倒计时
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        timer.text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        # 更新进度条
        progress = min(100, max(0, (elapsed_seconds / total_seconds) * 100))
        progress_bar.style(f'width: {progress}%')

        # 每0.5秒更新一次
        ui.timer(0.5, update_timer, once=True)

    # 初始调用
    update_timer()


# 创建页面
create_maintenance_page()

# 设置页面标题
ui.page_title("系统维护中")

# 运行应用
ui.run(title="系统维护", favicon="🚧", port=8080)
