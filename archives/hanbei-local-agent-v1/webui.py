from __future__ import annotations

from pathlib import Path

import streamlit as st
import yaml

from agent.workflow import WorkflowRouter

ROOT = Path(__file__).resolve().parent


def load_config() -> dict:
    config_path = ROOT / "config.yaml"
    if not config_path.exists():
        config_path = ROOT / "config.example.yaml"
    return yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}


st.set_page_config(page_title="Hanbei Local Agent", layout="wide")
st.title("汉北小龙虾本地智能体 v1")

config = load_config()
router = WorkflowRouter(config=config, root=ROOT)

task = st.selectbox("任务类型", ["content", "sales", "customer", "image", "code", "management"])
user_input = st.text_area("输入需求", height=220)

if st.button("运行", type="primary"):
    if not user_input.strip():
        st.warning("请先输入需求。")
    else:
        try:
            result = router.run(task=task, user_input=user_input)
            st.markdown(result)
        except Exception as exc:
            st.error(f"运行失败：{exc}")
