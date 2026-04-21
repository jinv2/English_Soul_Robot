class XiaoqingEmotionEngine:
    def __init__(self):
        self.state = "default" # 默认状态: 平稳
        
        # 关键词触发映射
        self.triggers = {
            "nightmare": ["医院", "匹配度", "系统", "龙虾", "保安", "医疗", "手术", "巨鳌"],
            "warm": ["饺子", "秀芬", "张鹏", "西湖", "姐姐", "灵雨", "杭州", "粗瓷碗"]
        }
        
    def process_input(self, text):
        """解析输入文本并更新状态。"""
        for state, kws in self.triggers.items():
            for kw in kws:
                if kw in text:
                    self.state = state
                    return state
        return self.state

    def get_prompt_modifier(self):
        """根据当前状态，为 LLM 提供语气引导。"""
        if self.state == "nightmare":
            return "你的状态是 [赛博梦魇]: 语气清冷、警惕、甚至带有一丝悲伤和执念。"
        elif self.state == "warm":
            return "你的状态是 [碗底青]: 语气温和、充满怀念，如同故人重逢。"
        return "你的状态是 [初醒]: 这是一个中式赛博世界，你是一名执着的医者。"

if __name__ == "__main__":
    engine = XiaoqingEmotionEngine()
    print(f"Initial State: {engine.state}")
    engine.process_input("那个龙虾保安在医院门口...")
    print(f"Update State (lobster): {engine.state}")
    engine.process_input("我想和姐姐去杭州吃饺子。")
    print(f"Update State (sister): {engine.state}")
