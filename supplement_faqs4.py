# -*- coding: utf-8 -*-
"""第四批补充 - 让剩余小配件机型达到 20+"""
import re

INPUT = 'src/data/sampleData.js'
OUTPUT = 'src/data/sampleData.js'

MACHINE_NAMES = {
    'ae85': 'AE85 扩展模块', 'r8': 'R8 旋转卡盘', 'r6': 'R6 滚轴',
    'f80': 'F80 空气辅助', 'd5': 'D5 空气净化器', 'f4n': 'F4N 蜂窝工作板',
    'fb2': 'FB2 防护罩', 'h1': 'H1 高底座'
}

BATCH4 = [
    # R8 extra
    ('R8 旋转卡盘步进电机参数如何设置', 'medium', ['tag-11', 'tag-5'], 'R8,步进电机,参数设置',
     '安装 R8 后需要在软件中设置旋转轴参数。',
     '在 LightBurn 中配置旋转轴步进参数。',
     '### 1. 设置步骤\n1. 打开 LightBurn\n2. 点击 Edit > Machine Settings\n3. 切换到 Rotary 标签页\n4. 勾选 Enable Rotary\n\n### 2. 关键参数\n1. Rotation Axis: 选择 Y-Axis 或 A-Axis\n2. Steps per Rotation: 根据电机和减速比计算\n3. 通常默认值 200 步/转可先尝试\n\n### 3. 校准方法\n1. 夹持一个已知周长的圆柱体\n2. 雕刻一条与轴线平行的线\n3. 测量实际线长与设计线长的比例\n4. 按比例调整 Steps per Rotation'),
    ('R8 旋转卡盘保养方法', 'low', ['tag-14', 'tag-11'], 'R8,保养,维护',
     '想了解 R8 旋转卡盘的日常保养方法。',
     '定期保养延长旋转卡盘使用寿命。',
     '### 1. 日常保养\n1. 使用后清洁卡爪上的碎屑\n2. 检查卡爪是否有磨损\n3. 用软布擦拭干净\n\n### 2. 定期检查\n1. 每月检查减速齿轮润滑\n2. 检查电机线缆是否完好\n3. 检查固定螺丝是否松动\n\n### 3. 存放注意\n1. 长期不用时断电存放\n2. 用防尘袋包装\n3. 存放在干燥环境'),
    ('R8 旋转卡盘能雕刻多粗的物品', 'low', ['tag-11', 'tag-13'], 'R8,直径,粗细',
     '想知道 R8 能夹持多粗的物品。',
     '了解 R8 的直径支持范围。',
     '### 1. 支持范围\n1. 最小直径：10mm\n2. 最大直径：120mm\n3. 推荐范围：30-90mm\n\n### 2. 注意事项\n1. 直径过大时工件可能不平衡\n2. 非常细的物品可能夹不紧\n3. 不规则形状需要定制夹具'),
    ('R8 旋转卡盘的减速比是多少', 'low', ['tag-11', 'tag-14'], 'R8,减速比,参数',
     '需要了解 R8 旋转卡盘的减速比来设置软件参数。',
     'R8 的减速比参数。',
     '### 1. 技术参数\n1. 电机类型：42 步进电机\n2. 减速比：1:6.5（约）\n3. 步距角：1.8 度\n4. 每转步数：约 1300 步（含减速）\n\n### 2. 软件设置\n1. LightBurn: Steps per Rotation 约 1300\n2. 实际值需根据具体批次微调\n3. 建议用校准方法精确设定'),
    # R6 extra
    ('R6 滚轴如何安装到 Kraft 上', 'medium', ['tag-11', 'tag-15'], 'R6,安装,Kraft',
     '想把 R6 滚轴安装到 Kraft 机型上。',
     '将 R6 滚轴正确安装到 Kraft。',
     '### 1. 安装步骤\n1. 关闭 Kraft 电源\n2. 将 R6 滚轴放置在工作区域内\n3. 连接电机线缆到 Kraft 主板\n4. 固定滚轴底座\n\n### 2. 软件配置\n1. 在 AtomStack Studio 中启用旋转模式\n2. 设置材料类型为卷状\n3. 设置材料宽度\n\n### 3. 测试\n1. 放入一段布料测试转动\n2. 检查是否有跑偏\n3. 做一个简单的雕刻测试'),
    ('R6 滚轴的最大速度是多少', 'low', ['tag-11', 'tag-14'], 'R6,速度,转速',
     '想知道 R6 滚轴的最大转速。',
     '了解 R6 的速度限制。',
     '### 1. 技术参数\n1. 最大转速：约 3 转/分钟\n2. 推荐转速：1-2 转/分钟\n3. 实际速度取决于材料厚度\n\n### 2. 速度建议\n1. 薄材料可以用较高转速\n2. 厚材料需要较低转速\n3. 根据雕刻效果调整'),
    ('R6 滚轴能雕刻多宽的材料', 'low', ['tag-11', 'tag-13'], 'R6,宽度,材料尺寸',
     '想知道 R6 滚轴能处理多宽的卷状材料。',
     '了解 R6 的宽度限制。',
     '### 1. 支持宽度\n1. 取决于机型的工作区域宽度\n2. R6 滚轴本身长度约 320mm\n3. 可处理标准宽度的布料卷\n\n### 2. 注意事项\n1. 材料宽度不要超出滚轴长度\n2. 超出部分需要预先裁切'),
    ('R6 滚轴雕刻皮革效果如何', 'medium', ['tag-11', 'tag-13'], 'R6,皮革,效果',
     '想知道用 R6 滚轴雕刻卷状皮革的效果。',
     '了解滚轴雕刻皮革的效果和参数。',
     '### 1. 效果说明\n1. 适合大面积连续图案\n2. 边缘清晰度不如平面雕刻\n3. 适合装饰性图案和花纹\n\n### 2. 参数建议\n1. 功率：40%-60%\n2. 速度：300-500mm/min\n3. 仅天然皮革\n\n### 3. 注意事项\n1. 皮革卷要绷紧\n2. 先用小面积测试\n3. 一次雕刻不宜过长'),
    # F80 extra
    ('F80 空气辅助气管如何选择', 'low', ['tag-9', 'tag-14'], 'F80,气管,选择',
     '需要为 F80 空气辅助购买合适的气管。',
     '了解气管规格和选择建议。',
     '### 1. 气管规格\n1. 内径：6mm 或 8mm\n2. 材质：PU 管（推荐）\n3. 长度：根据设备到气源距离\n4. 耐压：0.6MPa 以上\n\n### 2. 接头规格\n1. 快插接头 6mm 或 8mm\n2. 需要的接头数量：2-3 个\n3. 建议购买带密封圈接头\n\n### 3. 注意事项\n1. 气管不要过长（不超过 3 米）\n2. 避免折弯和挤压\n3. 定期检查是否有老化开裂'),
    ('F80 空气辅助需要多大功率的气泵', 'low', ['tag-9', 'tag-14'], 'F80,气泵,功率',
     '不知道配多大功率的空气压缩机。',
     '了解气泵功率要求。',
     '### 1. 最低要求\n1. 气流量：30L/min 以上\n2. 气压：0.1-0.3MPa\n3. 推荐使用静音气泵\n\n### 2. 推荐配置\n1. 小型桌面气泵：30-60L/min\n2. 中型气泵：60-100L/min（最佳）\n3. 大型工业压缩机：适合工厂使用\n\n### 3. 注意事项\n1. 油泵需要加装油水分离器\n2. 无油泵更适合激光雕刻\n3. 不要使用过大气压'),
    ('F80 空气辅助如何清洁维护', 'low', ['tag-9', 'tag-14'], 'F80,清洁,维护',
     'F80 空气辅助用久了需要清洁维护。',
     '定期清洁保持空气辅助性能。',
     '### 1. 清洁喷嘴\n1. 使用细针清理喷嘴堵塞\n2. 用压缩空气反吹\n3. 不要用金属针（会损伤喷嘴）\n\n### 2. 清洁管路\n1. 检查气管内是否有积水和油污\n2. 排放气管中的积水\n3. 更换老化气管\n\n### 3. 定期检查\n1. 检查气泵工作状态\n2. 检查气压是否正常\n3. 检查接口密封性'),
    # D5 extra
    ('D5 空气净化器的 CADR 值是多少', 'low', ['tag-10', 'tag-14'], 'D5,CADR,净化能力',
     '想知道 D5 空气净化器的净化能力参数。',
     '了解 D5 的 CADR 值和适用面积。',
     '### 1. 核心参数\n1. CADR：350 立方米/小时\n2. 适用面积：约 25-40 平方米\n3. 噪音：小于 55dB\n\n### 2. 适配场景\n1. 小型激光雕刻机：完全足够\n2. 中型激光雕刻机：配合排烟管使用\n3. 大型设备（A70）：建议两台并联\n\n### 3. 性能说明\n1. CADR 350 属于中等偏上水平\n2. 四层过滤系统效率高\n3. UV 杀菌功能可减少异味'),
    ('D5 空气净化器耗电量大吗', 'low', ['tag-10', 'tag-14'], 'D5,耗电,功率',
     '想知道 D5 空气净化器的耗电情况。',
     '了解 D5 的功率和能耗。',
     '### 1. 功率参数\n1. 最大功率：约 60W\n2. 低速模式：约 20W\n3. 待机功率：小于 5W\n\n### 2. 能耗估算\n1. 连续使用 8 小时约 0.5 度电\n2. 每月约 15 度电\n3. 电费影响很小\n\n### 3. 节能建议\n1. 不雕刻时关机\n2. 使用自动模式\n3. 定期清洁滤芯保持效率'),
    ('D5 空气净化器可以连接多个排烟口吗', 'medium', ['tag-10', 'tag-15'], 'D5,多排烟口,连接',
     '想用一个 D5 连接多台设备的排烟。',
     '了解 D5 的多设备连接能力。',
     '### 1. 接口规格\n1. 单个进烟口\n2. 可通过分路器连接多个排烟口\n3. 不建议超过 3 个排烟源\n\n### 2. 注意事项\n1. 分路后每个支路的抽力会减小\n2. 管道越长抽力越小\n3. 确保总排烟量不超过 CADR\n\n### 3. 推荐方案\n1. 单台设备配一个 D5 效果最好\n2. 多台设备建议使用排风系统\n3. 大空间可加排风扇辅助'),
    ('D5 空气净化器搬运注意事项', 'low', ['tag-10', 'tag-14'], 'D5,搬运,注意',
     '需要搬运 D5 空气净化器。',
     '安全搬运 D5 的注意事项。',
     '### 1. 搬运前\n1. 关闭电源并拔掉插头\n2. 取出滤芯单独包装（避免震动损坏）\n3. 清洁外部\n\n### 2. 搬运中\n1. 保持直立搬运\n2. 不要倒置或剧烈摇晃\n3. 使用原包装保护\n\n### 3. 安装后\n1. 重新安装滤芯\n2. 检查管道连接\n3. 通电测试'),
    # F4N extra
    ('F4N 蜂窝板与 A10 Pro V2 的适配问题', 'medium', ['tag-7', 'tag-15'], 'F4N,A10,适配',
     'F4N 蜂窝板放在 A10 Pro V2 上似乎不太贴合。',
     '检查适配性问题并调整。',
     '### 1. 尺寸确认\n1. F4N 尺寸：440x420mm\n2. A10 Pro V2 工作区域：410x400mm\n3. F4N 略大于工作区域，这是正常的\n\n### 2. 安装方法\n1. 将蜂窝板居中放置\n2. 四周可能略微超出\n3. 确保不影响激光头运动\n\n### 3. 焦点调整\n1. 蜂窝板表面高度约 15-20mm\n2. 使用自动对焦功能适配\n3. 手动对焦时注意测量高度'),
    ('F4N 蜂窝板可以自制吗', 'low', ['tag-14', 'tag-7'], 'F4N,自制,DIY',
     '想自己做一个蜂窝板替代 F4N。',
     '了解自制蜂窝板的可行性。',
     '### 1. 可行性\n1. 自制蜂窝板可行但效果不如原装\n2. 需要焊接或铆接技术\n3. 材料成本可能不比购买便宜\n\n### 2. 所需材料\n1. 钢制蜂窝板坯料\n2. 外框材料\n3. 焊接或铆接工具\n\n### 3. 建议\n1. 建议直接购买原装 F4N\n2. 原装精度和质量更好\n3. 自制可能影响切割质量'),
    # FB2 extra
    ('FB2 防护罩可以配合 D5 使用吗', 'medium', ['tag-10', 'tag-15'], 'FB2,D5,配合',
     '想同时使用 FB2 防护罩和 D5 空气净化器。',
     '将 FB2 的排烟接口连接到 D5。',
     '### 1. 连接方式\n1. FB2 侧面有排烟接口\n2. 用排烟管连接 FB2 到 D5\n3. 确保接口密封\n\n### 2. 效果\n1. 烟尘在防护罩内被有效收集\n2. 通过管道输送到 D5 过滤\n3. 实现闭环排烟系统\n\n### 3. 建议\n1. 这是推荐的组合方案\n2. 管道长度不超过 2 米\n3. 定期清洁管道'),
    # H1 extra
    ('H1 高底座安装后设备会晃吗', 'medium', ['tag-15', 'tag-7'], 'H1,晃动,稳定性',
     '担心安装 H1 高底座后设备不稳定。',
     '确保安装稳固。',
     '### 1. 安装检查\n1. 四个高底座都正确安装\n2. 每个螺丝都拧紧\n3. 设备放置在水平桌面上\n\n### 2. 稳定性测试\n1. 用手轻轻推动设备测试\n2. 不应有明显晃动\n3. 如有晃动检查螺丝\n\n### 3. 注意事项\n1. 不要在过高底座上高速运行\n2. 加工重心高的物品时要注意\n3. 必要时可在底座下加防滑垫'),
    # AE85 extra
    ('AE85 扩展模块包装内有什么', 'low', ['tag-15', 'tag-14'], 'AE85,包装,配件清单',
     '刚收到 AE85 扩展模块，需要确认配件。',
     '检查 AE85 的完整配件清单。',
     '### 1. 标准配件\n1. 加长导轨 x1\n2. 导轨连接板 x2\n3. 加长同步带 x1\n4. 同步带导轮支架 x2\n5. M5/M6 安装螺丝若干\n6. 内六角扳手 x1\n\n### 2. 检查方法\n1. 对照说明书清点\n2. 检查导轨是否有划痕\n3. 检查同步带是否完好\n\n### 3. 缺少配件\n1. 拍照记录\n2. 联系客服补发\n3. 保留包装箱'),
]


def generate_entry(mid, machine_name, title, priority, tags, keywords, summary, solution_title, steps):
    full_id = f'm-{mid}'
    content = f'## {solution_title}\n\n{steps}'
    content = content.replace('`', "'").replace('$', '')
    lines = [f"    f('{full_id}', '{title}', '{priority}', {tags},"]
    lines.append(f"      '{keywords}',")
    lines.append(f"      '{summary}',")
    lines.append(f"      '{solution_title}',")
    lines.append(f"      `{content}`)")
    return '\n'.join(lines)


def main():
    with open(INPUT, 'r', encoding='utf-8') as f:
        content = f.read()

    current = {}
    for m in re.finditer(r"f\('m-([^']+)'", content):
        mid = m.group(1)
        current[mid] = current.get(mid, 0) + 1

    existing_titles = set()
    for m in re.finditer(r"f\('m-[^']+',\s*'([^']+)'", content):
        existing_titles.add(m.group(1))

    new_entries = []
    for entry in BATCH4:
        title, priority, tags, keywords, summary, sol_title, steps = entry
        for mid, name in MACHINE_NAMES.items():
            if title.startswith(name):
                if current.get(mid, 0) < 22 and title not in existing_titles:
                    entry_text = generate_entry(mid, name, title, priority, tags, keywords, summary, sol_title, steps)
                    new_entries.append((mid, entry_text))
                    current[mid] = current.get(mid, 0) + 1
                    existing_titles.add(title)
                    print(f"  Added for {mid}: {title} ({current[mid]})")
                break

    if not new_entries:
        print("No new entries to add!")
        return

    insert_text = '\n'
    for mid, entry_text in new_entries:
        name = MACHINE_NAMES.get(mid, mid)
        insert_text += f'\n    // ================ {name} FAQ (batch4) ================\n'
        insert_text += entry_text + '\n'

    idx = content.rfind('  ]\n}')
    if idx < 0:
        for p in ['  ]\r\n}', ']\n}', ']\r\n}']:
            idx = content.rfind(p)
            if idx >= 0:
                break
    if idx < 0:
        idx = content.rfind(']')

    new_content = content[:idx] + insert_text + content[idx:]

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\nDone! Added {len(new_entries)} entries.")


if __name__ == '__main__':
    main()
