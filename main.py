"""
租赁电子产品销售培训工具
========================
功能：输入一个销售培训题目，DeepSeek 从 6 个维度生成衍生题目
维度：客户痛点、产品特性、使用场景、异议处理、竞品对比、价值主张
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量（从 .env 文件读取 API Key）
load_dotenv()

# 初始化 DeepSeek 客户端（兼容 OpenAI SDK 格式）
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# ============================================================
# 六个思考维度的 System Prompt 定义
# 每个维度引导 DeepSeek 从不同角度重新审视原始题目
# ============================================================
DIMENSIONS = {
    "1": {
        "name": "🎯 客户痛点",
        "prompt": (
            "你是一名资深的租赁电子产品销售培训师。"
            "请从【客户痛点】维度出发，将用户输入的原始题目改写成一个全新的培训题目。"
            "新题目要引导学员深入思考客户在租赁电脑/手机等电子设备时的核心痛点："
            "如一次性采购成本过高、设备快速贬值折旧、IT维护人力负担、设备更新换代频繁等。"
            "只输出新题目本身，不要输出任何解释说明。"
        ),
    },
    "2": {
        "name": "💻 产品特性",
        "prompt": (
            "你是一名资深的租赁电子产品销售培训师。"
            "请从【产品特性】维度出发，将用户输入的原始题目改写成一个全新的培训题目。"
            "新题目要引导学员从设备性能参数、配置灵活定制、品牌可选范围、新旧设备梯度、"
            "保修服务覆盖等产品特性角度重新审视销售场景。"
            "只输出新题目本身，不要输出任何解释说明。"
        ),
    },
    "3": {
        "name": "🏢 使用场景",
        "prompt": (
            "你是一名资深的租赁电子产品销售培训师。"
            "请从【使用场景】维度出发，将用户输入的原始题目改写成一个全新的培训题目。"
            "新题目要引导学员结合具体业务场景来思考销售策略："
            "如企业展会临时用机、短期项目团队扩容、远程办公设备交付、"
            "初创公司轻资产运营、季节性业务高峰弹性扩容等。"
            "只输出新题目本身，不要输出任何解释说明。"
        ),
    },
    "4": {
        "name": "🛡️ 异议处理",
        "prompt": (
            "你是一名资深的租赁电子产品销售培训师。"
            "请从【异议处理】维度出发，将用户输入的原始题目改写成一个全新的培训题目。"
            "新题目要引导学员预判并熟练应对客户常见异议："
            "如'租不如买划算'、'二手设备不安全'、'合同期太长不灵活'、"
            "'出了问题谁负责'、'数据安全怎么保障'等典型顾虑。"
            "只输出新题目本身，不要输出任何解释说明。"
        ),
    },
    "5": {
        "name": "⚖️ 竞品对比",
        "prompt": (
            "你是一名资深的租赁电子产品销售培训师。"
            "请从【竞品对比】维度出发，将用户输入的原始题目改写成一个全新的培训题目。"
            "新题目要引导学员对比分析不同方案的优劣势："
            "如租赁 vs 直接购买、不同租赁服务商之间的差异、"
            "融资租赁 vs 经营租赁、长租 vs 短租的成本效益对比等。"
            "只输出新题目本身，不要输出任何解释说明。"
        ),
    },
    "6": {
        "name": "✨ 价值主张",
        "prompt": (
            "你是一名资深的租赁电子产品销售培训师。"
            "请从【价值主张】维度出发，将用户输入的原始题目改写成一个全新的培训题目。"
            "新题目要引导学员提炼并向客户清晰传达租赁服务的核心价值："
            "如降本增效（CAPEX 转 OPEX）、灵活升级随需而变、一站式服务省心省力、"
            "始终使用最新设备保持竞争力、税务优化空间等。"
            "只输出新题目本身，不要输出任何解释说明。"
        ),
    },
}


def call_deepseek(system_prompt: str, user_question: str) -> str:
    """
    调用 DeepSeek API 生成衍生题目

    Args:
        system_prompt: 当前维度的 System Prompt
        user_question: 用户输入的原始题目

    Returns:
        DeepSeek 生成的衍生题目文本
    """
    response = client.chat.completions.create(
        model="deepseek-chat",  # 使用 DeepSeek 对话模型
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"原始题目：{user_question}"},
        ],
        temperature=0.8,       # 适度创造性
        max_tokens=500,        # 控制输出长度
    )
    return response.choices[0].message.content.strip()


def print_banner():
    """打印程序启动 Banner"""
    banner = """
╔══════════════════════════════════════════════════╗
║     🖥️ 租赁电子设备销售培训 · 多维出题工具      ║
║     Powered by DeepSeek AI                      ║
╚══════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """主函数：控制台交互循环"""
    print_banner()

    while True:
        # 获取用户输入的原始题目
        question = input("\n📝 请输入培训题目（输入 q 退出）：").strip()

        if question.lower() == "q":
            print("👋 感谢使用，再见！")
            break

        if not question:
            print("⚠️ 题目不能为空，请重新输入。")
            continue

        print(f"\n{'='*60}")
        print(f"📌 原始题目：{question}")
        print(f"{'='*60}")
        print("🔄 正在从 6 个维度生成衍生题目，请稍候...\n")

        # 遍历每个维度，调用 DeepSeek 生成衍生题目
        for key, dim in DIMENSIONS.items():
            print(f"{dim['name']}", end="", flush=True)
            try:
                result = call_deepseek(dim["prompt"], question)
                print(f"\n   → {result}\n")
            except Exception as e:
                print(f"\n   ❌ 生成失败：{e}\n")

        print(f"{'='*60}")
        print("✅ 全部维度生成完成！可以继续输入下一道题目。\n")


if __name__ == "__main__":
    main()
