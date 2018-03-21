# Extensive Evaluation of TCP Congestion Control Algorithms under Varied Network Environments

- [Extensive Evaluation of TCP Congestion Control Algorithms under Varied Network Environments](#extensive-evaluation-of-tcp-congestion-control-algorithms-under-varied-network-environments)
    - [一、绪论](#%E4%B8%80%E3%80%81%E7%BB%AA%E8%AE%BA)
        - [论文研究背景](#%E8%AE%BA%E6%96%87%E7%A0%94%E7%A9%B6%E8%83%8C%E6%99%AF)
        - [论文主要研究内容](#%E8%AE%BA%E6%96%87%E4%B8%BB%E8%A6%81%E7%A0%94%E7%A9%B6%E5%86%85%E5%AE%B9)
        - [论文的创新与贡献](#%E8%AE%BA%E6%96%87%E7%9A%84%E5%88%9B%E6%96%B0%E4%B8%8E%E8%B4%A1%E7%8C%AE)
        - [论文各章内容安排](#%E8%AE%BA%E6%96%87%E5%90%84%E7%AB%A0%E5%86%85%E5%AE%B9%E5%AE%89%E6%8E%92)
        - [术语说明](#%E6%9C%AF%E8%AF%AD%E8%AF%B4%E6%98%8E)
    - [二、相关研究综述](#%E4%BA%8C%E3%80%81%E7%9B%B8%E5%85%B3%E7%A0%94%E7%A9%B6%E7%BB%BC%E8%BF%B0)
        - [本章引论](#%E6%9C%AC%E7%AB%A0%E5%BC%95%E8%AE%BA)
        - [TCP拥塞控制的基本概念](#tcp%E6%8B%A5%E5%A1%9E%E6%8E%A7%E5%88%B6%E7%9A%84%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5)
        - [本文所涉及到的TCP拥塞算法简介](#%E6%9C%AC%E6%96%87%E6%89%80%E6%B6%89%E5%8F%8A%E5%88%B0%E7%9A%84tcp%E6%8B%A5%E5%A1%9E%E7%AE%97%E6%B3%95%E7%AE%80%E4%BB%8B)
        - [TCP拥塞算法性能测试研究综述](#tcp%E6%8B%A5%E5%A1%9E%E7%AE%97%E6%B3%95%E6%80%A7%E8%83%BD%E6%B5%8B%E8%AF%95%E7%A0%94%E7%A9%B6%E7%BB%BC%E8%BF%B0)
    - [三、测试方案](#%E4%B8%89%E3%80%81%E6%B5%8B%E8%AF%95%E6%96%B9%E6%A1%88)
        - [性能标准](#%E6%80%A7%E8%83%BD%E6%A0%87%E5%87%86)
        - [网络拓扑](#%E7%BD%91%E7%BB%9C%E6%8B%93%E6%89%91)
        - [测试工具](#%E6%B5%8B%E8%AF%95%E5%B7%A5%E5%85%B7)
        - [网络场景](#%E7%BD%91%E7%BB%9C%E5%9C%BA%E6%99%AF)
    - [四、基于有线网络的性能测试结果与分析](#%E5%9B%9B%E3%80%81%E5%9F%BA%E4%BA%8E%E6%9C%89%E7%BA%BF%E7%BD%91%E7%BB%9C%E7%9A%84%E6%80%A7%E8%83%BD%E6%B5%8B%E8%AF%95%E7%BB%93%E6%9E%9C%E4%B8%8E%E5%88%86%E6%9E%90)
        - [性能基准测试](#%E6%80%A7%E8%83%BD%E5%9F%BA%E5%87%86%E6%B5%8B%E8%AF%95)
        - [TCP性能测试](#tcp%E6%80%A7%E8%83%BD%E6%B5%8B%E8%AF%95)
        - [网络应用测试](#%E7%BD%91%E7%BB%9C%E5%BA%94%E7%94%A8%E6%B5%8B%E8%AF%95)
        - [算法间公平性测试](#%E7%AE%97%E6%B3%95%E9%97%B4%E5%85%AC%E5%B9%B3%E6%80%A7%E6%B5%8B%E8%AF%95)
        - [本章小结](#%E6%9C%AC%E7%AB%A0%E5%B0%8F%E7%BB%93)
    - [五、基于无线网络的性能测试结果与分析](#%E4%BA%94%E3%80%81%E5%9F%BA%E4%BA%8E%E6%97%A0%E7%BA%BF%E7%BD%91%E7%BB%9C%E7%9A%84%E6%80%A7%E8%83%BD%E6%B5%8B%E8%AF%95%E7%BB%93%E6%9E%9C%E4%B8%8E%E5%88%86%E6%9E%90)
        - [性能基准测试](#%E6%80%A7%E8%83%BD%E5%9F%BA%E5%87%86%E6%B5%8B%E8%AF%95)
        - [TCP性能测试](#tcp%E6%80%A7%E8%83%BD%E6%B5%8B%E8%AF%95)
        - [网络应用测试](#%E7%BD%91%E7%BB%9C%E5%BA%94%E7%94%A8%E6%B5%8B%E8%AF%95)
        - [算法间公平性测试](#%E7%AE%97%E6%B3%95%E9%97%B4%E5%85%AC%E5%B9%B3%E6%80%A7%E6%B5%8B%E8%AF%95)
        - [本章小结](#%E6%9C%AC%E7%AB%A0%E5%B0%8F%E7%BB%93)
    - [结论](#%E7%BB%93%E8%AE%BA)
    - [参考文献](#%E5%8F%82%E8%80%83%E6%96%87%E7%8C%AE)

## 一、绪论

### 论文研究背景

TCP（Transmission Control Protocol）协议是一种有连接的运输层协议，旨在为TCP/IP协议栈中的上层提供稳定、有序和不重复的数据传送服务。而在这种稳定可靠的数据传输服务中心中居于核心地位的，是用来控制一个数据包应该如何发送的TCP拥塞控制算法（Congestion Control Algorithm）[1]。拥塞控制算法能否有效地控制网络中的必定会出现的数据拥塞决定了TCP层所提供的服务质量高低。

而在过去的几十年里面，计算机网络所依赖的电子技术已经取得了巨大的进步，使得网络在带宽和误码率两方面有了明显改善。在这种情况下，Reno（New Reno）[2]、Vegas[3]和HighSpeed[4]等实现时间较早，但至今在现存系统中被广泛使用的拥塞控制算法是否能在现有的网络条件下有效地进行拥塞控制，值得我们去探讨。

同时，除了技术上的进步以外，不同的网络环境也对拥塞控制算法的有效性提出了巨大的挑战。比如，在数据中心网络（Data Center Network，DCN）的内部网络往往处于高带宽、低延迟和低误码率的理想状态；而蜂窝网络（Cellular Network）和无线局域网（Wireless Local Area Network，WLAN）的网络则常常与之相反；常用的广域网（Wide Area Network，WAN）和局域网（Local Area Network）的网络情况则相当多变。这些截然不同的网络环境对拥塞控制算法在不同场景下的有效性提出了巨大的挑战。因此，学界和工业界提出了各种拥塞控制算法以满足特定环境下对网络拥塞控制的要求，如DCN中常用的DC-TCP算法[5]以及在无线网络中常用的Westwood算法[6]等。然而，除了使用专用算法的DCN和蜂窝网络，WAN、LAN和WLAN等常用的网络类型是否存在一种通用（Generic）的拥塞控制算法也值得我们去探讨。

据相关文献资料[7]，在有线网络中，对用户的响应占据了繁忙时段网络总流量的三分之一。若要保证用户的请求能够在繁忙时段得到及时的相应，则必须对网路中的拥塞进行恰当的控制。而从网络管理员的角度来看，从源服务器到用户的网络可大致分为数据中心内部的私有网络（DCN）以及DCN网关到用户之间的公用网络。显然，后者所处的公用网络是不可控的。减轻数据中心网关到用户设备这段网络上的拥塞情况，提升目标服务的相应速度和稳定性将会对提高用户满意度产生积极影响。

### 论文主要研究内容

本次研究的主要内容是分别对有线和无线网络环境中的各种拥塞控制算法在不同的应用场景之下进行了全面的测试，并分析了各种算法在拥塞控制效果上的差异及其成因，并以此为基础提出了在不同网络场景中选择合适的拥塞控制算法的建议。本文的主要工作可简要描述为如下：

* 全面调研了现有的针对TCP拥塞控制算法的测试研究，重点研究了这些研究中关于设计实验与部署测试工具的部分。同时，针对性地在前人工作的基础上引入了符合当前网络环境的实验工具与实验方法。
* 本次研究针对有线和无线两种网络形式，设计了几种具有针对性的测试场景，并对相应场景中常用的拥塞控制算法进行了全面的测试。
* 对测试结果的深入分析。同时针对过往的研究工作中所存在的一些不足之处提出了可能的解决方法。

### 论文的创新与贡献

文章通过对有线和无线网络中的拥塞控制算法进行了全面的测试与分析，对拥塞控制领域的相关研究做出了以下两条贡献：

* 提出了几条在不同网络环境下选择合适的拥塞控制算法的参考意见。
* 在基于现代网络设备的有线和无线网络场景中均取得了详实的实验资料，为以后的改进提供了依据。

### 论文各章内容安排

本文共分为六章，除首章绪论外，其余章节的主要内容简介如下：

+ 第二章主要介绍了TCP拥塞控制的基本概念、所涉及到的算法和相关研究。
+ 第三章主要介绍本次实验的具体方案，包括测试的标准、网络拓扑、测试工具和网络场景等四方面。
+ 第四章主要介绍了在有线网络环境下进行的测试及其结论。
+ 第五章主要介绍了在无线网络环境下进行的测试及其结论。

结论于文末单独成章，对本文的工作进行了总结，并对下一步工作进行了展望。

### 术语说明

## 二、相关研究综述

### 本章引论

### TCP拥塞控制的基本概念

### 本文所涉及到的TCP拥塞算法简介

### TCP拥塞算法性能测试研究综述

## 三、测试方案

### 性能标准

### 网络拓扑

### 测试工具

### 网络场景

## 四、基于有线网络的性能测试结果与分析

### 性能基准测试

### TCP性能测试

### 网络应用测试

### 算法间公平性测试

### 本章小结

## 五、基于无线网络的性能测试结果与分析

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

