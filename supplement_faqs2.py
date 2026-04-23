# -*- coding: utf-8 -*-
"""第二批补充 - 为配件机型补充更多 FAQ 到 20+"""
import re

INPUT = 'src/data/sampleData.js'
OUTPUT = 'src/data/sampleData.js'

MACHINE_NAMES = {
    'ae85': 'AE85 扩展模块', 'r8': 'R8 旋转卡盘', 'r6': 'R6 滚轴',
    'f80': 'F80 空气辅助', 'd5': 'D5 空气净化器', 'f4n': 'F4N 蜂窝工作板',
    'fb2': 'FB2 防护罩', 'h1': 'H1 高底座', 'hurricane': 'Hurricane K60',
    'c4pro': 'C4 Pro'
}

# 配件机型专属 FAQ（第二批）
EXTRA_ACCESSORY_FAQS = [
    # R8 旋转卡盘 (额外)
    ('R8 旋转卡盘夹持不稳怎么办', 'high', ['tag-11', 'tag-7'], 'R8,夹持不稳,打滑',
     '使用旋转卡盘时工件容易打滑或脱落。',
     '调整夹持方式和力度来稳固工件。',
     '### 1. 检查夹持方式\n1. 确认卡爪是否正确夹持工件\n2. 调整卡爪间距适配工件直径\n3. 检查工件表面是否光滑\n\n### 2. 增加摩擦力\n1. 在卡爪内侧贴橡胶垫\n2. 在工件表面缠绕薄纸或胶带\n3. 使用弹性材料辅助固定\n\n### 3. 减轻工件重量\n1. 空心工件比实心更容易夹持\n2. 不要夹持过重的物品\n3. 小心平衡工件重心'),
    ('R8 旋转卡盘与 A70 Pro 如何连接', 'medium', ['tag-11', 'tag-15'], 'R8,连接,A70',
     '不知道 R8 旋转卡盘如何安装到 A70 Pro 上。',
     '将旋转卡盘安装到 A70 Pro 的预留接口。',
     '### 1. 准备工作\n1. 关闭设备电源\n2. 准备安装螺丝和工具\n3. 找到设备两侧的旋转轴安装孔\n\n### 2. 安装步骤\n1. 将旋转卡盘底座对准安装孔\n2. 用螺丝固定底座\n3. 连接电机线缆到主板\n4. 检查线缆是否被卡住\n\n### 3. 测试\n1. 通电后手动测试旋转\n2. 检查旋转方向是否正确\n3. 夹持一个工件测试稳定性'),
    ('R8 旋转卡盘能雕刻多长的物品', 'low', ['tag-11', 'tag-13'], 'R8,长度,尺寸',
     '想知道旋转卡盘能处理多长的工件。',
     '了解旋转卡盘的尺寸限制。',
     '### 1. 支持长度\n1. 卡盘间距可调范围：50-400mm\n2. 最大工件长度取决于卡盘间距\n3. 建议工件长度不超过 500mm\n\n### 2. 注意事项\n1. 工件过长会影响稳定性\n2. 中心部分凸出的工件需要特别注意\n3. 先用短工件测试'),
    # R6 滚轴 (额外)
    ('R6 滚轴与 R8 卡盘有什么区别', 'low', ['tag-11', 'tag-13'], 'R6,R8,区别,对比',
     '不确定该选 R6 滚轴还是 R8 旋转卡盘。',
     '了解两者的区别和适用场景。',
     '### 1. R8 旋转卡盘\n1. 卡盘式夹持，适合圆柱体\n2. 支持直径 10-120mm\n3. 精度高，适合圆形物品\n4. 适用：杯子、瓶子、笔筒\n\n### 2. R6 旋转滚轴\n1. 滚轴式支撑，适合柔性材料\n2. 支持卷状材料\n3. 适合大面积连续雕刻\n4. 适用：布料、皮革、纸张卷\n\n### 3. 选择建议\n1. 雕刻杯子/瓶子选 R8\n2. 雕刻布料/皮革选 R6\n3. 两者不能同时使用'),
    ('R6 滚轴材料跑偏怎么办', 'medium', ['tag-11', 'tag-7'], 'R6,跑偏,偏移',
     '使用 R6 滚轴雕刻时材料跑偏。',
     '调整张力和对齐来防止跑偏。',
     '### 1. 检查滚轴张力\n1. 两端滚轴张力要一致\n2. 调整张紧装置\n3. 材料要绷紧不松弛\n\n### 2. 导向调整\n1. 确保材料进料方向与滚轴垂直\n2. 使用导板辅助定位\n3. 轻材质用胶带固定边缘\n\n### 3. 速度调整\n1. 降低送进速度\n2. 减少急转弯雕刻'),
    ('R6 滚轴雕刻布料参数设置', 'medium', ['tag-11', 'tag-13'], 'R6,布料,参数',
     '想知道 R6 滚轴雕刻布料的参数。',
     '根据布料类型设置参数。',
     '### 1. 棉布参数\n1. 功率：30%-50%\n2. 速度：400-600mm/min\n3. 效果：清晰的烧焦痕迹\n\n### 2. 皮革参数\n1. 功率：40%-60%\n2. 速度：300-500mm/min\n3. 仅天然皮革\n\n### 3. 纸张参数\n1. 功率：20%-40%\n2. 速度：500-800mm/min\n3. 注意不要过深切断'),
    # F80 空气辅助 (额外)
    ('F80 空气辅助自动开关不工作怎么办', 'medium', ['tag-9', 'tag-2'], 'F80,自动开关,故障',
     'F80 空气辅助的自动开关功能不工作。',
     '检查控制线和设置。',
     '### 1. 检查控制线\n1. 确认控制线正确连接到主板\n2. 检查控制线是否有断路\n3. 重新插拔连接端子\n\n### 2. 检查软件设置\n1. 在 GRBL 中确认 M8/M9 指令支持\n2. 检查 LightBurn 的 Air Assist 设置\n3. 确认自动开关已启用\n\n### 3. 手动模式\n1. 自动开关不工作时可手动控制\n2. 雕刻开始前手动开启\n3. 雕刻结束后手动关闭'),
    ('F80 空气辅助噪音太大怎么办', 'low', ['tag-9', 'tag-7'], 'F80,噪音,异常',
     'F80 空气辅助运行时噪音异常大。',
     '检查气泵和管路。',
     '### 1. 检查气泵\n1. 确认气泵安装牢固\n2. 检查是否有松动部件\n3. 气泵底部加橡胶垫减震\n\n### 2. 检查管路\n1. 检查气管是否有漏气\n2. 检查接头是否密封\n3. 气管折弯会产生噪音\n\n### 3. 调整气压\n1. 降低气压可减少噪音\n2. 不需要最大风量时调低'),
    ('F80 空气辅助可以用于哪些机型', 'low', ['tag-9', 'tag-13'], 'F80,适用机型,兼容',
     '想知道 F80 可以用在哪些机型上。',
     '了解 F80 的兼容机型列表。',
     '### 1. 完全兼容\n1. A5 Pro\n2. A6 Pro\n3. A10 Pro V2\n4. A12 Pro\n5. A20 Pro V2\n\n### 2. 需要适配\n1. A70 Pro（需要专用接口）\n2. A70 Max（需要专用接口）\n\n### 3. 不兼容\n1. Swift / Swift Mini\n2. Class 1 机型（内置辅助）\n3. C4 Pro（CNC 不是激光）'),
    # D5 空气净化器 (额外)
    ('D5 空气净化器滤芯多久换一次', 'low', ['tag-10', 'tag-14'], 'D5,滤芯,更换周期',
     '不知道 D5 空气净化器的滤芯更换频率。',
     '了解各层滤芯的更换周期。',
     '### 1. 滤芯更换周期\n1. 初效滤芯：每月清洁，3 个月更换\n2. HEPA 滤芯：6 个月更换\n3. 活性炭滤芯：6 个月更换\n4. UV 灯管：12 个月更换\n\n### 2. 判断滤芯状态\n1. 净化效果明显下降\n2. 出风量减小\n3. 有异味漏出\n4. 指示灯提示更换\n\n### 3. 更换步骤\n1. 关闭净化器电源\n2. 打开滤芯仓门\n3. 按顺序更换滤芯\n4. 关闭仓门重启测试'),
    ('D5 空气净化器可以搭配哪些设备使用', 'low', ['tag-10', 'tag-13'], 'D5,搭配,适用设备',
     '想知道 D5 空气净化器可以搭配哪些设备。',
     '了解 D5 的适用范围。',
     '### 1. 完全适配\n1. 所有 A 系列激光雕刻机\n2. A20 系列激光雕刻机\n3. A70 系列激光雕刻机\n4. Hurricane K60 CO2 切割机\n\n### 2. 安装方式\n1. 通过排烟管连接设备排烟口\n2. 净化器放置在设备旁边\n3. 确保管道密封不漏气\n\n### 3. 注意事项\n1. 管道长度不超过 2 米\n2. 避免管道折弯\n3. 定期清洁管道'),
    # F4N 蜂窝板 (额外)
    ('F4N 蜂窝板可以用在其他机型上吗', 'low', ['tag-7', 'tag-13'], 'F4N,兼容,其他机型',
     '想知道 F4N 蜂窝板能不能用在非 A 系列机型上。',
     '了解 F4N 的适用范围。',
     '### 1. 适配机型\n1. A5 Pro / A6 Pro\n2. A10 Pro V2 / A12 Pro\n3. A20 Pro V2\n\n### 2. 不适配机型\n1. A70 Pro（工作区域更大，需定制蜂窝板）\n2. Swift/Swift Mini（工作区域太小）\n3. Kraft/P1/Fusion（内置工作台）\n4. C4 Pro（非激光设备）\n\n### 3. 尺寸确认\n1. F4N 尺寸：440x420mm\n2. 确保不超出机型工作区域\n3. 可适当裁切适配'),
    # FB2 防护罩 (额外)
    ('FB2 防护罩影响雕刻精度吗', 'medium', ['tag-10', 'tag-6'], 'FB2,精度,影响',
     '使用 FB2 防护罩后感觉雕刻精度下降。',
     '检查防护罩安装和操作方式。',
     '### 1. 安装确认\n1. 确认防护罩稳固安装\n2. 不要在雕刻过程中触碰防护罩\n3. 确保防护罩没有接触激光头\n\n### 2. 操作方式\n1. 先放下防护罩再开始雕刻\n2. 雕刻过程中不要打开防护罩\n3. 打开防护罩查看时要暂停雕刻\n\n### 3. 其他因素\n1. 精度下降可能与其他因素有关\n2. 检查同步带张力\n3. 检查焦点是否正确'),
    ('FB2 防护罩排烟接口如何连接', 'medium', ['tag-10', 'tag-15'], 'FB2,排烟,连接',
     '不知道如何将排烟管连接到防护罩。',
     '将排烟管正确连接到防护罩的排烟接口。',
     '### 1. 连接步骤\n1. 找到防护罩侧面的排烟接口\n2. 将排烟管一端套在接口上\n3. 用管夹固定\n4. 另一端连接到空气净化器或排风扇\n\n### 2. 注意事项\n1. 管道保持通畅不折弯\n2. 接口处确保密封\n3. 定期清洁管道内的积灰'),
    # H1 高底座 (额外)
    ('H1 高底座可以叠加使用吗', 'low', ['tag-15', 'tag-7'], 'H1,叠加,高度',
     '想知道 H1 高底座能不能叠加两个增加高度。',
     '了解叠加使用的安全性和限制。',
     '### 1. 叠加可行性\n1. 理论上可以叠加 2 个（增高 120mm）\n2. 不建议叠加超过 2 个\n3. 叠加后稳定性会降低\n\n### 2. 注意事项\n1. 叠加后必须确保稳定性\n2. 激光头行程需要足够\n3. 不要在叠加状态下高速运行\n4. 加工高物品时使用旋转轴需特别注意'),
    # AE85 (额外)
    ('AE85 扩展后切割精度会降低吗', 'medium', ['tag-7', 'tag-15'], 'AE85,精度,降低',
     '安装 AE85 扩展模块后感觉切割精度下降。',
     '校准和调整来恢复精度。',
     '### 1. 重新校准\n1. 扩展后需要重新校准步进参数\n2. 在软件中微调 Y 轴 steps/mm\n3. 做一个 100mm 的测试切割\n4. 对比实际尺寸与设计尺寸\n\n### 2. 检查导轨对齐\n1. 扩展导轨与原导轨必须完美对齐\n2. 用直尺检查导轨直线度\n3. 调整连接板使导轨平齐\n\n### 3. 同步带检查\n1. 确保同步带全程张力一致\n2. 检查扩展区域的同步带导轮'),
    # Hurricane (额外)
    ('Hurricane K60 红点定位如何校准', 'medium', ['tag-6', 'tag-5'], 'Hurricane,红点,校准',
     '红点定位与实际切割位置有偏差。',
     '调整红点定位器的位置使其与激光对齐。',
     '### 1. 校准步骤\n1. 在材料上贴一层胶带\n2. 用低功率打一个点\n3. 观察红点位置与激光点的偏差\n4. 调整红点定位器的调节螺丝\n5. 反复测试直到红点与激光点重合\n\n### 2. 注意事项\n1. 焦点变化时红点偏差可能不同\n2. 建议在不同焦距下分别校准\n3. 定期检查校准状态'),
    ('Hurricane K60 切割不同材料的参数', 'medium', ['tag-13', 'tag-14'], 'Hurricane,参数,材料',
     '不知道 K60 切割不同材料的参数设置。',
     '根据材料类型设置正确的切割参数。',
     '### 1. 透明亚克力\n1. 功率：80%-100%\n2. 速度：80-150mm/min\n3. 必须水冷和空气辅助\n\n### 2. 椴木板\n1. 3mm 板：功率 80%，速度 200mm/min\n2. 6mm 板：功率 100%，速度 100mm/min\n3. 10mm 板：需多次切割\n\n### 3. 密度板\n1. 3mm 板：功率 70%，速度 300mm/min\n2. 注意密度板胶水含量高\n\n### 4. 皮革\n1. 天然皮革：功率 60%，速度 400mm/min\n2. 不要加工人造革'),
    ('Hurricane K60 能雕刻玻璃吗', 'low', ['tag-13', 'tag-14'], 'Hurricane,玻璃,雕刻',
     '想知道 K60 能不能雕刻玻璃。',
     '了解 CO2 激光雕刻玻璃的方法。',
     '### 1. 可以但效果有限\n1. CO2 激光可以在玻璃上产生磨砂效果\n2. 不能做精细雕刻\n3. 效果为白色磨砂纹路\n\n### 2. 操作方法\n1. 在玻璃表面涂湿报纸或湿纸巾\n2. 使用低功率（30%-50%）\n3. 速度较慢（200-400mm/min）\n4. 切割后清洗干净\n\n### 3. 注意事项\n1. 玻璃容易受热炸裂\n2. 不要使用高功率\n3. 建议先用碎片测试'),
    # C4 Pro (额外)
    ('C4 Pro 如何安装和固定材料', 'medium', ['tag-7', 'tag-15'], 'C4 Pro,固定,安装材料',
     '不知道如何将材料固定在 C4 Pro 工作台上。',
     '使用正确的方法固定材料。',
     '### 1. 常用固定方法\n1. 螺丝固定：使用 T 型槽螺母和压板\n2. 双面胶：适合薄板材\n3. 真空吸盘：适合平整表面\n4. 台钳：适合小件物品\n\n### 2. 步骤\n1. 将材料放在工作台上\n2. 确定加工区域\n3. 在非加工区域设置固定点\n4. 固定后手动检查是否牢固\n\n### 3. 注意事项\n1. 固定点不要干涉加工路径\n2. 材料必须完全贴合工作台\n3. 翘曲的材料需要先压平'),
    ('C4 Pro 如何更换主轴', 'high', ['tag-15', 'tag-7'], 'C4 Pro,更换,主轴',
     'C4 Pro 主轴需要更换或维修。',
     '安全拆卸并安装新主轴。',
     '### 1. 拆卸旧主轴\n1. 关闭电源\n2. 拆下主轴固定螺丝\n3. 断开电源线缆\n4. 拔出主轴\n\n### 2. 安装新主轴\n1. 将新主轴插入安装位\n2. 对齐螺丝孔\n3. 连接电源线缆\n4. 拧紧固定螺丝\n\n### 3. 测试\n1. 通电后测试主轴转动\n2. 检查是否异响\n3. 在废料上试铣'),
    ('C4 Pro Z 轴高度如何校准', 'medium', ['tag-6', 'tag-7'], 'C4 Pro,Z轴,高度,校准',
     'C4 Pro Z 轴下刀深度不准确。',
     '校准 Z 轴高度和零点。',
     '### 1. 设置 Z 轴零点\n1. 将 Z 轴降到刀尖接触材料表面\n2. 在软件中设置该位置为 Z=0\n3. 使用自动探针功能（如有）\n\n### 2. 校准步骤\n1. 移动 Z 轴到材料表面\n2. 用一张薄纸检测接触\n3. 设置 Z=0\n4. 将 Z 轴升高 10mm\n5. 测量实际升高距离\n6. 如有偏差调整 Z 轴 steps/mm'),
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
    # Read the file
    with open(INPUT, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count current FAQs
    current = {}
    for m in re.finditer(r"f\('m-([^']+)'", content):
        mid = m.group(1)
        current[mid] = current.get(mid, 0) + 1
    
    print("Current counts:")
    for mid, count in sorted(current.items(), key=lambda x: -x[1]):
        needed = max(0, 22 - count)
        print(f"  {mid}: {count} (need {needed} more)")
    
    # Get existing titles
    existing_titles = set()
    for m in re.finditer(r"f\('m-[^']+',\s*'([^']+)'", content):
        existing_titles.add(m.group(1))
    
    new_entries = []
    for entry in EXTRA_ACCESSORY_FAQS:
        title, priority, tags, keywords, summary, sol_title, steps = entry
        # Find which machine this is for from the title prefix
        for mid, name in MACHINE_NAMES.items():
            if title.startswith(name):
                if current.get(mid, 0) < 22 and title not in existing_titles:
                    entry_text = generate_entry(mid, name, title, priority, tags, keywords, summary, sol_title, steps)
                    new_entries.append((mid, entry_text))
                    current[mid] = current.get(mid, 0) + 1
                    existing_titles.add(title)
                    print(f"  Added for {mid}: {title}")
                break
    
    if not new_entries:
        print("\nNo new entries to add!")
        return
    
    # Build insert text
    insert_text = '\n'
    for mid, entry_text in new_entries:
        name = MACHINE_NAMES.get(mid, mid)
        insert_text += f'\n    // ================ {name} FAQ (extra) ================\n'
        insert_text += entry_text + '\n'
    
    # Find insertion point
    idx = content.rfind('  ]\n}')
    if idx < 0:
        # Try alternate patterns
        for p in ['  ]\r\n}', ']\n}', ']\r\n}']:
            idx = content.rfind(p)
            if idx >= 0:
                break
    if idx < 0:
        idx = content.rfind(']')
    
    new_content = content[:idx] + insert_text + content[idx:]
    
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"\nDone! Added {len(new_entries)} entries. New size: {len(new_content)}")


if __name__ == '__main__':
    main()
