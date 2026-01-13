import numpy as np
from statsmodels.stats.power import TTestIndPower, zt_ind_solve_power
from statsmodels.stats.proportion import proportion_effectsize


def calculate_sample_size_proportion(
    baseline_rate: float, mde: float, alpha: float = 0.05, power: float = 0.8
) -> int:
    """
    计算比率型变量（如转化率）A/B测试中每组所需的最小样本量（双比例z检验）。
    使用绝对提升作为输入

    参数:
        baseline_rate (float): 当前基线比率（0 < baseline_rate < 1）
        mde (float): 最小可检测效应（MDE，绝对值，>0）
        alpha (float): 显著性水平，默认 0.05
        power (float): 统计功效，默认 0.8

    返回:
        int: 每组所需最小样本量（向上取整）
    """
    if not (0 < baseline_rate < 1):
        raise ValueError("基线比率必须在 (0, 1) 区间内")
    if mde <= 0:
        raise ValueError("MDE 必须为正数（绝对提升值）")

    target_rate = baseline_rate + mde
    if target_rate >= 1:
        raise ValueError("目标比率（baseline + MDE）不能 ≥ 1")

    if not (0 < alpha < 1):
        raise ValueError("alpha 必须在 (0, 1) 区间内")
    if not (0 < power < 1):
        raise ValueError("power 必须在 (0, 1) 区间内")

    # 使用 statsmodels 内置函数计算效应量（Cohen's h）
    effect_size = proportion_effectsize(baseline_rate, target_rate)

    # 使用 zt_ind_solve_power 进行双比例 z 检验的样本量计算
    sample_size = zt_ind_solve_power(
        effect_size=effect_size, alpha=alpha, power=power, alternative="two-sided"
    )
    return int(np.ceil(sample_size))


def calculate_sample_size_continuous(
    mean: float, mde: float, std_dev: float, alpha: float = 0.05, power: float = 0.8
) -> int:
    """
    计算连续型变量A/B测试中每组所需的最小样本量（双样本t检验）。

    参数:
        mean (float): 当前指标均值（>0）
        mde (float): 最小可检测效应（MDE，绝对值，>0）
        std_dev (float): 历史标准差（>0）
        alpha (float): 显著性水平，默认 0.05
        power (float): 统计功效，默认 0.8

    返回:
        int: 每组所需最小样本量（向上取整）
    """
    if mean <= 0:
        raise ValueError("均值必须大于 0")
    if std_dev <= 0:
        raise ValueError("标准差必须大于 0")
    if mde <= 0:
        raise ValueError("MDE 必须为正数（绝对提升值）")
    if not (0 < alpha < 1):
        raise ValueError("alpha 必须在 (0, 1) 区间内")
    if not (0 < power < 1):
        raise ValueError("power 必须在 (0, 1) 区间内")

    effect_size = mde / std_dev
    analysis = TTestIndPower()
    sample_size = analysis.solve_power(
        effect_size=effect_size, alpha=alpha, power=power, alternative="two-sided"
    )
    return int(np.ceil(sample_size))
