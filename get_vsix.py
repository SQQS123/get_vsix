import requests
import json

def get_vsix_url(publisher, extension_name, version=None):
    """
    获取VS Code插件的.vsix文件地址
    :param publisher: 插件发布者的ID
    :param extension_name: 插件的名称
    :param version: 可选，指定插件的版本号
    :return: vsix文件的下载地址或None
    """
    api_url = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"
    headers = {
        "Accept": "application/json;api-version=6.0-preview.1",
        "Content-Type": "application/json"
    }
    body = {
        "filters": [
            {
                "criteria": [
                    {"filterType": 7, "value": f"{publisher}.{extension_name}"}
                ]
            }
        ],
        "flags": 103
    }
    
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(body))
        response.raise_for_status()
        data = response.json()
        
        # 获取插件的最新版本或指定版本
        extensions = data.get("results", [{}])[0].get("extensions", [{}])
        for ext in extensions:
            versions = ext.get("versions", [])
            for v in versions:
                if version and v["version"] != version:
                    continue
                files = v.get("files", [])
                for file_info in files:
                    if file_info.get("assetType") == "Microsoft.VisualStudio.Services.VSIXPackage":
                        return file_info.get("source")
        return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# 示例：获取Python插件的最新版本的vsix地址
publisher = "ms-python"
extension_name = "python"
version = None  # 如果需要指定版本，可以设置为"2.0.0"等
vsix_url = get_vsix_url(publisher, extension_name, version)

if vsix_url:
    print(f"VSIX file URL: {vsix_url}")
else:
    print("Failed to get VSIX file URL.")

