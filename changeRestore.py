import os,sys
#读取py文件为text字符串
editlist=[{
	"name": "server.py",
	"isEditStr":"elif 'prompt_id' in json_data:",
	"changs":[
		{
			"primit":'''else:
                return web.json_response({"error": "no prompt", "node_errors": []}, status=400)''',
			"edit":'''elif 'prompt_id' in json_data:
                return web.json_response(json_data)
            else:
                return web.json_response({"error": "no prompt", "node_errors": []}, status=400)'''
		},
		{
			"primit":'''info['display_name'] = nodes.NODE_DISPLAY_NAME_MAPPINGS[node_class] if node_class in nodes.NODE_DISPLAY_NAME_MAPPINGS.keys() else node_class''',
			"edit":'''info['display_name'] = self.displayName[node_class] if hasattr(self,'displayName') and node_class in self.displayName.keys() else nodes.NODE_DISPLAY_NAME_MAPPINGS[node_class] if node_class in nodes.NODE_DISPLAY_NAME_MAPPINGS.keys() else node_class'''
		}
	]
},{
	"name": "comfy/cli_args.py",
	"isEditStr":"parser.add_argument(\"--cluster\", action=\"store_true\"",
	"changs":[
		{
			"primit":'''parser.add_argument("--multi-user", action="store_true", help="Enables per-user storage.")''',
			"edit":'''parser.add_argument("--multi-user", action="store_true", help="Enables per-user storage.")

parser.add_argument("--cluster", action="store_true", help="是否集群")
parser.add_argument("--isSection", action="store_true", help="分段负载")
parser.add_argument("--isMain", action="store_true", help="是否为主")
parser.add_argument("--basePath", type=str, default="127.0.0.1", help="服务地址")'''
		}
	]
}
]
filePath=os.path.dirname(os.path.abspath(__file__))
print('当前目录：',filePath)
base_path=filePath.split('custom_nodes')[0]
backupPath=os.path.join(filePath,'backup')
def read_py_file(file_path):
	with open(file_path, 'r',encoding='utf-8') as file:
		text = file.read()
	return text

def write_py_file(file_path, text):
	filePath=os.path.dirname(file_path)
	if not os.path.exists(filePath):
			os.makedirs(filePath)
	with open(file_path, 'w',encoding='utf-8') as file:
		file.write(text)


if __name__ == '__main__':
	isRestore='--res' in sys.argv
	print('-------开始还原-------' if isRestore else '--------开始修改--------')
	for i in editlist:
		file_path=os.path.join(base_path,i['name'])
		if not os.path.exists(file_path):
			print(file_path+'文件不存在')
			continue
		if not os.path.exists(backupPath):
			os.makedirs(backupPath)
		
		if isRestore:
			if not os.path.exists(os.path.join(backupPath,i['name'])):
				print('备份文件'+os.path.join(backupPath,i['name'])+'不存在无法还原')
				continue
			text=read_py_file(os.path.join(backupPath,i['name']))
			write_py_file(file_path, text)
		else:
			text=read_py_file(file_path)
			if text.find(i['isEditStr'])!=-1:
				continue
			write_py_file(os.path.join(backupPath,i['name']), text)
			textOld=text+''
			for j in i['changs']:
				if text.find(j['primit'])==-1:
					print(i['name']+'未找到修改位置，修改失败')
					text=textOld
					break
				text=text.replace(j['primit'],j['edit'])
			write_py_file(file_path, text)
	print('-------还原完成-------' if isRestore else '--------修改完成--------')

