# Hearts of Iron 4 inner circle modding tool（unofficial）
# 钢铁雄心4核心圈机制mod工具（非官方）

This is a tool that allows you to generate inner circle mechanisms in Hearts of Iron 4 mod development with one click. This tool can generate the cumbersome automatic control code for the inner circle mechanism, allowing you to focus on content development.
这是一个让你可以在钢铁雄心4mod开发中一键生成核心圈的工具，本工具可以生成核心圈机制繁琐的自动控制代码，让你专注于内容开发。

## Instructions
## 操作方法

1. Prepare a GUI file for the inner circle, refer to `interface/defaultgui.gui`.
2. Fill in `settings.yaml`, `characters.csv`, `national_focus.csv`, `other_localisation.csv` according to the comments in `settings.yaml`.
3. Run the program.
4. Create an `interface` folder in `output`, put the GUI file of the inner circle into it, and you will have all the code needed for the inner circle mechanism!
5. Merge `output` with your mod, modify the necessary files such as `history`, and supplement the localization content for the events controlling the national focus process in `events/MY_TEST_event_control_type_focus_event.txt`.

---

1. 准备一个核心圈的gui文件，可参考`interface/defaultgui.gui`
2. 按照`settings.yaml`中的注释填写`settings.yaml`、`characters.csv`、`national_focus.csv`、`other_localisation.csv`
3. 运行程序
4. 在`output`中创建`interface`文件夹，把核心圈的gui文件放进去，你就拥有一个核心圈机制需要的全部代码了！
5. 把`output`和你的mod合并，修改相关的必要文件如`history`，并为`events/MY_TEST_event_control_type_focus_event.txt`中控制国策流程的相关事件补充本地化内容即可。

## Version Information
## 版本说明

The program has not been fully tested and is currently in the beta stage, so there may still be some bugs. But to honor the glorious tradition of our great Paradox company, the beta version will also start from the official version number.

程序未经过充分测试，目前处于beta阶段，应该还有一些bug。但为了致敬我们伟大的paradox公司的光荣传统，beta版也会从正式的版本号开始。


The author's English are very not good, if you don't understand the comments, it must be the author's problem. welcome systematically modify the comments.

作者的英语很差，如果你读不懂注释那一定是作者的问题，欢迎对注释的系统性的修改。

## Buy me a coffee
## 请我喝咖啡

You can also send me a Steam gift card to my email.
你也可以向我的邮箱发送steam礼品卡。

![](aex19571oqzf3apkblli41e.png)

![](2024-12-24-17-14-59.png)

## Contributors
## 贡献者

- 👓时间转移👓 <leslielin0316@outlook.com>

## License
## 许可证

This project is licensed under the GPL License - see the [LICENSE](LICENSE) file for details.
本项目采用GPL许可证 - 详情请参见[LICENSE](LICENSE)文件。