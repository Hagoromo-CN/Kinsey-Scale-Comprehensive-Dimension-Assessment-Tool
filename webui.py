import gradio as gr
import numpy as np
import tempfile
import os
import sys

# ===================== 1. 打包适配（保留，注释说明用途） =====================
def resource_path(relative_path):
    """打包为exe时的资源路径适配（非打包运行时无影响）"""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 临时目录配置（Gradio官方推荐：仅在需要时设置，注释说明用途）
temp_dir = tempfile.mkdtemp()
os.environ["GRADIO_TEMP_DIR"] = temp_dir
os.environ["GRADIO_CACHE"] = temp_dir

# ===================== 2. 静态资源定义（分离配置与逻辑，官方推荐） =====================
# 2.1 双语界面文字（结构化存储，便于维护）
UI_TEXT = {
    "cn": {
        "title": "金赛量表全维度评估工具（50题双语版）",
        "ethic": """
## 🚨 重要伦理声明
1. 本工具仅为个人自我认知参考，不构成专业心理/性学诊断，性取向的核心是自我认同；
2. 性取向是连续谱，无「正常/不正常」之分，量表分数仅反映倾向，非绝对标签；
3. 所有作答数据仅在本地运行，无任何上传/存储，严格保护隐私；
4. 若存在性取向相关的心理困扰，建议咨询专业的性学咨询师/临床心理师；
5. 量表结果可能随个人经历、认知变化而改变，并非一成不变。
(注:❌)中文模式下会现阶段有一些bug,可以在中文下阅读题目后切换到英文作答
        """,
        "start_btn": "✅ 已阅读并同意，开始评估",
        "quiz_tab": "📝 开始答题",
        "result_tab": "📊 评估结果",
        "progress": "答题进度：{}/{}",
        "select_ans": "请选择你的答案",
        "prev_btn": "⬅️ 上一题",
        "next_btn": "➡️ 下一题",
        "submit_btn": "📤 提交所有答案",
        "lang_switch": "🌐 Switch to the English",
        "empty_tip": "❌ 还有未完成的题目！请返回完成第{}题后再提交。",
        "no_ans_tip": "❌ 请先选择本题答案后再进行下一步！",
        "submit_success_tip": "✅ 答题完成！请单击结果区按钮以展示评估结果",
        "core_title": "一、核心性取向等级",
        "core_avg": "核心维度平均分：",
        "core_grade": "最终金赛等级：",
        "core_inter": "等级解读：",
        "stress_title": "二、社会压力程度评估",
        "stress_avg": "社会压力平均分：",
        "stress_grade": "压力等级：",
        "stress_inter": "压力解读：",
        "asex_title": "三、无性恋倾向评估",
        "asex_avg": "无性恋倾向平均分：",
        "asex_grade": "倾向等级：",
        "asex_inter1": "✅ 无性恋倾向显著（优先判定为X等级）",
        "asex_inter2": "❌ 无性恋倾向不显著（核心等级为{}）",
        "tips_title": "💡 核心提示",
        "tip1": "1. 本评估仅为自我认知参考，不构成专业心理/性学诊断，性取向的核心是自我认同；",
        "tip2": "2. 社会压力程度反映当前的外部环境影响，与性取向本身无关，无需因压力否定自我；",
        "tip3": "3. 无性恋是正常的性取向类型之一，与0-6等级并行，无优劣之分；",
        "tip4": "4. 若存在性取向相关的困惑，建议咨询专业的性学咨询师，拒绝自我否定。",
        "launch_tip1": "✅ 金赛量表评估工具已启动！",
        "launch_tip2": "👉 浏览器将自动打开，或手动访问：http://127.0.0.1:7860",
        "launch_tip3": "⚠️  关闭此窗口将停止运行工具！"
    },
    "en": {
        "title": "Kinsey Scale Comprehensive Assessment Tool (50 Questions Bilingual Version)",
        "ethic": """
## 🚨 Important Ethical Statement
1. This tool is for personal self-awareness only and does not constitute professional psychological/sexological diagnosis; the core of sexual orientation is self-identification.
2. Sexual orientation exists on a continuous spectrum, with no "normal/abnormal" distinction; scale scores only reflect tendencies, not absolute labels.
3. All response data runs locally with no upload/storage; privacy is strictly protected.
4. If you have psychological distress related to sexual orientation, consult a professional sexological counselor/clinical psychologist.
5. Scale results may change with personal experience and cognition and are not fixed.
        """,
        "start_btn": "✅ I have read and agree, start assessment",
        "quiz_tab": "📝 Start Answering",
        "result_tab": "📊 Assessment Results",
        "progress": "Progress: {}/{}",
        "select_ans": "Please select your answer",
        "prev_btn": "⬅️ Previous Question",
        "next_btn": "➡️ Next Question",
        "submit_btn": "📤 Submit All Answers",
        "lang_switch": "🌐 切换到中文",
        "empty_tip": "❌ Unfinished questions! Please return to complete Question {} before submitting.",
        "no_ans_tip": "❌ Please select an answer for this question before proceeding!",
        "submit_success_tip": "✅ Answering completed! Please click the results area button to show assessment results",
        "core_title": "I. Core Sexual Orientation Level",
        "core_avg": "Core Dimension Average Score: ",
        "core_grade": "Final Kinsey Level: ",
        "core_inter": "Level Interpretation: ",
        "stress_title": "II. Social Stress Level Assessment",
        "stress_avg": "Social Stress Average Score: ",
        "stress_grade": "Stress Level: ",
        "stress_inter": "Stress Interpretation: ",
        "asex_title": "III. Asexuality Tendency Assessment",
        "asex_avg": "Asexuality Tendency Average Score: ",
        "asex_grade": "Tendency Level: ",
        "asex_inter1": "✅ Significant asexuality tendency (prioritized as Level X)",
        "asex_inter2": "❌ Insignificant asexuality tendency (core level is {})",
        "tips_title": "💡 Key Tips",
        "tip1": "1. This assessment is for personal self-awareness only and does not constitute professional psychological/sexological diagnosis; the core of sexual orientation is self-identification.",
        "tip2": "2. Social stress level reflects the impact of the current external environment and has nothing to do with sexual orientation itself; do not deny yourself due to stress.",
        "tip3": "3. Asexuality is a normal type of sexual orientation, parallel to levels 0-6, with no distinction of superiority or inferiority.",
        "tip4": "4. If you have doubts related to sexual orientation, consult a professional sexological counselor and reject self-denial.",
        "launch_tip1": "✅ Kinsey Scale Assessment Tool Launched!",
        "launch_tip2": "👉 Browser will open automatically, or visit manually: http://127.0.0.1:7860",
        "launch_tip3": "⚠️  Close this window to stop the tool!"
    }
}

# 2.2 核心维度解读（结构化存储）
KINSEY_INTERPRET = {
    "cn": {
        0: "【等级0：完全异性恋】仅对异性产生情感吸引、性幻想和恋爱/行为倾向，无任何同性倾向，自我认同为纯异性恋。",
        1: "【等级1：偏异性恋】几乎完全对异性有所有倾向，仅偶尔对同性产生极轻微的情感/视觉吸引，无实际同性亲密行为或仅有极偶然的想法。",
        2: "【等级2：轻微偏异性恋的双性恋】主要对异性有倾向，但对同性也有明显的情感/视觉吸引，可能有少量非实质性的同性亲密互动（如牵手/拥抱）。",
        3: "【等级3：无偏向的双性恋】对异性和同性的情感吸引、性幻想、恋爱倾向基本均等，是典型的双性恋，对两种性别的倾向无明显偏向。",
        4: "【等级4：轻微偏同性恋的双性恋】主要对同性有倾向，但对异性也有明显的情感/视觉吸引，可能有少量非实质性的异性亲密互动（如牵手/拥抱）。",
        5: "【等级5：偏同性恋】几乎完全对同性有所有倾向，仅偶尔对异性产生极轻微的情感/视觉吸引，无实际异性亲密行为或仅有极偶然的想法。",
        6: "【等级6：完全同性恋】仅对同性产生情感吸引、性幻想和恋爱/行为倾向，无任何异性倾向，自我认同为纯同性恋。",
        "X": "【等级X：无性恋】对任何性别的个体均无明显的情感吸引、性幻想或性冲动，亲密关系更侧重精神层面，无性别指向的性倾向。"
    },
    "en": {
        0: "[Level 0: Exclusively Heterosexual] Only experience emotional attraction, sexual fantasies, and romantic/behavioral tendencies toward the opposite sex, with no same-sex tendencies; self-identify as exclusively heterosexual.",
        1: "[Level 1: Predominantly Heterosexual] Almost all tendencies are toward the opposite sex, with only occasional minimal emotional/visual attraction to the same sex, no actual same-sex intimate behavior or only occasional thoughts.",
        2: "[Level 2: Bisexual with a slight heterosexual lean] Main tendencies are toward the opposite sex, but with obvious emotional/visual attraction to the same sex, possibly a small amount of non-substantive same-sex intimate interaction (e.g., holding hands/hugging).",
        3: "[Level 3: Bisexual with no lean] Emotional attraction, sexual fantasies, and romantic tendencies toward both sexes are basically equal; a typical bisexual with no obvious lean toward either gender.",
        4: "[Level 4: Bisexual with a slight homosexual lean] Main tendencies are toward the same sex, but with obvious emotional/visual attraction to the opposite sex, possibly a small amount of non-substantive opposite-sex intimate interaction (e.g., holding hands/hugging).",
        5: "[Level 5: Predominantly Homosexual] Almost all tendencies are toward the same sex, with only occasional minimal emotional/visual attraction to the opposite sex, no actual opposite-sex intimate behavior or only occasional thoughts.",
        6: "[Level 6: Exclusively Homosexual] Only experience emotional attraction, sexual fantasies, and romantic/behavioral tendencies toward the same sex, with no opposite-sex tendencies; self-identify as exclusively homosexual.",
        "X": "[Level X: Asexual] No obvious emotional attraction, sexual fantasies, or sexual impulses toward individuals of any gender; intimate relationships focus more on the spiritual level with no gender-directed sexual tendencies."
    }
}

STRESS_INTERPRET = {
    "cn": {
        0: "【社会压力程度：极低】几乎未感受到任何来自社会/家庭/朋友的性取向相关压力，能完全自由地表达自我。",
        1: "【社会压力程度：低】偶尔感受到轻微压力，但不会影响自我认同和日常表达，仅在特定场景下略有顾虑。",
        2: "【社会压力程度：中低】有一定压力，但可通过自我调节缓解，大部分场景下能正常表达自我倾向。",
        3: "【社会压力程度：中等】明显感受到压力，部分场景下会刻意隐藏自我倾向，偶尔产生焦虑情绪。",
        4: "【社会压力程度：中高】压力较显著，多数场景下会隐藏自我倾向，频繁因性取向问题产生焦虑/自我怀疑。",
        5: "【社会压力程度：高】压力显著，几乎不敢在任何公开场景表达自我倾向，长期因性取向问题产生心理负担。",
        6: "【社会压力程度：极高】承受极大的社会/家庭压力，完全不敢表达真实的性取向，甚至因压力产生严重心理困扰。"
    },
    "en": {
        0: "[Social Stress Level: Extremely Low] Almost no sexual orientation-related stress from society/family/friends, able to express oneself completely freely.",
        1: "[Social Stress Level: Low] Occasionally feel slight stress, but it does not affect self-identification and daily expression, with only minor concerns in specific scenarios.",
        2: "[Social Stress Level: Low-Medium] Some stress is felt, but it can be relieved through self-regulation, able to express personal tendencies normally in most scenarios.",
        3: "[Social Stress Level: Medium] Obvious stress is felt, deliberately hiding personal tendencies in some scenarios, occasionally experiencing anxiety.",
        4: "[Social Stress Level: Medium-High] Significant stress is felt, hiding personal tendencies in most scenarios, frequently experiencing anxiety/self-doubt due to sexual orientation issues.",
        5: "[Social Stress Level: High] Severe stress is felt, almost daring not to express personal tendencies in any public scenario, with long-term psychological burden due to sexual orientation issues.",
        6: "[Social Stress Level: Extremely High] Bear immense social/family pressure, daring not to express true sexual orientation at all, even experiencing severe psychological distress due to pressure."
    }
}

# 2.3 50题题库（结构化存储）
QUESTIONS_50 = [
    # 核心性取向维度（1-35题）
    (("1. 你会对哪一性别的人产生「心动」的强烈情感吸引？", "1. Which gender do you experience intense emotional attraction (heart flutter) toward?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("2. 你会对哪一性别的人产生性幻想（包括画面/场景想象）？", "2. Which gender do you have sexual fantasies (including visual/scenario imagination) about?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("3. 你更愿意与哪一性别的人建立长期恋爱关系（如婚姻/同居）？", "3. Which gender do you prefer to establish a long-term romantic relationship (e.g., marriage/cohabitation) with?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("4. 你会主动靠近/关注哪一性别的人（如主动聊天、刷相关内容）？", "4. Which gender do you take the initiative to approach/focus on (e.g., initiate conversations, browse related content)?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("5. 你会对哪一性别的人产生身体接触的渴望（如拥抱、牵手、亲吻）？", "5. Which gender do you desire physical contact (e.g., hugging, holding hands, kissing) with?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("6. 你在择偶时，优先考虑哪一性别的对象？", "6. Which gender do you prioritize when choosing a romantic partner?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("7. 你会对哪一性别的人产生「占有欲」（不想对方和别人亲近）？", "7. Which gender do you experience possessiveness toward (not wanting them to be close to others)?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("8. 你会因哪一性别的人出现而感到紧张/害羞（如脸红、心跳加速）？", "8. Which gender makes you feel nervous/shy (e.g., blushing, rapid heartbeat) when they appear?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("9. 你更愿意和哪一性别的人分享私密心事（如烦恼、喜悦）？", "9. Which gender do you prefer to share intimate thoughts (e.g., worries, joys) with?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("10. 你会对哪一性别的人产生「一见钟情」的感觉？", "10. Which gender do you experience 'love at first sight' toward?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("11. 你会被哪一性别的人的外貌/气质吸引（如觉得对方好看、有魅力）？", "11. Which gender's appearance/temperament attracts you (e.g., finding them good-looking, charming)?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("12. 你更想和哪一性别的人一起旅行/度过休闲时光？", "12. Which gender do you prefer to travel/spend leisure time with?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("13. 你会对哪一性别的人产生「吃醋」的情绪（对方和别人互动时）？", "13. Which gender do you experience jealousy toward when they interact with others?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("14. 你更愿意和哪一性别的人有肢体接触（如搭肩膀、摸头发）？", "14. Which gender do you prefer to have casual physical contact (e.g., patting the shoulder, touching the hair) with?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("15. 你会幻想和哪一性别的人结婚/组建家庭？", "15. Which gender do you fantasize about marrying/starting a family with?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("16. 你会对哪一性别的人产生「保护欲」（想照顾对方）？", "16. Which gender do you experience a desire to protect (wanting to take care of them) toward?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("17. 你更愿意和哪一性别的人一起看电影/吃饭（情侣式约会）？", "17. Which gender do you prefer to watch movies/eat with (couple-style dates)?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("18. 你会对哪一性别的人产生「被吸引」的目光追随（忍不住看对方）？", "18. Which gender do you experience attracted gaze fixation (unable to stop looking at them) toward?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("19. 你更想和哪一性别的人有亲密的语言交流（如情话、暧昧对话）？", "19. Which gender do you prefer to have intimate verbal communication (e.g., love words, ambiguous dialogue) with?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("20. 你会因哪一性别的人拒绝你而感到伤心/失落？", "20. Which gender's rejection makes you feel sad/disappointed?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("21. 你会对哪一性别的人产生「想要靠近」的冲动（如坐得近、主动搭讪）？", "21. Which gender do you experience an urge to approach (e.g., sit close, initiate a chat) toward?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("22. 你更愿意和哪一性别的人一起参加情侣式活动（如情人节约会）？", "22. Which gender do you prefer to participate in couple-style activities (e.g., Valentine's Day dates) with?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("23. 你会对哪一性别的人产生「心动不已」的生理反应（如心跳快、手抖）？", "23. Which gender do you experience intense physical reactions of attraction (e.g., rapid heartbeat, shaky hands) toward?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("24. 你更想和哪一性别的人分享成功/失败的情绪（第一时间想到的人）？", "24. Which gender do you first want to share emotions of success/failure with?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("25. 你会对哪一性别的人产生「专属感」（不想对方和别人太亲近）？", "25. Which gender do you experience a sense of exclusivity toward (not wanting them to be too close to others)?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("26. 你更愿意和哪一性别的人一起规划未来（如买房、养老）？", "26. Which gender do you prefer to plan the future (e.g., buying a house, retirement) with?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("27. 你会对哪一性别的人产生「性冲动」（生理层面的渴望）？", "27. Which gender do you experience sexual impulses (physical desire) toward?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("28. 你更想和哪一性别的人有深度的灵魂交流（三观、人生追求）？", "28. Which gender do you prefer to have in-depth spiritual communication (values, life pursuits) with?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("29. 你会因哪一性别的人夸奖你而感到开心/满足？", "29. Which gender's praise makes you feel happy/satisfied?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("30. 你自我认同的性取向更偏向哪一类别？", "30. Which category does your self-identified sexual orientation lean toward?"),
     (["仅异性恋", "偏异性恋", "轻微偏异性恋的双性恋", "无偏向双性恋", "轻微偏同性恋的双性恋", "偏同性恋", "仅同性恋"],
      ["Exclusively heterosexual", "Predominantly heterosexual", "Bisexual with a slight heterosexual lean", "Bisexual with no lean", "Bisexual with a slight homosexual lean", "Predominantly homosexual", "Exclusively homosexual"]),
     [0,1,2,3,4,5,6]),
    (("31. 你会主动向哪一性别的人表达欣赏/好感？", "31. Which gender do you take the initiative to express admiration/affection to?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("32. 你会对哪一性别的人的离开感到不舍/难过？", "32. Which gender's departure makes you feel reluctant/sad?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("33. 你更想和哪一性别的人有亲密的肢体接触（如依偎、拥抱）？", "33. Which gender do you prefer to have intimate physical contact (e.g., snuggling, hugging) with?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("34. 你会把哪一性别的人列入未来的人生规划中？", "34. Which gender do you include in your future life plans?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    (("35. 你会对哪一性别的人产生「灵魂契合」的感觉？", "35. Which gender do you experience a sense of 'spiritual connection' with?"),
     (["仅异性", "主要异性，偶尔同性", "多数异性，少数同性", "异性和同性差不多", "多数同性，少数异性", "主要同性，偶尔异性", "仅同性"],
      ["Exclusively opposite sex", "Predominantly opposite sex, occasionally same sex", "Mostly opposite sex, a few same sex", "Equal for opposite and same sex", "Mostly same sex, a few opposite sex", "Predominantly same sex, occasionally opposite sex", "Exclusively same sex"]),
     [0,1,2,3,4,5,6]),
    # 社会压力维度（36-40题）
    (("36. 你因自己的性取向倾向感受到的家庭压力程度？", "36. What is the level of family pressure you feel due to your sexual orientation tendencies?"),
     (["无压力", "极轻微", "轻微", "中等", "较显著", "显著", "极大"],
      ["No pressure", "Extremely slight", "Slight", "Medium", "Relatively significant", "Significant", "Extreme"]),
     [0,1,2,3,4,5,6]),
    (("37. 你因自己的性取向倾向感受到的朋友/社交圈压力程度？", "37. What is the level of pressure from friends/social circles you feel due to your sexual orientation tendencies?"),
     (["无压力", "极轻微", "轻微", "中等", "较显著", "显著", "极大"],
      ["No pressure", "Extremely slight", "Slight", "Medium", "Relatively significant", "Significant", "Extreme"]),
     [0,1,2,3,4,5,6]),
    (("38. 你因自己的性取向倾向感受到的社会/职场压力程度？", "38. What is the level of social/workplace pressure you feel due to your sexual orientation tendencies?"),
     (["无压力", "极轻微", "轻微", "中等", "较显著", "显著", "极大"],
      ["No pressure", "Extremely slight", "Slight", "Medium", "Relatively significant", "Significant", "Extreme"]),
     [0,1,2,3,4,5,6]),
    (("39. 你因隐藏性取向而产生的心理负担程度？", "39. What is the level of psychological burden you feel from hiding your sexual orientation?"),
     (["无负担", "极轻微", "轻微", "中等", "较显著", "显著", "极大"],
      ["No burden", "Extremely slight", "Slight", "Medium", "Relatively significant", "Significant", "Extreme"]),
     [0,1,2,3,4,5,6]),
    (("40. 你因性取向问题产生的自我怀疑/焦虑程度？", "40. What is the level of self-doubt/anxiety you feel due to sexual orientation issues?"),
     (["无焦虑", "极轻微", "轻微", "中等", "较显著", "显著", "极大"],
      ["No anxiety", "Extremely slight", "Slight", "Medium", "Relatively significant", "Significant", "Extreme"]),
     [0,1,2,3,4,5,6]),
    # 无性恋维度（41-50题）
    (("41. 你对任何性别的人产生性幻想的频率？", "41. How often do you have sexual fantasies about individuals of any gender?"),
     (["频繁", "较多", "偶尔", "极少", "几乎没有", "完全没有"],
      ["Frequent", "Quite often", "Occasional", "Very rare", "Almost never", "Never"]),
     [0,1,2,3,4,5]),
    (("42. 你对任何性别的人产生性冲动的频率？", "42. How often do you have sexual impulses toward individuals of any gender?"),
     (["频繁", "较多", "偶尔", "极少", "几乎没有", "完全没有"],
      ["Frequent", "Quite often", "Occasional", "Very rare", "Almost never", "Never"]),
     [0,1,2,3,4,5]),
    (("43. 你是否认为「性」是亲密关系的必要组成部分？", "43. Do you consider sex a necessary part of an intimate relationship?"),
     (["绝对必要", "很有必要", "有必要", "可有可无", "没必要", "完全没必要"],
      ["Absolutely necessary", "Very necessary", "Necessary", "Optional", "Unnecessary", "Completely unnecessary"]),
     [0,1,2,3,4,5]),
    (("44. 你主动追求性体验的意愿程度？", "44. What is your level of willingness to actively pursue sexual experiences?"),
     (["极强", "较强", "一般", "较弱", "极弱", "完全没有"],
      ["Extremely strong", "Strong", "Neutral", "Weak", "Extremely weak", "None at all"]),
     [0,1,2,3,4,5]),
    (("45. 你对他人的性暗示/性邀约的接受程度？", "45. What is your level of acceptance of sexual hints/advances from others?"),
     (["完全接受", "较接受", "一般", "较抗拒", "极抗拒", "完全抗拒"],
      ["Fully accept", "Relatively accept", "Neutral", "Relatively resist", "Extremely resist", "Fully resist"]),
     [0,1,2,3,4,5]),
    (("46. 你自我认同为「无性恋」的倾向程度？", "46. What is your level of tendency to self-identify as asexual?"),
     (["完全不认同", "较不认同", "一般", "较认同", "很认同", "完全认同"],
      ["Fully disagree", "Relatively disagree", "Neutral", "Relatively agree", "Strongly agree", "Fully agree"]),
     [0,1,2,3,4,5]),
    (("47. 你在亲密关系中，对性接触的期待程度？", "47. What is your level of expectation for sexual contact in an intimate relationship?"),
     (["极高", "较高", "一般", "较低", "极低", "完全没有"],
      ["Extremely high", "High", "Neutral", "Low", "Extremely low", "None at all"]),
     [0,1,2,3,4,5]),
    (("48. 你是否会因缺乏性体验而感到遗憾/不满？", "48. Do you feel regret/dissatisfaction due to a lack of sexual experience?"),
     (["极度遗憾", "较遗憾", "轻微遗憾", "无所谓", "不遗憾", "完全不在意"],
      ["Extremely regretful", "Relatively regretful", "Slightly regretful", "Indifferent", "Not regretful", "Completely unconcerned"]),
     [0,1,2,3,4,5]),
    (("49. 你对「无性恋是正常性取向」的认同程度？", "49. What is your level of agreement that asexuality is a normal sexual orientation?"),
     (["完全不认同", "较不认同", "一般", "较认同", "很认同", "完全认同"],
      ["Fully disagree", "Relatively disagree", "Neutral", "Relatively agree", "Strongly agree", "Fully agree"]),
     [0,1,2,3,4,5]),
    (("50. 你更倾向于建立无性生活的亲密关系吗？", "50. Do you prefer to establish an intimate relationship without sexual activity?"),
     (["完全不倾向", "较不倾向", "无所谓", "较倾向", "很倾向", "完全倾向"],
      ["Fully not inclined", "Relatively not inclined", "Indifferent", "Relatively inclined", "Strongly inclined", "Fully inclined"]),
     [0,1,2,3,4,5])
]

# 常量定义（大写，符合Python规范）
TOTAL_QUESTIONS = 50
CORE_END = 35
STRESS_END = 40
ASEX_START = 40

# ===================== 3. 核心业务逻辑（纯函数，无副作用，官方推荐） =====================
def get_question_content(lang: str, idx: int) -> tuple:
    """
    通用函数：获取指定语言、指定题目的文本和选项（提取重复逻辑，减少冗余）
    :param lang: 语言（cn/en）
    :param idx: 题目索引（0-49）
    :return: (题目文本, 选项列表)
    """
    q_text_cn, q_text_en = QUESTIONS_50[idx][0]
    q_opt_cn, q_opt_en = QUESTIONS_50[idx][1]
    q_text = q_text_cn if lang == "cn" else q_text_en
    q_opt = q_opt_cn if lang == "cn" else q_opt_en
    return q_text, q_opt

def calculate_results(answers: list, lang: str) -> str:
    """计分函数：纯函数，仅接收参数并返回结果（无副作用）"""
    # 拆分维度
    core_answers = answers[:CORE_END]
    stress_answers = answers[CORE_END:STRESS_END]
    asexual_answers = answers[ASEX_START:]

    # 计算核心性取向分数
    core_total = sum(core_answers)
    core_avg = round(core_total / CORE_END, 2)
    core_grade = round(core_avg) if core_avg <=6 else 6

    # 计算社会压力分数
    stress_total = sum(stress_answers)
    stress_avg = round(stress_total / (STRESS_END - CORE_END), 2)
    stress_grade = round(stress_avg) if stress_avg <=6 else 6

    # 计算无性恋分数
    asexual_total = sum(asexual_answers)
    asexual_avg = round(asexual_total / (TOTAL_QUESTIONS - ASEX_START), 2)
    asexual_grade = round(asexual_avg) if asexual_avg <=5 else 5

    # 判定最终金赛等级
    final_kinsey_grade = "X" if asexual_grade >= 4 else core_grade

    # 拼接结果文本
    ui = UI_TEXT[lang]
    kinsey = KINSEY_INTERPRET[lang]
    stress = STRESS_INTERPRET[lang]
    asex_inter = ui["asex_inter1"] if asexual_grade >=4 else ui["asex_inter2"].format(core_grade)

    result_text = f"""
### {ui["core_title"]}
- {ui["core_avg"]}{core_avg}
- {ui["core_grade"]}{final_kinsey_grade}
- {ui["core_inter"]}{kinsey[final_kinsey_grade]}

### {ui["stress_title"]}
- {ui["stress_avg"]}{stress_avg}
- {ui["stress_grade"]}{stress_grade}
- {ui["stress_inter"]}{stress[stress_grade]}

### {ui["asex_title"]}
- {ui["asex_avg"]}{asexual_avg}
- {ui["asex_grade"]}{asexual_grade}
- {ui["core_inter"]}{asex_inter}

### {ui["tips_title"]}
{ui["tip1"]}
{ui["tip2"]}
{ui["tip3"]}
{ui["tip4"]}
    """
    return result_text

# ===================== 4. 交互逻辑函数（遵循Gradio官方推荐：参数化、无硬编码） =====================
def init_quiz(lang: str) -> tuple:
    """初始化答题界面"""
    q_text, q_opt = get_question_content(lang, 0)
    ui = UI_TEXT[lang]
    return (
        gr.update(value=q_text),
        gr.update(choices=q_opt, label=ui["select_ans"], value=None),
        gr.update(value=ui["progress"].format(1, TOTAL_QUESTIONS)),
        gr.update(visible=False),
        gr.update(visible=True),
        gr.update(visible=False),
        0,
        [None]*TOTAL_QUESTIONS,
        ""
    )

def switch_language(current_lang: str, current_idx: int, answers_list: list, answer_scores: list) -> tuple:
    """切换语言（保留进度和答案）"""
    new_lang = "en" if current_lang == "cn" else "cn"
    ui = UI_TEXT[new_lang]
    q_text, q_opt = get_question_content(new_lang, current_idx)
    
    # 按钮显示控制
    show_prev = current_idx > 0
    show_next = current_idx < TOTAL_QUESTIONS - 1
    show_submit = current_idx == TOTAL_QUESTIONS - 1
    
    # 更新结果文本（如果已有答案）
    new_result = calculate_results(answer_scores, new_lang) if answer_scores else ""
    
    return (
        gr.update(value=new_lang),
        gr.update(value=ui["title"]),
        gr.update(value=ui["ethic"]),
        gr.update(value=ui["start_btn"]),
        gr.update(value=ui["lang_switch"]),
        gr.update(value=q_text),
        gr.update(choices=q_opt, label=ui["select_ans"], value=answers_list[current_idx]),
        gr.update(value=ui["progress"].format(current_idx+1, TOTAL_QUESTIONS)),
        gr.update(value=ui["prev_btn"], visible=show_prev),
        gr.update(value=ui["next_btn"], visible=show_next),
        gr.update(value=ui["submit_btn"], visible=show_submit),
        "",
        gr.update(value=new_result)
    )

def prev_question(current_idx: int, answers_list: list, current_choice: str, lang: str) -> tuple:
    """上一题逻辑（Gradio官方推荐：所有更新通过gr.update()参数传递）"""
    # 保存当前答案
    if current_choice is not None:
        answers_list[current_idx] = current_choice
    
    new_idx = current_idx - 1
    q_text, q_opt = get_question_content(lang, new_idx)
    ui = UI_TEXT[lang]
    
    # 按钮控制
    show_prev = new_idx > 0
    show_next = True
    show_submit = False
    
    # 核心修复：直接在gr.update()中传入value，而非后赋值
    return (
        gr.update(value=q_text),
        gr.update(choices=q_opt, label=ui["select_ans"], value=answers_list[new_idx]),
        gr.update(value=ui["progress"].format(new_idx+1, TOTAL_QUESTIONS)),
        gr.update(visible=show_prev),
        gr.update(visible=show_next),
        gr.update(visible=show_submit),
        new_idx,
        answers_list.copy(),
        ""
    )

def next_question(current_idx: int, answers_list: list, current_choice: str, lang: str) -> tuple:
    """下一题逻辑"""
    # 检查是否选择答案
    if current_choice is None:
        ui = UI_TEXT[lang]
        return (gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), current_idx, answers_list, ui["no_ans_tip"])
    
    # 保存答案
    answers_list[current_idx] = current_choice
    new_idx = current_idx + 1
    q_text, q_opt = get_question_content(lang, new_idx)
    ui = UI_TEXT[lang]
    
    # 按钮控制
    show_prev = True
    show_next = new_idx < TOTAL_QUESTIONS - 1
    show_submit = new_idx == TOTAL_QUESTIONS - 1
    
    return (
        gr.update(value=q_text),
        gr.update(choices=q_opt, label=ui["select_ans"], value=answers_list[new_idx]),
        gr.update(value=ui["progress"].format(new_idx+1, TOTAL_QUESTIONS)),
        gr.update(visible=show_prev),
        gr.update(visible=show_next),
        gr.update(visible=show_submit),
        new_idx,
        answers_list.copy(),
        ""
    )

def submit_quiz(answers_list: list, current_choice: str, current_idx: int, lang: str) -> tuple:
    """提交答案逻辑"""
    # 检查最后一题答案
    if current_choice is None:
        ui = UI_TEXT[lang]
        return (ui["no_ans_tip"], "", [])
    
    # 保存最后一题答案
    answers_list[current_idx] = current_choice
    
    # 检查是否有未答题
    if None in answers_list:
        empty_idx = answers_list.index(None) + 1
        ui = UI_TEXT[lang]
        return (ui["empty_tip"].format(empty_idx), "", [])
    
    # 转换答案为分数
    answer_scores = []
    for idx, ans in enumerate(answers_list):
        q_opt_cn, q_opt_en = QUESTIONS_50[idx][1]
        scores = QUESTIONS_50[idx][2]
        opt_list = q_opt_cn if lang == "cn" else q_opt_en
        ans_idx = opt_list.index(ans) if ans in opt_list else 0
        answer_scores.append(scores[ans_idx])
    
    # 生成结果
    result = calculate_results(answer_scores, lang)
    ui = UI_TEXT[lang]
    return (ui["submit_success_tip"], result, answer_scores)

# ===================== 5. 界面构建（Gradio官方推荐的Blocks模式） =====================
def create_gradio_interface() -> gr.Blocks:
    """创建Gradio界面（单一职责，符合官方推荐）"""
    # 自定义CSS（Gradio 4+/6+推荐写法）
    custom_css = """
    button {
        border: 2px solid #4CAF50 !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        margin: 4px !important;
    }
    button:hover {
        border-color: #2E7D32 !important;
        background-color: #f0f8f0 !important;
    }
    .gr-radio {
        border: 1px solid #ccc !important;
        border-radius: 6px !important;
        padding: 6px !important;
        margin: 2px !important;
    }
    .gr-textbox:empty {
        display: none !important;
    }
    .gr-textbox {
        color: #d32f2f !important;
        font-weight: bold !important;
        text-align: center !important;
        border: none !important;
        background: transparent !important;
    }
    """
    
    # Blocks构造函数传入CSS（官方推荐）
    with gr.Blocks(title=UI_TEXT["cn"]["title"], css=custom_css) as demo:
        # 状态管理（集中定义，命名清晰，官方推荐）
        current_lang = gr.State(value="cn")
        answer_scores = gr.State(value=[])
        current_idx = gr.State(value=0)
        answers_list = gr.State(value=[None]*TOTAL_QUESTIONS)

        # 顶部区域
        main_title = gr.Markdown(value=UI_TEXT["cn"]["title"])
        ethic_note = gr.Markdown(value=UI_TEXT["cn"]["ethic"])

        # 顶部按钮行
        with gr.Row():
            lang_switch_btn = gr.Button(value=UI_TEXT["cn"]["lang_switch"], variant="outline")
            start_btn = gr.Button(value=UI_TEXT["cn"]["start_btn"], variant="solid")

        # 提示信息
        tip_message = gr.Textbox(label="提示", value="", interactive=False, show_label=False, lines=1)

        # 答题Tab
        quiz_tab = gr.Tab(label="答题区", visible=False)
        with quiz_tab:
            progress_text = gr.Markdown(value=UI_TEXT["cn"]["progress"].format(1, TOTAL_QUESTIONS))
            gr.Markdown("---")
            question_text = gr.Markdown(value="")
            current_choice = gr.Radio(choices=[], label=UI_TEXT["cn"]["select_ans"], value=None)
            gr.Markdown("---")
            with gr.Row():
                prev_btn = gr.Button(value=UI_TEXT["cn"]["prev_btn"], variant="outline")
                next_btn = gr.Button(value=UI_TEXT["cn"]["next_btn"], variant="solid")
                submit_btn = gr.Button(value=UI_TEXT["cn"]["submit_btn"], variant="outline")

        # 结果Tab
        result_tab = gr.Tab(label="结果区", visible=False)
        with result_tab:
            result_output = gr.Markdown()

        # ===================== 事件绑定（Gradio官方推荐的链式调用） =====================
        # 语言切换
        lang_switch_btn.click(
            fn=switch_language,
            inputs=[current_lang, current_idx, answers_list, answer_scores],
            outputs=[
                current_lang, main_title, ethic_note, start_btn, lang_switch_btn,
                question_text, current_choice, progress_text,
                prev_btn, next_btn, submit_btn, tip_message, result_output
            ]
        )

        # 开始评估
        start_btn.click(
            fn=init_quiz,
            inputs=[current_lang],
            outputs=[question_text, current_choice, progress_text, prev_btn, next_btn, submit_btn, current_idx, answers_list, tip_message]
        ).then(
            fn=lambda: (gr.update(visible=True), gr.update(visible=False)),
            inputs=[],
            outputs=[quiz_tab, result_tab]
        )

        # 上一题
        prev_btn.click(
            fn=prev_question,
            inputs=[current_idx, answers_list, current_choice, current_lang],
            outputs=[question_text, current_choice, progress_text, prev_btn, next_btn, submit_btn, current_idx, answers_list, tip_message]
        )

        # 下一题
        next_btn.click(
            fn=next_question,
            inputs=[current_idx, answers_list, current_choice, current_lang],
            outputs=[question_text, current_choice, progress_text, prev_btn, next_btn, submit_btn, current_idx, answers_list, tip_message]
        )

        # 提交答案
        submit_btn.click(
            fn=submit_quiz,
            inputs=[answers_list, current_choice, current_idx, current_lang],
            outputs=[tip_message, result_output, answer_scores]
        ).then(
            fn=lambda: (gr.update(visible=False), gr.update(visible=True)),
            inputs=[],
            outputs=[quiz_tab, result_tab]
        )

    return demo

# ===================== 6. 主函数（单一入口，符合Python规范） =====================
if __name__ == "__main__":
    # 创建界面
    demo = create_gradio_interface()
    
    # 启动界面（仅调用一次，符合Gradio官方推荐）
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        inbrowser=True,
        show_error=False
    )
    
    # 控制台提示
    ui_cn = UI_TEXT["cn"]
    print("="*80)
    print(ui_cn["launch_tip1"])
    print(ui_cn["launch_tip2"])
    print(ui_cn["launch_tip3"])
    print("="*80)
    
    # 保持程序运行
    try:
        input("按Enter键退出程序...")
    except:
        pass
