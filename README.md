<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title></title>
    <style>
        .code-container {
            position: relative;
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }

        .copy-btn {
            position: absolute;
            top: 10px;
            right: 10px;
            padding: 5px 10px;
            cursor: pointer;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 3px;
        }

        .copy-btn:hover {
            background-color: #0056b3;
        }

        pre {
            margin: 0;
            font-family: Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace;
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        .note {
            color: red;
            font-weight: bold;
        }

        img {
            max-width: 100%;
            height: auto;
        }

        .link {
            color: #007bff;
        }
    </style>
</head>
<body>

    <h1>开机自动登录校园网指南</h1>

    <p><span class="note">注意事项:</span></p>
    <ul>
        <li>本指南仅适用于Windows系统。</li>
        <li>首次安装时，您需要在校园网登录页面输入您的账号、密码以及运营商编号(数据都保存在本地!!!)。如下图所示:</li>
    </ul>
    <img src="https://s2.loli.net/2024/04/29/oLZke7ijATqUwBG.png" alt="Login Image">

    <h2>第一步：创建自动登录脚本</h2>

    <p>1. 首先，打开记事本并输入以下内容:</p>

    <div class="code-container">
        <button class="copy-btn" onclick="copyCode('code-block-1')">复制</button>
        <pre id="code-block-1">start http://10.31.0.10/</pre>
    </div>

    <p>2. 保存文件时，文件名后缀为<code>.txt</code>（比如命名为<code>login.txt</code>）。保存后，您需要将文件后缀名<code>.txt</code>改为<code>.bat</code>（例如<code>login.bat</code>），请注意文件名不建议使用中文。</p>
    <img src="https://s2.loli.net/2024/04/07/6uz7yQVmw9Wd3JH.png" alt="步骤图1">

    <h2>第二步：设置开机自启动</h2>

    <p>1. 按住键盘上的<code>Win</code> + <code>R</code>组合键，输入以下命令并按下回车：</p>

    <div class="code-container">
        <button class="copy-btn" onclick="copyCode('code-block-2')">复制</button>
        <pre id="code-block-2">shell:startup</pre>
    </div>

    <p>2. 打开文件夹后，将刚才创建的<code>.bat</code>文件（如<code>login.bat</code>）剪切到这个文件夹中。这样，每次启动电脑时，系统会自动运行这个脚本，帮助您自动登录校园网。</p>
    <img src="https://s2.loli.net/2024/04/07/swlD8BoWM6GtaYf.png" alt="步骤图2">

    <p><span class="note">注意事项</span>: 上述步骤仅适用于Windows操作系统！</p>

    <p>对于iOS用户（非macOS），可以点击<a href="https://www.icloud.com/shortcuts/fafebf2fe5a44e7db2dd51394b2c6078" class="link">此链接</a>使用快捷指令。</p>

    <script>
        function copyCode(id) {
            const code = document.getElementById(id).innerText;
            
            // 检查浏览器是否支持Clipboard API
            if (navigator.clipboard) {
                navigator.clipboard.writeText(code).then(() => {
                    alert("代码已复制到剪贴板！");
                }).catch(err => {
                    alert("复制失败，请手动复制: " + err);
                });
            } else {
                // 不支持Clipboard API时，使用旧的方式进行手动复制
                const textarea = document.createElement("textarea");
                textarea.value = code;
                document.body.appendChild(textarea);
                textarea.select();
                try {
                    document.execCommand("copy");
                    alert("代码已复制到剪贴板！");
                } catch (err) {
                    alert("复制失败，请手动复制");
                }
                document.body.removeChild(textarea);
            }
        }
    </script>

</body>
</html>
