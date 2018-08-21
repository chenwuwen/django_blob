**安装提示**

在开始开发Django项目或者其他Python项目时,建议不直接安装Python
而是安装Anaconda 安装好Anaconda之后,先创建虚拟环境, conda create -n '虚拟环境名' python=版本
这个虚拟环境名可以自定义,可以使用自己的项目名,或者以要使用的Python版本来定义 如使用python3.6则可以
以python36来命令,创建好虚拟环境之后,激活该虚拟环境,然后再进行各种pip install xxx
Anaconda 使用相关 https://www.jianshu.com/p/d2e15200ee9b

以上属于开发相关的,关于部署,由于项目中依赖了许多第三方库,所以毫无疑问,要部署
的服务器上也需要安装其他库,这个时候我们需要知道该项目由哪些依赖[当然实际上
就是虚拟环境中site-packages中的包],所以我们需要安装一个第三方库[在开发模式下] 
安装  pip install  freeze
安装成功后,命令 pip freeze>Requirements.txt
即可将当前当前项目所使用的依赖导出到当前文件夹下的Requirements.txt文件内
其实这个类似于java中Maven的POM.xml Node中的package.json 文件,
打开文件,发现里面都是项目依赖的第三方库的名称及版本,此时我们只需要将,这个文件
上传到服务器,然后切换到要使用的虚拟环境,再使用命令 pip install -r Requirements.txt 即可将项目中的依赖
安装到服务器中。

