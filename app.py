import streamlit as st
from openai import OpenAI

# --- 页面配置 ---
st.set_page_config(page_title="AI 自由创作·国产加速版", page_icon="🚀", layout="wide")

# --- 侧边栏 ---
st.sidebar.title("⚙️ 引擎设置 (Kimi版)")

# 这里提示用户去哪里弄 Key
st.sidebar.info("👉 [点击这里去申请 Kimi Key](https://platform.moonshot.cn/) (注册即送免费额度)")
api_key = st.sidebar.text_input("输入 Kimi API Key", type="password")

# 模型选择 (换成了 Kimi 的模型)
model_choice = st.sidebar.selectbox("选择模型", ["moonshot-v1-8k", "moonshot-v1-32k"], index=0)
st.sidebar.caption("8k适合短篇，32k适合长篇连贯剧情")

# --- 主标题 ---
st.title("🚀 AI 小说创作器：国产极速版")
st.markdown("不需要梯子，速度更快，更懂中文语境！")

# --- 设定区域 ---
st.subheader("1. 设定你的世界")
col1, col2 = st.columns(2)
with col1:
    characters_def = st.text_area("👥 角色档案", height=150, placeholder="主角：林萧，性格腹黑...")
with col2:
    world_def = st.text_area("🌍 世界背景", height=150, placeholder="修仙界，等级分为练气、筑基...")

st.subheader("2. 剧情大纲")
plot_input = st.text_area("🎬 本章剧情", height=100, placeholder="林萧在拍卖会捡漏了一块破铁片...")

# --- 核心逻辑 (修改了 Base URL) ---
def generate_story():
    if not api_key:
        st.error("宝宝，请先在左侧填入 API Key 哦！")
        return

    # ❗❗❗ 关键修改在这里 ❗❗❗
    # 我们告诉代码：不要去连美国的 OpenAI，去连国内的 Kimi
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.moonshot.cn/v1", # 这里的地址换成了 Kimi 的
    )

    system_prompt = f"""
    你是一位专业的中文小说家。请根据用户设定写一章小说。
    要求：
    1. 沉浸式描写，多用感官细节。
    2. 对话要符合中文口语习惯，不要有翻译腔。
    3. 节奏紧凑。
    """

    user_prompt = f"""
    【角色】{characters_def}
    【背景】{world_def}
    【剧情】{plot_input}
    
    请开始写作：
    """

    try:
        with st.spinner("🚀 Kimi 正在飞速码字中..."):
            response = client.chat.completions.create(
                model=model_choice,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
            )
            return response.choices[0].message.content
    except Exception as e:
        st.error(f"出错了：{e}")
        return None

# --- 按钮 ---
if st.button("✨ 开始生成 (免魔法)", type="primary"):
    if not characters_def or not plot_input:
        st.warning("请填写完整设定哦~")
    else:
        result = generate_story()
        if result:
            st.markdown("---")
            st.write(result)
            st.download_button("💾 下载小说", data=result, file_name="story.txt")