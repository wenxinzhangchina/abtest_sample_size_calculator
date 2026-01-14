# 访问

Live Demo: Deployed on Streamlit Community Cloud. [Check it out!](https://abtestsamplesizecalculator-zhangwenxintest.streamlit.app/)

# 说明

## 1. 注意

该托管服务为免费共享平台，主要用于演示、原型展示或开发测试，不适用于生产环境。具体限制如下：

- 应用自动休眠机制
为节约计算资源，Streamlit Community Cloud 会在应用一段时间无访问请求后（通常为数分钟至几小时）自动将其置于“休眠”状态。

> 当您首次访问或长时间未访问时，可能会看到提示：
"This app has gone to sleep due to inactivity. Would you like to wake it back up?"
此时只需点击 “Wake it back up” 或刷新页面，系统将自动重启应用（首次加载可能需 5–15 秒）。

## 2. 不适用于生产场景的原因

- 无高可用性保障：应用会因不活跃而休眠，无法保证即时响应。
- 无服务等级协议（SLA）：官方明确声明 Community Cloud 不适用于生产部署。
- 资源受限：CPU、内存及运行时长均受限制，复杂任务可能失败。
- 状态不持久：每次休眠/唤醒都会重启进程，内存中的状态（如缓存、会话变量）将丢失。
- 域名与安全限制：仅支持 *.streamlit.app 子域名，无法绑定自定义域名或配置高级 HTTPS 策略。

## 3. 适用场景

- 快速分享原型或 Demo
- 教学演示或开源项目展示
- 内部工具临时试用
