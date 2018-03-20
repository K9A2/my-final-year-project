# Extensive Evaluation of TCP Congestion Control Algorithms under Varied Network Environments

## 绪论

### 论文研究背景

TCP（Transmission Control Protocol）协议是一种有连接的运输层协议，旨在为TCP/IP协议栈的上层提供稳定、有序和不重复的数据传送服务。而在这种稳定可靠的数据传输服务中心居于核心地位的，是最终控制一个数据包应该如何发送以及在什么时候发送的TCP拥塞控制算法（Congestion Control Algorithm）[1]。

在过去的几十年里面，计算机网络所依赖的电子技术已经取得了巨大的进步，使得网络在带宽和误码率两方面有了明显改善。在这种情况下，Reno（New Reno）[2]、Vegas[3]和HighSpeed[4]等设计时间较早的拥塞控制算法是否能在现有的网络条件下有效地进行拥塞控制值得我们去探讨。

除了技术上的进步，层出不穷的应用场景也对拥塞控制算法的有效性提出了巨大的挑战。比如，在数据中心网络（Data Center Network，DCN）的内部网络往往处于高带宽、低延迟和低误码率的理想状态；而蜂窝网络（Cellular Network）和无线局域网（Wireless Local Area Network，WLAN）的网络则常常与之相反。这些截然不同的网络应用场景同样对拥塞控制算法在不同场景下的有效性提出了巨大的挑战。因此，学界和工业界提出了各种在特定场景下使用的拥塞控制算法以满足特定场景对网络拥塞控制的需求，如DCN中常用的DC-TCP算法[5]以及在无线网络中常用的Westwood算法[6]等。

据相关文献资料[7]，在有线网络中，对用户的响应占据了繁忙时段网络总流量的三分之一。从QoS（Quality of Service，服务质量）的角度出发，若要保证用户的请求能够在繁忙时段得到及时的相应，则必须对网路中的拥塞进行恰当的控制。从网络管理员的角度出发，从服务源到用户的网络可大致分为数据中心内部的私有网络以及DCN网关到用户之间的公用网络。显然，后者是不可控的。减轻数据中心网关到用户设备这段网络上的拥塞情况，提升目标服务的相应速度和稳定性将会对提高用户满意度产生积极影响。

### 论文主要研究内容

本次研究的主要内容是对有线和无线网络环境中的各种拥塞控制算法在不同的应用场景之下进行全面的测试，并深入分析各种算法在拥塞控制效果上的差异及其成因。可简要描述为如下三点：

1. 全面调研了现有的针对TCP拥塞控制算法的测试研究，重点研究了这些研究中关于设计实验与部署测试工具的部分。同时，针对性地在前人工作的基础上引入了符合当前网络环境的实验工具与实验方法。
2. 本次研究针对有线和无线两种网络形式，设计了几种具有针对性的测试场景，并对相应场景中常用的拥塞控制算法进行了全面的测试。
3. 对测试结果的深入分析。同时针对过往的研究工作中所存在的一些不足之处提出了可能的解决方法。

### 论文的创新与贡献

文章通过对有线和无线网络中的拥塞控制算法进行了全面的测试与分析，对拥塞控制领域的相关研究做出了以下两条贡献：

1. 提出了几条在不同网络环境下选择合适的拥塞控制算法的参考意见。
2. 在基于现代网络设备的有线和无线网络场景中均取得了详实的实验资料，为以后的改进提供了依据。

### 论文各章内容安排

本文共分为六章，除首章绪论外，其余章节的主要内容简介如下：
第二章
第三章
第四章
第五章
结论于文末单独成章，对本文的工作进行了总结，并对下一步工作进行了展望。

### 术语说明

## 相关研究综述

### 本章引论

### TCP拥塞控制的基本概念

### TCP拥塞算法性能测试研究综述

### 本文所涉及到的TCP拥塞算法简介

## 测试方案

### 测试标准

### 测试拓扑

### 测试工具

### 测试类型

## 基于有线网络的性能测试结果与分析

### 性能基准测试

### TCP性能测试

### 网络应用测试

### 算法间公平性测试

### 本章小结

## 基于无线网络的性能测试结果与分析

### 性能基准测试

### TCP性能测试

### 网络应用测试

### 算法间公平性测试

### 本章小结

## 结论

## 参考文献

1. Cardwell N, Cheng Y, Gunn C S, et al. BBR: Congestion-based congestion control[J]. Queue, 2016, 14(5): 50.
2. Floyd S, Gurtov A, Henderson T. The NewReno modification to TCP's fast recovery algorithm[J]. 2004.
3. Brakmo L S, Peterson L L. TCP Vegas: End to end congestion avoidance on a global Internet[J]. IEEE Journal on selected Areas in communications, 1995, 13(8): 1465-1480.
4. Floyd S. HighSpeed TCP for large congestion windows[J]. 2003.
5. Nguyen T A N, Gangadhar S, Sterbenz J P G. Performance Evaluation of TCP Congestion Control Algorithms in Data Center Networks[C]//Proceedings of the 11th International Conference on Future Internet Technologies. ACM, 2016: 21-28.
6. Gerla M, Sanadidi M Y, Wang R, et al. TCP Westwood: Congestion window control using bandwidth estimation[C]//Global Telecommunications Conference, 2001. GLOBECOM'01. IEEE. IEEE, 2001, 3: 1698-1702.
7. Feknous M, Houdoin T, Le Guyader B, et al. Internet traffic analysis: A case study from two major European operators[C]//Computers and Communication (ISCC), 2014 IEEE Symposium on. IEEE, 2014: 1-7.

