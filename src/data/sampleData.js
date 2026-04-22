// AtomStack FAQ 管理系统 - 示例数据
// 包含全线产品机型和常见 FAQ

export function initSampleData(machineStore, faqStore) {
  const now = new Date().toISOString()

  // ===== 机型数据 =====
  const machines = [
    // A系列半导体雕刻机
    { id: 'm-a5pro', name: 'A5 Pro', categoryId: 'cat-1', model: 'A5 PRO V2', description: '入门级激光雕刻机，5W 激光功率，410×400mm 工作区域，适合初学者', specs: { '激光功率': '5W', '工作区域': '410×400mm', '雕刻精度': '0.06mm', '最大速度': '1000mm/min' } },
    { id: 'm-a6pro', name: 'A6 Pro', categoryId: 'cat-1', model: 'A6 Pro', description: '便携式折叠激光雕刻机，5.5W 激光功率，260×250mm 工作区域', specs: { '激光功率': '5.5W', '工作区域': '260×250mm', '雕刻精度': '0.06mm', '最大速度': '1000mm/min', '特色': '可折叠便携' } },
    { id: 'm-a10prov2', name: 'A10 Pro V2', categoryId: 'cat-1', model: 'A10 Pro V2', description: '中端激光雕刻机，10W 双激光耦合技术，410×400mm 工作区域', specs: { '激光功率': '10W', '工作区域': '410×400mm', '雕刻精度': '0.06mm', '最大速度': '10000mm/min', '特色': '双激光耦合' } },
    { id: 'm-a12pro', name: 'A12 Pro', categoryId: 'cat-1', model: 'A12 Pro', description: '12W 激光雕刻机，线性导轨 X 轴，410×400mm 工作区域', specs: { '激光功率': '12W', '工作区域': '410×400mm', '雕刻精度': '0.01mm', '最大速度': '10000mm/min', '特色': '线性导轨' } },
    { id: 'm-a20prov2', name: 'A20 Pro V2', categoryId: 'cat-1', model: 'A20 Pro V2', description: '高功率激光雕刻切割机，20W 光学功率，400×415mm 工作区域，支持空气辅助', specs: { '激光功率': '20W', '工作区域': '400×415mm', '雕刻精度': '0.01mm', '最大速度': '10000mm/min', '特色': '空气辅助、自动对焦' } },

    // 大功率雕刻机
    { id: 'm-a70pro', name: 'A70 Pro', categoryId: 'cat-2', model: 'A70 Pro', description: '工业级大功率激光雕刻切割机，35W 雕刻/70W 切割双模式，850×700mm 大工作区域', specs: { '激光功率': '35W雕刻/70W切割', '工作区域': '850×700mm', '雕刻精度': '0.01mm', '最大速度': '3000mm/min', '特色': '自动对焦、火焰报警、智能冷却' } },
    { id: 'm-a70max', name: 'A70 Max', categoryId: 'cat-2', model: 'A70 Max', description: '超大工作区域激光雕刻机，880×880mm 工作区域', specs: { '激光功率': '35W', '工作区域': '880×880mm', '雕刻精度': '0.01mm', '特色': '超大工作面积' } },
    { id: 'm-ae85', name: 'AE85', categoryId: 'cat-2', model: 'AE85', description: '扩展工作区域模块，可将工作面积扩展至 850×800mm', specs: { '工作区域': '850×800mm', '适用机型': 'A70 Pro 系列', '特色': '面积扩展' } },

    // 创新系列
    { id: 'm-kraft', name: 'Kraft', categoryId: 'cat-3', model: 'Kraft', description: '封闭式蓝红外双光源激光雕刻机，Class 1 安全认证，适合室内使用', specs: { '激光光源': '蓝光+红外双光源', '安全等级': 'Class 1', '特色': '封闭式、双光源' } },
    { id: 'm-p1', name: 'P1', categoryId: 'cat-3', model: 'P1', description: '全球首款一类安全双光智能激光雕刻机，Class 1 安全认证', specs: { '安全等级': 'Class 1', '特色': '一类安全认证、双光' } },
    { id: 'm-fusion', name: 'Fusion', categoryId: 'cat-3', model: 'Fusion', description: '多功能双光源激光雕刻机，20W 半导体激光，600mm/s 高速', specs: { '激光功率': '20W', '精度': '0.05mm', '速度': '600mm/s', '安全等级': 'Class 1' } },
    { id: 'm-atelier', name: 'Atelier', categoryId: 'cat-3', model: 'Atelier', description: '一类激光安全高速蓝光打标机，振镜激光技术', specs: { '激光类型': '振镜激光', '安全等级': 'Class 1', '特色': '防蓝光视窗' } },
    { id: 'm-swift', name: 'Swift', categoryId: 'cat-3', model: 'Swift', description: '智能 DIY 半导体激光雕刻机，便携设计', specs: { '特色': '便携、DIY' } },
    { id: 'm-swiftmini', name: 'Swift Mini', categoryId: 'cat-3', model: 'Swift Mini', description: '入门级袖珍激光雕刻机，超小巧设计', specs: { '特色': '袖珍、入门级' } },

    // CNC
    { id: 'm-c4pro', name: 'C4 Pro', categoryId: 'cat-4', model: 'C4 Pro', description: '四轴 CNC 雕刻机，支持木材、金属、亚克力等多种材料雕刻', specs: { '轴数': '4轴', '适用材料': '木材、金属、亚克力等', '特色': '四轴联动' } },

    // CO₂
    { id: 'm-hurricane', name: 'Hurricane (K60)', categoryId: 'cat-5', model: 'Hurricane K60', description: '桌面级高功率 CO₂ 激光切割机，支持多种材料深度切割', specs: { '激光类型': 'CO₂', '适用材料': '木材、亚克力、皮革等', '特色': '高功率切割' } },

    // 配件
    { id: 'm-r8', name: 'R8 旋转卡盘', categoryId: 'cat-6', model: 'R8', description: '旋转卡盘模块，用于圆柱形物体雕刻', specs: { '类型': '旋转卡盘', '最大直径': '80mm' } },
    { id: 'm-r6', name: 'R6 滚轴', categoryId: 'cat-6', model: 'R6', description: '滚轴旋转模块，适合大直径圆柱体雕刻', specs: { '类型': '滚轴旋转', '最大直径': '150mm' } },
    { id: 'm-f80', name: 'F80 双泵空气辅助', categoryId: 'cat-6', model: 'F80', description: '双泵空气辅助系统，10-80L/min 可调风量', specs: { '风量': '10-80L/min', '特色': '双泵、自动切换' } },
    { id: 'm-d5', name: 'D5 空气净化器', categoryId: 'cat-6', model: 'D5', description: '桌面型空气净化器，过滤激光切割产生的烟尘', specs: { '类型': '桌面净化', '特色': '多层过滤' } },
  ]

  machines.forEach(m => machineStore.addMachine(m, true))
  save('faq-machines', machineStore.machines)

  // ===== FAQ 数据 =====
  const faqs = [
    // A10 Pro V2 FAQ
    {
      id: 'faq-1', machineId: 'm-a10prov2', title: 'A10 Pro V2 开机后激光头不亮，不出光怎么办？',
      priority: 'critical', status: 'published',
      tags: ['tag-1', 'tag-8'],
      keywords: '激光不亮,不出光,开机无反应,烧毁,不工作',
      summary: '用户反映 A10 Pro V2 开机后激光头完全不出光，无任何激光反应。可能原因包括激光模块损坏、线缆松动、控制板故障或软件设置错误。',
      solution: `## 排查步骤\n\n### 1. 检查线缆连接\n- 确认激光模块与主板之间的排线已插紧\n- 检查排线是否有破损或折断\n- 重新插拔两端连接器\n\n### 2. 测试激光输出\n- 打开 LaserGRBL 或 LightBurn 软件\n- 设置 **最低功率**（如 5%）\n- 点击「测试」按钮，观察是否有微弱光点\n\n### 3. 检查安全开关\n- 确认限位开关没有被卡住\n- 检查主板上的安全跳线是否正常\n\n### 4. 软件检查\n- 确认激光模式已开启（不是预览模式）\n- 检查「LaserGRBL → 设置」中功率参数是否正确\n\n### 5. 硬件故障\n如果以上步骤均无效，激光模块可能已损坏：\n- 联系售后进行模块更换\n- 提供购买凭证和故障视频`,
      content: '> ⚠️ 注意：绝对不能用眼睛直视激光！测试时务必佩戴防护眼镜。'
    },
    {
      id: 'faq-2', machineId: 'm-a10prov2', title: 'A10 Pro V2 雕刻出来的图案模糊不清怎么解决？',
      priority: 'high', status: 'published',
      tags: ['tag-3', 'tag-6', 'tag-13'],
      keywords: '模糊,不清晰,焦点,对焦,精度差,质量差',
      summary: '雕刻结果模糊，线条粗糙或边缘不清晰。通常与焦点调节不当、速度过快或功率不足有关。',
      solution: `## 解决方案\n\n### 1. 调节焦点（最常见原因）\n- 将激光头移到材料表面\n- 旋动激光头底部对焦旋钮\n- 使焦点恰好对准材料表面（约 5mm 距离）\n- 用薄纸测试：对焦正确时纸能被轻微烧焦\n\n### 2. 调整雕刻参数\n| 材料 | 功率 | 速度 | 建议 |\n|------|------|------|------|\n| 木材 | 70-100% | 200-500mm/min | 先低后高 |\n| 亚克力 | 50-70% | 300-600mm/min | 贴保护膜 |\n| 不锈钢 | 100% | 100-200mm/min | 需涂层 |\n\n### 3. 检查皮带松紧\n- X/Y 轴皮带过松会导致雕刻偏移\n- 用手指按压皮带，应有适度张力\n- 拧紧皮带张紧螺丝`,
      content: '对焦是激光雕刻最重要的环节之一。每次更换材料厚度后都需要重新对焦。'
    },
    {
      id: 'faq-3', machineId: 'm-a10prov2', title: 'A10 Pro V2 无法连接电脑/USB 识别不到',
      priority: 'high', status: 'published',
      tags: ['tag-2', 'tag-5'],
      keywords: '连接不上,USB,识别不了,驱动,CH340,连接失败',
      summary: '电脑无法识别设备，LaserGRBL 或 LightBurn 无法连接雕刻机。',
      solution: `## 排查步骤\n\n### 1. 安装 CH340 驱动\n- AtomStack 使用 CH340 USB 转串口芯片\n- 下载地址：搜索「CH340 驱动下载」\n- 安装后重启电脑\n- 在「设备管理器 → 端口」中应看到 COM 口\n\n### 2. 检查 USB 线\n- 更换一根高质量 USB 数据线\n- 不要使用充电线（仅供电无数据传输）\n\n### 3. 检查端口设置\n- 波特率设置为 **115200**\n- 确认选择的 COM 口正确\n\n### 4. Windows 10/11 特殊处理\n- 设置 → 隐私 → 允许应用访问设备\n- 暂时关闭杀毒软件后重试`,
      content: null
    },

    // A20 Pro V2 FAQ
    {
      id: 'faq-4', machineId: 'm-a20prov2', title: 'A20 Pro V2 使用空气辅助时切割效果不好怎么办？',
      priority: 'high', status: 'published',
      tags: ['tag-4', 'tag-9'],
      keywords: '切割不透,切不断,空气辅助,风量,气压,切割深度',
      summary: '使用空气辅助进行切割时，材料切不透或切面发黄。需要调整风量、焦点和切割参数。',
      solution: `## 解决方案\n\n### 1. 空气辅助设置\n- 风量调至 **40-60 L/min**（薄材料）或 **60-80 L/min**（厚材料）\n- 喷嘴对准切割位置\n- 确保气泵正常工作\n\n### 2. 切割参数调整\n| 材料 | 厚度 | 功率 | 速度 | 次数 |\n|------|------|------|------|------|\n| 胶合板 | 3mm | 100% | 200mm/min | 2-3次 |\n| 胶合板 | 5mm | 100% | 150mm/min | 3-5次 |\n| 亚克力 | 3mm | 90% | 150mm/min | 2-3次 |\n\n### 3. 切割技巧\n- 将焦点调至材料 **表面以下 1-2mm**\n- 切割前在材料表面贴美纹纸防焦\n- 多次切割比一次慢速效果更好`,
      content: '> 💡 多次快速切割比一次慢速切割效果更好，且减少焦边。'
    },
    {
      id: 'faq-5', machineId: 'm-a20prov2', title: 'A20 Pro V2 自动对焦功能异常怎么处理？',
      priority: 'medium', status: 'published',
      tags: ['tag-6', 'tag-7'],
      keywords: '自动对焦,失灵,异常,调焦,自动调焦',
      summary: 'A20 Pro V2 自带的自动对焦功能无法正常工作，每次都需要手动调焦。',
      solution: `## 处理步骤\n\n### 1. 检查对焦传感器\n- 检查激光头底部的传感器是否被灰尘遮挡\n- 用软布清洁传感器表面\n- 确认传感器线缆连接牢固\n\n### 2. 检查软件设置\n- LightBurn: Edit → Device Settings → 确认 Auto-Focus 已启用\n- LaserGRBL: 检查是否选择正确的机型配置\n\n### 3. 重置对焦参数\n- 断电重启设备\n- 按住面板按钮 5 秒重置\n- 重新执行一次手动对焦后切换为自动模式`,
      content: null
    },

    // A70 Pro FAQ
    {
      id: 'faq-6', machineId: 'm-a70pro', title: 'A70 Pro 火焰报警器频繁触发怎么解决？',
      priority: 'critical', status: 'published',
      tags: ['tag-10', 'tag-4'],
      keywords: '火焰报警,报警器响,误报,安全保护,火焰检测',
      summary: 'A70 Pro 在正常切割时火焰报警器频繁触发，导致设备自动停机。可能是报警器位置不当或切割参数问题。',
      solution: `## 解决方案\n\n### 1. 调整报警器位置\n- 火焰传感器位于激光头侧面\n- 将传感器旋转 **45°** 远离切割区域\n- 确保传感器不被切割产生的火星直接照射\n\n### 2. 调整切割参数\n- 降低切割速度（不要太慢）\n- 确保空气辅助正常工作\n- 切割厚材料时增加风量\n\n### 3. 材料处理\n- 使用干燥的木材（湿木材容易起火）\n- 切割前清除材料表面的易燃涂层\n\n> ⚠️ 如果确实发生起火，请立即关闭设备电源，使用灭火器处理！`,
      content: '火焰报警是重要的安全保护功能，不建议完全关闭。'
    },
    {
      id: 'faq-7', machineId: 'm-a70pro', title: 'A70 Pro Y 轴运动有异响怎么办？',
      priority: 'medium', status: 'published',
      tags: ['tag-7', 'tag-14'],
      keywords: '异响,噪音,Y轴,嘎吱,摩擦,运动异常',
      summary: 'A70 Pro 的 Y 轴在移动时发出异常噪音，可能是导轨需要润滑或安装不水平。',
      solution: `## 解决方案\n\n### 1. 检查导轨\n- 用干净的布清洁 Y 轴导轨\n- 在导轨上涂抹适量润滑脂（推荐锂基润滑脂）\n- 来回移动 Y 轴数次使润滑脂均匀分布\n\n### 2. 检查水平\n- 用水平仪检查机器是否水平放置\n- 调节四个脚垫使机器水平\n- 不水平会导致偏载和异响\n\n### 3. 检查皮带\n- 确认 Y 轴两侧皮带松紧一致\n- 不一致的张力会导致运动偏移和噪音`,
      content: null
    },

    // Kraft FAQ
    {
      id: 'faq-8', machineId: 'm-kraft', title: 'Kraft 双光源如何切换？什么时候用红外激光？',
      priority: 'medium', status: 'published',
      tags: ['tag-1', 'tag-13'],
      keywords: '双光源,红外,蓝光,切换,什么时候用,选择',
      summary: 'Kraft 搭载蓝光和红外双光源激光模块，用户不清楚如何切换以及在什么场景下使用哪种光源。',
      solution: `## 光源选择指南\n\n### 蓝光激光（405nm）\n- ✅ **适用材料**: 木材、亚克力、纸板、皮革、塑料\n- ✅ **适用场景**: 表面雕刻、浅层切割\n\n### 红外激光（1064nm）\n- ✅ **适用材料**: 金属（不锈钢、铝）、部分塑料\n- ✅ **适用场景**: 金属标记、深色塑料雕刻\n\n### 切换方法\n1. 在 LaserGRBL/LightBurn 中选择激光源\n2. 或通过机器面板的激光选择按钮切换\n3. 切换后需要重新对焦\n\n> ⚠️ 红外激光同样有安全风险，请勿直视光束！`,
      content: null
    },

    // C4 Pro FAQ
    {
      id: 'faq-9', machineId: 'm-c4pro', title: 'C4 Pro CNC 雕刻时材料飞出怎么办？',
      priority: 'critical', status: 'published',
      tags: ['tag-10', 'tag-7'],
      keywords: '材料飞出,固定不住,CNC,安全,夹具,飞溅',
      summary: 'C4 Pro 在进行 CNC 雕刻时，由于主轴高速旋转，如果材料固定不当会导致材料飞出，存在安全隐患。',
      solution: `## 安全措施\n\n### 1. 正确固定材料\n- 使用随机的夹具固定材料\n- 大块材料使用 **至少两个夹具**\n- 薄材料使用双面胶固定在工作台上\n\n### 2. 检查夹具状态\n- 确认夹具螺丝已拧紧\n- 长时间使用后夹具可能松动，定期检查\n\n### 3. 设置正确的进给速度\n- 首次使用新工艺时用 **低进给速度**\n- 逐步提高速度，观察材料稳定性\n\n### 4. 安全操作\n- 雕刻过程中不要打开防护门\n- 首件试切时在旁边观察\n- 准备急停按钮随时可用\n\n> ⚠️ CNC 主轴转速极高（可达 20000 RPM），材料飞出可能造成严重伤害！`,
      content: null
    },

    // R8 旋转卡盘 FAQ
    {
      id: 'faq-10', machineId: 'm-r8', title: 'R8 旋转卡盘安装后无法正常旋转怎么解决？',
      priority: 'medium', status: 'published',
      tags: ['tag-11', 'tag-7'],
      keywords: '旋转卡盘,R8,不转,安装,步进电机,旋转失败',
      summary: 'R8 旋转卡盘安装到机器后无法正常旋转，或者旋转时物体打滑。',
      solution: `## 解决方案\n\n### 1. 连接检查\n- 确认旋转卡盘线缆连接到主板的 **A轴端口**（非 Y 轴）\n- 不同机型的旋转轴接口位置可能不同，请参考说明书\n\n### 2. 软件配置\n- LightBurn: 编辑 → 设备设置 → 启用旋转轴\n- 设置正确的 **旋转直径** 和 **步数/度** 参数\n- A10/A20 系列: 通常设置 1.8° 步距角\n\n### 3. 物体固定\n- 使用卡盘爪紧固物体\n- 大直径物体使用橡胶套增加摩擦力\n- 不要超过卡盘最大承重\n\n### 4. 常见旋转参数\n| 物体直径 | 速度 | 建议 |\n|---------|------|------|\n| 20-40mm | 300-600mm/min | 杯子、笔筒 |\n| 40-80mm | 200-400mm/min | 瓶子、罐子 |`,
      content: null
    },

    // F80 空气辅助 FAQ
    {
      id: 'faq-11', machineId: 'm-f80', title: 'F80 双泵空气辅助风量不足怎么处理？',
      priority: 'medium', status: 'published',
      tags: ['tag-9', 'tag-15'],
      keywords: '空气辅助,风量不足,气压低,F80,气泵,气嘴',
      summary: 'F80 空气辅助系统风量明显不足，影响切割效果。可能是气管堵塞、气泵故障或接头漏气。',
      solution: `## 排查步骤\n\n### 1. 检查气路\n- 检查气管是否有折弯或压扁\n- 检查所有接头是否漏气（用肥皂水检测）\n- 清洁喷嘴，确保没有堵塞\n\n### 2. 检查气泵\n- 确认气泵电源连接正常\n- 听气泵工作声音是否正常（不应有异常噪音）\n- 检查进气口是否通畅\n\n### 3. 调节风量\n- 顺时针旋转调压阀增大风量\n- F80 支持自动切换：开始切割时自动启动，停止时自动关闭\n\n### 4. 定期维护\n- 每月清洁一次空气过滤芯\n- 每季度检查一次气管老化情况`,
      content: null
    },

    // Hurricane (K60) FAQ
    {
      id: 'faq-12', machineId: 'm-hurricane', title: 'Hurricane K60 CO₂ 激光管不亮或功率不足怎么办？',
      priority: 'critical', status: 'published',
      tags: ['tag-1', 'tag-15'],
      keywords: 'CO2,激光管不亮,功率不足,Hurricane,K60,激光管寿命',
      summary: 'K60 CO₂ 激光管不亮或切割能力明显下降。CO₂ 激光管有寿命限制，也可能是水冷或电源问题。',
      solution: `## 排查步骤\n\n### 1. 检查水冷系统\n- CO₂ 激光管 **必须** 有循环水冷\n- 检查水温：正常应为 **15-25°C**\n- 水温过高会导致功率下降或激光管损坏\n- 检查水泵是否正常工作\n\n### 2. 检查激光管\n- 观察激光管内是否有气泡（正常应为淡紫色辉光）\n- 如果管壁出现白色粉末或发黑，说明管子老化\n- CO₂ 激光管寿命通常为 **2000-5000 小时**\n\n### 3. 检查电源\n- 检查激光电源板指示灯\n- 测量电源输出电压是否正常\n\n### 4. 镜片清洁\n- 定期清洁反射镜和聚焦镜\n- 使用无水乙醇和擦镜纸\n- 脏污镜片会导致 30% 以上功率损失`,
      content: '> ⚠️ CO₂ 激光管属于易耗品，正常使用寿命 1-2 年（视使用频率而定）。'
    },

    // 通用 FAQ
    {
      id: 'faq-13', machineId: 'm-a10prov2', title: 'LightBurn 软件如何配置 AtomStack 机型？',
      priority: 'medium', status: 'published',
      tags: ['tag-5', 'tag-12'],
      keywords: 'LightBurn,配置,设置,软件,连接,AtomStack',
      summary: 'LightBurn 是 AtomStack 推荐的专业雕刻软件。本文介绍如何配置 LightBurn 连接 AtomStack 设备。',
      solution: `## 配置步骤\n\n### 1. 安装 LightBurn\n- 从 [lightburnsoftware.com](https://lightburnsoftware.com) 下载\n- 安装后激活（AtomStack 用户可享受专属折扣码）\n\n### 2. 添加设备\n1. 打开 LightBurn → Help → 搜索设备\n2. 或手动添加：\n   - 设备类型: **GRBL**\n   - 波特率: **115200**\n   - COM 口: 在设备管理器中查看\n\n### 3. 机型设置\n- 工作区域根据具体机型设置\n- A10 Pro V2: **410×400mm**\n- A20 Pro V2: **400×415mm**\n- A70 Pro: **850×700mm**\n\n### 4. 首次连接\n1. 打开机器电源\n2. USB 连接电脑\n3. 点击 LightBurn 的「连接」按钮\n4. 看到「Connected」即成功`,
      content: 'LaserGRBL 免费但功能有限；LightBurn 付费但功能强大，适合专业用户。'
    },
    {
      id: 'faq-14', machineId: 'm-a5pro', title: 'A5 Pro 雕刻亚克力时表面有毛刺怎么解决？',
      priority: 'low', status: 'published',
      tags: ['tag-3', 'tag-13', 'tag-4'],
      keywords: '亚克力,毛刺,切面粗糙,发黄,光洁度',
      summary: 'A5 Pro 切割或雕刻亚克力后边缘有毛刺或发黄，影响美观。',
      solution: `## 解决方案\n\n### 1. 防止发黄\n- 雕刻前在亚克力表面 **贴一层美纹纸或保护膜**\n- 使用空气辅助吹走碎屑\n- 降低速度、提高功率\n\n### 2. 减少毛刺\n- 使用 **多次浅切割** 代替一次深切割\n- 每次切割深度不超过 1-2mm\n- 切割后用火焰抛光切面（小心操作）\n\n### 3. 推荐参数\n| 亚克力类型 | 功率 | 速度 | 备注 |\n|-----------|------|------|------|\n| 铸造亚克力 | 100% | 80-120mm/min | 切割效果好 |\n| 挤压亚克力 | 80-100% | 60-100mm/min | 容易发黄 |`,
      content: null
    },
    {
      id: 'faq-15', machineId: 'm-fusion', title: 'Fusion Class 1 安全认证意味着什么？可以不用防护吗？',
      priority: 'medium', status: 'published',
      tags: ['tag-10'],
      keywords: 'Class 1,安全认证,防护,不需要防护眼镜,安全等级',
      summary: 'Fusion 获得了 Class 1 激光安全认证，很多用户不确定这意味着什么，是否还需要额外防护。',
      solution: `## Class 1 安全等级说明\n\n### 什么是 Class 1？\n- Class 1 是 **最高安全等级** 的激光产品\n- 在正常操作下，设备外壳能完全屏蔽激光辐射\n- 不会对人眼和皮肤造成危害\n\n### Fusion 的安全设计\n- 封闭式机身结构\n- 防蓝光/红外视窗\n- 开门自动断光保护\n- 符合 IEC 60825-1 标准\n\n### 注意事项\n- ✅ 正常使用无需佩戴防护眼镜\n- ✅ 在封闭舱门关闭的情况下安全操作\n- ⚠️ **切勿在舱门打开时启动雕刻**\n- ⚠️ **切勿拆卸安全联锁装置**\n- ⚠️ 设备损坏后安全性能可能下降，需及时维修`,
      content: '虽然 Class 1 设备非常安全，但仍建议将设备放在儿童接触不到的地方。'
    },
  ]

  // 设置时间戳和初始计数
  const timeBase = Date.now()
  faqs.forEach((faq, i) => {
    const hoursAgo = i * 3
    const createdAt = new Date(timeBase - hoursAgo * 3600000).toISOString()
    faq.createdAt = createdAt
    faq.updatedAt = createdAt
    faq.viewCount = Math.floor(Math.random() * 500) + 10
    faq.helpfulCount = Math.floor(Math.random() * 50)
    faq.rating = (3 + Math.random() * 2).toFixed(1) * 1
    faq.ratingCount = Math.floor(Math.random() * 30) + 1
  })

  faqs.forEach(f => faqStore.addFaq(f, true))
  save('faq-list', faqStore.faqs)
}

function save(key, data) {
  try { localStorage.setItem(key, JSON.stringify(data)) } catch { }
}
