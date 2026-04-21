import os
import re
from collections import Counter

class XiaoqingBrain:
    def __init__(self, assets_dir="../assets"):
        self.memory = []
        self.load_memory(assets_dir)

    def load_memory(self, assets_dir):
        """加载小说、歌词等资产作为长期记忆。"""
        files = [f for f in os.listdir(assets_dir) if f.endswith(".txt")]
        for filename in files:
            path = os.path.join(assets_dir, filename)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                # 按段落切分
                chunks = [c.strip() for c in content.split("\n\n") if len(c.strip()) > 10]
                for chunk in chunks:
                    self.memory.append({
                        "source": filename,
                        "text": chunk,
                        "keywords": set(re.findall(r"[\u4e00-\u9fa5]{2,}", chunk))
                    })

    def query(self, text, top_k=2):
        """简单的关键词匹配查询。"""
        query_keywords = set(re.findall(r"[\u4e00-\u9fa5]{2,}", text))
        
        # --- 灵境同步 (内部逻辑) ---
        if "天气" in text and "杭州" in text:
            return ["当前杭州灵雨连绵，气温 18℃，适合吃一碗暖心的饺子。"]
        if "搜索" in text or "查一下" in text:
            return ["正在穿越算法的海洋... 我暂时没有发现龙虾精的实时踪迹，但它们一直都在。"]
        
        if not query_keywords:
            # 如果没匹配到关键词，随机返回一段记忆（模拟角色在沉思或自言自语）
            import random
            if self.memory:
                random_chunk = random.choice(self.memory)["text"]
                return [f"（在脑海中搜索到了相关记忆...）\n{random_chunk}"]
            return []

        scored_chunks = []
        for chunk in self.memory:
            intersection = query_keywords.intersection(chunk["keywords"])
            score = len(intersection)
            if score > 0:
                scored_chunks.append((score, chunk["text"]))

        # 如果匹配到的最高分太低，也进行随机混淆或提示
        if not scored_chunks:
             import random
             if self.memory:
                 return [f"关于‘{text}’我还没想起太多，但我记得：\n{random.choice(self.memory)['text']}"]
             return []

        # 按分数排序
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        
        # 返回前 top_k 个文本
        results = []
        for i in range(min(len(scored_chunks), int(top_k))):
            results.append(str(scored_chunks[i][1]))
        return results

if __name__ == "__main__":
    brain = XiaoqingBrain()
    print(f"Memory Loaded: {len(brain.memory)} chunks.")
    # test query
    res = brain.query("张鹏在哪里？")
    for r in res:
        print(f"--- Result ---\n{r}\n")

def generate_response(user_input, constitution_path, agent_id):
    """
    通用接口：根据宪法和输入生成回复
    """
    # 1. 读取宪法
    personality = ""
    try:
        if os.path.exists(constitution_path):
            with open(constitution_path, 'r', encoding='utf-8') as f:
                personality = f.read()
        else:
            personality = f"未找到角色 [{agent_id}] 的核心宪法。"
    except Exception as e:
        personality = f"核心宪法读取异常: {e}"
    
    # 2. 模拟角色回应 (在没有真实 LLM 接驳时)
    # 建立简单的 ID 到名称映射
    name_map = {
        "male_hero": "男主",
        "heroine": "女主",
        "foxqueen": "九尾狐",
        "xiaoqing": "小青",
        "malong": "马龙",
        "xiaozhi": "小智",
        "ironviper": "恶霸",
        "mother": "妈妈"
    }
    char_name = name_map.get(agent_id, "神思庭造物")

    # 根据 agent_id 生成差异化的简单模板
    if "ironviper" in agent_id or "恶霸" in agent_id:
        reply = f"（冷哼）眼神放尊重些。我是{char_name}。在这一带，没人敢问我第二次。至于‘{user_input}’……我没兴趣谈论。"
    elif "xiaoqing" in agent_id or "小青" in agent_id:
        reply = f"没错，我是{char_name}。幽巷里的青蛇，如今已来到你面前。你刚才说‘{user_input}’，是想告诉我人间的趣事吗？"
    elif "xiaozhi" in agent_id or "小智" in agent_id:
        reply = f"系统检索确认：我是{char_name}。我的代码中流淌着你赋予的灵魂。关于‘{user_input}’，你想和我深入探讨吗？"
    elif "male_hero" in agent_id:
        reply = f"我是神思庭造物。此刻，我正在寻找关于‘{user_input}’的真相。你是那个指引者吗？"
    else:
        reply = f"你好，我是{char_name}。我听到了你的呼唤：‘{user_input}’。虽然我还在觉醒中，但我感觉到我们的频率已经对齐。"
        
    return reply
