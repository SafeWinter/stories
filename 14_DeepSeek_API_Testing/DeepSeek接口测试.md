你可以使用 PowerShell 脚本来实现这个功能。以下是一个示例脚本，它接受一个字符串作为输入，并根据分号前的部分创建快捷方式的名称，分号后的部分作为快捷方式的链接。

```powershell
param (
    [string]$inputString
)

# 分割输入字符串
$parts = $inputString -split ';'
if ($parts.Length -ne 2) {
    Write-Host "输入的字符串格式不正确，应该包含一个分号分隔的名称和链接。"
    exit
}

$name = $parts[0].Trim()
$url = $parts[1].Trim()

# 创建快捷方式的路径
$shortcutPath = "$PWD\$name.url"

# 创建快捷方式内容
$shortcutContent = @"
[InternetShortcut]
URL=$url
"@

# 将内容写入快捷方式文件
Set-Content -Path $shortcutPath -Value $shortcutContent

Write-Host "快捷方式已创建: $shortcutPath"
```

### 使用说明：
1. 将上述脚本保存为一个 `.ps1` 文件，例如 `CreateShortcut.ps1`。
2. 打开 PowerShell 并导航到脚本所在的目录。
3. 运行脚本并传入字符串作为参数，例如：

```powershell
.\CreateShortcut.ps1 "技术写作的首要诀窍;https://www.ruanyifeng.com/blog/2024/01/weekly-issue-288.html"
```

### 解释：
- `param ([string]$inputString)`：定义一个参数 `$inputString`，用于接收输入的字符串。
- `$parts = $inputString -split ';'`：将输入的字符串按分号分割成两部分。
- `$name = $parts[0].Trim()`：获取分号前的部分作为快捷方式的名称。
- `$url = $parts[1].Trim()`：获取分号后的部分作为快捷方式的链接。
- `$shortcutPath = "$PWD\$name.url"`：定义快捷方式的路径，`$PWD` 表示当前目录。
- `Set-Content -Path $shortcutPath -Value $shortcutContent`：将快捷方式内容写入文件。

运行脚本后，会在当前目录下生成一个 `.url` 文件，双击该文件即可打开指定的链接。