<?php
$upload_status = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!isset($_FILES['file']) || $_FILES['file']['error'] !== UPLOAD_ERR_OK) {
        $upload_status = '文件上传失败';
    } else {
        $file = $_FILES['file'];
        $filename = $file['name'];
        $tmp_name = $file['tmp_name'];
        $content = file_get_contents($tmp_name);

        // 仅删除非法字符，不禁止上传
        $filtered_name = preg_replace('/php|htaccess/i', '', $filename);
        $filtered_name = preg_replace('/php|htaccess/i', '', $filtered_name); // 二次过滤
        if ($filtered_name === '' || $filtered_name === '.' || $filtered_name === '..') {
            $filtered_name = 'upload_' . uniqid() . '.dat';
            $upload_status = '原始文件名过滤后为非法名，已自动重命名为：' . $filtered_name;
        }
        // 内容检测
        if (preg_match('/<\?php|<\?|@/i', $content)) {
            $upload_status = '文件内容包含敏感标签';
        } else {
            $target_dir = __DIR__ . '/uploads/';
            if (!is_dir($target_dir)) mkdir($target_dir, 0777, true);
            $target_file = $target_dir . $filtered_name;
            if (move_uploaded_file($tmp_name, $target_file)) {
                $upload_status .= ($upload_status ? '<br>' : '') . '文件上传成功，文件位置：/uploads/' . htmlspecialchars($filtered_name);
            } else {
                $upload_status .= ($upload_status ? '<br>' : '') . '保存文件失败';
            }
        }
    }
}
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>ezupload</title>
    <style>
        body {
            background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 99%, #fad0c4 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-family: 'Segoe UI', 'Arial', sans-serif;
        }
        .container {
            background: rgba(255,255,255,0.85);
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            padding: 40px 30px 30px 30px;
            text-align: center;
            max-width: 400px;
        }
        h1 {
            background: linear-gradient(90deg, #ff6a00, #ee0979, #00c3ff, #ffff1c);
            background-size: 400% 400%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: rainbow 5s ease infinite;
            font-size: 2.2em;
            margin-bottom: 20px;
        }
        @keyframes rainbow {
            0% {background-position:0% 50%}
            50% {background-position:100% 50%}
            100% {background-position:0% 50%}
        }
        .upload-box {
            margin: 20px 0;
        }
        input[type="file"] {
            display: none;
        }
        .custom-file-label {
            display: inline-block;
            padding: 10px 25px;
            background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
            color: #fff;
            border-radius: 30px;
            cursor: pointer;
            font-size: 1.1em;
            margin-bottom: 10px;
            transition: background 0.3s;
        }
        .custom-file-label:hover {
            background: linear-gradient(90deg, #fa709a 0%, #fee140 100%);
        }
        .submit-btn {
            padding: 10px 30px;
            background: linear-gradient(90deg, #30cfd0 0%, #330867 100%);
            color: #fff;
            border: none;
            border-radius: 30px;
            font-size: 1.1em;
            cursor: pointer;
            margin-top: 10px;
            transition: background 0.3s;
        }
        .submit-btn:hover {
            background: linear-gradient(90deg, #f7971e 0%, #ffd200 100%);
        }
        .status {
            margin-top: 20px;
            font-size: 1.1em;
            color: #d7263d;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>ezupload</h1>
        <form method="post" enctype="multipart/form-data" onsubmit="return checkFileType()">
            <div class="upload-box">
                <label class="custom-file-label" for="file">选择图片文件</label>
                <input type="file" id="file" name="file" accept="image/gif,image/png,image/jpeg" required>
            </div>
            <button class="submit-btn" type="submit">上传</button>
        </form>
        <?php if ($upload_status): ?>
            <div class="status"><?php echo $upload_status; ?></div>
        <?php endif; ?>
    </div>
    <script>
    function checkFileType() {
        const fileInput = document.getElementById('file');
        if (!fileInput.value) return false;
        const file = fileInput.files[0];
        if (!file) return false;
        const allowedTypes = ['image/gif', 'image/png', 'image/jpeg'];
        if (!allowedTypes.includes(file.type)) {
            alert('只能上传图片文件！');
            return false;
        }
        return true;
    }
    document.querySelector('.custom-file-label').onclick = function() {
        document.getElementById('file').click();
    };
    </script>
</body>
</html> 