import os
import re  # 导入正则表达式模块

class LamReadFileList:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "keywords1": ("STRING", {"default": "*", "description": "First keyword(s) to filter filenames, separated by '/'"}),
            },
            "optional": {
                "folder_path": ("STRING", { "description": "Path to the folder containing files"}),
                "input_list": ("LIST", { "description": "Alternative list of files to filter"}),
                "listin": ("LIST", {"description": "Unformatted text list to filter"}),
                "file_formats1": ("STRING", { "default": "*", "description": "File format(s) for Keywords 1, separated by '/'"}),
                "dummy_parameter": ("INT", {"default": 0}),  # 添加虚拟参数
            }
        }

    RETURN_TYPES = ("LIST", "LIST", "INT")
    RETURN_NAMES = ("filtered_results", "listout", "file_count")
    FUNCTION = "filter_files"
    CATEGORY = "lam"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, should_change=True, *args, **kwargs):
        if should_change:
            return float("NaN")
        else:
            return False

    def filter_files(self, keywords1, folder_path=None, input_list=None, listin=None, dummy_parameter=0, **kwargs):
        # 优先使用 listin，如果未提供则使用 input_list，如果未提供则使用 folder_path
        if listin and len(listin) > 0:
            all_files = listin
        elif input_list and len(input_list) > 0:
            all_files = input_list
        elif folder_path:
            #目录不存在创建目录
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]
        else:
            all_files = []

        filtered_results = []
        unformatted_list = []  # 用于存储未格式化的文件列表
        total_files_count = 0  # 初始化文件计数

        # 获取 keywords1 作为必填字段
        keywords = keywords1.split("/")
        file_formats = kwargs.get("file_formats1", "").split("/")

        filtered_list = []

        for file in all_files:
            # 忽略文件夹，只处理文件
            if not os.path.isfile(file):
                continue

            filename, ext = os.path.splitext(os.path.basename(file))

            # 处理文件格式的通配符和 OR 逻辑
            format_match = False
            for fmt in file_formats:
                if fmt == "*":
                    format_match = True
                    break
                elif "|" in fmt:
                    # OR 逻辑处理
                    or_formats = fmt.split('|')
                    if any(ext.lower().lstrip('.') == or_fmt.lower() for or_fmt in or_formats):
                        format_match = True
                        break
                else:
                    if ext.lower().lstrip('.') == fmt.lower():
                        format_match = True
                        break

            # 处理关键词通配符组合，使用不区分大小写的正则表达式，并处理空格视为 AND 的逻辑
            keyword_match = True  # 初始化为 True
            for keyword in keywords:
                # 分割关键词，处理空格为 AND 逻辑
                sub_keywords = keyword.split()
                for sub_keyword in sub_keywords:
                    # 否定匹配：检查是否有 "!" 否定符号
                    if sub_keyword.startswith("!"):
                        # 匹配不应包含的内容
                        pattern = re.compile(re.escape(sub_keyword[1:]).replace(r'\*', '.*'), re.IGNORECASE)
                        if pattern.search(filename):
                            keyword_match = False
                            break
                    else:
                        # 处理 OR 的逻辑
                        or_parts = sub_keyword.split('|')
                        or_match = False
                        for part in or_parts:
                            # 处理通配符的特殊情况
                            if part.startswith('*') and not part.endswith('*'):
                                # 匹配右边有内容的情况
                                pattern = re.compile(r'.+' + re.escape(part[1:]) + r'\b', re.IGNORECASE)
                            elif part.endswith('*') and not part.startswith('*'):
                                # 匹配左边有内容的情况
                                pattern = re.compile(r'\b' + re.escape(part[:-1]) + r'.+', re.IGNORECASE)
                            else:
                                # 通用匹配
                                pattern = re.compile(re.escape(part).replace(r'\*', '.*'), re.IGNORECASE)

                            if pattern.search(filename):
                                or_match = True
                                break

                        if not or_match:
                            keyword_match = False
                            break

                if not keyword_match:
                    break

            # 如果格式和关键词都匹配，添加到过滤列表
            if format_match and keyword_match:
                filtered_list.append(file)

        # 将过滤后的文件列表格式化，每个文件在新行显示
        formatted_list = "\n".join(filtered_list)
        filtered_results.append(formatted_list)

        # 保存未格式化的文件列表
        unformatted_list.extend(filtered_list)

        # 统计文件数量
        total_files_count += len(filtered_list)

        # 返回格式化列表、未格式化列表、文件计数
        return (filtered_results, unformatted_list, total_files_count)

NODE_CLASS_MAPPINGS = {
    "LamReadFileList": LamReadFileList
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LamReadFileList": "读取文件列表"
}
