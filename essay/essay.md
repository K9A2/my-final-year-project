# Extensive Evaluation of TCP Congestion Control Algorithms under Varied Network Environments

- [Extensive Evaluation of TCP Congestion Control Algorithms under Varied Network Environments](#extensive-evaluation-of-tcp-congestion-control-algorithms-under-varied-network-environments)
    - [1. 绪论](#1-%E7%BB%AA%E8%AE%BA)
        - [1.1 论文研究背景](#11-%E8%AE%BA%E6%96%87%E7%A0%94%E7%A9%B6%E8%83%8C%E6%99%AF)
        - [1.2 论文主要研究内容](#12-%E8%AE%BA%E6%96%87%E4%B8%BB%E8%A6%81%E7%A0%94%E7%A9%B6%E5%86%85%E5%AE%B9)
        - [1.3 论文的创新与贡献](#13-%E8%AE%BA%E6%96%87%E7%9A%84%E5%88%9B%E6%96%B0%E4%B8%8E%E8%B4%A1%E7%8C%AE)
        - [1.4 论文各章内容安排](#14-%E8%AE%BA%E6%96%87%E5%90%84%E7%AB%A0%E5%86%85%E5%AE%B9%E5%AE%89%E6%8E%92)
        - [1.5 术语说明](#15-%E6%9C%AF%E8%AF%AD%E8%AF%B4%E6%98%8E)
    - [2. 相关研究综述](#2-%E7%9B%B8%E5%85%B3%E7%A0%94%E7%A9%B6%E7%BB%BC%E8%BF%B0)
        - [2.1 本章引论](#21-%E6%9C%AC%E7%AB%A0%E5%BC%95%E8%AE%BA)
        - [2.2 TCP拥塞控制的基本概念](#22-tcp%E6%8B%A5%E5%A1%9E%E6%8E%A7%E5%88%B6%E7%9A%84%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5)
            - [2.2.1 拥塞的来源与拥塞窗口](#221-%E6%8B%A5%E5%A1%9E%E7%9A%84%E6%9D%A5%E6%BA%90%E4%B8%8E%E6%8B%A5%E5%A1%9E%E7%AA%97%E5%8F%A3)
            - [2.2.2 慢开始、拥塞避免、快重传和快恢复](#222-%E6%85%A2%E5%BC%80%E5%A7%8B%E3%80%81%E6%8B%A5%E5%A1%9E%E9%81%BF%E5%85%8D%E3%80%81%E5%BF%AB%E9%87%8D%E4%BC%A0%E5%92%8C%E5%BF%AB%E6%81%A2%E5%A4%8D)
            - [2.2.3 AIMD](#223-aimd)
        - [2.3 本文所涉及到的TCP拥塞算法](#23-%E6%9C%AC%E6%96%87%E6%89%80%E6%B6%89%E5%8F%8A%E5%88%B0%E7%9A%84tcp%E6%8B%A5%E5%A1%9E%E7%AE%97%E6%B3%95)
        - [2.4 TCP拥塞算法性能测试相关研究](#24-tcp%E6%8B%A5%E5%A1%9E%E7%AE%97%E6%B3%95%E6%80%A7%E8%83%BD%E6%B5%8B%E8%AF%95%E7%9B%B8%E5%85%B3%E7%A0%94%E7%A9%B6)
    - [3. 测试方案](#3-%E6%B5%8B%E8%AF%95%E6%96%B9%E6%A1%88)
        - [3.1 性能标准](#31-%E6%80%A7%E8%83%BD%E6%A0%87%E5%87%86)
        - [3.2 网络拓扑](#32-%E7%BD%91%E7%BB%9C%E6%8B%93%E6%89%91)
        - [3.3 测试工具](#33-%E6%B5%8B%E8%AF%95%E5%B7%A5%E5%85%B7)
        - [3.4 网络场景](#34-%E7%BD%91%E7%BB%9C%E5%9C%BA%E6%99%AF)
    - [4. 基于有线网络的性能测试结果与分析](#4-%E5%9F%BA%E4%BA%8E%E6%9C%89%E7%BA%BF%E7%BD%91%E7%BB%9C%E7%9A%84%E6%80%A7%E8%83%BD%E6%B5%8B%E8%AF%95%E7%BB%93%E6%9E%9C%E4%B8%8E%E5%88%86%E6%9E%90)
        - [4.1 性能基准测试](#41-%E6%80%A7%E8%83%BD%E5%9F%BA%E5%87%86%E6%B5%8B%E8%AF%95)
        - [4.2 TCP性能测试](#42-tcp%E6%80%A7%E8%83%BD%E6%B5%8B%E8%AF%95)
        - [4.3 网络应用测试](#43-%E7%BD%91%E7%BB%9C%E5%BA%94%E7%94%A8%E6%B5%8B%E8%AF%95)
        - [4.4 算法间公平性测试](#44-%E7%AE%97%E6%B3%95%E9%97%B4%E5%85%AC%E5%B9%B3%E6%80%A7%E6%B5%8B%E8%AF%95)
        - [4.5 本章小结](#45-%E6%9C%AC%E7%AB%A0%E5%B0%8F%E7%BB%93)
    - [5. 基于无线网络的性能测试结果与分析](#5-%E5%9F%BA%E4%BA%8E%E6%97%A0%E7%BA%BF%E7%BD%91%E7%BB%9C%E7%9A%84%E6%80%A7%E8%83%BD%E6%B5%8B%E8%AF%95%E7%BB%93%E6%9E%9C%E4%B8%8E%E5%88%86%E6%9E%90)
        - [5.1 性能基准测试](#51-%E6%80%A7%E8%83%BD%E5%9F%BA%E5%87%86%E6%B5%8B%E8%AF%95)
        - [5.2 TCP性能测试](#52-tcp%E6%80%A7%E8%83%BD%E6%B5%8B%E8%AF%95)
        - [5.3 网络应用测试](#53-%E7%BD%91%E7%BB%9C%E5%BA%94%E7%94%A8%E6%B5%8B%E8%AF%95)
        - [5.4 算法间公平性测试](#54-%E7%AE%97%E6%B3%95%E9%97%B4%E5%85%AC%E5%B9%B3%E6%80%A7%E6%B5%8B%E8%AF%95)
        - [5.5 本章小结](#55-%E6%9C%AC%E7%AB%A0%E5%B0%8F%E7%BB%93)
    - [6. 结论](#6-%E7%BB%93%E8%AE%BA)
    - [参考文献](#%E5%8F%82%E8%80%83%E6%96%87%E7%8C%AE)

## 1. 绪论

### 1.1 论文研究背景

TCP（Transmission Control Protocol）协议是一种有连接的运输层协议，旨在为TCP/IP协议栈中的上层提供稳定、有序和不重复的数据传送服务。而在这种稳定可靠的数据传输服务中心中居于核心地位的，是用来控制一个数据包应该如何发送的TCP拥塞控制算法（Congestion Control Algorithm）[1]。拥塞控制算法能否有效地控制网络中的必定会出现的数据拥塞决定了TCP层所提供的服务质量高低。

而在过去的几十年里面，计算机网络所依赖的电子技术已经取得了巨大的进步，使得网络在带宽和误码率两方面有了明显改善。在这种情况下，Reno（New Reno）[2]、Vegas[3]和HighSpeed[4]等实现时间较早，但至今在现存系统中被广泛使用的拥塞控制算法是否能在现有的网络条件下有效地进行拥塞控制，值得我们去探讨。

同时，除了技术上的进步以外，不同的网络环境也对拥塞控制算法的有效性提出了巨大的挑战。比如，在数据中心网络（Data Center Network，DCN）的内部网络往往处于高带宽、低延迟和低误码率的理想状态；而蜂窝网络（Cellular Network）和无线局域网（Wireless Local Area Network，WLAN）的网络则常常与之相反；常用的广域网（Wide Area Network，WAN）和局域网（Local Area Network）的网络情况则相当多变。这些截然不同的网络环境对拥塞控制算法在不同场景下的有效性提出了巨大的挑战。因此，学界和工业界提出了各种拥塞控制算法以满足特定环境下对网络拥塞控制的要求，如DCN中常用的DC-TCP算法[5]以及在无线网络中常用的Westwood算法[6]等。然而，除了使用专用算法的DCN和蜂窝网络，WAN、LAN和WLAN等常用的网络类型是否存在一种通用（Generic）的拥塞控制算法也值得我们去探讨。

据相关文献资料[7]，在有线网络中，对用户的响应占据了繁忙时段网络总流量的三分之一。若要保证用户的请求能够在繁忙时段得到及时的相应，则必须对网路中的拥塞进行恰当的控制。而从网络管理员的角度来看，从源服务器到用户的网络可大致分为数据中心内部的私有网络（DCN）以及DCN网关到用户之间的公用网络。显然，后者所处的公用网络是不可控的。减轻数据中心网关到用户设备这段网络上的拥塞情况，提升目标服务的相应速度和稳定性将会对提高用户满意度产生积极影响。

### 1.2 论文主要研究内容

本次研究的主要内容是分别对有线和无线网络环境中的各种拥塞控制算法在不同的应用场景之下进行了全面的测试，并分析了各种算法在拥塞控制效果上的差异及其成因，并以此为基础提出了在不同网络场景中选择合适的拥塞控制算法的建议。本文的主要工作可简要描述如下：

* 全面调研了现有的针对TCP拥塞控制算法的测试研究，重点研究了这些研究中关于设计实验与部署测试工具的部分。同时，针对性地在前人工作的基础上引入了符合当前网络环境的实验工具与实验方法。
* 本次研究针对有线和无线两种网络形式，设计了几种具有针对性的测试场景，并对相应场景中常用的拥塞控制算法进行了全面的测试。
* 对测试结果的深入分析。同时针对过往的研究工作中所存在的一些不足之处提出了可能的解决方法。

### 1.3 论文的创新与贡献

文章通过对有线和无线网络中的拥塞控制算法进行了全面的测试与分析，对拥塞控制领域的相关研究做出了以下两条贡献：

* 提出了几条在不同网络环境下选择合适的拥塞控制算法的参考意见。
* 在基于现代网络设备的有线和无线网络场景中均取得了详实的实验资料，为以后的改进提供了依据。

### 1.4 论文各章内容安排

本文共分为六章，除首章绪论外，其余章节的主要内容简介如下：

+ 第二章主要介绍了TCP拥塞控制的基本概念、所涉及到的算法和相关研究。
+ 第三章主要介绍本次实验的具体方案，包括测试的标准、网络拓扑、测试工具和网络场景等四方面。
+ 第四章主要介绍了在有线网络环境下进行的测试及其结论。
+ 第五章主要介绍了在无线网络环境下进行的测试及其结论。

结论于文末单独成章，对本文的工作进行了总结，并对下一步工作进行了展望。

### 1.5 术语说明

## 2. 相关研究综述

### 2.1 本章引论

### 2.2 TCP拥塞控制的基本概念

#### 2.2.1 拥塞的来源与拥塞窗口

由于TCP采用了有连接的方式来传输数据，所以每一条连接以及其上的数据就可以抽象地描述为一个“流（Flow）”。而在实际的传输过程中，一条TCP流中的数据，从源节点到目的节点往往会需要经过多次转发。而在这个转发的过程中，由于转发节点（主要是各种路由器和交换机）的处理能力有限，需要把收到的数据进行缓存后，在处理能力许可的情况下再行处理。那么，在这个等待处理的过程中，流中的数据包将不可避免地在此处产生拥塞。

如果数据的发送方没有采用拥塞避免机制，那么由于发送方无法在连接超时之前收到被堵塞在链路中的数据包的确认（Acknowledgement），那么它将认为此数据包已在途中丢失，并重传（Retransmit）此数据包。这样，就会进一步加重已经产生的拥塞，并最终导致网络死锁。

而在启用了拥塞控制算的通信双方中，发送方将会维护一个类似于滑动窗口的拥塞窗口（Congestion Window，在Linux内核代码中缩写为cwnd）,用来限制已发送但未确认的数据包的数量。当cwnd < ssthresh（Slow Start Threshold，慢启动阈值，由网络状态设定）时，发送方就会认为网络中发生了拥堵，并进入拥塞避免（Congestion Avoidance）状态，调用设定的拥塞避免算法以减轻网络中的拥堵。

#### 2.2.2 慢开始、拥塞避免、快重传和快恢复

慢开始、拥塞避免（Congestion Avoidance）、快重传（Fast Retransmit）和快恢复（Fast Recovery）是TCP层进行拥塞控制的重要概念，在RFC 5681[21]中有详细描述。

慢开始（Slow start）指的是发送方以一个较小的拥塞窗口大小，比如1至10个MSS（Maximum Segment Size，最大分段大小）来发送数据并使得cwnd的值翻倍，以探测网络所能承载的最大数据量，并避免在未知网络具体情况的情况下就发送大量数据而使网络出现拥塞。具体地，每当发送方接收到一个数据包的确认时，就会使拥塞窗口的大小增加一个MSS，直到发送的数据超过了接收方的接收窗口（Receiver Window，rwnd）大小、超过了ssthresh的限制等异常情况，又或者网络中出现了拥塞，可简要描述如下：

* 在cwnd增长至与ssthresh相当时又或者超出了接收方的rwnd，就将用线性增长的方式来使得cwnd得以继续缓慢地增长。具体地就是在每经过RTT（Round Trip Time，往返时延）的时间就使cwnd增加一个MSS的大小。
* 若发送方察觉到网络中出现了拥塞，就将进入拥塞避免状态，并调用系统中指定的拥塞控制算法以降低网络中的数据包的数量，其具体操作由拥塞控制算法确定。而此种情况下的拥塞控制效果也是本次研究的重点。

在TCP的具体实现中，当接收方收到了一个失序抵达的数据包时，应当立刻向发送方回复一个重复的确认，以通知发送方此数据包未按预定顺序抵达，并提示应当收到的数据包的编号。通常而言，造成数据包失序抵达的原因可以是网络出现了拥塞、网络调换了数据包的顺序[22]又或者是网络复制了一个数据包等原因。对于发送方而言，收到重复的确认就可以认为是网络出现了拥塞。除了重复的确认以为，重传计时器超时也被认为是由于网络发生了拥塞而导致的。

而为了加快从拥塞中回复的流程，发送方往往采用“快恢复”机制来发送丢失的数据包。即发送方在通过三重ACK来确认一个数据包的丢失之后，立刻重传此数据包，而非等候重传计时器超时。

通常而言，慢启动机制将缓慢地增加cwnd的值以探测网络的最大负载。而在丢包重传的情况下，未丢失数据包之前的网络负责则是网络可以接受的。如果直接使用慢启动机制来是的cwnd减半则不利于发送方快速恢复到丢包之前的状态。所以，在快恢复机制把丢失的数据包重传之后，称为“快恢复”的机制将接替“快重传”机制的控制权直到下一个不重复的ACK抵达接收方。与慢开始（即拥塞窗口cwnd现在不设置为1）的不同之处是，cwnd值被设置为ssthresh减半后的数值，然后开始执行拥塞避免算法（即所谓的加法增大），使得拥塞窗口缓慢地线性增大。

#### 2.2.3 AIMD

AIMD（Additive-Increase/Multiplicative-Decrease，加法增加、乘法减小）算法，是一种用来相对公平地分配链路带宽的反馈性算法，是一种对上节所属四种算法的高度抽象。其特点是，不存在拥塞时，使用加法来缓慢地增加拥塞窗口的大小；当网络出现拥塞是，乘法地减小拥塞窗口，以降低网络的拥塞程度。当网路中有的流都采用AIMD算法时，每一个流最终都将获得相等的带宽份额。通常而言，发送者会在每一个RTT长度的时间中让拥塞窗口增加一个MSS的大小。

### 2.3 本文所涉及到的TCP拥塞算法

### 2.4 TCP拥塞算法性能测试相关研究

由于对TCP拥塞控制算法在不同网络环境下进行测试以检查其有效性十分重要，学界和工业界的研究人员均对此问题进行了大量研究。

Mario Hock等人在其研究中[8]对新提出并已经得到广泛应用的拥塞控制算法BBR在带宽（Throughput）、排队延迟（Queuing delay）、丢包率（Packet loss）和公平性（Fairness）等几个方面进行了独立而深入的测试与分析。由于他们已经对包含BBR在内的常用的拥塞控制算法的底层进行了深入分析，故本文便从上层应用的角度来分析拥塞控制算法的有效性。

Kevin Ong等人在其研究中[9]中对无线网络中的常用拥塞控制算法在进行了详细的测试。然而他们的文章中只有带宽和延迟两个测试项目，并不能完全反应算法的真实性能。

TAN Nguyen等人在其研究[11]中引入了NS-2模拟器以深入分析算法的性能差异。然而，作者的实验是基于DCN的，并不能反应这些算法在因特网中的表现。Thomas Lukaseder等人在其研究中[10]使用NetFPGA给测试网络引入可控的丢包率，并研究了New Reno、Scalable、HighSpeed、H-TCP、BIC和CUBIC等算法在不同丢包率下的性能差异，并分析差异的的成因。然而，作者的实验是基于国有的教育网，其结论同样并不适用与因特网。

论文发表时间较早的有Callegari等人的研究[12]，对Linux 2.6内核所包含的13种拥塞控制算法均进行了测试；以及LA Grieco等人所做的研究[13]，其中引入了模拟测试和场景测试的概念。他们的研究方案与结论对我进行本次研究给予了重要的参考。

## 3. 测试方案

### 3.1 性能标准

### 3.2 网络拓扑

### 3.3 测试工具

### 3.4 网络场景

## 4. 基于有线网络的性能测试结果与分析

### 4.1 性能基准测试

### 4.2 TCP性能测试

### 4.3 网络应用测试

### 4.4 算法间公平性测试

### 4.5 本章小结

## 5. 基于无线网络的性能测试结果与分析

### 5.1 性能基准测试

### 5.2 TCP性能测试

### 5.3 网络应用测试

### 5.4 算法间公平性测试

### 5.5 本章小结

## 6. 结论

## 参考文献

1. Cardwell N, Cheng Y, Gunn C S, et al. BBR: Congestion-based congestion control[J]. Queue, 2016, 14(5): 50.
2. Floyd S, Gurtov A, Henderson T. The NewReno modification to TCP's fast recovery algorithm[J]. 2004.
3. Brakmo L S, Peterson L L. TCP Vegas: End to end congestion avoidance on a global Internet[J]. IEEE Journal on selected Areas in communications, 1995, 13(8): 1465-1480.
4. Floyd S. HighSpeed TCP for large congestion windows[J]. 2003.
5. Nguyen T A N, Gangadhar S, Sterbenz J P G. Performance Evaluation of TCP Congestion Control Algorithms in Data Center Networks[C]//Proceedings of the 11th International Conference on Future Internet Technologies. ACM, 2016: 21-28.
6. Gerla M, Sanadidi M Y, Wang R, et al. TCP Westwood: Congestion window control using bandwidth estimation[C]//Global Telecommunications Conference, 2001. GLOBECOM'01. IEEE. IEEE, 2001, 3: 1698-1702.
7. Feknous M, Houdoin T, Le Guyader B, et al. Internet traffic analysis: A case study from two major European operators[C]//Computers and Communication (ISCC), 2014 IEEE Symposium on. IEEE, 2014: 1-7.
8. Hock M, Bless R, Zitterbart M. Experimental evaluation of BBR congestion control[C]//Network Protocols (ICNP), 2017 IEEE 25th International Conference on. IEEE, 2017: 1-10.
9. Ong K, Murray D, McGill T. Large-Sample comparison of TCP congestion control mechanisms over wireless networks[C]//Advanced Information Networking and Applications Workshops (WAINA), 2016 30th International Conference on. IEEE,Brakmo L S, Peterson L L. TCP Vegas: End to end congestion avoidance on a global Internet[J]. IEEE Journal on selected Areas in communications, 1995, 13(8): 1465-1480. 2016: 420-426.
10. Lukaseder T, Bradatsch L, Erb B, et al. A comparison of TCP congestion control algorithms in 10G networks[C]//Local Computer Networks (LCN), 2016 IEEE 41st Conference on. IEEE, 2016: 706-714.
11. Nguyen T A N, Gangadhar S, Sterbenz J P G. Performance Evaluation of TCP Congestion Control Algorithms in Data Center Networks[C]//Proceedings of the 11th International Conference on Future Internet Technologies. ACM, 2016: 21-28.
12. Callegari C, Giordano S, Pagano M, et al. Behavior analysis of TCP Linux variants[J]. Computer Networks, 2012, 56(1): 462-476.
13. Grieco L A, Mascolo S. Performance evaluation and comparison of Westwood+, New Reno, and Vegas TCP congestion control[J]. ACM SIGCOMM Computer Communication Review, 2004, 34(2): 25-38.
14. RFC 793, https://tools.ietf.org/html/rfc793
15. RFC 2001, https://tools.ietf.org/html/rfc2001
16. Jacobson V. Congestion avoidance and control[C]//ACM SIGCOMM computer communication review. ACM, 1988, 18(4): 314-329.
17. Floyd S, Gurtov A, Henderson T. The NewReno modification to TCP's fast recovery algorithm[J]. 2004.
18. Brakmo L S, Peterson L L. TCP Vegas: End to end congestion avoidance on a global Internet[J]. IEEE Journal on selected Areas in communications, 1995, 13(8): 1465-1480.
19. Ha S, Rhee I, Xu L. CUBIC: a new TCP-friendly high-speed TCP variant[J]. ACM SIGOPS operating systems review, 2008, 42(5): 64-74.
20. Xu L, Harfoush K, Rhee I. Binary increase congestion control (BIC) for fast long-distance networks[C]//INFOCOM 2004. Twenty-third AnnualJoint Conference of the IEEE Computer and Communications Societies. IEEE, 2004, 4: 2514-2524.
21. RFC 5681, https://tools.ietf.org/html/rfc5681
22. Paxson V. End-to-end Internet packet dynamics[C]//ACM SIGCOMM Computer Communication Review. ACM, 1997, 27(4): 139-152.
