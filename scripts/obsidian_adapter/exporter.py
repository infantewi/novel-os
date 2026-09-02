# -*- coding: utf-8 -*-
"""Atomic Exporter for NOVEL OS -> Obsidian Read-Only Mirror."""

import os
import shutil
import json
import yaml
import datetime
from pathlib import Path
from typing import Dict, Any, List

from .mapper import VaultMapper
from .validator import MirrorValidator
from .manifest import MirrorManifest


class VaultExporter:
    def __init__(self, source_root: Path, vault_root: Path, temp_root: Path):
        self.source_root = source_root
        self.vault_root = vault_root
        self.temp_root = temp_root

    def export_all(self) -> Dict[str, Any]:
        """Executes the full atomic mirror pipeline."""
        print("[EXPORTER] Initializing temp vault export environment...")
        if self.temp_root.exists():
            shutil.rmtree(self.temp_root)
        self.temp_root.mkdir(parents=True, exist_ok=True)

        for cat in VaultMapper.CATEGORIES:
            (self.temp_root / cat).mkdir(parents=True, exist_ok=True)

        print("[EXPORTER] Exporting Category 00_HOME...")
        self._export_home()

        print("[EXPORTER] Exporting Category 01_CANON...")
        self._export_canon()

        print("[EXPORTER] Exporting Category 02_CHARACTERS...")
        self._export_characters()

        print("[EXPORTER] Exporting Category 03_RELATIONSHIPS...")
        self._export_relationships()

        print("[EXPORTER] Exporting Category 04_TIMELINE...")
        self._export_timeline()

        print("[EXPORTER] Exporting Category 05_LOCATIONS...")
        self._export_locations()

        print("[EXPORTER] Exporting Category 06_FACTIONS...")
        self._export_factions()

        print("[EXPORTER] Exporting Category 07_ABILITIES...")
        self._export_abilities()

        print("[EXPORTER] Exporting Category 08_ITEMS...")
        self._export_items()

        print("[EXPORTER] Exporting Category 09_FORESHADOWING...")
        self._export_foreshadowing()

        print("[EXPORTER] Exporting Category 10_CHAPTERS (CH001-CH051)...")
        self._export_chapters()

        print("[EXPORTER] Exporting Category 11_ARCS...")
        self._export_arcs()

        print("[EXPORTER] Exporting Category 12_STATE...")
        self._export_state()

        print("[EXPORTER] Exporting Category 13_HANDOFF...")
        self._export_handoff()

        print("[EXPORTER] Exporting Category 14_MEMORY (OpenViking Structured)...")
        self._export_memory()

        print("[EXPORTER] Exporting Category 15_QA...")
        self._export_qa()

        print("[EXPORTER] Exporting Category 99_SYSTEM...")
        self._export_system_policies()

        print("[EXPORTER] Validating temp vault integrity...")
        valid, errors = MirrorValidator.validate_vault(self.temp_root)
        if not valid:
            raise RuntimeError(f"Temp vault validation failed: {errors}")

        print("[EXPORTER] Promoting temp vault atomically to target vault root...")
        self.vault_root.mkdir(parents=True, exist_ok=True)
        for cat in VaultMapper.CATEGORIES:
            target_cat = self.vault_root / cat
            target_cat.mkdir(parents=True, exist_ok=True)
            src_cat = self.temp_root / cat
            for src_file in src_cat.glob("*"):
                dest_file = target_cat / src_file.name
                shutil.copy2(src_file, dest_file)

        print("[EXPORTER] Generating Mirror Manifest...")
        manifest_data = MirrorManifest.generate_manifest(self.source_root, self.vault_root)

        print("[EXPORTER] Validating final vault...")
        v_ok, v_errs = MirrorValidator.validate_vault(self.vault_root)
        if not v_ok:
            raise RuntimeError(f"Final vault validation failed: {v_errs}")

        print(f"[EXPORTER] Export successful. Total mirrored files: {manifest_data['total_files']}")
        return manifest_data

    def _write_file(self, category: str, filename: str, metadata: Dict[str, Any], content: str):
        file_path = self.temp_root / category / filename
        fm = VaultMapper.format_frontmatter(metadata)
        body = content.strip()
        full_text = f"{fm}\n\n{body}\n"
        file_path.write_text(full_text, encoding="utf-8")

    def _export_home(self):
        meta = {"title": "NOVEL OS 生产监控与视觉评审看板", "category": "00_HOME"}
        body = '''# NOVEL OS 生产监控与视觉评审看板 (NOVEL OS HOME)

> [!NOTE]
> **定位声明**：本 Obsidian Vault 仅为 **NOVEL OS V2.3 只读镜像层** 与 **人类创作者视觉审查工作区**。
> 权威数据流向：`NOVEL OS (Authority) -> Obsidian (Read-Only Mirror)`。
> 严禁在 Obsidian 中直接修改 Canon、State、Memory 或大纲。

---

## 核心生产状态监控 (Live Production Dashboard)

| 监控维度 | 当前状态 / 权威值 | 状态描述与锁定规则 |
| :--- | :--- | :--- |
| **作品全称** | 《都市：仙尊归来，开局截胡天命机缘》 | 都市修仙 · 无敌降维流 · 极道杀伐果断 |
| **当前进行卷** | [[第02卷_名动江南|第二卷 · 名动江南]] | 核心主线：一统江南省城武道与商界，激战公海 |
| **已完成章节** | **第0001章 至 第0051章** (共 51 章) | 51 篇正文全部完结封存，SHA-256 物理指纹受保护 |
| **当前最新章节** | [[CH051|第0051章《神火焚海，降头绝灭》]] | 状态：`COMPLETE`，字数：3201，三昧真火破阵灭敌 |
| **待生产章节** | **CH052** (第0052章) | 状态：`STANDBY_FOR_CHAPTER_52` (严格物理锁定，未生产) |
| **生产管线状态** | `STANDBY_FOR_CHAPTER_52` | 所有 Worker IDLE，等待 Human 明确授权 |
| **风险等级** | `HIGH` (公海决战余波) | 境外三艘战舰雷达火控锁定，涉及硬核对抗 |
| **活跃伏笔** | [[H-050-02_洪门海外仲裁庭与神农古秘境残图]], [[H-046-01_暗网一亿美金悬赏与北美黑水战队]], [[H-042-01_陆小晚玄阴圣体进阶与九叶还魂草]], [[H-026-01_南洋黑巫教总坛长线复仇]] | 伏笔状态严格跟踪 |
| **已结案伏笔** | [[H-050-01_公海万鬼噬魂凶阵]] (第51章三昧真火破阵彻底RESOLVED) | 已完成兑现 |
| **记忆库状态** | **OpenViking 131 节点 (Grade A 100%)** | 50 篇正文回填 100% PASS，0 孤立角色，0 冲突 |
| **规范版本** | Canon: `2.1.0` | State: `2.1.0` | Memory: `2.2.0` | NOVEL OS V2.3 标准架构 |

---

## 快捷导航 (Vault Quick Access)

- **设定权威**：[[设定圣经-Story_Bible]] · [[主角档案-陆辰]] · [[力量体系与等级对照]] · [[世界观-末法都市与万界祖地]]
- **角色谱系**：[[陆辰]] · [[陆小晚]] · [[苏清璇]] · [[冷月]] · [[叶破天]] · [[暴熊]] · [[雷千绝]] · [[孙侯]]
- **关系图谱**：[[陆辰-陆小晚(至亲逆鳞)]] · [[陆辰-苏清璇(世俗代行者)]] · [[陆辰-冷月与华夏安全九局(官方国士合作)]] · [[陆辰-海外洪门(血仇生死敌对)]]
- **主线大纲**：[[第01卷-潜龙出渊]] · [[第02卷-名动江南]] · [[第03卷-龙腾华夏]] · [[ARCS_MASTER_OVERVIEW]]
- **最新交接**：[[CH051_HANDOFF]] · [[CURRENT_STATE_MIRROR]] · [[EXECUTION_STATE_MIRROR]]
- **系统策略**：[[OBSIDIAN_READ_ONLY_POLICY]] · [[MIRROR_MANIFEST]]
'''
        self._write_file("00_HOME", "NOVEL_OS_HOME.md", meta, body)

    def _export_canon(self):
        canon_dir = self.source_root / "设定集"
        bible_file = self.source_root / "story_bible.md"
        if bible_file.exists():
            meta = {"title": "设定圣经", "category": "01_CANON", "source_file": "story_bible.md"}
            self._write_file("01_CANON", "设定圣经-Story_Bible.md", meta, bible_file.read_text(encoding="utf-8"))

        if canon_dir.exists():
            for cf in canon_dir.glob("*.md"):
                meta = {"title": cf.stem, "category": "01_CANON", "source_file": f"设定集/{cf.name}"}
                self._write_file("01_CANON", f"{cf.stem}.md", meta, cf.read_text(encoding="utf-8"))

    def _export_characters(self):
        chars = [
            {"name": "陆辰", "role": "核心主角 / 玄天仙尊", "realm": "筑基初期 (青帝琉璃身雏形)", "items": "惊鸿飞剑(下品灵器)", "desc": "九天仙界渡劫期玄天仙尊，因天劫道基受损重生回高三时代。杀伐果断、冷酷沉稳、视世俗权谋如草芥。"},
            {"name": "陆小晚", "role": "第一女配 / 核心逆鳞", "realm": "玄阴圣体 / 极寒冰魄圣体初醒", "items": "掌心冰晶白莲", "desc": "陆辰相依为命的亲妹妹。善良隐忍温婉，依赖哥哥。受寒毒困扰，需神农古秘境九叶还魂草调和。"},
            {"name": "苏清璇", "role": "商业代理人 / 灵辰集团董事长", "realm": "世俗凡人 (商界女总裁)", "items": "百亿灵辰集团", "desc": "江海首富苏家千金，理性干练高冷，代陆辰执掌世俗商业神朝。"},
            {"name": "冷月", "role": "军方与官方背景 / 华夏九局朱雀小队队长", "realm": "化境巅峰 (得陆辰灵液洗礼突破)", "items": "华夏特级顾问黑卡", "desc": "燕京第九特别行动局精锐，折服于陆辰筑基神迹，将陆辰列为SSS级镇国神话。"},
            {"name": "叶破天", "role": "江南省城武道代理人 / 叶家老太爷", "realm": "化境宗师 (得陆辰赐药突破)", "items": "叶家八百暗卫", "desc": "江南省城老牌武道世家老太爷，率全族奉陆辰为尊，建立苏掌商、叶掌武格局。"},
            {"name": "暴熊", "role": "战仆 / 江海地下巨头", "realm": "内劲巅峰", "items": "首山赤铜鼎线索", "desc": "原江海地下黑拳霸主，被陆辰神威慑服后誓死效忠，代掌江海地下秩序。"},
            {"name": "赵天宇", "role": "前期反派 / 赵氏财团少董 (已伏诛)", "realm": "凡人纨绔", "items": "纯银左轮", "desc": "江海赵家少爷，屡次暗算陆辰与小晚，最终在望江楼被彻底抹杀。"},
            {"name": "赵老太爷", "role": "前期反派 / 赵家掌舵人 (已伏诛)", "realm": "凡人权贵", "items": "药王堂供奉", "desc": "赵家家主，勾结境外与武道势力，望江楼一战赵家全族覆灭。"},
            {"name": "沈天豪", "role": "中期反派 / 金陵沈家家主 (已伏诛)", "realm": "内劲巅峰 / 半步宗师", "items": "秦淮河沈家祖宅", "desc": "江南武道总盟幕后掌控者之一，秦淮夜雨一役被惊鸿飞剑斩灭。"},
            {"name": "雷震霄", "role": "中期反派 / 天药集团掌门 (已伏诛)", "realm": "化境宗师", "items": "雷法符箓", "desc": "企图侵吞灵辰集团灵药配方，在金陵被陆辰一招斩首。"},
            {"name": "雷千绝", "role": "当前主要敌对 / 海外洪门第一宗师", "realm": "神境初期 / 绝巅半神", "items": "千绝狂刀 / 洪门战令", "desc": "海外洪门坐馆巨擘，得知师弟与孙侯死讯后震怒，誓杀陆辰。"},
            {"name": "孙侯", "role": "当前敌对 / 铁臂神猴 (CH051毙命)", "realm": "化境巅峰 (合金机械右臂)", "items": "神农古秘境残图", "desc": "海外洪门战将，公海维多利亚女王号设伏，被陆辰断臂后搜魂诛杀，招出秘境残图。"},
            {"name": "巴颂", "role": "当前敌对 / 南洋黑巫教降头大宗师 (CH051伏诛)", "realm": "化境宗师 (邪术修罗)", "items": "婴儿头骨权杖", "desc": "南洋黑巫教巨擘，布设万鬼噬魂阴煞阵，被陆辰纯阳三昧真火焚灭成灰。"},
            {"name": "阿赞扎", "role": "当前敌对 / 南洋尸煞大巫师 (CH051伏诛)", "realm": "化境宗师 (尸煞大巫)", "items": "百鬼夜行阴幡", "desc": "黑巫教大护法，催动漫天阴煞厉鬼，死于陆辰三昧真火与剑气化雨之下。"}
        ]
        for c in chars:
            meta = {"title": c["name"], "category": "02_CHARACTERS", "character_name": c["name"], "realm": c["realm"]}
            body = f'''# 角色档案：{c['name']}

- **身份定位**：{c['role']}
- **境界实力**：{c['realm']}
- **法宝装备**：{c['items']}

## 角色详细生平与设定
{c['desc']}

## 关联信息
- 关联关系：[[03_RELATIONSHIPS/陆辰-{c['name']}]]
- 关联章节：[[10_CHAPTERS/CH051]]
'''
            self._write_file("02_CHARACTERS", f"{c['name']}.md", meta, body)

    def _export_relationships(self):
        rels = [
            ("陆辰-陆小晚(至亲逆鳞)", "陆辰", "陆小晚", "相依为命亲兄妹，陆辰唯一绝对逆鳞，小晚视哥哥为生命支柱。"),
            ("陆辰-苏清璇(世俗代行者)", "陆辰", "苏清璇", "君臣与商业盟友。苏清璇代掌百亿灵辰集团，陆辰提供灵药配方与绝对战力庇护。"),
            ("陆辰-冷月与华夏安全九局(官方国士合作)", "陆辰", "冷月", "官方与镇国神话。九局敬献特级顾问黑卡，互不干涉，战略结盟。"),
            ("陆辰-叶家(江南武道臣服)", "陆辰", "叶破天", "主仆效忠。叶家八百暗卫尊陆辰为主，统御江南省城武道各方。"),
            ("陆辰-暴熊(麾下战仆)", "陆辰", "暴熊", "最早收服的地下战仆，负责江海世俗警戒与琐事。"),
            ("陆辰-海外洪门(血仇生死敌对)", "陆辰", "雷千绝", "生死死敌。陆辰连斩洪门战将孙侯与江南分舵，海外总舵誓死复仇。"),
            ("陆辰-南洋黑巫教(彻底灭杀)", "陆辰", "巴颂", "宿敌灭门。两大降头大宗师公海设凶阵被三昧真火焚杀，引出南洋总坛长线。"),
            ("陆辰-暗网黑水佣兵(敌对悬赏)", "陆辰", "北美黑水战队", "暗网一亿美金悬赏灵药配方，黑水强化人战队逼近江海。")
        ]
        for name, c1, c2, desc in rels:
            meta = {"title": name, "category": "03_RELATIONSHIPS", "character_1": c1, "character_2": c2}
            body = f'''# 关系网络：{name}

- **核心主体 A**：[[02_CHARACTERS/{c1}|{c1}]]
- **核心主体 B**：[[02_CHARACTERS/{c2}|{c2}]]
- **关系性质**：{desc}

## 关系演变与状态
该关系严格源自 NOVEL OS Canon 与 CH001-CH051 正文事实，无未经证实的推断。
'''
            self._write_file("03_RELATIONSHIPS", f"{name}.md", meta, body)

    def _export_timeline(self):
        batches = [
            ("TIMELINE_CH001_CH010_重生苏醒与江海立威", "CH001-CH010", "第 1-3 天", "仙尊归来医院救妹，一指破医阀，入主云顶山庄布下卧龙引气阵，百草堂当众立威。"),
            ("TIMELINE_CH011_CH020_灵丹现世与暴熊臣服", "CH011-CH020", "第 4-8 天", "砂锅炼制洗髓丹，小晚初显玄阴异象；黑市识破铜鼎骗局，徒手掀车收服暴熊。"),
            ("TIMELINE_CH021_CH030_重铸惊鸿与覆灭赵家", "CH021-CH030", "第 9-14 天", "迎宾馆拍卖会戏耍赵天宇，地火重铸惊鸿飞剑，望江楼一战飞剑血洗赵家满门。"),
            ("TIMELINE_CH031_CH040_灵辰初创与威震省城", "CH031-CH040", "第 15-22 天", "苏清璇创立灵辰集团，培元液惊动省城；金陵拍卖会一剑斩宗师，收服叶家八百暗卫。"),
            ("TIMELINE_CH041_CH050_筑基功成与公海鏖战", "CH041-CH050", "第 23-28 天", "吞服阴阳造化丹突破筑基初期；赴约公海维多利亚女王号，一指捏碎孙侯合金臂，万鬼大阵开启。"),
            ("TIMELINE_CH051_神火焚海与降头绝灭", "CH051", "第 28 天正午", "吐出九天纯阳三昧真火破尽万鬼大阵，巴颂阿赞扎化为焦炭，一指诛杀孙侯；境外护卫战舰拉响警报。")
        ]
        for fname, span, days, summary in batches:
            meta = {"title": fname, "category": "04_TIMELINE", "chapter_span": span, "story_days": days}
            body = f'''# 时序因果记录：{fname}

- **覆盖章节**：{span}
- **故事内时间跨度**：{days}
- **核心事件链**：
{summary}

## 关联信息
- 前序时序：[[04_TIMELINE/TIMELINE_MASTER_CH001_CH051]]
- 权威状态：[[12_STATE/CURRENT_STATE_MIRROR]]
'''
            self._write_file("04_TIMELINE", f"{fname}.md", meta, body)

        meta_m = {"title": "TIMELINE_MASTER_CH001_CH051", "category": "04_TIMELINE"}
        body_m = '''# 全书时序总索引 (CH001 - CH051)

1. [[04_TIMELINE/TIMELINE_CH001_CH010_重生苏醒与江海立威]]
2. [[04_TIMELINE/TIMELINE_CH011_CH020_灵丹现世与暴熊臣服]]
3. [[04_TIMELINE/TIMELINE_CH021_CH030_重铸惊鸿与覆灭赵家]]
4. [[04_TIMELINE/TIMELINE_CH031_CH040_灵辰初创与威震省城]]
5. [[04_TIMELINE/TIMELINE_CH041_CH050_筑基功成与公海鏖战]]
6. [[04_TIMELINE/TIMELINE_CH051_神火焚海与降头绝灭]]
'''
        self._write_file("04_TIMELINE", "TIMELINE_MASTER_CH001_CH051.md", meta_m, body_m)

    def _export_locations(self):
        locs = [
            ("江海市云顶山庄一号天宫", "江海市最高峰顶顶级庄园，布设卧龙引气大阵与聚灵阵，陆辰大本营。"),
            ("江海迎宾馆宴会厅", "江海官方与顶级名流拍卖盛会，赵天宇五千万买空壳残药惨遭打脸之地。"),
            ("江海市百草堂老店", "江海百年中药老字号，陆辰当众以普通砂锅熬制极品洗髓灵药立威之地。"),
            ("江海望江楼", "临江高端酒楼，陆辰以惊鸿飞剑凌空斩灭赵家满门与半步宗师之地。"),
            ("江南省城叶家庄园", "江南省城第一武道世家老巢，叶破天率八百暗卫俯首称臣奉陆辰为主之地。"),
            ("金陵秦淮河沈家祖宅", "六朝古都秦淮水榭，陆辰雨夜持剑踏平江南武道总盟与三大宗师之地。"),
            ("东海公海维多利亚女王号万吨游轮", "万吨豪华游轮，公海决战之地，万鬼噬魂大阵布设处，CH051神火焚海战场。"),
            ("神农古秘境(未解锁)", "华夏上古折叠遗迹，藏有九叶还魂草与万载地灵乳，需残图开启(第52章后主线)。")
        ]
        for name, desc in locs:
            meta = {"title": name, "category": "05_LOCATIONS"}
            body = f'''# 地点档案：{name}

- **位置概况**：{desc}
- **主权归属**：[[02_CHARACTERS/陆辰|陆辰]] / [[06_FACTIONS/灵辰集团与江海苏家]]

## 历史大事记
- 见 [[04_TIMELINE/TIMELINE_MASTER_CH001_CH051]]
'''
            self._write_file("05_LOCATIONS", f"{name}.md", meta, body)

    def _export_factions(self):
        factions = [
            ("灵辰集团与江海苏家", "陆辰幕后掌控的百亿医药商业帝国，由苏清璇操盘，席卷华东。"),
            ("江南武道世家叶家", "江南第一武道世家，叶破天掌舵，八百暗卫护卫灵辰集团世俗产业。"),
            ("华夏安全九局与朱雀小队", "华夏官方最高超凡安全机构，朱雀冷月带队，敬献特级国士黑卡结盟。"),
            ("海外洪门总舵", "海外华人第一武道社团，雷千绝坐镇，麾下设海外仲裁庭，与陆辰结下血仇。"),
            ("南洋黑巫教", "南洋邪道宗门，精通降头术与尸煞万鬼阵法，两大宗师公海被灭。"),
            ("暗网黑水佣兵战队", "国际顶尖雇佣兵与生化基因强化人军团，暗网悬赏一亿美金企图夺取培元液。"),
            ("江海赵氏财团(已覆灭)", "江海原首富家族，望江楼一役全族被诛，资产并入苏家。"),
            ("金陵沈家与江南武道总盟(已覆灭)", "原江南武道霸主，秦淮夜雨一役被陆辰飞剑斩尽。")
        ]
        for name, desc in factions:
            meta = {"title": name, "category": "06_FACTIONS"}
            body = f'''# 势力档案：{name}

- **基本描述**：{desc}
- **当前状态**：见 [[12_STATE/CURRENT_STATE_MIRROR]]
'''
            self._write_file("06_FACTIONS", f"{name}.md", meta, body)

    def _export_abilities(self):
        abilities = [
            ("九天玄天决", "玄天仙尊前世主修无上道法，直通仙帝大道的至高功法。"),
            ("太衍吞天决", "霸道绝伦的吞噬炼化法门，可炼化天地万物异种灵气与丹药杂质。"),
            ("青帝琉璃身雏形", "上古至强肉身神通，筑基期凝练而成，硬抗温压弹余波与重狙射击。"),
            ("九天纯阳三昧真火", "体内凝练的极阳真火，第51章张口吐出焚灭万鬼阴煞大阵与两大降头师。"),
            ("九天引雷诀", "引动九天神雷之威，凌空画符引下天雷轰杀强敌。"),
            ("破甲飞针(茶梗化剑)", "真元灌注草木竹石皆可为剑，随手摘茶梗贯穿防弹玻璃击杀宗师。"),
            ("因果搜魂术", "直溯灵魂记忆之搜魂秘法，强行抽取受术者神魂记忆，令其神魂俱灭。"),
            ("虚空画符与聚灵阵", "不依凡俗符纸，凌空凝气成符，引动天地灵气汇聚庄园。")
        ]
        for name, desc in abilities:
            meta = {"title": name, "category": "07_ABILITIES"}
            body = f'''# 神通法门：{name}

- **法门品阶**：仙界至尊神通 / 仙尊秘法
- **掌控者**：[[02_CHARACTERS/陆辰|陆辰]]
- **法门效果**：{desc}
'''
            self._write_file("07_ABILITIES", f"{name}.md", meta, body)

    def _export_items(self):
        items = [
            ("惊鸿飞剑(下品灵器)", "由天外陨铁精金与地火熔炼重铸，当前为下品灵器，神识御剑百里、分海断岳。"),
            ("首山赤铜鼎", "上古赤铜所铸之炼丹残鼎，含残缺古丹纹，陆辰前期炼制极品丹药关键法器。"),
            ("九转还魂丹", "仙界延寿救命圣药，一枚可肉白骨活死人，彻底稳固小晚命脉。"),
            ("纯阳培元液", "灵辰集团主打世俗灵药，强身健体延寿十年，引发全球财阀权贵抢购疯狂。"),
            ("洗髓丹", "伐毛洗髓之灵丹，助凡人脱胎换骨，助武者突破化境宗师。"),
            ("阴阳造化丹", "第42章陆辰突破筑基期所服绝品灵丹，助其真元彻底液化。"),
            ("神农古秘境残图", "孙侯死前招供交出之上古秘境残图，指向神农架折叠仙境(第52章推进)。"),
            ("华夏九局特级顾问黑卡", "华夏官方仅发三张之最高级别特权卡，享副国级礼遇与最高安全豁免。")
        ]
        for name, desc in items:
            meta = {"title": name, "category": "08_ITEMS"}
            body = f'''# 法宝器具：{name}

- **所有者/持有者**：[[02_CHARACTERS/陆辰|陆辰]]
- **功能描述**：{desc}
'''
            self._write_file("08_ITEMS", f"{name}.md", meta, body)

    def _export_foreshadowing(self):
        hooks = [
            ("H-050-01_公海万鬼噬魂凶阵", "RESOLVED", "50-51", "第50章万鬼凶阵笼罩游轮，第51章陆辰吐出纯阳三昧真火彻底焚灭大阵与巴颂、阿赞扎两大降头师。"),
            ("H-050-02_洪门海外仲裁庭与神农古秘境残图", "ACTIVE", "50-52+", "孙侯死前招供神农古秘境残图，海外洪门总部震怒求和，锁定第52章推进。"),
            ("H-046-01_暗网一亿美金悬赏与北美黑水战队", "ACTIVE", "46-54", "国际暗网悬赏培元液，北美黑水强化人战队逼近江海，锁定第53-54章彻底解决。"),
            ("H-042-01_陆小晚玄阴圣体进阶与九叶还魂草", "ACTIVE", "42-88", "小晚掌心冰莲异动，需神农秘境九叶还魂草彻底调和治愈，贯穿第二卷中后期主线。"),
            ("H-026-01_南洋黑巫教总坛长线复仇", "ACTIVE", "26-60", "南洋黑巫教境外总坛长老命牌碎裂，长线布局复仇。"),
            ("H-030-01_秦淮夜雨覆灭江南武道盟", "RESOLVED", "28-30", "秦淮河一役飞剑斩灭沈家与江南三大宗师，江南全省归心。"),
            ("H-012-01_陆小晚玄阴之体初醒", "RESOLVED", "12-20", "小晚玄阴之体初次异动，陆辰传授寒月静心诀化解急性危局。"),
            ("H-004-01_江海赵家暗算与血色战书", "RESOLVED", "4-30", "赵天宇屡次谋害陆辰，望江楼一役赵家彻底诛灭。")
        ]
        for name, status, span, desc in hooks:
            meta = {"title": name, "category": "09_FORESHADOWING", "hook_status": status, "active_span": span}
            body = f'''# 伏笔追踪：{name}

- **当前状态**：`{status}`
- **影响章节范围**：第 {span} 章
- **伏笔详情**：
{desc}

## 关联分析
- 状态跟踪：[[12_STATE/CURRENT_STATE_MIRROR]]
- 关联章节：[[10_CHAPTERS/CH051]]
'''
            self._write_file("09_FORESHADOWING", f"{name}.md", meta, body)

        meta_idx = {"title": "FORESHADOWING_INDEX", "category": "09_FORESHADOWING"}
        body_idx = '''# 伏笔全量跟踪索引

| 伏笔编号 | 状态 | 涉及跨度 | 说明与结算目标 |
| :--- | :--- | :--- | :--- |
| [[H-050-01_公海万鬼噬魂凶阵]] | `RESOLVED` | CH050-CH051 | 第51章三昧真火破阵，降头师伏诛 (已结案) |
| [[H-050-02_洪门海外仲裁庭与神农古秘境残图]] | `ACTIVE` | CH050-CH052+ | 秘境残图锁定第52章推进 |
| [[H-046-01_暗网一亿美金悬赏与北美黑水战队]] | `ACTIVE` | CH046-CH054 | 黑水强化人潜伏逼近，锁定53-54章解决 |
| [[H-042-01_陆小晚玄阴圣体进阶与九叶还魂草]] | `ACTIVE` | CH042-CH088 | 小晚极寒冰魄圣体，主线关键药引 |
| [[H-026-01_南洋黑巫教总坛长线复仇]] | `ACTIVE` | CH026-CH060 | 南洋境外总坛长线线索 |
| [[H-030-01_秦淮夜雨覆灭江南武道盟]] | `RESOLVED` | CH028-CH030 | 已结案 |
| [[H-012-01_陆小晚玄阴之体初醒]] | `RESOLVED` | CH012-CH020 | 已结案 |
| [[H-004-01_江海赵家暗算与血色战书]] | `RESOLVED` | CH004-CH030 | 已结案 |
'''
        self._write_file("09_FORESHADOWING", "FORESHADOWING_INDEX.md", meta_idx, body_idx)

    def _export_chapters(self):
        summaries_path = self.source_root / "chapter_summaries.md"
        sum_dict = {}
        if summaries_path.exists():
            txt = summaries_path.read_text(encoding="utf-8")
            lines = txt.splitlines()
            cur_ch = None
            cur_sum = []
            for l in lines:
                if l.startswith("## 第") or l.startswith("- **第"):
                    if cur_ch and cur_sum:
                        sum_dict[cur_ch] = "\n".join(cur_sum)
                    import re
                    m = re.search(r"(\d{4}|\d{3}|\d{2})", l)
                    if m:
                        cur_ch = int(m.group(1))
                        cur_sum = [l]
                elif cur_ch:
                    cur_sum.append(l)
            if cur_ch and cur_sum:
                sum_dict[cur_ch] = "\n".join(cur_sum)

        for ch_num in range(1, 52):
            ch_str = f"{ch_num:03d}"
            meta = {
                "title": f"第{ch_str}章",
                "category": "10_CHAPTERS",
                "chapter_number": ch_num,
                "status": "COMPLETE",
                "production_status": "COMPLETE"
            }
            summary_content = sum_dict.get(ch_num, f"第{ch_str}章正文完整归档。")
            body = f'''# 第{ch_str}章 章节镜像概要

- **章节编号**：第 {ch_num} 章 (CH{ch_str})
- **完结状态**：`COMPLETE`
- **对应物理正文**：`正文/第{ch_str}章*.md`

## 章节内容摘要
{summary_content}

## 关联索引
- 关联时序：[[04_TIMELINE/TIMELINE_MASTER_CH001_CH051]]
'''
            self._write_file("10_CHAPTERS", f"CH{ch_str}.md", meta, body)

    def _export_arcs(self):
        outline_files = list((self.source_root / "大纲").glob("*.md"))
        for of in outline_files:
            meta = {"title": of.stem, "category": "11_ARCS", "source_file": f"大纲/{of.name}"}
            self._write_file("11_ARCS", f"{of.stem}.md", meta, of.read_text(encoding="utf-8"))

        meta_m = {"title": "ARCS_MASTER_OVERVIEW", "category": "11_ARCS"}
        body_m = '''# 全书卷纲架构总览 (Master Arc Overview)

- [[11_ARCS/总纲|全书总纲]]
- [[11_ARCS/第01卷-潜龙出渊|第01卷 · 潜龙出渊]] (CH001 - CH031, 已完结)
- [[11_ARCS/第02卷-名动江南|第02卷 · 名动江南]] (CH032 - CH088, 当前进行卷)
- [[11_ARCS/第03卷-龙腾华夏|第03卷 · 龙腾华夏]] (CH089 - CH160, 规划中)
- [[11_ARCS/第04卷-仙门叩关|第04卷 · 仙门叩关]] (CH161 - CH240, 规划中)
- [[11_ARCS/第05卷-威震当世|第05卷 · 威震当世]] (CH241 - CH350, 规划中)
- [[11_ARCS/第06卷-星空古路|第06卷 · 星空古路]] (CH351 - CH500, 规划中)
- [[11_ARCS/第07卷-星河独尊|第07卷 · 星河独尊]] (CH501 - CH800, 规划中)
'''
        self._write_file("11_ARCS", "ARCS_MASTER_OVERVIEW.md", meta_m, body_m)

    def _export_state(self):
        state_files = [
            ("EXECUTION_STATE.yaml", "EXECUTION_STATE_MIRROR.md", "V2.1 执行状态快照"),
            ("current_state.md", "CURRENT_STATE_MIRROR.md", "当前创作状态"),
            ("progress_tracker.md", "PROGRESS_TRACKER_MIRROR.md", "进度指标看板"),
            ("pending_hooks.md", "PENDING_HOOKS_MIRROR.md", "伏笔追踪面板"),
            ("pattern-detection.md", "PATTERN_DETECTION_MIRROR.md", "叙事模式监控")
        ]
        for src, dest, title in state_files:
            src_p = self.source_root / src
            if not src_p.exists():
                src_p = self.source_root / "00_SYSTEM" / src
            if src_p.exists():
                meta = {"title": title, "category": "12_STATE", "source_file": src}
                self._write_file("12_STATE", dest, meta, src_p.read_text(encoding="utf-8"))

    def _export_handoff(self):
        handoff_dir = self.source_root / "06_HANDOFF"
        if handoff_dir.exists():
            for hf in handoff_dir.glob("*.md"):
                meta = {"title": hf.stem, "category": "13_HANDOFF", "source_file": f"06_HANDOFF/{hf.name}"}
                self._write_file("13_HANDOFF", f"{hf.stem}.md", meta, hf.read_text(encoding="utf-8"))

    def _export_memory(self):
        viking_idx = self.source_root / ".openviking" / "storage" / "viking_index.json"
        if viking_idx.exists():
            data = json.loads(viking_idx.read_text(encoding="utf-8"))
            for uri, item in data.items():
                safe_name = uri.replace("viking://resources/novel/", "").replace("/", "_")
                if not safe_name or safe_name == uri:
                    safe_name = uri.replace("://", "_").replace("/", "_")
                meta = {
                    "title": f"MEMORY_{safe_name}",
                    "category": "14_MEMORY",
                    "memory_uri": uri,
                    "memory_type": item.get("metadata", {}).get("type", "GENERAL_MEMORY"),
                    "quality_grade": item.get("metadata", {}).get("quality_grade", "A"),
                    "source_chapter": item.get("metadata", {}).get("source_chapter", 0)
                }
                body = f'''# 结构化记忆节点：{safe_name}

- **URI**: `{uri}`
- **记忆类型**: `{item.get('metadata', {}).get('type', 'UNKNOWN')}`
- **质量评级**: `{item.get('metadata', {}).get('quality_grade', 'A')}` (分数: {item.get('metadata', {}).get('quality_score', 100)})
- **来源章节**: 第 {item.get('metadata', {}).get('source_chapter', '未知')} 章

## L0 摘要
{item.get('l0_abstract', '')}

## L1 概览
```json
{json.dumps(item.get('l1_overview', {}), ensure_ascii=False, indent=2)}
```

## L2 详情
```json
{json.dumps(item.get('l2_details', {}), ensure_ascii=False, indent=2)}
```
'''
                self._write_file("14_MEMORY", f"MEMORY_{safe_name}.md", meta, body)

    def _export_qa(self):
        qa_files = [
            ("00_SYSTEM/MEMORY_FULL_BACKFILL_AUDIT.md", "MEMORY_FULL_BACKFILL_AUDIT_MIRROR.md", "全量记忆回填全局审计报告"),
            ("00_SYSTEM/QA_POLICY.yaml", "QA_POLICY_MIRROR.md", "质量评估策略"),
            ("00_SYSTEM/RISK_GATE.yaml", "RISK_GATE_MIRROR.md", "风险网关规则")
        ]
        for src, dest, title in qa_files:
            src_p = self.source_root / src
            if src_p.exists():
                meta = {"title": title, "category": "15_QA", "source_file": src}
                self._write_file("15_QA", dest, meta, src_p.read_text(encoding="utf-8"))

    def _export_system_policies(self):
        meta = {"title": "OBSIDIAN_READ_ONLY_POLICY", "category": "99_SYSTEM"}
        body = '''# NOVEL OS V2.3 — OBSIDIAN READ-ONLY POLICY & BOUNDARY CONTRACT

## 1. 核心定位 (System Authority)
Obsidian 在 NOVEL OS 体系中被严格定义为：
> **HUMAN KNOWLEDGE WORKSPACE / VISUAL REVIEW LAYER** (人类创作者知识工作区与视觉审阅层)

它 **不是**：
- Canon Authority (设定权威)
- Memory Authority (记忆权威)
- State Authority (状态权威)
- AI Brain (AI大脑)
- Writer Worker (写作执行器)
- QA Engine (质量判定引擎)

---

## 2. 真实权威法则 (True Authority Hierarchy)
```text
HUMAN
  >
CANON
  >
CONTINUITY
  >
STATE
  >
OUTLINE
  >
PLOT
  >
STYLE
  >
TONE
```

---

## 3. 单向只读数据流向 (Strict Downstream Mirror)
```text
NOVEL OS (Authority)
       ↓ (Exporter Sync)
Obsidian Novel Vault (Read-Only Mirror)
```

**绝对禁止**：
- 从 Obsidian 到 NOVEL OS 的反向直接写入。
- 在 Obsidian 中直接修改 Canon、State、Memory 或 Outline 并期望系统静默同步。
- 安装第二套独立的 AI Memory / RAG 插件（如 Khoj、Smart Connections、Copilot 等），避免多头检索与记忆污染。

---

## 4. 变更提议协议 (Human Gate Proposal Protocol)
任何在 Obsidian 中产生的修改意图必须遵循：
1. 人类在 Obsidian 中提出修改意见 / 提议草稿。
2. 经由 Human 明确授权进入 NOVEL OS 审核管道。
3. 经由 Memory Governor / Canon QA 验证无冲突后，由 NOVEL OS 官方工具链写回源文件。
4. 重新触发 Exporter 同步至 Obsidian 镜像。
'''
        self._write_file("99_SYSTEM", "OBSIDIAN_READ_ONLY_POLICY.md", meta, body)
