---
--- @author zsh in 2023/3/27 21:40
---

local locale = LOC.GetLocaleCode();
local L = (locale == "zh" or locale == "zht" or locale == "zhr") and true or false;

L = true; -- 暂时没有英译

local TEXT = require("languages.mone.loc");
local prefabsInfo = TEXT.prefabsInfo;

STRINGS.MONE_STRINGS = {};

local STRINGS = STRINGS.MONE_STRINGS;
local upper = string.upper;

-----------------------------------------------------------------------------------------------------------
--[[ ]]
-----------------------------------------------------------------------------------------------------------
--升级版·晾肉架
STRINGS[upper("mone_meatrack")] = L
        and [[
        - 同一点位种植
        - 配方便宜
        ]]
        or [[]];

--超级牛铃
STRINGS[upper("mone_beef_bell")] = L
        and [[
        - 只能被强制攻击
        - 不会生成便便
        - 不触发陷阱
        - 有训诫值不会发情
        - 不受群体仇恨影响
        - 不乱跑
        - 驯服度不会自然下降
        - 戴牛角帽无视顺从值直接上牛且回满顺从值
        - 骑牛可以使用武器
        ]]
        or [[]];

--升级版·蝙蝠棒
STRINGS[upper("mone_batbat")] = L
        and [[
        - 
        ]]
        or [[]];

--升级版·晨星锤
STRINGS[upper("mone_nightstick")] = L
        and [[
        - 
        ]]
        or [[]];

--升级版·三尾猫鞭
STRINGS[upper("mone_whip")] = L
        and [[
        - 
        ]]
        or [[]];


--腐化火腿棒
STRINGS[upper("mone_hambat")] = L
        and [[
        - 属性同火腿棒，但是反过来的，越腐烂伤害越高
        ]]
        or [[]];

-- 单身狗
STRINGS[upper("mone_single_dog")] = L
        and [[
        - 周期探测一定半径内的狗子，秒杀
        ]]
        or [[]];
-- 每个周期扣除其最大生命值 20% 的血量
-----------------------------------------------------------------------------------------------------------
--[[ 更多物品·一 ]]
-----------------------------------------------------------------------------------------------------------
-- [new prefab sample] 未完成品
STRINGS[upper("mone_soul_leaves_trigger")] = L
        and [[
        - 原地留下一个灵魂出窍的身体，玩家立刻进入选人阶段
        - 原地留下的灵魂出窍的身体后续可以通过附体的方式重新获得操控权
        ]]
        or [[]];


-- 灯笼
STRINGS[upper("mone_redlantern")] = L
        and [[
        - 类似提灯但是丢地上不消耗耐久
        - 猴子和坎普斯都不会偷
        ]]
        or [[]];
-- 毒矛
STRINGS[upper("mone_spear_poison")] = L
        and [[
        - 可以对目标周围造成1.5格范围伤害
        - 固定为25点伤害
        ]]
        or [[]];
-- 保鲜袋
STRINGS[upper("mone_storage_bag")] = L
        and [[
        - 4格，永久保鲜
        - 只能存放允许放入冰箱的物品
        ]]
        or [[]];
-- 材料袋
STRINGS[upper("mone_candybag")] = L
        and [[
        - 可随身携带
        - 可以存放草、树枝、燧石、石头、金块、木头
        ]]
        or [[]];
-- 工具袋
STRINGS[upper("mone_tool_bag")] = L
        and [[
        - 可随身携带
        - 只允许存放有 tool 等标签的物品
        ]]
        or [[]];
-- 小食物袋
STRINGS[upper("mone_spicepack")] = L
        and [[
        - 可随身携带
        - 可以存放任何有新鲜度的物品
        - 可以保鲜，厨师袋的保鲜效果
        ]]
        or [[]];

-- 食物袋
STRINGS[upper("mone_icepack")] = L
        and [[
        - 可随身携带
        - 可以存放任何有新鲜度的物品
        - 可以保鲜，默认是盐盒的保鲜效果
        ]]
        or [[]];
-- 装备袋
STRINGS[upper("mone_backpack")] = L
        and [[
        - 可随身携带
        - 允许存放可被装备的物品
        ]]
        or [[]];
-- 收纳袋
STRINGS[upper("mone_piggyback")] = L
        and [[
        - 40格容量
        - 可随身携带
        ]]
        or [[]];
-- 收割者的砍刀
STRINGS[upper("mone_harvester_staff")] = L
        and [[
        - 快速采集但采集降饥饿度
        - 增加5%移速
        ]]
        or [[]];
-- 收割者的黄金砍刀
STRINGS[upper("mone_harvester_staff_gold")] = L
        and [[
        - 快速采集但采集降饥饿度
        - 增加10%移速
        ]]
        or [[]];
-- 暗夜空间斗篷
STRINGS[upper("mone_nightspace_cape")] = L
        and [[
        - 24格或14格容量，在模组配置里可以修改。
        - 类似骨甲、穿戴者可以在水上行走
        - 冬季保暖 180，夏季隔热 180
        ]]
        or [[]];
-- 海上麻袋
STRINGS[upper("mone_seasack")] = L
        and [[
        - 14格
        - 隔热120秒
        - 移速10%
        ]]
        or [[]];
-- 树木栽培家
STRINGS[upper("mone_arborist")] = L
        and [[
        - 放入树种，会在半径2.5格地皮内圆形种植树木
        - 每5秒会灭一次半径3.5格地皮内的焖烧/火焰
        - 树种目前只是原版的五种树种
        - 画大饼：未来实现圆形、心形等种植方式。
        ]]
        or [[]];
STRINGS[upper("mone_skull_chest")] = L
        and [[
        - 25格容器，可以存放杂物。
        - 作者本人对杂物的定义是：不常用，但是放箱子里又觉得占空间。
        - 除此以外，木头也能放进来哈
        ]]
        or [[]];
-- - 但是除此以外，诸如树枝、草、木头、石头等这类基础物品也能放进来
-- 燃气帽
STRINGS[upper("mone_gashat")] = L
        and [[
        - 低理智时高防御和高攻击
        - 1-0.8，80%防御1倍攻击。0.8-0.55，85%防御1.15倍攻击。
        - 0.55-0.3，85%防御1.3倍攻击。0.3-0.15，90%防御1.5倍攻击。
        - 0.15-0，95%防御2倍攻击
        ]]
        or [[]];
STRINGS[upper("mone_waterchest_inv")] = L
        and [[
        - 120格、不可燃、只允许被玩家摧毁、可随身携带
        ]]
        or [[]];
STRINGS[upper("mone_pith")] = L
        and [[
        - 耐久度等于草甲，但防御度为70%
        ]]
        or [[]];
STRINGS[upper("mone_brainjelly")] = L
        and [[
        - 四季控温
        - 春秋30度，夏10度，冬60度
        ]]
        or [[]];
STRINGS[upper("mone_double_umbrella")] = L
        and [[
        - 70%防雨，隔热效果为眼球伞的2倍
        - 带上之后人物头上缺了一块贴图，不太会动画，暂时未能解决
        ]]
        or [[]];
STRINGS[upper("mone_pheromonestone")] = L
        and [[
        - 使装备无耐久(新鲜度、燃料、使用次数、护甲)
        - 注意：当你发现某个物品突然又有耐久了，那是因为该物品发生
        了变化，比如伯尼变大变小，每次变化伯尼都不再是原来的伯尼了
        ]]
        or [[]];
STRINGS[upper("mone_pheromonestone2")] = L
        and [[
        - 使容器较高速度返鲜，每10秒回复大概2%的新鲜度
        - 注意：假如你的容器是类似能力勋章的坎普斯宝匣这种既可以放置，又可以拆除的物品，
        由于拆除时旧物品会被删除，生成了一个新的物品，所以该功能必然是会失效的。
        ]]
        or [[]];
STRINGS[upper("mone_walking_stick")] = L
        and [[
        - 手持增加100%的移动速度，但有耐久。
        - 耐久大概是火把的三倍吧？
        ]]
        or [[]];
STRINGS[upper("mone_wardrobe")] = L
        and [[
        - 36格，存放你的装备。
        - 补充：不只是装备，类似排箫这种现在也能放进去了
        ]]
        or [[]];
STRINGS[upper("mone_halberd")] = L
        and [[
        - 砍树的时候自动出树根！
        - 斧头+镐头+锤子(2.5倍效果)
        - 伤害设置成了14点，所以即使是大力士也能抓鼹鼠了。
        ]]
        or [[]];
STRINGS[upper("mone_chiminea")] = L
        and [[
        - 将物品放入其中，点击删除按钮即可
        - 限制了某些物品不允许放入其中
        ]]
        or [[]];
-- 如有必要的话，倒是可以添加个仅管理员可以删除的功能...
STRINGS[upper("mone_city_lamp")] = L
        and [[
        - 范围1.5格地皮
        ]]
        or [[]];
STRINGS[upper("mone_bathat")] = L
        and [[
        - 佩戴后右键人物可以飞行
        - PS1：假如你的服务器延迟过高，会出现上下抖动的情况
        - PS2：该功能只是个简单功能，体验上可能不是太好
        ]]
        or [[]];
-- 画大饼：未来优化体验，至少是更换云朵贴图、添加新动作、限制飞行时被允许的动作队列
STRINGS[upper("mone_piggybag")] = L
        and [[
        - 九格、可以存放部分容器和部分其他物品
        - 其他物品大概是原版的照明工具
        ]]
        or [[]];
STRINGS[upper("mone_bookstation")] = L
        and [[
        - 可以随身携带小书架
        - 不提供科学引擎的效果、薇克巴顿靠近回复速度并不会加倍
        ]]
        or [[]];
STRINGS[upper("mone_wathgrithr_box")] = L
        and [[
        - 8格，存放女武神的歌谣
        ]]
        or [[]];
STRINGS[upper("mone_wanda_box")] = L
        and [[
        - 存放旺达的钟表(死亡时，容器内的第二次机会表会掉落！)
        - 为了实现`第二次机会表会掉落`方便，所以限制了容器只能放在口袋里
        ]]
        or [[]];
STRINGS[upper("mone_poisonblam")] = L
        and [[
        - 使有新鲜度的物品瞬间腐烂
        ]]
        or [[]];
STRINGS[upper("mie_relic_2")] = L
        and [[
        - 关闭图腾后，55%概率物品翻倍，45%概率直接消失。买定离手！
        ]]
        or [[]];
STRINGS[upper("mie_icemaker")] = L
        and [[
        - 它把火变成冰！
        ]]
        or [[]];
STRINGS[upper("mie_obsidianfirepit")] = L
        and [[
        - 照明范围和燃烧时间都是普通火坑的3倍有余
        ]]
        or [[]];
STRINGS[upper("mie_bear_skin_cabinet")] = L
        and [[
        - 永久保鲜、可以存放任何有新鲜度的物体
        ]]
        or [[]];
STRINGS[upper("mie_watersource")] = L
        and [[
        - 25格、可以装水
        - 可以存放`食物和耕作`栏以及一些种田必需的物品
        ]]
        or [[]];
STRINGS[upper("mie_wooden_drawer")] = L
        and [[
        - 不可燃的箱子，只允许玩家摧毁。
        - 分拣机不会将物品转移到其中。
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        -
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        -
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        -
        ]]
        or [[]];
-----------------------------------------------------------------------------------------------------------
--[[ 更多物品·二 ]]
-----------------------------------------------------------------------------------------------------------
STRINGS[upper("mone_firesuppressor")] = L
        and [[
        - 增加了捡起周围物品并分类转移的功能
        - 本物品在其他功能上和原版的物品差别不大
        ]]
        or [[]];
STRINGS[upper("mone_treasurechest")] = L
        and [[
        - 16格或25格或36格，在模组配置里可以修改。
        - 本物品在其他功能上和原版的物品差别不大
        - 可以使用弹性空间制造器升级，但是升级后将无法被摧毁！
        ]]
        or [[]];
STRINGS[upper("mone_dragonflychest")] = L
        and [[
        - 16格或25格或36格，在模组配置里可以修改。
        - 本物品在其他功能上和原版的物品差别不大
        - 可以使用弹性空间制造器升级，但是升级后将无法被摧毁！
        ]]
        or [[]];
STRINGS[upper("mone_icebox")] = L
        and [[
        - 16格或25格或36格，在模组配置里可以修改。
        - 本物品在其他功能上和原版的物品差别不大
        - 可以使用弹性空间制造器升级，但是升级后将无法被摧毁！
        ]]
        or [[]];
STRINGS[upper("mone_saltbox")] = L
        and [[
        - 16格或25格或36格，在模组配置里可以修改。
        - 本物品在其他功能上和原版的物品差别不大
        - 可以使用弹性空间制造器升级，但是升级后将无法被摧毁！
        ]]
        or [[]];
STRINGS[upper("mone_dragonflyfurnace")] = L
        and [[
        - 类似龙鳞火炉加强版
        - 九格容器，目前只能存放暖石
        - 部分功能尚未实现，敬请期待...
        ]]
        or [[]];
STRINGS[upper("mone_moondial")] = L
        and [[
        - 类似反作用的龙鳞火炉
        - 九格容器，目前只能存放暖石
        - 你可以轻松将暖石降温到-20度
        - 一直处于满月的流水状态，比较好看
        ]]
        or [[]];
STRINGS[upper("mone_waterballoon")] = L
        and [[
        - 一次制作六个。谨慎使用！别一个点几百个树苗啊...
        - 一次可以让最多80颗树种(原版的五种)发芽
        - 一次可以让范围内所有发芽后的树种(树苗状态，原版的五种)长到第一阶段
        - 一次可以让范围内所有树木(原版的五种)直接长到最高阶段，且只能生效一次！
        - 一次可以让范围内几乎所有农作物种子在能够生长的时候(白天/矮星)直接长成巨大作物。
        ]]
        or [[]];

STRINGS[upper("mone_orangestaff")] = L
        and [[
        - 增加25%的移动速度
        - 装备者拥有快速采集的能力
        - 无消耗、无耐久，但有五秒冷却时间
        - 请尽量不要用扫把换皮肤，因为会导致不同皮肤间的特效不匹配甚至消失。
        ]]
        or [[]];
STRINGS[upper("mone_boomerang")] = L
        and [[
        - 伤害34、自动接、无耐久
        - 回旋镖的攻击范围和飞行速度增加
        - 攻击到目标后会在目标周围弹来弹去
        - 使用这个回旋镖造成的伤害是真实伤害
        - 使用这个回旋镖可以秒杀致命亮茄...
        ]]
        or [[]];
STRINGS[upper("mone_armor_metalplate")] = L
        and [[
        - 不减移速
        - 勉强可以作为大理石甲的替代品
        ]]
        or [[]];
STRINGS[upper("mone_eyemaskhat")] = L
        and [[
        - 耐久增加，防御力增加
        - 位面防御 20
        - 可以成组喂食
        - 耐久为0不消失但失去效果
        ]]
        or [[]];
STRINGS[upper("mone_shieldofterror")] = L
        and [[
        - 盾反（但存在贴图丢失情况）
        - 耐久增加，防御力增加
        - 位面伤害 20，位面防御 20
        - 可以成组喂食
        - 耐久为0不消失但失去效果
        ]]
        or [[]];
STRINGS[upper("mone_farm_plow_item")] = L
        and [[
        - 一次挖九个坑（按道理来说十个坑最佳，但是实现起来不太方便）
        - 部署时附近的农田杂物会被删除
        - 工作完毕会自动归还给它的部署者（5格地皮内）
        ]]
        or [[]];
STRINGS[upper("mone_fishingnet")] = L
        and [[
        - 科雷的废稿，渔网，捕鱼用的
        - 鱼越重，消耗的耐久越高！
        ]]
        or [[]];
STRINGS[upper("mone_garlic_structure")] = L
        and [[
        - 蝙蝠靠近1秒内被熏死(因为蝙蝠是吸血鬼？)
        ]]
        or [[]];
STRINGS[upper("mone_seedpouch")] = L
        and [[
        - 14格、种子永鲜、80%防雨
        ]]
        or [[]];
STRINGS[upper("mone_dummytarget")] = L
        and [[
        - 每2秒嘲讽一次半径4格内非友军生物。受到攻击会反伤，反伤值为34点。
        - 击杀傀儡者，会受到10%其最大生命值的真实伤害。
        - 被动：青蛙必须死。注意：玩家使用锤子攻击是可以杀死傀儡的。
        - 傀儡受到攻击时，有10%的概率反伤值为100点，有百分之一的概率，反伤值为目标最大生命值。
        ]]
        or [[]];
STRINGS[upper("mie_fish_box")] = L
        and [[
        - 50格，10倍保鲜，只允许被玩家摧毁，可以制冷的
        - 目前冰块会腐烂，暂时还没能解决这个问题。（2023-06-15：已解决）
        ]]
        or [[]];
STRINGS[upper("mie_waterpump")] = L
        and [[
        - 可以给周围缺水的农田浇水，也可以和植物对话。也能灭火。
        ]]
        or [[]];
STRINGS[upper("mie_bushhat")] = L
        and [[
        - 可以让大多数生物直接丢失仇恨。红宝石可以修复。
        ]]
        or [[]];
STRINGS[upper("mie_tophat")] = L
        and [[
        - 拥有贝雷帽的全部效果，沃尔夫冈佩戴后不掉力量值。
        ]]
        or [[]];
STRINGS[upper("mie_sand_pit")] = L
        and [[
        - 蚁狮的沙坑贴图。
        - 用铲子可以摧毁。
        - 等价于半自动的物品转移功能，但是占地面积小。
        ]]
        or [[]];
STRINGS[upper("mie_ordinary_bundle_state1")] = L
        and [[
        - 【警告】 允许打包的目标过多，请谨慎使用，避免崩溃
        - 允许打包所有能被摧毁的目标
        - 关于被摧毁：建筑能被敲掉、树木可以被陨石砸掉等
        ]]
        or [[]];
STRINGS[upper("mie_bundle_state1")] = L
        and [[
        - 【警告】 允许打包的目标过多，请谨慎使用，避免崩溃
        - 除了有限的一些目标，几乎都可以打包
        ]]
        or [[]];
STRINGS[upper("mie_book_horticulture")] = L
        and [[
        - 采集巨大作物要小心噢！
        - 采集过程完全等价于玩家在采集。
        - 阅读时，采集半径3.75格内的植株等。
        ]]
        or [[]];
STRINGS[upper("mie_book_silviculture")] = L
        and [[
        - 阅读时，收纳半径3.75格内的物品。
        - 如果是树根，会帮你铲除！
        - 注意：铲树根的过程等价于玩家在铲。
        - 提示：可以通过将任何物品放在懒人书上来右键打开它
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        -
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        -
        ]]
        or [[]];
-----------------------------------------------------------------------------------------------------------
--[[ 更多物品·三 ]]
-----------------------------------------------------------------------------------------------------------
STRINGS[upper("mone_beef_wellington")] = L
        and [[
        - 肉食，半天内增加2.5倍伤害
        - 使用者添加 50 点位面伤害值，20 点位面防御
        - 一次制作四个
        ]]
        or [[]];
STRINGS[upper("mone_chicken_soup")] = L
        and [[
        - 肉食，有10%的概率回满三维（一次制作五个）
        ]]
        or [[]];
STRINGS[upper("mone_stomach_warming_hamburger")] = L
        and [[
        - 永久增加1点饥饿值上限
        - 为了避免兼容性问题，限制了：仅原版，且排除机器人和小鱼人
        ]]
        or [[]];
STRINGS[upper("mone_stomach_warming_hamburger_copy")] = L
        and [[
        - 一次制作十个
        ]]
        or [[]];
STRINGS[upper("mone_lifeinjector_vb")] = L
        and [[
        - 永久增加10点
        - 为了避免兼容性问题，限制了：仅原版，且排除旺达和小鱼人
        ]]
        or [[]];
STRINGS[upper("mone_lifeinjector_vb_copy")] = L
        and [[
        - 一次制作十个
        ]]
        or [[]];
STRINGS[upper("mone_honey_ham_stick")] = L
        and [[
        - 一天内效率提高两倍，时间可累加(一次制作五个)
        - 击杀Boss的时候有一定概率触发双倍掉落效果（需要在配置中开启）
        ]]
        or [[]];
STRINGS[upper("mone_guacamole")] = L
        and [[
        - 夜视半天，无视沙尘暴，时间不可叠加(一次制作五个)
        ]]
        or [[]];
STRINGS[upper("mone_glommer_poop_food")] = L
        and [[
        - 让格罗姆立刻拉一次粑粑
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        -
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        -
        ]]
        or [[]];
-----------------------------------------------------------------------------------------------------------
--[[ 更多物品·原版栏 ]]
-----------------------------------------------------------------------------------------------------------

-----------------------------------------------------------------------------------------------------------
STRINGS[upper("featherpencil_copy")] = L
        and [[
        - 一次制作四个
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        -
        ]]
        or [[]];
-----------------------------------------------------------------------------------------------------------
STRINGS[upper("mie_granary_meats")] = L
        and [[
        - 10倍保鲜
        ]]
        or [[]];
STRINGS[upper("mie_granary_greens")] = L
        and [[
        - 10倍保鲜
        ]]
        or [[]];
STRINGS[upper("mie_new_granary")] = L
        and [[
        - 50格，10倍保鲜，可以放蔬菜、水果、种子。
        ]]
        or [[]];
STRINGS[upper("mie_well")] = L
        and [[
        - 水井、可以遏制半径4格内的焖烧
        ]]
        or [[]];
STRINGS[upper("mie_bananafan_big")] = L
        and [[
        - 呼风唤雨
        ]]
        or [[]];
STRINGS[upper("mie_yjp")] = L
        and [[
        - 满水满肥，雨水补给。
        - 枯萎的作物复活、灭火、低于20%停雨。
        ]]
        or [[]];
STRINGS[upper("mie_cash_tree_ground")] = L
        and [[
        - 每分钟回复25理智
        - 每隔两天左右随机掉落一个宝石
        ]]
        or [[]];
STRINGS[upper("mie_myth_fuchen")] = L
        and [[
        - 增加移速，消除生物仇恨，可以施展技能隔空取物！
        ]]
        or [[]];
STRINGS[upper("mie_poop_flingomatic")] = L
        and [[
        - 给植物和农场施肥
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        -
        ]]
        or [[]];
-----------------------------------------------------------------------------------------------------------
--[[ 更多物品·修改栏 ]]
-----------------------------------------------------------------------------------------------------------
STRINGS[upper("whip_mi_copy")] = L
        and [[
        - 不建议和同样修改了该物品的模组一起开启！
        - 原版物品，但是通过此处制作出来就会被修改
        - 伤害翻倍
        ]]
        or [[]];
STRINGS[upper("wateringcan_mi_copy")] = L
        and [[
        - 不建议和同样修改了该物品的模组一起开启！
        - 原版物品，但是通过此处制作出来就会被修改
        - 二格，存放鱼，返鲜鱼
        ]]
        or [[]];
STRINGS[upper("premiumwateringcan_mi_copy")] = L
        and [[
        - 不建议和同样修改了该物品的模组一起开启！
        - 原版物品，但是通过此处制作出来就会被修改
        - 四格，存放鱼，返鲜鱼
        ]]
        or [[]];
STRINGS[upper("batbat_mi_copy")] = L
        and [[
        - 不建议和同样修改了该物品的模组一起开启！
        - 原版物品，但是通过此处制作出来就会被修改
        - 耐久翻倍
        ]]
        or [[]];
STRINGS[upper("nightstick_mi_copy")] = L
        and [[
        - 不建议和同样修改了该物品的模组一起开启！
        - 原版物品，但是通过此处制作出来就会被修改
        - 电子元件可以修复
        ]]
        or [[]];
STRINGS[upper("hivehat_mi_copy")] = L
        and [[
        - 不建议和同样修改了该物品的模组一起开启！
        - 原版物品，但是通过此处制作出来就会被修改
        - 防御值由70%改为90%
        - 采集蜂蜜/靠近杀人蜂巢不会出杀人蜂
        - 佩戴者拥有昆虫标签，蜜蜂不会主动攻击
        - 蜜蜂/杀人蜂永远都不会对你有持续的仇恨
        ]]
        or [[]];
STRINGS[upper("eyemaskhat_mi_copy")] = L
        and [[
        - 不建议和同样修改了该物品的模组一起开启！
        - 原版物品，但是通过此处制作出来就会被修改
        - 成组喂食以恢复耐久
        - 耐久为0不消失，但没有防护效果
        ]]
        or [[]];
STRINGS[upper("shieldofterror_mi_copy")] = L
        and [[
        - 不建议和同样修改了该物品的模组一起开启！
        - 原版物品，但是通过此处制作出来就会被修改
        - 成组喂食以恢复耐久
        - 耐久为0不消失，但没有防护效果
        ]]
        or [[]];
-----------------------------------------------------------------------------------------------------------
--[[ 备忘各类物品的功能 ]]
-----------------------------------------------------------------------------------------------------------
if not isDebug() then
    return;
end

-- 疯狂科学家实验室
STRINGS[upper("madscience_lab_copy")] = L
        and [[
        - 疯狂科学家实验室，万圣节活动的科技建筑。
        ]]
        or [[]];
STRINGS[upper("halloween_experiment_bravery")] = L
        and [[
        - 小药液持续4分钟，大药液持续6分钟。
        - 喝下药液，玩家在接下来的一段时间内砍树或开启箱子时，不会再因为飞出的“完全正常的蝙蝠”而损失理智值。
        ]]
        or [[]];
STRINGS[upper("halloween_experiment_health")] = L
        and [[
        - 喝下瓶装乐观混合剂，立即回复8生命，并在接下来的一分钟内每2秒回复1生命。
        - 喝下壶装乐观混合剂，立即回复20生命，并在接下来的一分钟内每2秒回复1生命。
        ]]
        or [[]];
STRINGS[upper("halloween_experiment_sanity")] = L
        and [[
        - 喝下少许刚毅勇气，立即回复5理智，并在接下来的一分钟内每2秒回复1理智。
        - 喝下杯装刚毅勇气，立即回复15理智，并在接下来的一分钟内每2秒回复1理智。
        ]]
        or [[]];
STRINGS[upper("halloween_experiment_volatile")] = L
        and [[
        - 将两种晶体加入营火/火坑，会小幅度加大火势，并赋予火焰特殊的粒子效果。持续1分钟。
        ]]
        or [[]];
STRINGS[upper("halloween_experiment_moon")] = L
        and [[
        - 把月亮精华液对着特定物品使用，可以将它们变异。
        - 具体内容请去`https://dontstarve.huijiwiki.com`查阅`疯狂科学家实验室`词条。
        ]]
        or [[]];
STRINGS[upper("halloween_experiment_root")] = L
        and [[
        - 完全正常的树根：种植后会出现完全正常的树苗，它会在一段时间后长成完全正常的树。
        ]]
        or [[]];

-- 女武神
STRINGS[upper("battlesong_durability")] = L
        and [[
        - 使有使用次数的武器的耐久消耗减少33%
        ]]
        or [[]];
STRINGS[upper("battlesong_healthgain")] = L
        and [[
        - 女武神每次攻击+0.5HP/队友+1HP
        ]]
        or [[]];
STRINGS[upper("battlesong_sanitygain")] = L
        and [[
        - 持续性团队buff。女武神和队友每次攻击+1San
        ]]
        or [[]];
STRINGS[upper("battlesong_sanityaura")] = L
        and [[
        - 持续性团队buff。减San光环效果减少50%(巨鹿中庭都有效果)
        ]]
        or [[]];
STRINGS[upper("battlesong_fireresistance")] = L
        and [[
        - 持续性团队buff。减少33%受到的火焰伤害
        ]]
        or [[]];
STRINGS[upper("battlesong_instant_taunt")] = L
        and [[
        - 拉取部分生物仇恨(不包括Boss类)
        ]]
        or [[]];
STRINGS[upper("battlesong_instant_panic")] = L
        and [[
        - 让部分生物4s内乱跑(类似火魔杖点燃但不会解除仇恨)
        - 不包括Boss/影怪/固定/钻地/海洋生物
        - 对小弟类Boss有较好的效果(蜂后、座狼、蜘蛛女王)
        ]]
        or [[]];

-- 老奶奶
STRINGS[upper("book_birds")] = L
        and [[
        - 消耗50理智，召唤一大群鸟
        ]]
        or [[]];
STRINGS[upper("book_horticulture")] = L
        and [[
        - 消耗33理智，催熟食用类作物
        ]]
        or [[]];
STRINGS[upper("book_silviculture")] = L
        and [[
        - 消耗33理智，催熟非食用类植物
        ]]
        or [[]];
STRINGS[upper("book_sleep")] = L
        and [[
        - 消耗33理智，催眠周围生物
        ]]
        or [[]];
STRINGS[upper("book_brimstone")] = L
        and [[
        - 消耗33理智，降下16道闪电
        ]]
        or [[]];
STRINGS[upper("book_tentacles")] = L
        and [[
        - 消耗50理智，召唤3只触手
        ]]
        or [[]];
STRINGS[upper("book_fish")] = L
        and [[
        - 消耗33理智，召唤3群海鱼
        ]]
        or [[]];
STRINGS[upper("book_fire")] = L
        and [[
        - 消耗33理智，扑灭火焰和闷烧，生成火焰笔
        ]]
        or [[]];
STRINGS[upper("book_web")] = L
        and [[
        - 消耗33理智，生成减速蜘蛛网
        ]]
        or [[]];
STRINGS[upper("book_temperature")] = L
        and [[
        - 消耗33理智，将体温恢复到35度，清空潮湿度
        ]]
        or [[]];
STRINGS[upper("book_light")] = L
        and [[
        - 消耗33理智，召唤天光，持续半天
        ]]
        or [[]];
STRINGS[upper("book_moon")] = L
        and [[
        - 消耗50理智，将月相改为满月
        ]]
        or [[]];
STRINGS[upper("book_rain")] = L
        and [[
        - 消耗33理智，下雨或停雨
        ]]
        or [[]];
STRINGS[upper("book_bees")] = L
        and [[
        - 消耗33理智，召唤2只嗡嗡蜜蜂为你作战
        ]]
        or [[]];
STRINGS[upper("book_research_station")] = L
        and [[
        - 消耗33理智，暂时解锁制作配方
        ]]
        or [[]];
STRINGS[upper("book_horticulture_upgraded")] = L
        and [[
        - 消耗33理智，催熟更多食用类作物，自动照料
        ]]
        or [[]];
STRINGS[upper("book_light_upgraded")] = L
        and [[
        - 消耗33理智，召唤天光，持续2天
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        -
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        -
        ]]
        or [[]];



-- 机器人
STRINGS[upper("")] = L
        and [[
        - 生物扫描分析仪
        - 安装在地上用于扫描不同特种生物，来解锁电路蓝图以及获得生物数据。
        - 当范围内有可扫描生物时会有灯光提示。
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        - 电路提取器
        - 用于拆除已装电路，无耐久。
        - 如果拆除生效的电路，会损失该电路占用的全部电力。
        - 拆除电路会消耗电路25%耐久
        ]]
        or [[]];
STRINGS[upper("wx78module_")] = L
        and [[
        - 胃增益电路
        - 通过扫描猎犬解锁
        - 增加机器人40饱食度上限，占用1格电量
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        - 超级胃增益电路
        - 通过扫描熊大/缀食者解锁
        - 增加机器人100饱食度上限，占用2格电量
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        - 处理器电路
        - 通过扫描蝴蝶解锁
        - 增加机器人40点理智上限，占用1格电量
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        - 超级处理器电路
        - 通过扫描影怪解锁
        - 增加机器人100点理智上限，占用2格电量
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        - 强化电路
        - 通过扫描蜘蛛解锁
        - 增加机器人50点生命值上限，占用1格电量
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        - 超级强化电路
        - 通过扫描护士蜘蛛解锁
        - 增加机器人100点生命值上限，占用2格电量
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        - 加速电路
        - 通过扫描兔子解锁
        - 为机器人提供加速buff，占用6格电量
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        - 超级加速电路
        - 通过扫描机械战车/远古守护者解锁
        - 加速效果与加速电路相同，但只占用2格电量
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        - 制冷电路
        - 通过扫描蓝色猎犬/独眼巨鹿解锁
        - 使机器人变成一个冷源，使在机器人物品栏里的物品降温，保鲜等。
        - 制冷和制热电路同时生效会相互抵消。
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        - 热能电路
        - 通过扫描红色猎犬/龙蝇解锁
        - 使机器人变成一个冷源，使在机器人物品栏里的物品升温，加速腐烂等。
        - 制冷和制热电路同时生效会相互抵消。
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        - 照明电路
        - 通过扫描荧光果/鱿鱼/蠕虫解锁
        - 为机器人提供半径1.5格地皮的照明，占用3格电量
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        - 光电电路
        - 通过扫描鼹鼠解锁
        - 为机器人提供鼹鼠帽一样的夜视效果，占用4格电量
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        - 豆豆电路
        - 通过扫描蜂后解锁
        - 为机器人提供一个10点/分的血量恢复buff，占用3格电量
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        - 合唱盒电路
        - 通过扫描帝王蟹/寄居蟹解锁
        - 为机器人提供一个4.4点/分的精神恢复buff
        - 同时机器人可以直接与植物交流
        ]]
        or [[]];
STRINGS[upper("")] = L
        and [[
        - 电气化电路
        - 通过扫描伏特电羊解锁
        - 为机器人提供免疫雷劈效果，占用3格电量
        - 同时有30点反伤单体雷电伤害(可叠加)
        ]]
        or [[]];
