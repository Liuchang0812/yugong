# 迁移工具使用方法

迁移工具支持将OSS, Qiniu，文件列表等文件迁移到COS对象存储。工具只支持在 linux/macos 下运行，需要安装Python2.7。

## 安装方法

推荐使用pip或者easy_install安装，安装pip的方法，可以参考[官网](https://pip.pypa.io/en/latest/installing/)。

```bash
    pip install cos_migrate_tool
```

## 使用方法

在安装成功后，系统会有一个可执行命令 `cos_migrate_tool`，之后的迁移过程都是使用该命令。执行命令的方式如下：

```bash
    cos_migrate_tool -c /path/to/your/conf
```

在配置文件中，需要配置一个工作目录，之后迁移过程中产生的临时文件都在放置在该目录，请保证目录空间足够大，如果并行执行多个迁移任务，推荐使用不同的目录。

在迁移过程中，你可以查看你设定的工作目录下面的 fail_file.txt 来查看迁移失败的文件列表。

## 配置文件

配置文件模板, common 部分配置基本配置,workspace是上述的工作目录。source 部分配置数据源的信息，如果你想迁移oss到cos，该部分就是配置oss的属性。destination 部分配置cos属性。

```bash
[common]
workspace=/tmp/tmp6

[source]
type=oss
accesskeyid=
accesskeysecret=
bucket=
endpoint=

[destination]
type=cosv4
region=shanghai
accesskeyid=
appid=
accesskeysecret=
bucket=sdktest
```

### 迁移OSS

```bash
[common]
workspace=/tmp/tmp6

[source]
type=oss
accesskeyid=         # oss accesskey id
accesskeysecret=     # oss accesskey secret
bucket=              # 要迁移的bucket名
endpoint=            # oss 的endpoint，例如 oss-cn-beijing.aliyuncs.com

[destination]
type=cosv4
region=shanghai            # cos 的 region，如shanghai, guangzhou
accesskeyid=               # cos 的 accesskeyid
appid=                     # cos 的 appid
accesskeysecret=           # cos 的 accesskeysecret
bucket=sdktest             # cos 的 bucket
```

###  迁移qiniu

```bash
[common]
workspace=/tmp/tmp11

[source]
type=qiniu
accesskeyid=            # qiniu 的 accesskeyid
accesskeysecret=        # qiniu 的 accesskeysecret
bucket=                 # 要迁移的qiniu的bucket
domain_url=             # qiniu 的下载域名

[destination]
type=cosv4
region=shanghai            # cos 的 region，如shanghai, guangzhou
accesskeyid=               # cos 的 accesskeyid
appid=                     # cos 的 appid
accesskeysecret=           # cos 的 accesskeysecret
bucket=sdktest             # cos 的 bucket
```

### 迁移列表文件

```bash
[common]
workspace=

[source]
type=url
url_list_file=/tmp/urllist.txt   #要迁移的文件url列表文件，文件每一行为一个完整的url
timeout=3

[destination]
type=cosv4
region=
accesskeyid=
appid=
accesskeysecret=
bucket=
```