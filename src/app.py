import streamlit as st
from sample_size_calc import (
    calculate_sample_size_proportion,
    calculate_sample_size_continuous,
)


def main():
    st.set_page_config(page_title="AB实验样本量计算器", layout="wide")
    st.title("🧪 AB实验最小样本量计算器")
    st.markdown("""
    输入业务参数，自动计算每组所需最小样本量。
    """)

    # 初始化session state
    if "current_tab" not in st.session_state:
        st.session_state.current_tab = "📊 比例型指标"
    if "show_result" not in st.session_state:
        st.session_state.show_result = False
    if "result_data" not in st.session_state:
        st.session_state.result_data = {}

    # 添加侧边栏说明
    with st.sidebar:
        st.header("ℹ️ 使用说明")
        st.markdown("""
        - **比例型指标**: 适用于转化率、点击率等
        - **连续型指标**: 适用于平均值类指标
        """)

        st.markdown("---")
        st.markdown("**参数说明**:")
        st.markdown("- 显著性水平 α: 通常设为 0.05")
        st.markdown("- 统计功效 1-β: 通常设为 0.8 或更高")

    # 使用radio buttons代替tabs来更好追踪标签页切换
    tab_names = ["📊 比例型指标", "📏 连续型指标"]
    selected_tab = st.radio("选择指标类型", tab_names, format_func=lambda x: x)

    # 更新当前标签页并检查是否发生变化
    prev_tab = st.session_state.current_tab
    st.session_state.current_tab = selected_tab

    # 如果标签页改变了，清除之前的结果
    if prev_tab != st.session_state.current_tab:
        st.session_state.show_result = False

    # 根据选中的标签页显示对应的表单
    if selected_tab == "📊 比例型指标":
        st.subheader("比例型指标")
        st.markdown("适用于转化率、点击率等比例型指标")

        col1, col2 = st.columns(2)
        with col1:
            baseline_abs = (
                st.number_input(
                    "基线转化率 (%)",
                    min_value=0.01,
                    max_value=100.0,
                    value=10.0,
                    step=0.1,
                    key="abs_baseline",
                    help="当前基准转化率，例如：10 表示 10%",
                )
                / 100
            )
        with col2:
            mde_abs = (
                st.number_input(
                    "最小可检测效应 (绝对值%)",
                    min_value=0.01,
                    max_value=100.0,
                    value=1.0,
                    step=0.1,
                    key="abs_mde",
                    help="期望检测到的最小绝对变化，例如：1 表示从 10% 到 11%",
                )
                / 100
            )

        col3, col4 = st.columns(2)
        with col3:
            alpha_abs = st.slider(
                "显著性水平 α", 0.01, 0.1, 0.05, step=0.01, key="abs_alpha"
            )
        with col4:
            power_abs = st.slider(
                "统计功效 (1-β)", 0.7, 0.95, 0.8, step=0.05, key="abs_power"
            )

    else:  # 连续型指标
        st.subheader("连续型指标")
        st.markdown("适用于平均停留时间、平均订单金额等连续型指标")

        col1, col2, col3 = st.columns(3)
        with col1:
            mean_val = st.number_input(
                "当前指标均值",
                value=100.0,
                step=1.0,
                key="cont_mean",
                help="当前指标的平均值",
            )
        with col2:
            mde_val = st.number_input(
                "最小可检测效应 (MDE)",
                value=5.0,
                step=0.1,
                key="cont_mde",
                help="期望检测到的最小绝对变化值",
            )
        with col3:
            std_dev_val = st.number_input(
                "历史标准差",
                min_value=0.1,
                value=15.0,
                step=0.5,
                key="cont_std",
                help="历史数据的标准差",
            )

        col4, col5 = st.columns(2)
        with col4:
            alpha_cont = st.slider(
                "显著性水平 α", 0.01, 0.1, 0.05, step=0.01, key="cont_alpha"
            )
        with col5:
            power_cont = st.slider(
                "统计功效 (1-β)", 0.7, 0.95, 0.8, step=0.05, key="cont_power"
            )

    # 计算按钮
    st.markdown("---")
    if st.button("🔍 计算样本量", type="primary", use_container_width=True):
        try:
            # 根据当前标签页执行相应计算
            if st.session_state.current_tab == "📊 比例型指标":
                n = calculate_sample_size_proportion(
                    baseline_abs, mde_abs, alpha_abs, power_abs
                )
                st.session_state.result_data = {
                    "n": n,
                    "indicator_type": "比例型指标",
                    "is_continuous": False,
                }
                st.session_state.show_result = True

            else:  # 连续型指标
                n = calculate_sample_size_continuous(
                    mean_val, mde_val, std_dev_val, alpha_cont, power_cont
                )
                st.session_state.result_data = {
                    "n": n,
                    "indicator_type": "连续型指标",
                    "is_continuous": True,
                }
                st.session_state.show_result = True

        except ValueError as e:
            st.error(f"输入参数错误: {str(e)}")
        except Exception as e:
            st.error(f"计算过程中出现错误: {str(e)}")

    # 显示结果
    if st.session_state.show_result:
        display_result(
            st.session_state.result_data["n"],
            st.session_state.result_data["indicator_type"],
            st.session_state.result_data["is_continuous"],
        )


def display_result(n, indicator_type, is_continuous=False):
    """显示计算结果"""
    if n == float("inf"):
        st.warning("无法检测到有效提升，请检查输入参数")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"✅ 每组所需最小样本量：**{n:,}**")
        with col2:
            st.info(f"📊 总样本量（A + B）：**{2 * n:,}**")

        st.caption(f"注：基于双样本{('t' if is_continuous else 'Z')}检验，双尾检验")


if __name__ == "__main__":
    main()
