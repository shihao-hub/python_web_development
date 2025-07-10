import re


def extract_item_descriptions(lua_content):
    """
    从 Lua 内容中提取物品描述
    格式示例:
        -- 物品名称
        STRINGS[upper("item_id")] = L
            and [[
            描述内容
            ]]
            or [[]];
    """
    pattern = r'--\s*(.*?)\nSTRINGS\[upper\(".*?"\)\]\s*=\s*L\s+and\s+\[\[\s*(.*?)\s*\]\]'
    items = re.findall(pattern, lua_content, re.DOTALL)
    return items


def format_markdown(items):
    """将提取的物品格式化为 Markdown"""
    md_content = ""
    for name, description in items:
        # 清理描述内容（移除多余缩进和空格）
        cleaned_desc = "\n".join(line.strip() for line in description.splitlines() if line.strip())
        md_content += f"---\n{name}\n\n{cleaned_desc}\n\n"
    return md_content


def convert_lua_to_markdown(lua_file_path, output_md_path):
    """主函数：读取 Lua 文件并生成 Markdown 文件"""
    try:
        with open(lua_file_path, 'r', encoding='utf-8') as f:
            lua_content = f.read()

        items = extract_item_descriptions(lua_content)

        if not items:
            print("未找到有效的物品描述")
            return

        markdown_content = format_markdown(items)

        with open(output_md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        print(f"成功生成 Markdown 文件: {output_md_path}")
        print(f"共提取 {len(items)} 个物品描述")

    except Exception as e:
        print(f"处理过程中出错: {e}")


if __name__ == "__main__":
    # 配置输入输出路径
    input_lua_file = "init_tooltips.lua"  # 输入的 Lua 文件路径
    output_md_file = "output.md"  # 输出的 Markdown 文件路径

    convert_lua_to_markdown(input_lua_file, output_md_file)
